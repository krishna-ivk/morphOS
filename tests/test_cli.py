import json

from skyforce import cli


class StubOrchestrator:
    def run_workflow(self, workflow, mode="factory", seed_path=None, repo_path=None):
        return {
            "run_id": "run-new",
            "workflow": workflow,
            "status": "completed",
            "mode": mode,
            "connectivity_mode": "deploy_enabled",
            "pause_reason": None,
            "summary_short": f"Workflow `{workflow}` is `completed`.",
            "status_line": "COMPLETED 1/1 steps completed",
            "steps": [],
            "validation": None,
            "pending_approval": None,
            "deferred_actions": [],
            "evidence_refs": [],
        }

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

    def cancel_run(self, run_id, reason=None):
        return {
            "run_id": run_id,
            "status": "cancelled",
            "pause_reason": "cancelled",
            "ended_at": "2026-03-01T00:11:00+00:00",
            "context": {"cancel_reason": reason},
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
            "checkpoint": {"step_id": "request_release_approval"},
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

    def status(self, run_id):
        data = self.run_summary(run_id)

        data.update(
            {
                "run_status": "paused",
                "current_step_index": 1,
                "execution_checkpoint_id": "cp-1",
            }
        )
        return data

    def list_workflows(self):
        return {
            "count": 1,
            "workflows": [{"name": "release_pipeline", "path": "workflows/release_pipeline.yaml"}],
        }

    def context_search(self, query, consumer="operator", limit=5):
        return {
            "query": query,
            "consumer": consumer,
            "matched": 1,
            "results": [
                {
                    "context_id": "repo-doc-1",
                    "title": "Context Hub Guide",
                    "source": "repo-local-docs",
                    "trust_label": "curated",
                    "access_label": "public",
                    "uri": "docs/guide.md",
                    "summary": "Grounded retrieval guidance.",
                }
            ],
        }

    def context_get(self, context_id, consumer="operator"):
        return {
            "context_id": context_id,
            "title": "Context Hub Guide",
            "content": "Guide content",
            "annotations": [],
        }

    def context_list_annotations(
        self, context_id, consumer="operator", include_pending=False
    ):
        return {
            "context_id": context_id,
            "consumer": consumer,
            "annotations": [
                {
                    "annotation_id": "annotation-1",
                    "status": "active",
                    "author_kind": "human",
                    "author_id": "alice",
                    "trust_label": "annotated",
                    "access_label": "public",
                    "content": "Use this guide first.",
                }
            ],
        }

    def context_create_annotation(self, context_id, **kwargs):
        return {
            "annotation_id": "annotation-1",
            "context_id": context_id,
            "status": "active"
            if kwargs.get("author_kind") == "human"
            else "pending_review",
            "author_kind": kwargs.get("author_kind"),
            "author_id": kwargs.get("author_id"),
            "content": kwargs.get("content"),
        }

    def context_promote_annotation(self, annotation_id, **kwargs):
        return {
            "annotation_id": annotation_id,
            "status": "active",
            "approved_by": kwargs.get("approver"),
            "trust_label": kwargs.get("trust_label"),
        }

    def promote_workspace_changes(
        self, run_id, apply=False, step_id=None, only_files=None, exclude_files=None
    ):
        selected = only_files or ["sample.txt"]
        if exclude_files:
            selected = [path for path in selected if path not in exclude_files]
        return {
            "run_id": run_id,
            "dry_run": not apply,
            "matched": 1,
            "candidates": [
                {
                    "step_id": step_id or "implement_features",
                    "promotion_ready": True,
                    "source_repo_path": "/tmp/source",
                    "workspace_path": "/tmp/workspace",
                    "workspace_files": ["sample.txt"],
                    "selected_files": selected,
                    "selection": {
                        "only_files": only_files or [],
                        "exclude_files": exclude_files or [],
                    },
                    "combined_patch_path": "/tmp/patch.diff",
                    "source_dirty": False,
                    "changed_file_count": 1,
                    "identical_file_count": 0,
                    "missing_workspace_file_count": 0,
                    "file_statuses": [
                        {
                            "path": "sample.txt",
                            "status": "overwrite",
                            "checksums": {"source": "oldhash", "workspace": "newhash"},
                            "preview": "--- sample.txt\n+++ sample.txt\n@@ -1 +1 @@\n-old\n+new",
                        }
                    ],
                }
            ],
            "promoted": []
            if not apply
            else [
                {
                    "files_promoted": selected,
                    "checksums": [
                        {
                            "path": (selected or ["sample.txt"])[0],
                            "source_before": "oldhash",
                            "workspace": "newhash",
                            "source_after": "newhash",
                        }
                    ],
                }
            ],
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


def test_cli_run_uses_workflow_argument(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["run", "release_pipeline"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["workflow"] == "release_pipeline"


def test_cli_sudoku_launches_gui(monkeypatch):
    launched = {"called": False}

    def fake_launch():
        launched["called"] = True

    monkeypatch.setattr(cli, "_launch_sudoku", fake_launch)
    assert cli.main(["sudoku"]) == 0
    assert launched["called"] is True


def test_cli_status(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["status", "run-1"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["run_status"] == "paused"
    assert output["execution_checkpoint_id"] == "cp-1"


def test_cli_cancel(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["cancel", "run-1", "--reason", "user requested"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "cancelled"
    assert output["context"]["cancel_reason"] == "user requested"


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


def test_cli_workflows(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["workflows"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["count"] == 1
    assert output["workflows"][0]["name"] == "release_pipeline"


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


def test_cli_context_search_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["context-search", "--query", "Context Hub"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["matched"] == 1
    assert output["results"][0]["context_id"] == "repo-doc-1"


def test_cli_context_search_human(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["context-search", "--query", "Context Hub", "--human"]) == 0
    output = capsys.readouterr().out
    assert "Context matches: 1" in output
    assert "Context Hub Guide" in output


def test_cli_context_annotate_and_promote(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            [
                "context-annotate",
                "repo-doc-1",
                "--author-kind",
                "human",
                "--author-id",
                "alice",
                "--content",
                "Use this guide first.",
            ]
        )
        == 0
    )
    created = json.loads(capsys.readouterr().out)
    assert created["annotation_id"] == "annotation-1"
    assert cli.main(["context-promote", "annotation-1", "--approver", "alice"]) == 0
    promoted = json.loads(capsys.readouterr().out)
    assert promoted["status"] == "active"


def test_cli_promote_workspace(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["promote-workspace", "run-1", "--apply"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is False
    assert output["promoted"][0]["files_promoted"] == ["sample.txt"]
    assert output["promoted"][0]["checksums"][0]["source_after"] == "newhash"


def test_cli_promote_workspace_human(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert cli.main(["promote-workspace", "run-1", "--human"]) == 0
    output = capsys.readouterr().out
    assert "Promote workspace (preview): 1 matched for run-1" in output
    assert "implement_features" in output
    assert "sample.txt: overwrite" in output
    assert "checksums: source=oldhash workspace=newhash" in output
    assert "preview:" in output


def test_cli_promote_workspace_only_file(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(["promote-workspace", "run-1", "--apply", "--only-file", "sample.txt"])
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["candidates"][0]["selected_files"] == ["sample.txt"]
    assert output["promoted"][0]["files_promoted"] == ["sample.txt"]


def test_cli_promote_workspace_exclude_file(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Orchestrator", lambda repo_root: StubOrchestrator())
    assert (
        cli.main(
            [
                "promote-workspace",
                "run-1",
                "--apply",
                "--only-file",
                "sample.txt",
                "--exclude-file",
                "sample.txt",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["candidates"][0]["selected_files"] == []
    assert output["promoted"][0]["files_promoted"] == []
