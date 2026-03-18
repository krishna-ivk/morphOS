import json

from skyforce import cli


class StubOrchestrator:
    def resume_connectivity_paused_runs(self, dry_run=False):
        return {"dry_run": dry_run, "runs": []}

    def list_paused_runs(
        self,
        workflow=None,
        pause_reason=None,
        status="paused",
        older_than_days=None,
        limit=None,
    ):
        runs = [
            {
                "run_id": "run-1",
                "workflow": workflow,
                "pause_reason": pause_reason,
                "status": status,
            },
            {
                "run_id": "run-2",
                "workflow": workflow,
                "pause_reason": pause_reason,
                "status": status,
            },
        ]
        if limit is not None:
            runs = runs[: max(0, limit)]
        return {"runs": runs}

    def logs(self, run_id, limit=None):
        return {
            "run_id": run_id,
            "events": [{"event_type": "workflow.started"}],
            "limit": limit,
        }

    def inspect_deferred_actions(self, run_id):
        return {"run_id": run_id, "deferred_actions": [], "pending_approval": None}

    def list_pending_approvals(
        self,
        run_id=None,
        workflow=None,
        pause_reason=None,
        status="pending",
        older_than_days=None,
        limit=None,
    ):
        return {
            "filters": {
                "run_id": run_id,
                "workflow": workflow,
                "pause_reason": pause_reason,
                "status": status,
                "older_than_days": older_than_days,
                "limit": limit,
            },
            "matched": 1,
            "queue_totals": {"all": 2, "pending": 1, "approved": 1, "rejected": 0},
            "preview": {
                "policy": "oldest_first",
                "direction": "asc",
                "ordered_by": "requested_at",
                "tie_breaker": "run_id",
                "total_candidates": 1,
                "oldest_candidate_at": "2026-03-01T00:10:00+00:00",
                "newest_candidate_at": "2026-03-01T00:10:00+00:00",
            },
            "approvals": [
                {
                    "run_id": "run-1",
                    "step_id": "request_release_approval",
                    "status": status,
                    "workflow": workflow,
                    "pause_reason": pause_reason,
                    "requested_at": "2026-03-01T00:10:00+00:00",
                    "summary_snippet": "Workflow `release_pipeline` is `paused`.",
                    "order": {
                        "position": 1,
                        "policy": "oldest_first",
                        "direction": "asc",
                        "ordered_by": "requested_at",
                        "value": "2026-03-01T00:10:00+00:00",
                        "tie_breaker": "run_id",
                    },
                }
            ],
        }

    def archive_runs(self, **kwargs):
        return {
            "dry_run": not kwargs.get("apply", False),
            "matched": 1,
            "archived": [],
            "preview": {
                "total_candidates": 1,
                "oldest_candidate_at": "2026-03-01T00:10:00+00:00",
                "newest_candidate_at": "2026-03-01T00:10:00+00:00",
            },
            "filters": {
                "older_than_days": kwargs.get("older_than_days"),
                "limit": kwargs.get("limit"),
            },
            "candidates": [
                {
                    "run_id": "run-1",
                    "workflow": kwargs.get("workflow"),
                    "status": "completed",
                    "pause_reason": None,
                    "mode": "factory",
                    "origin": "manual",
                    "started_at": "2026-03-01T00:00:00+00:00",
                    "ended_at": "2026-03-01T00:10:00+00:00",
                    "archive_basis_at": "2026-03-01T00:10:00+00:00",
                    "path": "/tmp/run-1",
                }
            ],
            "skipped": [],
        }

    def batch_apply_approvals(self, **kwargs):
        apply = kwargs.get("apply", False)
        candidate = {
            "run_id": "run-1",
            "requested_at": "2026-03-01T00:10:00+00:00",
            "summary_snippet": "Workflow `release_pipeline` is `paused`.",
            "order": {
                "position": 1,
                "policy": "oldest_first",
                "direction": "asc",
                "ordered_by": "requested_at",
                "value": "2026-03-01T00:10:00+00:00",
                "tie_breaker": "run_id",
            },
        }
        return {
            "dry_run": not apply,
            "decision": kwargs.get("decision"),
            "reason": kwargs.get("reason"),
            "filters": {
                "run_id": kwargs.get("run_id"),
                "workflow": kwargs.get("workflow"),
                "pause_reason": "approval",
                "status": "pending",
                "older_than_days": kwargs.get("older_than_days"),
                "limit": kwargs.get("limit"),
            },
            "queue_totals": {"all": 2, "pending": 1, "approved": 1, "rejected": 0},
            "preview": {
                "policy": "oldest_first",
                "direction": "asc",
                "ordered_by": "requested_at",
                "tie_breaker": "run_id",
                "total_candidates": 1,
                "oldest_candidate_at": "2026-03-01T00:10:00+00:00",
                "newest_candidate_at": "2026-03-01T00:10:00+00:00",
            },
            "filtered_counts": {"matched": 1, "applied": int(apply), "skipped": 0},
            "matched": 1,
            "applied": int(apply),
            "candidates": [] if apply else [candidate],
            "results": []
            if not apply
            else [
                {**candidate, "decision": kwargs.get("decision"), "status": "completed"}
            ],
            "skipped": [],
        }

    def cleanup_test_runs(self, **kwargs):
        return {
            "dry_run": not kwargs.get("apply", False),
            "matched": 1,
            "preview": {
                "total_candidates": 1,
                "oldest_candidate_at": "2026-03-01T00:10:00+00:00",
                "newest_candidate_at": "2026-03-01T00:10:00+00:00",
            },
            "filters": {
                "workflow": kwargs.get("workflow"),
                "origin": "test",
                "statuses": ["completed", "failed"],
                "older_than_days": kwargs.get("older_than_days"),
                "limit": kwargs.get("limit"),
                "include_paused": kwargs.get("include_paused", False),
            },
            "archived": [],
            "candidates": [{"run_id": "run-test-1", "origin": "test"}],
            "skipped": [],
        }

    def run_summary(self, run_id):
        return {
            "run_id": run_id,
            "workflow": "release_pipeline",
            "status_line": "PAUSED 2/5 steps completed",
            "mode": "factory",
            "connectivity_mode": "deploy_enabled",
            "pause_reason": "approval",
            "summary_short": "Workflow `release_pipeline` is `paused`.",
            "steps": [
                {"step_id": "run_tests", "status": "completed", "output_ref": None}
            ],
            "validation": {
                "overall_result": "pass",
                "summary": {"total": 7, "failed": 0, "skipped": 0},
            },
            "pending_approval": {
                "step_id": "request_release_approval",
                "reason": "Release actions require human approval.",
            },
            "deferred_actions": [],
            "evidence_refs": ["artifacts/evidence.json"],
        }

    def run_codex_smoke(self, repo_path="."):
        return {
            "run_id": "run-smoke",
            "workflow": "codex_smoke",
            "status": "completed",
            "backend_used": "codex",
            "model_worker_error_path": None,
            "task_result": {"task_id": "SMOKE-001", "backend": "codex"},
        }

    class job_store:
        @staticmethod
        def latest_run_id(**kwargs):
            return "run-1"


