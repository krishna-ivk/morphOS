from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field


class FeatureItem(BaseModel):
    name: str
    description: str
    priority: str
    acceptance_criteria: list[str]
    dependencies: list[str] = Field(default_factory=list)


class FeaturePlan(BaseModel):
    project_name: str
    features: list[FeatureItem]


class TaskItem(BaseModel):
    id: str
    task: str
    description: str
    status: str = "pending"
    assigned_agent: str
    feature_ref: str
    depends_on: list[str] = Field(default_factory=list)


class ValidationCheck(BaseModel):
    name: str
    result: Literal["pass", "fail", "skip"]
    evidence_ref: str | None = None
    details: str | None = None


class ValidationReport(BaseModel):
    run_id: str
    overall_result: Literal["pass", "fail", "skip"]
    checks: list[ValidationCheck]


class ArchitectureFinding(BaseModel):
    severity: str
    summary: str


class ArchitectureReport(BaseModel):
    repo_path: str
    overall_health: Literal["healthy", "concerns", "critical"]
    findings: list[ArchitectureFinding | dict[str, Any]] = Field(default_factory=list)


class CodingTaskReceipt(BaseModel):
    task_id: str
    status: str
    files_written: list[str] = Field(default_factory=list)
    tests_written: list[str] = Field(default_factory=list)
    patch_path: str | None = None
    error: str | None = None
    partial_output_ref: str | None = None
    backend: str | None = None
    model_worker_error_path: str | None = None
    cited_reference_context: list[dict[str, Any]] = Field(default_factory=list)


@dataclass
class AgentInvocation:
    agent: str
    repo_root: Any
    run_dir: Any
    context: dict[str, Any]
    payload: dict[str, Any]


@dataclass
class StepState:
    step_id: str
    status: str
    output_ref: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "StepState":
        return cls(
            step_id=payload.get("step_id", ""),
            status=payload.get("status", "pending"),
            output_ref=payload.get("output_ref"),
            details=payload.get("details", {}) or {},
        )


@dataclass
class RunState:
    run_id: str
    workflow: str
    mode: str
    status: str
    pause_reason: str | None
    steps: list[StepState]
    context: dict[str, Any]
    started_at: str
    ended_at: str | None = None
    origin: str = "test"
    current_step_index: int = 0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RunState":
        return cls(
            run_id=payload.get("run_id", ""),
            workflow=payload.get("workflow", ""),
            mode=payload.get("mode", "factory"),
            status=payload.get("status", "pending"),
            pause_reason=payload.get("pause_reason"),
            steps=[StepState.from_dict(item) for item in payload.get("steps", [])],
            context=payload.get("context", {}) or {},
            started_at=payload.get("started_at", ""),
            ended_at=payload.get("ended_at"),
            origin=payload.get("origin", "test"),
            current_step_index=payload.get("current_step_index", 0),
        )
