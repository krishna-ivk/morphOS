"""Canonical event taxonomy for morphOS - unified event language across all repos."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from dataclasses import dataclass, asdict


# Canonical event families
RUN_FAMILY = "run"
STEP_FAMILY = "step"
VALIDATION_FAMILY = "validation"
APPROVAL_FAMILY = "approval"
PROMOTION_FAMILY = "promotion"

# Canonical event types
RUN_STARTED = "run.started"
RUN_BLOCKED = "run.blocked"
RUN_COMPLETED = "run.completed"
RUN_FAILED = "run.failed"
RUN_CANCELLED = "run.cancelled"
RUN_PAUSED = "run.paused"

STEP_EXECUTING = "step.executing"
STEP_COMPLETED = "step.completed"
STEP_FAILED = "step.failed"
STEP_DEFERRED = "step.deferred"
STEP_APPROVAL_REQUESTED = "step.approval_requested"

VALIDATION_STARTED = "validation.started"
VALIDATION_COMPLETED = "validation.completed"
VALIDATION_FAILED = "validation.failed"

APPROVAL_REQUESTED = "approval.requested"
APPROVAL_APPROVED = "approval.approved"
APPROVAL_REJECTED = "approval.rejected"

PROMOTION_READY = "promotion.ready"
PROMOTION_STARTED = "promotion.started"
PROMOTION_COMPLETED = "promotion.completed"
PROMOTION_FAILED = "promotion.failed"

ALL_EVENT_TYPES = {
    RUN_STARTED,
    RUN_BLOCKED,
    RUN_COMPLETED,
    RUN_FAILED,
    RUN_CANCELLED,
    RUN_PAUSED,
    STEP_EXECUTING,
    STEP_COMPLETED,
    STEP_FAILED,
    STEP_DEFERRED,
    STEP_APPROVAL_REQUESTED,
    VALIDATION_STARTED,
    VALIDATION_COMPLETED,
    VALIDATION_FAILED,
    APPROVAL_REQUESTED,
    APPROVAL_APPROVED,
    APPROVAL_REJECTED,
    PROMOTION_READY,
    PROMOTION_STARTED,
    PROMOTION_COMPLETED,
    PROMOTION_FAILED,
}


@dataclass
class MorphOSEvent:
    """Universal event structure - the single truth language for the factory."""

    event_type: str
    timestamp: str
    run_id: str
    workspace_id: str
    issue_identifier: str
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        event_type: str,
        run_id: str,
        workspace_id: str = "",
        issue_identifier: str = "",
        payload: dict[str, Any] | None = None,
    ) -> "MorphOSEvent":
        if event_type not in ALL_EVENT_TYPES:
            family = event_type.split(".")[0]
            if family not in {
                RUN_FAMILY,
                STEP_FAMILY,
                VALIDATION_FAMILY,
                APPROVAL_FAMILY,
                PROMOTION_FAMILY,
            }:
                pass  # Allow custom event types for extensibility
        return cls(
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            run_id=run_id,
            workspace_id=workspace_id,
            issue_identifier=issue_identifier,
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MorphOSEvent":
        return cls(**data)


class EventTaxonomy:
    """Manages canonical event emission for morphOS runs."""

    def __init__(
        self,
        run_dir: Path,
        run_id: str,
        workspace_id: str = "",
        issue_identifier: str = "",
    ):
        self.run_dir = Path(run_dir)
        self.run_id = run_id
        self.workspace_id = workspace_id
        self.issue_identifier = issue_identifier

    def emit(
        self, event_type: str, payload: dict[str, Any] | None = None
    ) -> MorphOSEvent:
        event = MorphOSEvent.create(
            event_type=event_type,
            run_id=self.run_id,
            workspace_id=self.workspace_id,
            issue_identifier=self.issue_identifier,
            payload=payload,
        )
        self._append_event(event)
        return event

    def run_started(self, workflow: str, mode: str = "factory") -> MorphOSEvent:
        return self.emit(RUN_STARTED, {"workflow": workflow, "mode": mode})

    def run_completed(self, steps_completed: int, total_steps: int) -> MorphOSEvent:
        return self.emit(
            RUN_COMPLETED,
            {"steps_completed": steps_completed, "total_steps": total_steps},
        )

    def run_failed(self, reason: str, step_id: str | None = None) -> MorphOSEvent:
        payload = {"reason": reason}
        if step_id:
            payload["step_id"] = step_id
        return self.emit(RUN_FAILED, payload)

    def run_blocked(self, reason: str, step_id: str | None = None) -> MorphOSEvent:
        payload = {"reason": reason}
        if step_id:
            payload["step_id"] = step_id
        return self.emit(RUN_BLOCKED, payload)

    def run_cancelled(self, reason: str) -> MorphOSEvent:
        return self.emit(RUN_CANCELLED, {"reason": reason})

    def run_paused(self, reason: str, step_id: str | None = None) -> MorphOSEvent:
        payload = {"reason": reason}
        if step_id:
            payload["step_id"] = step_id
        return self.emit(RUN_PAUSED, payload)

    def step_executing(
        self, step_id: str, step_type: str, command: str | None = None
    ) -> MorphOSEvent:
        payload = {"step_id": step_id, "step_type": step_type}
        if command:
            payload["command"] = command
        return self.emit(STEP_EXECUTING, payload)

    def step_completed(
        self, step_id: str, output_ref: str | None = None
    ) -> MorphOSEvent:
        payload = {"step_id": step_id}
        if output_ref:
            payload["output_ref"] = output_ref
        return self.emit(STEP_COMPLETED, payload)

    def step_failed(self, step_id: str, reason: str) -> MorphOSEvent:
        return self.emit(STEP_FAILED, {"step_id": step_id, "reason": reason})

    def step_deferred(self, step_id: str, reason: str) -> MorphOSEvent:
        return self.emit(STEP_DEFERRED, {"step_id": step_id, "reason": reason})

    def step_approval_requested(
        self, step_id: str, reason: str | None = None
    ) -> MorphOSEvent:
        payload = {"step_id": step_id}
        if reason:
            payload["reason"] = reason
        return self.emit(STEP_APPROVAL_REQUESTED, payload)

    def validation_started(self, step_id: str, contracts: list[str]) -> MorphOSEvent:
        return self.emit(
            VALIDATION_STARTED, {"step_id": step_id, "contracts": contracts}
        )

    def validation_completed(self, step_id: str, result: str) -> MorphOSEvent:
        return self.emit(VALIDATION_COMPLETED, {"step_id": step_id, "result": result})

    def validation_failed(self, step_id: str, reason: str) -> MorphOSEvent:
        return self.emit(VALIDATION_FAILED, {"step_id": step_id, "reason": reason})

    def approval_requested(
        self, step_id: str, reason: str | None = None
    ) -> MorphOSEvent:
        payload = {"step_id": step_id}
        if reason:
            payload["reason"] = reason
        return self.emit(APPROVAL_REQUESTED, payload)

    def approval_approved(self, step_id: str, approver: str = "") -> MorphOSEvent:
        return self.emit(APPROVAL_APPROVED, {"step_id": step_id, "approver": approver})

    def approval_rejected(self, step_id: str, reason: str) -> MorphOSEvent:
        return self.emit(APPROVAL_REJECTED, {"step_id": step_id, "reason": reason})

    def promotion_ready(self, step_id: str, file_count: int) -> MorphOSEvent:
        return self.emit(
            PROMOTION_READY, {"step_id": step_id, "file_count": file_count}
        )

    def promotion_started(self, step_id: str, branch_name: str) -> MorphOSEvent:
        return self.emit(
            PROMOTION_STARTED, {"step_id": step_id, "branch_name": branch_name}
        )

    def promotion_completed(
        self, step_id: str, pr_url: str | None = None
    ) -> MorphOSEvent:
        payload = {"step_id": step_id}
        if pr_url:
            payload["pr_url"] = pr_url
        return self.emit(PROMOTION_COMPLETED, payload)

    def promotion_failed(self, step_id: str, reason: str) -> MorphOSEvent:
        return self.emit(PROMOTION_FAILED, {"step_id": step_id, "reason": reason})

    def get_timeline(self) -> list[MorphOSEvent]:
        events_path = self.run_dir / "artifacts" / "events_canonical.json"
        if not events_path.exists():
            return []
        data = json.loads(events_path.read_text(encoding="utf-8"))
        return [MorphOSEvent.from_dict(e) for e in data]

    def get_events_by_family(self, family: str) -> list[MorphOSEvent]:
        return [e for e in self.get_timeline() if e.event_type.startswith(f"{family}.")]

    def get_run_status(self) -> str | None:
        events = self.get_events_by_family(RUN_FAMILY)
        if not events:
            return None
        last = events[-1]
        return last.event_type.split(".")[-1]

    def _append_event(self, event: MorphOSEvent) -> None:
        events_path = self.run_dir / "artifacts" / "events_canonical.json"
        events_path.parent.mkdir(parents=True, exist_ok=True)
        events = []
        if events_path.exists():
            events = json.loads(events_path.read_text(encoding="utf-8"))
        events.append(event.to_dict())
        events_path.write_text(json.dumps(events, indent=2), encoding="utf-8")
