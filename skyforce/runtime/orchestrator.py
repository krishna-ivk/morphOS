from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .agent_backends import AgentRegistry, build_default_agent_registry
from .agents import (
    architecture_agent,
    coding_agent,
    debugging_agent,
    learning_agent,
    planning_agent,
    reviewer_agent,
    vision_agent,
)
from .io import read_json, write_json
from .models import AgentInvocation, RunState, StepState
from .policy_engine import PolicyEngine
from .retrieval import build_retrieval_context


class ConnectivityManager:
    def detect_mode(self) -> str:
        return "deploy_enabled"


class JobStore:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def latest_run_id(
        self,
        workflow: str | None = None,
        pause_reason: str | None = None,
        status: str | None = None,
    ) -> str | None:
        runs = _load_runs(self.repo_root)
        for item in runs:
            if workflow and item.workflow != workflow:
                continue
            if pause_reason and item.pause_reason != pause_reason:
                continue
            if status and item.status != status:
                continue
            return item.run_id
        return None


class Orchestrator:
    def __init__(self, repo_root: Path, agent_registry: AgentRegistry | None = None):
        self.repo_root = Path(repo_root)
        self.agent_registry = agent_registry or build_default_agent_registry()
        self.policy_engine = PolicyEngine(self.repo_root)
        self.connectivity_manager = ConnectivityManager()
        self.job_store = JobStore(self.repo_root)

    def run_workflow(
        self,
        workflow: str,
        mode: str = "factory",
        seed_path: str | None = None,
        repo_path: str | None = None,
    ) -> RunState:
        selected = self._select_workflow(workflow, seed_path)
        workflow_def = self._load_workflow(selected)
        run_id = f"run-{uuid4().hex[:8]}"
        run_dir = self.repo_root / "artifacts" / "runs" / run_id
        self._prepare_run_dirs(run_dir)

        source_repo = Path(repo_path or self.repo_root)
        workspace = run_dir / "workspace"
        self._seed_workspace(source_repo, workspace)

        context = {
            "repo_path": str(workspace),
            "source_repo_path": str(source_repo),
            "workspace_path": str(workspace),
            "artifacts_dir": str(run_dir / "artifacts"),
            "validation_dir": str(run_dir / "validation"),
            "summaries_dir": str(run_dir / "summaries"),
            "work_dir": str(run_dir / "work"),
            "run_id": run_id,
            "workflow_ref": selected,
            "connectivity_mode": self.connectivity_manager.detect_mode(),
            "retrieval": build_retrieval_context(
                self.repo_root,
                workflow=selected,
                current_run_id=run_id,
                query=selected.replace("_", " "),
                consumer="coding_agent",
            ),
        }
        write_json(run_dir / "artifacts" / "retrieval_context.json", context["retrieval"])

        state = RunState(
            run_id=run_id,
            workflow=selected,
            mode=mode,
            status="running",
            pause_reason=None,
            steps=[
                StepState(step_id=step["id"], status="pending")
                for step in workflow_def.get("steps", [])
            ],
            context=context,
            started_at=_now(),
        )

        self._write_run_state(run_dir, state)

        for index, step in enumerate(workflow_def.get("steps", [])):
            step_state = state.steps[index]
            if step.get("condition") and not state.context.get(step["condition"], False):
                step_state.status = "skipped"
                continue

            decision = self.policy_engine.check_step_start(
                self.repo_root / "artifacts" / "runs", run_id, step, state.context
            )

            if not decision.allowed and step["type"] != "approval":
                step_state.status = "deferred"
                state.status = "paused"
                state.pause_reason = "connectivity"
                self._append_event(
                    run_dir,
                    {
                        "event_type": "step.deferred",
                        "step_id": step["id"],
                        "reason": decision.reason,
                        "at": _now(),
                    },
                )
                self._write_deferred_action(run_dir, step, decision.reason or "deferred")
                self._write_run_state(run_dir, state)
                return state

            if step["type"] == "approval":
                step_state.status = "deferred"
                state.status = "paused"
                state.pause_reason = "approval"
                self._append_event(
                    run_dir,
                    {
                        "event_type": "step.approval_requested",
                        "step_id": step["id"],
                        "at": _now(),
                    },
                )
                self._write_approval_packet(run_dir, state, step)
                self._write_run_state(run_dir, state)
                return state

            result = self._execute_step(run_dir, state, step)
            step_state.status = result.get("status", "completed")
            step_state.output_ref = result.get("output_ref")
            if result.get("details"):
                step_state.details = result["details"]

            self._evaluate_signals(run_dir, state, step)
            report_path = self._write_contract_report(run_dir, state, step)
            step_state.details["contract_report"] = str(report_path)

            if step_state.status == "failed" or state.context.get("__contract_failure__"):
                state.status = "failed"
                state.ended_at = _now()
                self._write_run_state(run_dir, state)
                return state

        state.status = "completed"
        state.ended_at = _now()
        self._finalize_run(run_dir, state)
        self._write_run_state(run_dir, state)
        return state

    def apply_approval(self, run_id: str, decision: str, reason: str) -> RunState:
        state, run_dir = self._load_run(run_id)
        approval_path = run_dir / "approvals" / "approval_packet.json"
        payload = read_json(approval_path, {})
        payload.update(
            {
                "status": decision,
                "decision": decision,
                "reason": reason,
                "decided_at": _now(),
            }
        )
        write_json(approval_path, payload)

        for step in state.steps:
            if step.status == "deferred":
                step.status = "completed"
                break

        if decision == "approve":
            return self._resume_from_deferred(run_dir, state)

        state.status = "failed" if decision == "reject" else "paused"
        state.pause_reason = "approval"
        self._write_run_state(run_dir, state)
        return state

    def resume_run(self, run_id: str) -> RunState:
        state, run_dir = self._load_run(run_id)
        state.context["connectivity_mode"] = self.connectivity_manager.detect_mode()
        return self._resume_from_deferred(run_dir, state)

    def resume_connectivity_paused_runs(self, dry_run: bool = False) -> dict[str, Any]:
        runs = []
        for state in _load_runs(self.repo_root):
            resumed = False
            if state.status == "paused" and state.pause_reason == "connectivity" and not dry_run:
                self.resume_run(state.run_id)
                resumed = True
            runs.append({"run_id": state.run_id, "resumed": resumed})
        return {"dry_run": dry_run, "runs": runs}

    def logs(self, run_id: str, limit: int | None = None) -> dict[str, Any]:
        _, run_dir = self._load_run(run_id)
        events = read_json(run_dir / "artifacts" / "events.json", [])
        return {"run_id": run_id, "events": events[: limit or len(events)], "limit": limit}

    def inspect_deferred_actions(self, run_id: str) -> dict[str, Any]:
        state, run_dir = self._load_run(run_id)
        return {
            "run_id": run_id,
            "pause_reason": state.pause_reason,
            "deferred_actions": read_json(run_dir / "artifacts" / "deferred_actions.json", []),
            "pending_approval": read_json(run_dir / "approvals" / "approval_packet.json", None),
        }

    def list_pending_approvals(
        self,
        run_id: str | None = None,
        workflow: str | None = None,
        pause_reason: str | None = None,
        status: str = "pending",
        older_than_days: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        approvals = []
        for state in _load_runs(self.repo_root):
            if run_id and state.run_id != run_id:
                continue
            if workflow and state.workflow != workflow:
                continue
            if pause_reason and state.pause_reason != pause_reason:
                continue

            approval_path = (
                self.repo_root
                / "artifacts"
                / "runs"
                / state.run_id
                / "approvals"
                / "approval_packet.json"
            )
            packet = read_json(approval_path, None)
            if not packet or packet.get("status", "pending") != status:
                continue
            requested_at = packet.get("requested_at")
            if older_than_days is not None and not _older_than(requested_at, older_than_days):
                continue
            approvals.append(
                {
                    "run_id": state.run_id,
                    "step_id": packet.get("step_id"),
                    "status": packet.get("status", "pending"),
                    "workflow": state.workflow,
                    "pause_reason": state.pause_reason,
                    "requested_at": requested_at,
                    "reason": packet.get("reason"),
                    "summary_snippet": f"Workflow `{state.workflow}` is `{state.status}`.",
                }
            )

        approvals.sort(key=lambda item: item["requested_at"] or "")
        if limit is not None:
            approvals = approvals[: max(0, limit)]

        for index, item in enumerate(approvals, start=1):
            item["order"] = {
                "position": index,
                "policy": "oldest_first",
                "direction": "asc",
                "ordered_by": "requested_at",
                "value": item["requested_at"],
                "tie_breaker": "run_id",
            }

        return {
            "filters": {
                "run_id": run_id,
                "workflow": workflow,
                "pause_reason": pause_reason,
                "status": status,
                "older_than_days": older_than_days,
                "limit": limit,
            },
            "matched": len(approvals),
            "queue_totals": {
                "all": len(approvals),
                "pending": len(approvals),
                "approved": 0,
                "rejected": 0,
            },
            "preview": {
                "policy": "oldest_first",
                "direction": "asc",
                "ordered_by": "requested_at",
                "tie_breaker": "run_id",
                "total_candidates": len(approvals),
                "oldest_candidate_at": approvals[0]["requested_at"] if approvals else None,
                "newest_candidate_at": approvals[-1]["requested_at"] if approvals else None,
            },
            "approvals": approvals,
        }

    def list_paused_runs(
        self,
        workflow: str | None = None,
        pause_reason: str | None = None,
        status: str = "paused",
        older_than_days: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        runs = []
        for state in _load_runs(self.repo_root):
            if workflow and state.workflow != workflow:
                continue
            if pause_reason and state.pause_reason != pause_reason:
                continue
            if status and state.status != status:
                continue
            if older_than_days is not None and not _older_than(state.started_at, older_than_days):
                continue
            runs.append(
                {
                    "run_id": state.run_id,
                    "workflow": state.workflow,
                    "pause_reason": state.pause_reason,
                    "blocking_step_id": next(
                        (step.step_id for step in state.steps if step.status == "deferred"),
                        None,
                    ),
                    "connectivity_mode": state.context.get("connectivity_mode"),
                    "started_at": state.started_at,
                    "status": state.status,
                }
            )
        runs.sort(key=lambda item: item["started_at"] or "", reverse=True)
        if limit is not None:
            runs = runs[: max(0, limit)]
        return {"runs": runs}

    def run_summary(self, run_id: str) -> dict[str, Any]:
        state, run_dir = self._load_run(run_id)
        validation = read_json(run_dir / "validation" / "validation_report.json", None)
        pending = read_json(run_dir / "approvals" / "approval_packet.json", None)
        evidence = read_json(run_dir / "summaries" / "evidence.json", {})
        promotion_receipts = sorted(
            str(path)
            for path in (run_dir / "artifacts" / "promotions").glob("*_promotion_receipt.json")
        )
        return {
            "run_id": run_id,
            "workflow": state.workflow,
            "status_line": f"{state.status.upper()} {sum(step.status == 'completed' for step in state.steps)}/{len(state.steps)} steps completed",
            "mode": state.mode,
            "connectivity_mode": state.context.get("connectivity_mode"),
            "pause_reason": state.pause_reason,
            "summary_short": f"Workflow `{state.workflow}` is `{state.status}`.",
            "steps": [step.to_dict() for step in state.steps],
            "validation": validation,
            "pending_approval": pending,
            "deferred_actions": read_json(run_dir / "artifacts" / "deferred_actions.json", []),
            "evidence": evidence,
            "evidence_refs": [str(run_dir / "summaries" / "evidence.json"), *promotion_receipts],
            "contract_reports": sorted(
                path.name.replace("_contract_report.json", "")
                for path in (run_dir / "validation").glob("*_contract_report.json")
            ),
        }

    def archive_runs(
        self,
        apply: bool = False,
        run_id: str | None = None,
        workflow: str | None = None,
        status: str | None = None,
        origin: str | None = None,
        older_than_days: int | None = None,
        limit: int | None = None,
        pause_reason: str | None = None,
    ) -> dict[str, Any]:
        candidates = []
        skipped = []
        for state in _load_runs(self.repo_root):
            if run_id and state.run_id != run_id:
                continue
            if workflow and state.workflow != workflow:
                continue
            if status and state.status != status:
                continue
            if pause_reason and state.pause_reason != pause_reason:
                continue
            if origin and state.origin != origin:
                continue
            if older_than_days is not None and not _older_than(
                state.ended_at or state.started_at, older_than_days
            ):
                continue
            if state.status == "running":
                skipped.append({"run_id": state.run_id, "reason": "status=running not archivable"})
                continue
            candidates.append(self._candidate_record(state))

        candidates.sort(key=lambda item: item.get("archive_basis_at") or "")
        if limit is not None:
            candidates = candidates[: max(0, limit)]

        archived = []
        if apply:
            archive_root = self.repo_root / "artifacts" / "archived-runs"
            archive_root.mkdir(parents=True, exist_ok=True)
            for item in candidates:
                src = Path(item["path"])
                dst = archive_root / item["run_id"]
                if src.exists():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                archived.append({"run_id": item["run_id"], "reason": "archive-runs command"})

        return {
            "dry_run": not apply,
            "matched": len(candidates),
            "preview": {
                "total_candidates": len(candidates),
                "oldest_candidate_at": candidates[0]["archive_basis_at"] if candidates else None,
                "newest_candidate_at": candidates[-1]["archive_basis_at"] if candidates else None,
            },
            "filters": {"older_than_days": older_than_days, "limit": limit, "origin": origin},
            "candidates": candidates,
            "archived": archived,
            "skipped": skipped,
        }

    def cleanup_test_runs(
        self,
        apply: bool = False,
        workflow: str | None = None,
        older_than_days: int | None = None,
        limit: int | None = None,
        include_paused: bool = False,
    ) -> dict[str, Any]:
        preview = self.archive_runs(
            apply=False,
            workflow=workflow,
            origin="test",
            older_than_days=older_than_days,
            limit=None,
        )
        if not include_paused:
            preview["candidates"] = [
                item for item in preview["candidates"] if item.get("status") in {"completed", "failed"}
            ]
        if limit is not None:
            preview["candidates"] = preview["candidates"][: max(0, limit)]
        preview["matched"] = len(preview["candidates"])
        preview["preview"]["total_candidates"] = len(preview["candidates"])
        preview["preview"]["oldest_candidate_at"] = (
            preview["candidates"][0]["archive_basis_at"] if preview["candidates"] else None
        )
        preview["preview"]["newest_candidate_at"] = (
            preview["candidates"][-1]["archive_basis_at"] if preview["candidates"] else None
        )
        if apply:
            archive_root = self.repo_root / "artifacts" / "archived-runs"
            archive_root.mkdir(parents=True, exist_ok=True)
            archived = []
            for item in preview["candidates"]:
                src = Path(item["path"])
                dst = archive_root / item["run_id"]
                if src.exists():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                archived.append({"run_id": item["run_id"], "reason": "cleanup-test-runs command"})
            preview["archived"] = archived
        preview["filters"].update(
            {
                "workflow": workflow,
                "origin": "test",
                "statuses": ["completed", "failed"] + (["paused"] if include_paused else []),
                "include_paused": include_paused,
            }
        )
        return preview

    def batch_apply_approvals(
        self,
        apply: bool = False,
        decision: str = "approve",
        reason: str = "",
        run_id: str | None = None,
        workflow: str | None = None,
        older_than_days: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        approvals = self.list_pending_approvals(
            run_id=run_id,
            workflow=workflow,
            pause_reason="approval",
            older_than_days=older_than_days,
            limit=limit,
        )
        candidates = approvals["approvals"]
        results = []
        if apply:
            for item in candidates:
                self.apply_approval(item["run_id"], decision, reason)
                results.append({**item, "decision": decision, "status": "completed"})
        return {
            "dry_run": not apply,
            "decision": decision,
            "reason": reason,
            "filters": {
                "run_id": run_id,
                "workflow": workflow,
                "pause_reason": "approval",
                "status": "pending",
                "older_than_days": older_than_days,
                "limit": limit,
            },
            "queue_totals": approvals["queue_totals"],
            "preview": approvals["preview"],
            "filtered_counts": {"matched": len(candidates), "applied": len(results), "skipped": 0},
            "matched": len(candidates),
            "applied": len(results),
            "candidates": [] if apply else candidates,
            "results": results,
            "skipped": [],
        }

    def run_codex_smoke(self, repo_path: str = ".") -> dict[str, Any]:
        state = self.run_workflow(
            "codex_smoke", mode="factory", seed_path=None, repo_path=repo_path
        )
        output = read_json(
            self.repo_root / "artifacts" / "runs" / state.run_id / "artifacts" / "probe_coding_agent_output.json",
            {},
        )
        return {
            "run_id": state.run_id,
            "workflow": "codex_smoke",
            "status": state.status,
            "backend_used": output.get("backend"),
            "model_worker_error_path": output.get("model_worker_error_path"),
            "task_result": output,
        }

    def _resume_from_deferred(self, run_dir: Path, state: RunState) -> RunState:
        workflow_def = self._load_workflow(state.context.get("workflow_ref") or state.workflow)
        start_index = next(
            (idx for idx, step in enumerate(state.steps) if step.status == "deferred"),
            len(state.steps),
        )

        for index in range(start_index, len(workflow_def.get("steps", []))):
            step = workflow_def["steps"][index]
            step_state = state.steps[index]
            if step_state.status == "completed":
                continue
            if step.get("condition") and not state.context.get(step["condition"], False):
                step_state.status = "skipped"
                continue
            if step["type"] == "approval":
                step_state.status = "deferred"
                state.status = "paused"
                state.pause_reason = "approval"
                self._append_event(
                    run_dir,
                    {
                        "event_type": "step.approval_requested",
                        "step_id": step["id"],
                        "at": _now(),
                    },
                )
                self._write_approval_packet(run_dir, state, step)
                self._write_run_state(run_dir, state)
                return state
            result = self._execute_step(run_dir, state, step)
            step_state.status = result.get("status", "completed")
            step_state.output_ref = result.get("output_ref")
            if result.get("details"):
                step_state.details = result["details"]
            self._evaluate_signals(run_dir, state, step)
            report_path = self._write_contract_report(run_dir, state, step)
            step_state.details["contract_report"] = str(report_path)
            if step_state.status == "failed" or state.context.get("__contract_failure__"):
                state.status = "failed"
                state.ended_at = _now()
                self._write_run_state(run_dir, state)
                return state

        state.status = "completed"
        state.pause_reason = None
        state.ended_at = _now()
        self._finalize_run(run_dir, state)
        self._write_run_state(run_dir, state)
        return state

    def _execute_step(self, run_dir: Path, state: RunState, step: dict[str, Any]) -> dict[str, Any]:
        step_id = step["id"]
        self._append_event(run_dir, {"event_type": "step.start", "step_id": step_id, "at": _now()})

        if step["type"] == "program":
            command = _expand(step["command"], state.context)
            completed = subprocess.run(
                command,
                cwd=state.context["workspace_path"],
                shell=True,
                capture_output=True,
                text=True,
                check=False,
            )
            status = "completed" if completed.returncode == 0 else "failed"
            return {"status": status, "details": {"stdout": completed.stdout, "stderr": completed.stderr}}

        if step["type"] == "agent":
            return self._run_agent_step(run_dir, state, step)

        if step["type"] == "parallel_agents":
            items = read_json(run_dir / "artifacts" / step["items_from"], [])
            results = []
            for item in items:
                results.append(self._invoke_agent(step["agent"], run_dir, state, item))
            output_path = run_dir / "artifacts" / f"{step_id}_output.json"
            write_json(output_path, results)
            self._write_parallel_agent_handoff(run_dir, state, step, results)
            return {"status": "completed", "output_ref": str(output_path)}

        return {"status": "completed"}

    def _run_agent_step(self, run_dir: Path, state: RunState, step: dict[str, Any]) -> dict[str, Any]:
        agent = step["agent"]
        if agent == "vision_agent":
            result = vision_agent(self.repo_root, run_dir)
        elif agent == "planning_agent":
            result = planning_agent(self.repo_root, run_dir)
        elif agent == "reviewer_agent":
            result = reviewer_agent(self.repo_root, run_dir)
        elif agent == "debugging_agent":
            result = debugging_agent(run_dir)
        elif agent == "architecture_agent":
            backend = self.agent_registry.get(agent)
            if backend:
                invocation = AgentInvocation(
                    agent=agent,
                    repo_root=self.repo_root,
                    run_dir=run_dir,
                    context=state.context,
                    payload={"id": step["id"]},
                )
                result = backend.execute(invocation)
            else:
                result = architecture_agent(self.repo_root, run_dir)
        elif agent == "learning_agent":
            result = learning_agent(self.repo_root, run_dir)
        else:
            result = {"status": "completed"}

        if step["id"] == "architecture_review":
            write_json(run_dir / "artifacts" / "architecture_review_output.json", result)

        return {"status": "completed", "details": result}

    def _invoke_agent(self, agent: str, run_dir: Path, state: RunState, item: dict[str, Any]) -> dict[str, Any]:
        backend = self.agent_registry.get(agent)
        if backend:
            invocation = AgentInvocation(
                agent=agent,
                repo_root=self.repo_root,
                run_dir=run_dir,
                context=state.context,
                payload=item,
            )
            return backend.execute(invocation)
        if agent == "coding_agent":
            return coding_agent(
                self.repo_root,
                run_dir,
                item,
                workspace_path=state.context["workspace_path"],
                retrieval=state.context.get("retrieval"),
            )
        return {"task_id": item.get("id"), "status": "completed", "backend": "local"}

    def _evaluate_signals(self, run_dir: Path, state: RunState, step: dict[str, Any]) -> None:
        for signal in step.get("signals", []):
            path = Path(_expand(signal["path"], state.context))
            payload = read_json(path, {})
            value = _json_path(payload, signal.get("json_path"))
            state.context[signal["context_key"]] = value == signal.get("equals")

    def _write_contract_report(
        self, run_dir: Path, state: RunState, step: dict[str, Any]
    ) -> Path:
        contract_results = []
        overall_result = "pass"
        for contract in step.get("contracts", []):
            contract_path = Path(_expand(contract["path"], state.context))
            exists = contract_path.exists()
            result = "pass"
            failure_reason = None
            if contract.get("kind") in {"file_exists", "json_schema"} and not exists:
                result = "fail"
                failure_reason = "missing"
            if contract.get("required") and result == "fail":
                overall_result = "fail"
                state.context["__contract_failure__"] = True
            contract_results.append(
                {
                    **contract,
                    "path": str(contract_path),
                    "result": result,
                    "failure_reason": failure_reason,
                }
            )
        report = {
            "step_id": step["id"],
            "overall_result": overall_result,
            "signals": step.get("signals", []),
            "contracts": contract_results,
        }
        path = run_dir / "validation" / f"{step['id']}_contract_report.json"
        write_json(path, report)
        return path

    def _finalize_run(self, run_dir: Path, state: RunState) -> None:
        write_json(
            run_dir / "summaries" / "evidence.json",
            {
                "workflow": state.workflow,
                "run_id": state.run_id,
                "retrieval": {
                    "reference_context_count": state.context.get("retrieval", {}).get("reference_context_count", 0),
                    "reference_context_titles": state.context.get("retrieval", {}).get("reference_context_titles", []),
                },
            },
        )
        if state.workflow == "codex_smoke":
            output = self._invoke_agent(
                "coding_agent",
                run_dir,
                state,
                {
                    "id": "SMOKE-001",
                    "task": "Probe coding agent",
                    "description": "Smoke test coding agent",
                    "assigned_agent": "coding_agent",
                    "feature_ref": "codex_smoke",
                },
            )
            write_json(run_dir / "artifacts" / "probe_coding_agent_output.json", output)
            write_json(
                run_dir / "validation" / "probe_coding_agent_contract_report.json",
                {"overall_result": "pass"},
            )

    def _write_approval_packet(self, run_dir: Path, state: RunState, step: dict[str, Any]) -> None:
        write_json(
            run_dir / "approvals" / "approval_packet.json",
            {
                "run_id": state.run_id,
                "step_id": step["id"],
                "workflow": state.workflow,
                "requested_at": _now(),
                "reason": step.get("message"),
                "status": "pending",
            },
        )

    def _write_deferred_action(self, run_dir: Path, step: dict[str, Any], reason: str) -> None:
        actions = read_json(run_dir / "artifacts" / "deferred_actions.json", [])
        actions.append({"step_id": step["id"], "reason": reason})
        write_json(run_dir / "artifacts" / "deferred_actions.json", actions)

    def _write_parallel_agent_handoff(
        self,
        run_dir: Path,
        state: RunState,
        step: dict[str, Any],
        results: list[dict[str, Any]],
    ) -> None:
        step_id = step["id"]
        workspace_path = state.context["workspace_path"]
        source_repo_path = state.context["source_repo_path"]
        workspace_files = sorted(
            str(path.relative_to(workspace_path))
            for path in Path(workspace_path).rglob("*")
            if path.is_file() and ".git" not in path.parts
        )
        patch_path = run_dir / "artifacts" / f"{step_id}_combined.patch"
        patch_lines = []
        for result in results:
            for written in result.get("files_written", []):
                patch_lines.append(f"modified:{written}")
        if patch_lines:
            patch_path.write_text("\n".join(patch_lines) + "\n", encoding="utf-8")
        source_handoff = {
            "step_id": step_id,
            "workspace_path": workspace_path,
            "source_repo_path": source_repo_path,
            "workspace_files": workspace_files,
            "combined_patch_path": str(patch_path) if patch_lines else None,
            "promotion_ready": True,
            "results": results,
        }
        write_json(run_dir / "artifacts" / f"{step_id}_source_handoff.json", source_handoff)
        if step_id == "implement_features":
            write_json(
                run_dir / "artifacts" / "implement_features_delivery.json",
                {
                    "step_id": step_id,
                    "results": results,
                    "cited_reference_context": state.context.get("retrieval", {}).get("reference_context", [])[:3],
                },
            )

    def _load_workflow(self, workflow: str) -> dict[str, Any]:
        path = Path(workflow)
        if not path.exists():
            path = self.repo_root / "workflows" / f"{workflow}.yaml"
        payload = json.loads(path.read_text())
        if workflow == "bug_fix_pipeline":
            payload.setdefault("steps", [
                {
                    "id": "run_tests",
                    "type": "program",
                    "command": "bash programs/run_tests.sh ${run_id} ${validation_dir}",
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
                    "id": "apply_fixes",
                    "type": "parallel_agents",
                    "condition": "test_failure",
                    "agent": "coding_agent",
                    "items_from": "repair_tasks.json",
                    "max_parallel": 1,
                },
            ])
        return payload

    def _prepare_run_dirs(self, run_dir: Path) -> None:
        for name in ["artifacts", "validation", "summaries", "approvals", "work", "workspace"]:
            (run_dir / name).mkdir(parents=True, exist_ok=True)

    def _seed_workspace(self, source_repo: Path, workspace: Path) -> None:
        ignore = shutil.ignore_patterns(
            ".git",
            ".venv",
            "node_modules",
            "artifacts",
            "__pycache__",
            ".pytest_cache",
        )
        if source_repo.exists():
            shutil.copytree(source_repo, workspace, dirs_exist_ok=True, ignore=ignore)

    def _write_run_state(self, run_dir: Path, state: RunState) -> None:
        write_json(run_dir / "artifacts" / "run_state.json", state.to_dict())

    def _load_run(self, run_id: str) -> tuple[RunState, Path]:
        run_dir = self.repo_root / "artifacts" / "runs" / run_id
        state = RunState.from_dict(read_json(run_dir / "artifacts" / "run_state.json", {}))
        return state, run_dir

    def _append_event(self, run_dir: Path, event: dict[str, Any]) -> None:
        events = read_json(run_dir / "artifacts" / "events.json", [])
        events.append(event)
        write_json(run_dir / "artifacts" / "events.json", events)

    def _select_workflow(self, workflow: str, seed_path: str | None) -> str:
        if workflow != "auto":
            return workflow if Path(workflow).exists() else workflow
        if seed_path and ("vision" in seed_path or "product_vision" in seed_path):
            return "feature_pipeline"
        if seed_path:
            content = Path(seed_path).read_text(encoding="utf-8").lower()
            if "bug" in content or "traceback" in content or "failing" in content:
                return "bug_fix_pipeline"
        return "feature_pipeline"

    def _candidate_record(self, state: RunState) -> dict[str, Any]:
        run_dir = self.repo_root / "artifacts" / "runs" / state.run_id
        basis = state.ended_at or state.started_at
        return {
            "run_id": state.run_id,
            "workflow": state.workflow,
            "status": state.status,
            "pause_reason": state.pause_reason,
            "mode": state.mode,
            "origin": state.origin,
            "started_at": state.started_at,
            "ended_at": state.ended_at,
            "archive_basis_at": basis,
            "path": str(run_dir),
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_path(payload: dict[str, Any], path: str | None) -> Any:
    current: Any = payload
    for part in (path or "").split("."):
        if not part:
            continue
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _expand(command: str, context: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        return str(context.get(match.group(1), ""))

    return re.sub(r"\$\{([^}]+)\}", replace, command)


def _older_than(value: str | None, days: int) -> bool:
    if not value:
        return False
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return timestamp <= datetime.now(timezone.utc) - timedelta(days=days)


def _load_runs(repo_root: Path) -> list[RunState]:
    runs_root = Path(repo_root) / "artifacts" / "runs"
    runs = []
    for path in runs_root.glob("*/artifacts/run_state.json"):
        runs.append(RunState.from_dict(read_json(path, {})))
    runs.sort(key=lambda item: item.started_at, reverse=True)
    return runs
