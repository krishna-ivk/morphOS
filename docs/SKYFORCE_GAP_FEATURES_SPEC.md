# Skyforce Gap Features Specification

This document defines the technical specifications for resolving the architectural gaps identified between the `skyforce` runtime implementation and the `morphOS` doctrine.

The goal is to provide concrete implementation blueprints for the missing features in `skyforce/runtime/`.

## 1. Missing Core Interfaces

The `skyforce` runtime currently imports several classes that do not exist or are insufficiently defined. These must be implemented.

### 1.1 `AgentRegistry`
*   **Purpose**: To resolve string identifiers (e.g., `coding_agent`) into executable agent backends or functions.
*   **Interface**:
    ```python
    class AgentRegistry:
        def register(self, name: str, backend: AgentBackend) -> None: ...
        def get(self, name: str) -> AgentBackend | None: ...
    ```
*   **Location**: `skyforce/runtime/agent_backends.py`

### 1.2 `PolicyEngine`
*   **Purpose**: To evaluate runtime conditions and determine if an action or step is allowed based on the `P1_POLICY_HOOKS_SPEC.md`.
*   **Interface**:
    ```python
    @dataclass
    class PolicyDecision:
        allowed: bool
        reason: str | None

    class PolicyEngine:
        def __init__(self, repo_root: Path): ...
        def check_step_start(self, runs_dir: Path, run_id: str, step: dict[str, Any], context: dict[str, Any]) -> PolicyDecision: ...
        def check_tool_execution(self, tool_action: ToolAction) -> PolicyDecision: ...
    ```
*   **Location**: `skyforce/runtime/policy_engine.py`

### 1.3 `RunState` and `StepState`
*   **Purpose**: Strongly typed representations of the workflow execution state.
*   **Location**: `skyforce/runtime/models.py`

---

## 2. Universal Event Taxonomy (`EventBus`)

Currently, `Orchestrator._append_event()` writes raw dictionaries to `events.json`. This violates the `P1_EVENT_TAXONOMY_SPEC.md`.

### 2.1 `MorphOSEvent`
*   **Structure**:
    ```python
    from dataclasses import dataclass
    from datetime import datetime
    from typing import Any

    @dataclass
    class MorphOSEvent:
        event_type: str
        timestamp: str
        run_id: str
        workspace_id: str
        payload: dict[str, Any]
    ```

### 2.2 `EventBus`
*   **Purpose**: A centralized service for emitting, validating, and persisting events.
*   **Interface**:
    ```python
    class EventBus:
        def __init__(self, storage_path: Path): ...
        def emit(self, event: MorphOSEvent) -> None: ...
        def query(self, run_id: str) -> list[MorphOSEvent]: ...
    ```
*   **Location**: `skyforce/runtime/events.py`

---

## 3. Action and Signal Contracts

Agents currently execute as monolithic functions that perform direct side-effects. They must be refactored to use standard invocation contracts and emit semantic signals.

### 3.1 `ActionRequest` and `ActionResponse`
*   **Purpose**: Standardize how the Orchestrator assigns work to an Agent.
*   **Structure**:
    ```python
    @dataclass
    class ActionRequest:
        assignment_id: str
        run_id: str
        task_execution_id: str
        agent_id: str
        action_type: str
        context: dict[str, Any]

    @dataclass
    class ActionResponse:
        status: str  # e.g., "completed", "failed", "blocked"
        structured_result: dict[str, Any]
        artifact_refs: list[str]
        signals: list[Signal]
    ```

### 3.2 `Signal`
*   **Purpose**: Semantic messages emitted by agents (e.g., `agent.blocked`, `action.progress`).
*   **Structure**:
    ```python
    @dataclass
    class Signal:
        signal_type: str
        payload: dict[str, Any]
        emitted_at: str
    ```
*   **Location**: `skyforce/runtime/actions.py` and `skyforce/runtime/signals.py`

---

## 4. Tool Registry and Execution Engine

The orchestrator currently uses `subprocess.run` directly for `program` steps, and the `coding_agent` performs raw filesystem manipulation. These must be abstracted behind a governed tool boundary.

### 4.1 `ToolDescriptor`
*   **Purpose**: Durable metadata defining a tool's capabilities and risk.
*   **Structure**:
    ```python
    @dataclass
    class ToolDescriptor:
        tool_id: str
        action_family: str  # e.g., "filesystem.write"
        risk_level: str     # "low", "medium", "high", "critical"
        input_schema: dict[str, Any]
    ```

### 4.2 `ToolAction`
*   **Purpose**: A proposed or executed use of a tool.
*   **Structure**:
    ```python
    @dataclass
    class ToolAction:
        tool_action_id: str
        run_id: str
        tool_id: str
        payload: dict[str, Any]
        status: str  # "planned", "pending_approval", "running", "completed", "failed"
    ```

### 4.3 `ToolRegistry` and `ToolExecutionEngine`
*   **Purpose**: The Registry discovers and loads tools. The Execution Engine enforces policy gates before executing them.
*   **Interface**:
    ```python
    class ToolRegistry:
        def get_descriptor(self, tool_id: str) -> ToolDescriptor: ...
        def list_available_tools(self, role: str) -> list[ToolDescriptor]: ...

    class ToolExecutionEngine:
        def __init__(self, registry: ToolRegistry, policy_engine: PolicyEngine): ...
        def execute(self, action: ToolAction) -> dict[str, Any]: ...
    ```
*   **Location**: `skyforce/runtime/tools.py`

---

## 5. Implementation Roadmap

1.  **Phase 1: Foundation**: Create `models.py`, `policy_engine.py`, and `agent_backends.py` with mock/stub implementations so the orchestrator can run without `ImportError`.
2.  **Phase 2: Observability**: Implement `events.py` and refactor `Orchestrator._append_event()` to use the `EventBus`.
3.  **Phase 3: Execution Boundaries**: Implement `actions.py` and `tools.py`. Refactor the `coding_agent` to return a `ToolAction` (e.g., `filesystem.write`) instead of modifying files directly.
4.  **Phase 4: Tool Engine Integration**: Wire the `ToolExecutionEngine` into the Orchestrator so that tools requested by agents are evaluated by the `PolicyEngine` before execution.