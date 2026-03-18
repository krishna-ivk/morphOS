from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from skyforce.runtime.orchestrator import Orchestrator


def _format_run_summary(data: dict[str, Any]) -> str:
    lines = [
        f"Run: {data['run_id']}",
        f"Workflow: {data['workflow']}",
        f"Status: {data['status_line']}",
        f"Mode: {data['mode']}",
        f"Connectivity: {data['connectivity_mode']}",
        f"Pause reason: {data['pause_reason']}",
        "",
        data["summary_short"],
    ]
    validation = data.get("validation")
    if validation:
        summary = validation.get("summary", {})
        lines.extend(
            [
                "",
                "Validation:",
                f"- pytest: {validation.get('overall_result')} ({summary.get('total', 0)} total, {summary.get('failed', 0)} failed, {summary.get('skipped', 0)} skipped)",
            ]
        )
    approval = data.get("pending_approval")
    if approval:
        lines.extend(
            [
                "",
                "Pending approval:",
                f"- {approval.get('step_id')}",
                f"- {approval.get('reason')}",
            ]
        )
    if data.get("deferred_actions"):
        lines.extend(["", "Deferred actions:"])
        for item in data["deferred_actions"]:
            lines.append(f"- {item.get('step_id')}: {item.get('reason')}")
    lines.extend(["", "Steps:"])
    for step in data.get("steps", []):
        line = f"- {step['status']} {step['step_id']}"
        if step.get("output_ref"):
            line += f" -> {step['output_ref']}"
        lines.append(line)
    lines.extend(["", "Evidence:"])
    for path in data.get("evidence_refs", []):
        lines.append(f"- {path}")
    return "\n".join(lines) + "\n"


def _format_approvals(data: dict[str, Any]) -> str:
    lines = [
        f"Approvals: {data.get('matched', 0)} matched (pending {data.get('queue_totals', {}).get('pending', 0)} / total {data.get('queue_totals', {}).get('all', 0)})"
    ]
    preview = data.get("preview") or {}
    if preview.get("policy"):
        lines.append(
            f"Order: {preview.get('policy')} by {preview.get('ordered_by')} ({preview.get('direction')})"
        )
    for item in data.get("approvals", []):
        lines.extend(
            [
                "",
                f"{item.get('run_id')}  {item.get('workflow')}  {item.get('step_id')}",
                f"  requested: {item.get('requested_at')}",
                f"  reason: {item.get('reason')}",
                f"  summary: {item.get('summary_snippet')}",
            ]
        )
    return "\n".join(lines) + "\n"


def _format_approve_runs(data: dict[str, Any]) -> str:
    queue_totals = data.get("queue_totals", {})
    filtered_counts = data.get("filtered_counts", {})
    apply_mode = not data.get("dry_run", True)
    action = "apply" if apply_mode else "preview"
    lines = [
        f"Approve runs ({action}): {data.get('matched', 0)} matched, {filtered_counts.get('applied', data.get('applied', 0))} applied, {filtered_counts.get('skipped', len(data.get('skipped', [])))} skipped (pending {queue_totals.get('pending', 0)} / total {queue_totals.get('all', 0)})",
        f"Decision: {data.get('decision')} - {data.get('reason')}",
    ]
    preview = data.get("preview") or {}
    if preview.get("policy"):
        lines.append(
            f"Order: {preview.get('policy')} by {preview.get('ordered_by')} ({preview.get('direction')})"
        )
    candidate_ids = [
        item.get("run_id") for item in data.get("candidates", []) if item.get("run_id")
    ]
    if candidate_ids:
        lines.append(f"Candidate run ids: {', '.join(candidate_ids)}")
    results = data.get("results", [])
    if results:
        lines.append("Results:")
        for item in results:
            order = item.get("order") or {}
            position = order.get("position")
            prefix = f"- {position}. " if position else "- "
            lines.append(
                f"{prefix}{item.get('run_id')} -> {item.get('status')} ({item.get('decision')})"
            )
    elif apply_mode:
        lines.append("Results: none")
    else:
        for item in data.get("candidates", []):
            order = item.get("order") or {}
            position = order.get("position")
            prefix = f"- {position}. " if position else "- "
            lines.append(f"{prefix}{item.get('run_id')}")
    return "\n".join(lines) + "\n"


