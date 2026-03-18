import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from skyforce.runtime.agent_backends import (
    AgentBackend,
    AgentInvocation,
    ModelWorkerBackend,
    build_default_agent_registry,
)
from skyforce.runtime.agents import debugging_agent
from skyforce.runtime.io import write_json
from skyforce.runtime.orchestrator import Orchestrator


def test_feature_pipeline_creates_artifacts(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    assert (run_dir / "artifacts" / "feature_plan.json").exists()
    assert (run_dir / "artifacts" / "tasks.json").exists()
    assert (run_dir / "validation" / "test_results.json").exists()
    assert (run_dir / "validation" / "interpret_vision_contract_report.json").exists()
    assert (run_dir / "validation" / "split_tasks_contract_report.json").exists()
    assert (run_dir / "validation" / "run_tests_contract_report.json").exists()
    evidence = json.loads((run_dir / "summaries" / "evidence.json").read_text())
    assert evidence["workflow"] == "feature_pipeline"
    rerun = next(step for step in state.steps if step.step_id == "rerun_tests")
    review = next(
        step for step in state.steps if step.step_id == "request_validation_review"
    )
    assert rerun.status == "skipped"
    assert review.status == "skipped"


def test_release_pipeline_pauses_for_approval(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "paused"
    resumed = orchestrator.apply_approval(
        state.run_id, "approve", "Tests passed and release is approved."
    )
    assert resumed.steps[2].status == "completed"
    assert resumed.status == "completed"


def test_repo_evaluation_generates_architecture_report(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    report = json.loads(
        (run_dir / "artifacts" / "architecture_report.json").read_text()
    )
    assert report["overall_health"] in {"healthy", "concerns", "critical"}


def test_auto_workflow_selection_uses_bug_fix_pipeline(repo_root, tmp_path):
    orchestrator = Orchestrator(repo_root)
    seed = tmp_path / "bug.md"
    seed.write_text("# Login bug\n\nTests are failing with a traceback in auth flow.\n")
    state = orchestrator.run_workflow(
        "auto", mode="factory", seed_path=str(seed), repo_path=str(repo_root)
    )
    assert state.workflow == "bug_fix_pipeline"


def test_auto_workflow_selection_uses_feature_pipeline_for_vision(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "auto",
        mode="factory",
        seed_path=str(repo_root / "docs" / "vision" / "product_vision.md"),
        repo_path=str(repo_root),
    )
    assert state.workflow == "feature_pipeline"


def test_release_pipeline_defers_when_connectivity_is_insufficient(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "paused"
    assert state.steps[0].status == "deferred"


def test_release_pipeline_replays_deferred_step_when_connectivity_returns(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.pause_reason == "connectivity"
    orchestrator.connectivity_manager.detect_mode = lambda: "online_read"
    resumed = orchestrator.resume_run(state.run_id)
    assert resumed.steps[0].status == "completed"
    assert resumed.status == "paused"
    assert resumed.pause_reason == "approval"


def test_resume_connectivity_paused_runs_resumes_only_connectivity_runs(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    deferred = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    approval = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert deferred.pause_reason == "connectivity"
    assert approval.pause_reason == "approval"
    result = orchestrator.resume_connectivity_paused_runs()
    resumed = {item["run_id"]: item for item in result["runs"]}
    assert resumed[deferred.run_id]["resumed"] is True
    assert resumed[approval.run_id]["resumed"] is False


def test_logs_and_deferred_inspection(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    logs = orchestrator.logs(state.run_id, limit=5)
    deferred = orchestrator.inspect_deferred_actions(state.run_id)
    assert logs["run_id"] == state.run_id
    assert len(logs["events"]) >= 1
    assert deferred["pause_reason"] == "connectivity"
    assert len(deferred["deferred_actions"]) >= 1


def test_list_pending_approvals_and_run_summary(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    approvals = orchestrator.list_pending_approvals()
    assert approvals["matched"] >= 1
    assert approvals["queue_totals"]["pending"] >= 1
    assert approvals["preview"]["policy"] == "oldest_first"
    record = next(
        item for item in approvals["approvals"] if item["run_id"] == state.run_id
    )
    assert record["summary_snippet"]
    assert record["pause_reason"] == "approval"
    assert record["order"]["policy"] == "oldest_first"
    summary = orchestrator.run_summary(state.run_id)
    assert summary["pending_approval"]["status"] == "pending"
    assert summary["validation"]["overall_result"] == "pass"
    assert "run_tests" in summary["contract_reports"]
    assert (
        str(
            repo_root
            / "artifacts"
            / "runs"
            / state.run_id
            / "summaries"
            / "evidence.json"
        )
        in summary["evidence_refs"]
    )


def test_list_paused_runs_filtered(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    connectivity = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    approval = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    data = orchestrator.list_paused_runs(
        workflow="release_pipeline", pause_reason="approval"
    )
    run_ids = {item["run_id"] for item in data["runs"]}
    assert approval.run_id in run_ids
    assert connectivity.run_id not in run_ids


def test_list_paused_runs_limit(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "offline"
    for _ in range(3):
        orchestrator.run_workflow(
            "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
        )
    full = orchestrator.list_paused_runs()
    limited = orchestrator.list_paused_runs(limit=1)
    assert len(limited["runs"]) == 1
    assert limited["runs"][0]["run_id"] == full["runs"][0]["run_id"]


def test_list_paused_runs_filters_by_age(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    states = [
        orchestrator.run_workflow(
            "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
        )
        for _ in range(2)
    ]
    ages = [20, 1]
    for state, days in zip(states, ages, strict=True):
        run_state_path = (
            repo_root
            / "artifacts"
            / "runs"
            / state.run_id
            / "artifacts"
            / "run_state.json"
        )
        payload = json.loads(run_state_path.read_text())
        payload["started_at"] = (
            datetime.now(timezone.utc) - timedelta(days=days)
        ).isoformat()
        run_state_path.write_text(json.dumps(payload, indent=2) + "\n")
    data = orchestrator.list_paused_runs(older_than_days=7)
    run_ids = {item["run_id"] for item in data["runs"]}
    assert states[0].run_id in run_ids
    assert states[1].run_id not in run_ids


def test_contract_signal_sets_test_failure_context(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.context["test_failure"] is False
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    report = json.loads(
        (run_dir / "validation" / "run_tests_contract_report.json").read_text()
    )
    assert report["signals"][0]["context_key"] == "test_failure"


def test_codex_smoke_validates_coding_receipt_contract(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "codex_smoke", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    report = json.loads(
        (run_dir / "validation" / "probe_coding_agent_contract_report.json").read_text()
    )
    assert report["overall_result"] == "pass"


def test_orchestrator_fails_on_missing_required_contract(repo_root, tmp_path):
    workflow = {
        "name": "missing_contract",
        "steps": [
            {
                "id": "noop",
                "type": "agent",
                "agent": "learning_agent",
                "contracts": [
                    {
                        "name": "missing_file",
                        "path": "${artifacts_dir}/does_not_exist.json",
                        "kind": "file_exists",
                        "required": True,
                    }
                ],
            }
        ],
    }
    workflow_path = tmp_path / "missing_contract.json"
    workflow_path.write_text(json.dumps(workflow, indent=2) + "\n")
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        str(workflow_path), mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "failed"


def test_program_steps_execute_inside_run_workspace(repo_root, tmp_path):
    workflow = {
        "name": "workspace_exec",
        "steps": [
            {
                "id": "write_marker",
                "type": "program",
                "command": "python3 -c \"from pathlib import Path; Path('workspace_marker.txt').write_text('ok')\"",
                "contracts": [
                    {
                        "name": "marker_exists",
                        "path": "${workspace_path}/workspace_marker.txt",
                        "kind": "file_exists",
                    }
                ],
            }
        ],
    }
    workflow_path = tmp_path / "workspace_exec.json"
    workflow_path.write_text(json.dumps(workflow, indent=2) + "\n")
    marker_root = repo_root / "workspace_marker.txt"
    if marker_root.exists():
        marker_root.unlink()
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        str(workflow_path), mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    assert (run_dir / "workspace" / "workspace_marker.txt").exists()
    assert not marker_root.exists()


def test_run_context_uses_isolated_workspace_path(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    assert state.context["workspace_path"] == str(run_dir / "workspace")
    assert state.context["source_repo_path"] == str(repo_root)
    assert state.context["repo_path"] == str(run_dir / "workspace")


def test_retrieval_context_uses_prior_completed_runs(repo_root):
    orchestrator = Orchestrator(repo_root)
    first = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    second = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert first.status == "completed"
    assert second.status == "completed"
    retrieval = second.context["retrieval"]
    assert retrieval["workflow"] == "feature_pipeline"
    assert retrieval["exemplar_count"] >= 1
    assert any(item["run_id"] == first.run_id for item in retrieval["exemplars"])


def test_coding_agent_note_includes_retrieved_lessons(repo_root):
    orchestrator = Orchestrator(repo_root)
    first = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    second = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert first.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / second.run_id
    work_notes = sorted((run_dir / "work").glob("TASK-*.md"))
    assert work_notes
    content = work_notes[0].read_text()
    assert "Retrieved lessons:" in content


def test_codex_smoke_reports_retrieval_context(repo_root, monkeypatch):
    registry = build_default_agent_registry()
    registry.register("coding_agent", ModelWorkerBackend(mode_override="auto"))
    orchestrator = Orchestrator(repo_root, agent_registry=registry)

    def fake_execute(self, invocation):
        assert "retrieval" in invocation.context
        return {
            "task_id": "SMOKE-001",
            "status": "completed",
            "files_written": [],
            "tests_written": [],
            "patch_path": None,
            "error": None,
            "partial_output_ref": None,
            "backend": "codex",
            "retrieval_used": invocation.context["retrieval"],
        }

    monkeypatch.setattr(ModelWorkerBackend, "execute", fake_execute)
    result = orchestrator.run_codex_smoke(repo_path=str(repo_root))
    assert "retrieval_used" in result["task_result"]


def test_bounded_retry_loop_escalates_on_persistent_failure(repo_root, tmp_path):
    fail_payload = {
        "run_id": "temp-run",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {"total": 1, "passed": 0, "failed": 1, "skipped": 0},
        "overall_result": "fail",
        "tests": [
            {
                "name": "synthetic::failure",
                "result": "fail",
                "duration_ms": 1,
                "error_message": "forced fail",
                "stack_trace": None,
            }
        ],
    }
    writer_path = tmp_path / "write_fail_results.py"
    writer_path.write_text(
        "from pathlib import Path\n"
        "import json, sys\n"
        f"payload = {json.dumps(fail_payload)!r}\n"
        "target = Path(sys.argv[1])\n"
        "target.mkdir(parents=True, exist_ok=True)\n"
        "(target / 'test_results.json').write_text(payload)\n"
    )
    workflow = {
        "name": "bounded_retry",
        "steps": [
            {
                "id": "run_tests",
                "type": "program",
                "command": f"python3 {writer_path} ${{validation_dir}}",
                "contracts": [
                    {
                        "name": "test_results",
                        "path": "${validation_dir}/test_results.json",
                        "kind": "json_schema",
                        "schema_name": "TestResults",
                    }
                ],
                "signals": [
                    {
                        "name": "test_failure_signal",
                        "path": "${validation_dir}/test_results.json",
                        "json_path": "overall_result",
                        "equals": "fail",
                        "context_key": "test_failure",
                    }
                ],
            },
            {
                "id": "diagnose_failures",
                "type": "agent",
                "condition": "test_failure",
                "agent": "debugging_agent",
                "contracts": [
                    {
                        "name": "repair_tasks",
                        "path": "${artifacts_dir}/repair_tasks.json",
                        "kind": "json_schema",
                        "schema_name": "TaskList",
                    }
                ],
            },
            {
                "id": "apply_fixes",
                "type": "parallel_agents",
                "condition": "test_failure",
                "agent": "coding_agent",
                "items_from": "repair_tasks.json",
                "max_parallel": 1,
                "contracts": [
                    {
                        "name": "applied_fix_results",
                        "path": "${artifacts_dir}/apply_fixes_output.json",
                        "kind": "file_exists",
                    }
                ],
            },
            {
                "id": "rerun_tests",
                "type": "program",
                "condition": "test_failure",
                "command": f"python3 {writer_path} ${{validation_dir}}",
                "contracts": [
                    {
                        "name": "rerun_test_results",
                        "path": "${validation_dir}/test_results.json",
                        "kind": "json_schema",
                        "schema_name": "TestResults",
                    }
                ],
                "signals": [
                    {
                        "name": "persistent_test_failure_signal",
                        "path": "${validation_dir}/test_results.json",
                        "json_path": "overall_result",
                        "equals": "fail",
                        "context_key": "persistent_test_failure",
                    }
                ],
            },
            {
                "id": "request_review",
                "type": "approval",
                "condition": "persistent_test_failure",
                "message": "Human review required after bounded retry.",
            },
        ],
    }
    workflow_path = tmp_path / "bounded_retry.json"
    workflow_path.write_text(json.dumps(workflow, indent=2) + "\n")
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        str(workflow_path), mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "paused"
    assert state.pause_reason == "approval"
    assert state.context["test_failure"] is True
    assert state.context["persistent_test_failure"] is True
    review = next(step for step in state.steps if step.step_id == "request_review")
    apply_step = next(step for step in state.steps if step.step_id == "apply_fixes")
    assert apply_step.status == "completed"
    assert review.status == "deferred"


def test_debugging_agent_writes_repair_tasks(repo_root, tmp_path):
    run_dir = tmp_path / "run"
    (run_dir / "validation").mkdir(parents=True, exist_ok=True)
    failing_results = {
        "tests": [
            {
                "name": "tests::broken",
                "result": "fail",
                "error_message": "forced failure",
            }
        ]
    }
    (run_dir / "validation" / "test_results.json").write_text(
        json.dumps(failing_results, indent=2) + "\n"
    )
    result = debugging_agent(run_dir)
    assert result["count"] == 1
    repair_tasks = json.loads((run_dir / "artifacts" / "repair_tasks.json").read_text())
    assert repair_tasks[0]["id"] == "REPAIR-001"
    assert repair_tasks[0]["assigned_agent"] == "coding_agent"


def test_bug_fix_pipeline_skips_apply_fixes_when_tests_pass(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "bug_fix_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    apply_step = next(step for step in state.steps if step.step_id == "apply_fixes")
    assert apply_step.status == "skipped"


def test_archive_runs_dry_run_and_apply(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    preview = orchestrator.archive_runs(apply=False, run_id=state.run_id)
    assert preview["candidates"][0]["run_id"] == state.run_id
    assert preview["preview"]["total_candidates"] == 1
    applied = orchestrator.archive_runs(apply=True, run_id=state.run_id)
    assert applied["matched"] == 1
    assert applied["candidates"][0]["run_id"] == state.run_id
    assert applied["archived"][0]["reason"] == "archive-runs command"
    assert (repo_root / "artifacts" / "archived-runs" / state.run_id).exists()


def test_archive_runs_skips_running_runs(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    run_state = json.loads((run_dir / "artifacts" / "run_state.json").read_text())
    run_state["status"] = "running"
    (run_dir / "artifacts" / "run_state.json").write_text(
        json.dumps(run_state, indent=2) + "\n"
    )
    preview = orchestrator.archive_runs(apply=False, run_id=state.run_id)
    assert preview["matched"] == 0
    assert preview["skipped"][0]["reason"] == "status=running not archivable"


def test_archive_runs_filters_by_age_and_limit(repo_root):
    orchestrator = Orchestrator(repo_root)
    states = [
        orchestrator.run_workflow(
            "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
        )
        for _ in range(3)
    ]
    ages = [20, 10, 1]
    for state, days in zip(states, ages, strict=True):
        run_dir = repo_root / "artifacts" / "runs" / state.run_id
        payload = json.loads((run_dir / "artifacts" / "run_state.json").read_text())
        ended_at = datetime.now(timezone.utc) - timedelta(days=days)
        started_at = ended_at - timedelta(minutes=10)
        payload["started_at"] = started_at.isoformat()
        payload["ended_at"] = ended_at.isoformat()
        (run_dir / "artifacts" / "run_state.json").write_text(
            json.dumps(payload, indent=2) + "\n"
        )
    preview = orchestrator.archive_runs(
        apply=False,
        workflow="repo_evaluation",
        status="completed",
        older_than_days=7,
        limit=1,
    )
    assert preview["dry_run"] is True
    assert preview["matched"] == 1
    assert len(preview["candidates"]) == 1
    assert preview["candidates"][0]["workflow"] == "repo_evaluation"
    assert preview["preview"]["total_candidates"] == 1
    assert preview["filters"]["older_than_days"] == 7


def test_batch_apply_approvals_dry_run_and_apply(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    preview = orchestrator.batch_apply_approvals(
        apply=False,
        decision="approve",
        reason="Tests passed",
        workflow="release_pipeline",
    )
    assert preview["matched"] >= 1
    assert preview["queue_totals"]["pending"] >= 1
    assert preview["preview"]["policy"] == "oldest_first"
    assert preview["filtered_counts"]["matched"] == preview["matched"]
    assert preview["candidates"][0]["summary_snippet"]
    assert preview["candidates"][0]["order"]["position"] == 1
    applied = orchestrator.batch_apply_approvals(
        apply=True,
        decision="approve",
        reason="Tests passed",
        run_id=state.run_id,
    )
    assert applied["applied"] == 1
    assert applied["filtered_counts"]["applied"] == 1
    assert applied["results"][0]["run_id"] == state.run_id
    assert applied["results"][0]["summary_snippet"]
    assert applied["results"][0]["order"]["position"] == 1


def test_list_pending_approvals_returns_explicit_oldest_first_order(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    states = [
        orchestrator.run_workflow(
            "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
        )
        for _ in range(2)
    ]
    ages = [20, 10]
    for state, days in zip(states, ages, strict=True):
        approval_path = (
            repo_root
            / "artifacts"
            / "runs"
            / state.run_id
            / "approvals"
            / "approval_packet.json"
        )
        payload = json.loads(approval_path.read_text())
        requested_at = datetime.now(timezone.utc) - timedelta(days=days)
        payload["requested_at"] = requested_at.isoformat()
        approval_path.write_text(json.dumps(payload, indent=2) + "\n")
    approvals = orchestrator.list_pending_approvals(workflow="release_pipeline")
    matching = [
        item
        for item in approvals["approvals"]
        if item["run_id"] in {state.run_id for state in states}
    ]
    assert [item["run_id"] for item in matching] == [states[0].run_id, states[1].run_id]
    assert matching[0]["order"]["position"] < matching[1]["order"]["position"]
    assert [item["order"]["value"] for item in matching] == [
        item["requested_at"] for item in matching
    ]
    assert approvals["preview"]["policy"] == "oldest_first"


def test_list_pending_approvals_filters_by_age_and_limit(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    states = [
        orchestrator.run_workflow(
            "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
        )
        for _ in range(2)
    ]
    ages = [20, 2]
    for state, days in zip(states, ages, strict=True):
        approval_path = (
            repo_root
            / "artifacts"
            / "runs"
            / state.run_id
            / "approvals"
            / "approval_packet.json"
        )
        payload = json.loads(approval_path.read_text())
        requested_at = datetime.now(timezone.utc) - timedelta(days=days)
        payload["requested_at"] = requested_at.isoformat()
        approval_path.write_text(json.dumps(payload, indent=2) + "\n")
    filtered = orchestrator.list_pending_approvals(
        workflow="release_pipeline",
        older_than_days=7,
        limit=1,
    )
    assert filtered["matched"] == 1
    assert filtered["filters"]["older_than_days"] == 7
    assert filtered["filters"]["limit"] == 1


def test_cleanup_test_runs_preserves_manual_runs_and_paused_by_default(repo_root):
    orchestrator = Orchestrator(repo_root)
    test_completed = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    test_completed_dir = (
        repo_root
        / "artifacts"
        / "runs"
        / test_completed.run_id
        / "artifacts"
        / "run_state.json"
    )
    completed_payload = json.loads(test_completed_dir.read_text())
    completed_payload["started_at"] = datetime.now(timezone.utc).isoformat()
    completed_payload["ended_at"] = datetime.now(timezone.utc).isoformat()
    test_completed_dir.write_text(json.dumps(completed_payload, indent=2) + "\n")
    paused = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    run_dir = (
        repo_root
        / "artifacts"
        / "runs"
        / paused.run_id
        / "artifacts"
        / "run_state.json"
    )
    payload = json.loads(run_dir.read_text())
    payload["status"] = "paused"
    run_dir.write_text(json.dumps(payload, indent=2) + "\n")
    preview = orchestrator.cleanup_test_runs(
        apply=False,
        workflow="repo_evaluation",
        older_than_days=0,
    )
    run_ids = {item["run_id"] for item in preview["candidates"]}
    assert test_completed.run_id in run_ids
    assert paused.run_id not in run_ids
    assert preview["filters"]["origin"] == "test"


def test_cleanup_test_runs_can_include_paused(repo_root):
    orchestrator = Orchestrator(repo_root)
    orchestrator.connectivity_manager.detect_mode = lambda: "deploy_enabled"
    state = orchestrator.run_workflow(
        "release_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    approval_path = (
        repo_root
        / "artifacts"
        / "runs"
        / state.run_id
        / "approvals"
        / "approval_packet.json"
    )
    approval_payload = json.loads(approval_path.read_text())
    approval_payload["requested_at"] = datetime.now(timezone.utc).isoformat()
    approval_path.write_text(json.dumps(approval_payload, indent=2) + "\n")
    preview = orchestrator.cleanup_test_runs(
        apply=False,
        workflow="release_pipeline",
        older_than_days=0,
        include_paused=True,
    )
    run_ids = {item["run_id"] for item in preview["candidates"]}
    assert state.run_id in run_ids


def test_cleanup_test_runs_apply_reports_archived_candidates(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    applied = orchestrator.cleanup_test_runs(
        apply=True,
        workflow="repo_evaluation",
        older_than_days=0,
    )
    assert applied["matched"] >= 1
    matched_candidate = next(
        item for item in applied["candidates"] if item["run_id"] == state.run_id
    )
    matched_receipt = next(
        item for item in applied["archived"] if item["run_id"] == state.run_id
    )
    assert matched_candidate["origin"] == "test"
    assert matched_receipt["reason"] == "cleanup-test-runs command"


def test_codex_smoke_workflow_runs_single_inline_task(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "codex_smoke", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    output = json.loads(
        (run_dir / "artifacts" / "probe_coding_agent_output.json").read_text()
    )
    assert output["task_id"] == "SMOKE-001"


def test_run_codex_smoke_reports_backend_used(repo_root, monkeypatch):
    registry = build_default_agent_registry()
    registry.register("coding_agent", ModelWorkerBackend(mode_override="auto"))
    orchestrator = Orchestrator(repo_root, agent_registry=registry)
    original_execute = ModelWorkerBackend.execute

    def fake_execute(self, invocation):
        if invocation.agent == "coding_agent":
            return {
                "task_id": "SMOKE-001",
                "status": "completed",
                "files_written": [],
                "tests_written": [],
                "patch_path": None,
                "error": None,
                "partial_output_ref": None,
                "backend": "codex",
            }
        return original_execute(self, invocation)

    monkeypatch.setattr(ModelWorkerBackend, "execute", fake_execute)
    result = orchestrator.run_codex_smoke(repo_path=str(repo_root))
    assert result["workflow"] == "codex_smoke"
    assert result["backend_used"] in {"local", "local_fallback", "codex", "opencode"}


class StubArchitectureBackend(AgentBackend):
    def execute(self, invocation: AgentInvocation) -> dict[str, object]:
        report_path = invocation.run_dir / "artifacts" / "architecture_report.json"
        write_json(
            report_path,
            {
                "repo_path": invocation.context["repo_path"],
                "overall_health": "healthy",
                "findings": [],
            },
        )
        return {"architecture_report_path": str(report_path), "backend": "stub"}


def test_repo_evaluation_accepts_custom_agent_backend(repo_root):
    registry = build_default_agent_registry()
    registry.register("architecture_agent", StubArchitectureBackend())
    orchestrator = Orchestrator(repo_root, agent_registry=registry)
    state = orchestrator.run_workflow(
        "repo_evaluation", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    assert state.status == "completed"
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    output = json.loads(
        (run_dir / "artifacts" / "architecture_review_output.json").read_text()
    )
    assert output["backend"] == "stub"


def test_model_worker_accepts_fenced_json_and_validates(
    monkeypatch, repo_root, tmp_path
):
    monkeypatch.setenv("SKYFORCE_CODING_AGENT_BACKEND", "codex")
    backend = ModelWorkerBackend()
    invocation = AgentInvocation(
        agent="coding_agent",
        repo_root=repo_root,
        run_dir=tmp_path,
        context={"validation_dir": str(tmp_path / "validation")},
        payload={
            "id": "TASK-001",
            "task": "Do work",
            "description": "desc",
            "assigned_agent": "coding_agent",
            "feature_ref": "Feature",
        },
    )
    monkeypatch.setattr(
        "skyforce.runtime.agent_backends.shutil.which", lambda name: "/usr/bin/codex"
    )

    def fake_run(command, cwd, input, text, capture_output, timeout, check):
        assert "--output-schema" in command
        assert "--ask-for-approval" not in command
        assert command[-1] == "-"
        assert input is not None
        response_path = Path(command[command.index("--output-last-message") + 1])
        response_path.write_text(
            '```json\n{"task_id":"TASK-001","status":"completed","files_written":[],"tests_written":[],"patch_path":null}\n```'
        )
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = backend.execute(invocation)
    assert result["task_id"] == "TASK-001"
    assert result["backend"] == "codex"


def test_model_worker_adds_skip_git_repo_check_outside_git(
    monkeypatch, repo_root, tmp_path
):
    monkeypatch.setenv("SKYFORCE_CODING_AGENT_BACKEND", "codex")
    backend = ModelWorkerBackend()
    invocation = AgentInvocation(
        agent="coding_agent",
        repo_root=tmp_path,
        run_dir=tmp_path,
        context={"validation_dir": str(tmp_path / "validation")},
        payload={
            "id": "TASK-001",
            "task": "Do work",
            "description": "desc",
            "assigned_agent": "coding_agent",
            "feature_ref": "Feature",
        },
    )
    monkeypatch.setattr(
        "skyforce.runtime.agent_backends.shutil.which", lambda name: "/usr/bin/codex"
    )

    def fake_run(command, cwd, input, text, capture_output, timeout, check):
        assert "--skip-git-repo-check" in command
        response_path = Path(command[command.index("--output-last-message") + 1])
        response_path.write_text(
            '{"task_id":"TASK-001","status":"completed","files_written":[],"tests_written":[],"patch_path":null}'
        )
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = backend.execute(invocation)
    assert result["backend"] == "codex"


def test_model_worker_falls_back_and_writes_error_artifact(
    monkeypatch, repo_root, tmp_path
):
    monkeypatch.setenv("SKYFORCE_CODING_AGENT_BACKEND", "codex")
    backend = ModelWorkerBackend()
    invocation = AgentInvocation(
        agent="coding_agent",
        repo_root=repo_root,
        run_dir=tmp_path,
        context={"validation_dir": str(tmp_path / "validation")},
        payload={
            "id": "TASK-001",
            "task": "Do work",
            "description": "desc",
            "assigned_agent": "coding_agent",
            "feature_ref": "Feature",
        },
    )
    monkeypatch.setattr(
        "skyforce.runtime.agent_backends.shutil.which", lambda name: "/usr/bin/codex"
    )

    def fake_run(command, cwd, input, text, capture_output, timeout, check):
        response_path = Path(command[command.index("--output-last-message") + 1])
        response_path.write_text(
            '{"task_id":"WRONG","status":"completed","files_written":[],"tests_written":[],"patch_path":null}'
        )
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = backend.execute(invocation)
    assert result["backend"] == "local_fallback"
    assert "model_worker_error_path" in result
    assert Path(result["model_worker_error_path"]).exists()


def test_build_default_agent_registry_uses_local_by_default(monkeypatch):
    monkeypatch.delenv("SKYFORCE_CODING_AGENT_BACKEND", raising=False)
    registry = build_default_agent_registry()
    assert "coding_agent" not in registry.backends


def test_build_default_agent_registry_registers_model_worker(monkeypatch):
    monkeypatch.setenv("SKYFORCE_CODING_AGENT_BACKEND", "codex")
    registry = build_default_agent_registry()
    assert "coding_agent" in registry.backends
