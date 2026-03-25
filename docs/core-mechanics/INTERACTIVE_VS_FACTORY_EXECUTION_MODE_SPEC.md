# Interactive vs Factory Execution Mode Spec

This document defines the technical specifications for implementing the split between exploratory work and fully specified execution runs, as identified in the `morphOS v0 Implementation Board`.

## Why This Spec Exists
The `morphOS` MVP requires the system to distinguish between when an operator's intent is still forming ("interactive") versus when the work may run uninterrupted to a gate ("factory").

Currently, `skyforce` handles all runs similarly. Without explicitly differentiating these modes, agents either ask too many questions during routine execution or make unchecked assumptions during ambiguous planning.

## 1. Execution Modes

### 1.1 `interactive`
*   **Purpose**: Used when the intent, scope, or context is not yet fully specified. The agent acts as a collaborator, prioritizing communication and planning over side-effecting actions.
*   **Behavior**:
    *   Agent stops frequently to ask for clarification.
    *   High-risk tools (e.g., `code.patch`, `git.push`) are strictly blocked by the `PolicyEngine` unless explicitly overridden.
    *   Workflow heavily relies on `planning_agent` and `vision_agent`.
*   **Outcome**: Produces a `feature_plan.json`, `execution_plan.json`, or a structured `WorkOrder`.

### 1.2 `factory`
*   **Purpose**: Used when the intent is fully specified, verified, and ready for end-to-end execution.
*   **Behavior**:
    *   Agent runs uninterrupted until it hits a pre-defined policy gate (e.g., `validation_gate` or `approval_gate`).
    *   Assumes silence implies consent; relies on deterministic middleware and error handlers rather than blocking for human input.
    *   Full suite of role-allowed tools is available.
*   **Outcome**: Produces code changes, artifacts, validation reports, and an `approval_packet.json` ready for promotion.

## 2. Technical Implementation Blueprint

### 2.1 Mode Configuration
The execution mode is defined at the instantiation of a `RunState`.

```python
from dataclasses import dataclass
from typing import Literal

ExecutionMode = Literal["interactive", "factory"]

@dataclass
class RunState:
    run_id: str
    mode: ExecutionMode
    # ... other fields
```

### 2.2 Orchestrator State Transitions
The `skyforce-symphony` orchestrator must alter its routing and pausing behavior based on `RunState.mode`.

```python
class Orchestrator:
    def _execute_step(self, run_dir: Path, state: RunState, step: dict[str, Any]) -> dict[str, Any]:
        if state.mode == "interactive":
            # 1. Enforce strict tool limitations
            # 2. If a step encounters ambiguity, pause with pause_reason="user_input_required"
            # 3. Emit specific signals back to Command Centre Live
            pass
        elif state.mode == "factory":
            # 1. Provide full tool access (subject to standard workspace policies)
            # 2. If a step fails, attempt deterministic retries before pausing
            pass
```

### 2.3 Policy Engine Rules
The `PolicyEngine` must become mode-aware.

```python
class PolicyEngine:
    def check_tool_execution(self, tool_action: ToolAction, context: Dict[str, Any]) -> PolicyDecision:
        mode = context.get("execution_mode", "factory")
        risk = tool_action.descriptor.risk_level

        if mode == "interactive" and risk in ["high", "critical"]:
            return PolicyDecision(
                allowed=False,
                reason=f"High risk tool '{tool_action.tool_id}' is blocked in interactive mode."
            )

        # ... factory rules ...
        return PolicyDecision(allowed=True)
```

### 2.4 Command Centre Live (UI)
The operator UI must visually distinguish between the two modes:
1.  **Interactive Mode UI**: Features a chat-like interface or a rapid feedback loop for refining the `WorkOrder`.
2.  **Factory Mode UI**: Features a Kanban-style pipeline, progress bars, and approval queues.

## 3. Workflow Examples

### Interactive Session
1.  **Operator**: "I want to add a login page."
2.  **Symphony**: Starts run in `interactive` mode.
3.  **Agent (Vision/Planning)**: "Do you want to use OAuth or email/password? Where should the mock data live?"
4.  **Operator**: Answers questions.
5.  **Agent**: Generates `execution_plan.json` and transitions the artifact to the operator.
6.  **Operator**: Clicks "Execute Plan". Symphony transitions the session or spawns a new run in `factory` mode.

### Factory Session
1.  **Symphony**: Receives approved `execution_plan.json`. Starts run in `factory` mode.
2.  **Agent (Coding)**: Executes the plan, modifying files and running tests.
3.  **Agent**: Fails a test, automatically runs a repair loop (no human intervention).
4.  **Agent**: Completes work, emits `approval.requested` signal.
5.  **Operator**: Reviews changes in the queue and clicks "Approve for Promotion".