def test_cli_paused_runs(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["paused-runs"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["runs"][0]["run_id"] == "run-1"


def test_cli_paused_runs_passes_filters(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            [
                "paused-runs",
                "--workflow",
                "release_pipeline",
                "--pause-reason",
                "approval",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["runs"][0]["workflow"] == "release_pipeline"


def test_cli_paused_runs_limit_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["paused-runs", "--limit", "1"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert len(output["runs"]) == 1
    assert output["runs"][0]["run_id"] == "run-1"


def test_cli_paused_runs_passes_age_and_limit(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["paused-runs", "--older-than-days", "7", "--limit", "1"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert len(output["runs"]) == 1


def test_cli_paused_runs_human(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["paused-runs", "--human"]) == 0
    output = capsys.readouterr().out
    assert "Paused runs:" in output
    assert "run-1" in output


def test_cli_paused_runs_limit_human(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["paused-runs", "--human", "--limit", "1"]) == 0
    output = capsys.readouterr().out
    assert "Paused runs: 1" in output
    assert "run-1" in output
    assert "run-2" not in output


def test_cli_logs(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["logs", "run-1", "--limit", "5"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["run_id"] == "run-1"
    assert output["limit"] == 5


def test_cli_resume_paused_connectivity_dry_run(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["resume-paused-connectivity", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True


def test_cli_approvals(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["approvals"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["matched"] == 1
    assert output["queue_totals"]["pending"] == 1
    assert output["preview"]["policy"] == "oldest_first"
    assert output["approvals"][0]["run_id"] == "run-1"
    assert output["approvals"][0]["order"]["position"] == 1


def test_cli_approvals_human(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["approvals", "--human"]) == 0
    output = capsys.readouterr().out
    assert "Approvals:" in output
    assert "run-1" in output
    assert "request_release_approval" in output


def test_cli_approvals_passes_run_id_age_and_limit(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            ["approvals", "--run-id", "run-1", "--older-than-days", "7", "--limit", "2"]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["filters"]["run_id"] == "run-1"
    assert output["filters"]["older_than_days"] == 7
    assert output["filters"]["limit"] == 2


def test_cli_approve_runs_dry_run(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["approve-runs", "--decision", "approve", "--reason", "ok"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True
    assert output["matched"] == 1
    assert output["queue_totals"]["all"] == 2
    assert output["preview"]["policy"] == "oldest_first"
    assert output["candidates"][0]["summary_snippet"]
    assert output["candidates"][0]["order"]["position"] == 1


def test_cli_approve_runs_passes_age_and_limit(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            [
                "approve-runs",
                "--decision",
                "approve",
                "--reason",
                "ok",
                "--older-than-days",
                "3",
                "--limit",
                "1",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["filters"]["older_than_days"] == 3
    assert output["filters"]["limit"] == 1


def test_cli_approve_runs_human_preview(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(["approve-runs", "--decision", "approve", "--reason", "ok", "--human"])
        == 0
    )
    output = capsys.readouterr().out
    assert "Approve runs (preview): 1 matched" in output
    assert "Order: oldest_first by requested_at (asc)" in output
    assert "Candidate run ids: run-1" in output
    assert "- 1. run-1" in output


def test_cli_approve_runs_human_apply(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            [
                "approve-runs",
                "--decision",
                "approve",
                "--reason",
                "ok",
                "--apply",
                "--human",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "Approve runs (apply): 1 matched" in output
    assert "Results:" in output
    assert "run-1 -> completed (approve)" in output


def test_cli_archive_runs(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["archive-runs", "--workflow", "release_pipeline"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["matched"] == 1
    assert output["preview"]["total_candidates"] == 1
    assert output["candidates"][0]["run_id"] == "run-1"


def test_cli_archive_runs_passes_age_and_limit(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["archive-runs", "--older-than-days", "7", "--limit", "2"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["filters"]["older_than_days"] == 7
    assert output["filters"]["limit"] == 2


def test_cli_archive_runs_apply_reports_archived_candidates(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["archive-runs", "--apply", "--workflow", "release_pipeline"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is False
    assert output["candidates"][0]["run_id"] == "run-1"


def test_cli_summary_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["summary", "run-1", "--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["run_id"] == "run-1"


def test_cli_summary_text(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["summary", "run-1"]) == 0
    output = capsys.readouterr().out
    assert "Run: run-1" in output
    assert "Pending approval:" in output


def test_cli_summary_uses_latest_matching_run(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["summary", "--workflow", "release_pipeline", "--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["run_id"] == "run-1"


def test_cli_codex_smoke(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["codex-smoke", "--repo-path", "."]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["workflow"] == "codex_smoke"
    assert output["backend_used"] == "codex"


def test_cli_cleanup_test_runs(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(["cleanup-test-runs", "--older-than-days", "7", "--limit", "2"]) == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["filters"]["origin"] == "test"
    assert output["filters"]["older_than_days"] == 7
    assert output["filters"]["limit"] == 2


def test_cli_cleanup_test_runs_apply_reports_archived_candidates(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["cleanup-test-runs", "--apply"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is False
    assert output["candidates"][0]["run_id"] == "run-test-1"