def _format_paused_runs(data: dict[str, Any]) -> str:
    runs = data.get("runs", [])
    lines = [f"Paused runs: {len(runs)}"]
    for item in runs:
        lines.extend(
            [
                "",
                f"{item.get('run_id')}  {item.get('workflow')}  {item.get('pause_reason')}",
                f"  blocking: {item.get('blocking_step_id')}",
                f"  connectivity: {item.get('connectivity_mode')}",
                f"  started: {item.get('started_at')}",
            ]
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skyforce")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument(
        "workflow", help="Workflow name, 'auto', or workflow file path"
    )
    run_parser.add_argument(
        "--mode", default="factory", choices=["interactive", "factory"]
    )
    run_parser.add_argument("--seed", help="Seed file path")
    run_parser.add_argument("--repo-path", help="Repository path", default=".")
    run_parser.add_argument("--resume", help="Resume a paused run by id")

    resume_parser = subparsers.add_parser("resume", help="Resume a paused run")
    resume_parser.add_argument("run_id")

    resume_connectivity_parser = subparsers.add_parser(
        "resume-paused-connectivity", help="Resume eligible connectivity-paused runs"
    )
    resume_connectivity_parser.add_argument("--dry-run", action="store_true")

    approve_parser = subparsers.add_parser(
        "approve", help="Approve or reject a pending gate"
    )
    approve_parser.add_argument("run_id")
    approve_parser.add_argument(
        "--decision", required=True, choices=["approve", "reject"]
    )
    approve_parser.add_argument("--reason", required=True)

    approve_runs_parser = subparsers.add_parser(
        "approve-runs", help="Approve or reject matched pending approvals"
    )
    approve_runs_parser.add_argument(
        "--decision", required=True, choices=["approve", "reject"]
    )
    approve_runs_parser.add_argument("--reason", required=True)
    approve_runs_parser.add_argument("--apply", action="store_true")
    approve_runs_parser.add_argument("--run-id")
    approve_runs_parser.add_argument("--workflow")
    approve_runs_parser.add_argument("--older-than-days", type=int)
    approve_runs_parser.add_argument("--limit", type=int)
    approve_runs_parser.add_argument("--human", action="store_true")

    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("run_id", nargs="?")

    logs_parser = subparsers.add_parser("logs", help="Show run event logs")
    logs_parser.add_argument("run_id")
    logs_parser.add_argument("--limit", type=int)

    deferred_parser = subparsers.add_parser(
        "deferred-actions", help="Inspect deferred actions for a run"
    )
    deferred_parser.add_argument("run_id")

    approvals_parser = subparsers.add_parser("approvals", help="List approvals")
    approvals_parser.add_argument("--run-id")
    approvals_parser.add_argument("--workflow")
    approvals_parser.add_argument(
        "--pause-reason", choices=["approval", "connectivity"]
    )
    approvals_parser.add_argument(
        "--status", choices=["pending", "approved", "rejected"], default="pending"
    )
    approvals_parser.add_argument("--older-than-days", type=int)
    approvals_parser.add_argument("--limit", type=int)
    approvals_parser.add_argument("--human", action="store_true")

    summary_parser = subparsers.add_parser("summary", help="Show run summary")
    summary_parser.add_argument("run_id", nargs="?")
    summary_parser.add_argument("--json", action="store_true", dest="as_json")
    summary_parser.add_argument("--workflow")
    summary_parser.add_argument("--pause-reason", choices=["approval", "connectivity"])
    summary_parser.add_argument(
        "--status", choices=["running", "paused", "completed", "failed"]
    )

    paused_parser = subparsers.add_parser("paused-runs", help="List paused runs")
    paused_parser.add_argument("--workflow")
    paused_parser.add_argument("--pause-reason", choices=["approval", "connectivity"])
    paused_parser.add_argument(
        "--status",
        choices=["running", "paused", "completed", "failed"],
        default="paused",
    )
    paused_parser.add_argument("--older-than-days", type=int)
    paused_parser.add_argument("--limit", type=int)
    paused_parser.add_argument("--human", action="store_true")

    archive_parser = subparsers.add_parser("archive-runs", help="Archive selected runs")
    archive_parser.add_argument("--apply", action="store_true")
    archive_parser.add_argument("--run-id")
    archive_parser.add_argument("--workflow")
    archive_parser.add_argument("--pause-reason", choices=["approval", "connectivity"])
    archive_parser.add_argument(
        "--status", choices=["paused", "completed", "failed", "running"]
    )
    archive_parser.add_argument("--origin", choices=["manual", "test"])
    archive_parser.add_argument("--older-than-days", type=int)
    archive_parser.add_argument("--limit", type=int)

    cleanup_parser = subparsers.add_parser(
        "cleanup-test-runs", help="Safely archive test-origin runs"
    )
    cleanup_parser.add_argument("--apply", action="store_true")
    cleanup_parser.add_argument("--workflow")
    cleanup_parser.add_argument("--older-than-days", type=int)
    cleanup_parser.add_argument("--limit", type=int)
    cleanup_parser.add_argument("--include-paused", action="store_true")

    codex_smoke_parser = subparsers.add_parser(
        "codex-smoke", help="Run a minimal coding_agent model-worker smoke test"
    )
    codex_smoke_parser.add_argument("--repo-path", default=".")

    subparsers.add_parser("workflows", help="List available workflows")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    orchestrator = Orchestrator(repo_root)

    if args.command == "run":
        if args.resume:
            state = orchestrator.resume_run(args.resume)
        else:
            state = orchestrator.run_workflow(
                workflow_ref=args.workflow,
                mode=args.mode,
                seed_path=args.seed,
                repo_path=args.repo_path,
            )
        print(json.dumps(state.model_dump(mode="json"), indent=2))
        return 0 if state.status in {"completed", "paused"} else 1

    if args.command == "resume":
        state = orchestrator.resume_run(args.run_id)
        print(json.dumps(state.model_dump(mode="json"), indent=2))
        return 0 if state.status in {"completed", "paused"} else 1

    if args.command == "resume-paused-connectivity":
        data = orchestrator.resume_connectivity_paused_runs(dry_run=args.dry_run)
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "approve":
        state = orchestrator.apply_approval(args.run_id, args.decision, args.reason)
        print(json.dumps(state.model_dump(mode="json"), indent=2))
        return 0 if state.status in {"completed", "paused"} else 1

    if args.command == "approve-runs":
        data = orchestrator.batch_apply_approvals(
            apply=args.apply,
            decision=args.decision,
            reason=args.reason,
            run_id=args.run_id,
            workflow=args.workflow,
            older_than_days=args.older_than_days,
            limit=args.limit,
        )
        if args.human:
            print(_format_approve_runs(data), end="")
        else:
            print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "status":
        data = orchestrator.status(args.run_id)
        print(json.dumps(data, indent=2))
        return 0

    if args.command == "logs":
        data = orchestrator.logs(args.run_id, args.limit)
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "deferred-actions":
        data = orchestrator.inspect_deferred_actions(args.run_id)
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "approvals":
        data = orchestrator.list_pending_approvals(
            run_id=args.run_id,
            workflow=args.workflow,
            pause_reason=args.pause_reason,
            status=args.status,
            older_than_days=args.older_than_days,
            limit=args.limit,
        )
        if args.human:
            print(_format_approvals(data), end="")
        else:
            print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "summary":
        run_id = args.run_id or orchestrator.job_store.latest_run_id(
            workflow=args.workflow,
            pause_reason=args.pause_reason,
            status=args.status,
        )
        if not run_id:
            print(json.dumps({"error": "No runs found"}, indent=2))
            return 1
        data = orchestrator.run_summary(run_id)
        if args.as_json:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(_format_run_summary(data), end="")
        return 0

    if args.command == "paused-runs":
        data = orchestrator.list_paused_runs(
            workflow=args.workflow,
            pause_reason=args.pause_reason,
            status=args.status,
            older_than_days=args.older_than_days,
            limit=args.limit,
        )
        if args.human:
            print(_format_paused_runs(data), end="")
        else:
            print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "archive-runs":
        data = orchestrator.archive_runs(
            apply=args.apply,
            run_id=args.run_id,
            workflow=args.workflow,
            pause_reason=args.pause_reason,
            status=args.status,
            origin=args.origin,
            older_than_days=args.older_than_days,
            limit=args.limit,
        )
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "codex-smoke":
        data = orchestrator.run_codex_smoke(repo_path=args.repo_path)
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "cleanup-test-runs":
        data = orchestrator.cleanup_test_runs(
            apply=args.apply,
            workflow=args.workflow,
            older_than_days=args.older_than_days,
            limit=args.limit,
            include_paused=args.include_paused,
        )
        print(json.dumps(data, indent=2, default=str))
        return 0

    if args.command == "workflows":
        print(json.dumps(orchestrator.list_workflows(), indent=2))
        return 0

    parser.error("Unknown command")
    return 2
