# Skyforce Codebase: Gap Analysis, Architecture Review, and Code Review

This document evaluates the current state of the `skyforce` repository against the `morphOS` reference architecture and doctrinal specifications.

## 1. Gap Analysis

The `morphOS` documentation outlines an ambitious, Elixir-inspired architecture with strong isolation between workflow orchestration, durable state execution, human approvals, and agentic capabilities. The current `skyforce` codebase implements a functional but tightly coupled slice of this vision.

### Missing Core Abstractions
Based on the imports in `orchestrator.py`, several critical components are either missing entirely from the repository or are stubbed poorly:
*   **`policy_engine.py`**: The `PolicyEngine` is imported but does not exist in the source tree. This violates the `P1_POLICY_HOOKS_SPEC.md` which demands a dedicated policy evaluator.
*   **`models.py`**: Strong types (`AgentInvocation`, `RunState`, `StepState`) are imported but missing. The codebase relies heavily on raw dictionaries for state tracking and event appending.
*   **`agent_backends.py`**: The `AgentRegistry` and backend resolution mechanisms are missing.

### Missing Doctrinal Features
*   **Event Taxonomy (`P1_EVENT_TAXONOMY_SPEC.md`)**: The orchestrator currently emits raw dictionaries (`self._append_event(..., {"event_type": "step.start", ...})`) instead of strongly typed `MorphOSEvent` objects. There is no shared event bus or registry.
*   **Action and Signal Contracts (`AGENT_SIGNAL_AND_ACTION_MODEL.md`)**: Agents currently execute as monolithic Python functions (e.g., `coding_agent(...)`) that perform their own side-effects (writing files directly). They do not emit semantic `Signal`s, nor are they invoked via a standardized `ActionRequest`.
*   **Tool Registry (`TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`)**: Agents do not request tools from a governed registry. The `coding_agent` manually applies fixes via `replace`, `append`, or `create` blocks parsed directly from a text directive. There is no concept of a `ToolAction` or approval-aware tool gating.
*   **Git-Native Work Ledger (`GIT_NATIVE_WORK_LEDGER_SPEC.md`)**: State is currently persisted loosely in an `artifacts/` folder rather than a formal append-only git ledger.

## 2. Architecture Decisions Review

### Orchestrator Monolith
The `Orchestrator` class in `skyforce/runtime/orchestrator.py` is doing too much. According to the architecture (`openai/symphony` influence):
*   Symphony owns workflow meaning and transitions.
*   Durable owns persistence and recovery.
*   Agents own execution.

Currently, `Orchestrator` handles file system seeding, JSON parsing, tool execution (via `subprocess.run`), agent dispatching, and durable state serialization. This violates the boundary principles set out in `AGENT_SIGNAL_AND_ACTION_MODEL.md`.

### Durable State
The current implementation writes JSON state files (`run_state.json`) and events (`events.json`) to the local file system. While this aligns with the "filesystem-first" `morphOS` doctrine, it lacks the formal Checkpoint/Resume boundaries required by the `wavezync/durable` influence. Resume logic (`_resume_from_deferred`) relies on finding the first `deferred` step and re-running from there, which could be brittle if step idempotency is not guaranteed.

### Agent / Tool Boundary
The most critical architectural violation is the lack of a tool boundary. The `coding_agent` function directly reads and writes files into the `workspace`. According to `AGENT_SIGNAL_AND_ACTION_MODEL.md`, agents should propose actions, and tools should execute side-effects after passing policy checks. The current implementation bypasses the `tool_gate` entirely.

## 3. Code Reviews

### `skyforce/runtime/orchestrator.py`
*   **Missing Imports**: `PolicyEngine`, `AgentRegistry`, `AgentInvocation`, `RunState`, and `StepState` are imported but do not exist in the repository. This causes immediate `ImportError`s unless these files are meant to be provided dynamically or were forgotten in the commit.
*   **Hardcoded Workflows**: `_load_workflow` has a hardcoded injection for `bug_fix_pipeline` if it is loaded. Workflow definitions should be entirely declarative (YAML/JSON) and loaded through the `WorkflowRegistry` as defined in `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`.
*   **Error Handling**: `subprocess.run(..., check=False)` is used for the `program` step type. If a program fails, the orchestrator continues or marks it failed, but doesn't capture standardized error classes.
*   **State Coupling**: The `JobStore` implementation traverses the `artifacts/runs` directory to find the latest run. This O(N) operation will scale poorly and should be replaced by a proper index (`index.json` or database).

### `skyforce/runtime/agents.py`
*   **Mocked Logic**: Many agents (e.g., `vision_agent`, `learning_agent`, `reviewer_agent`) are completely mocked and return hardcoded JSON. While fine for a structural prototype, this needs to be wired to actual LLM backends or the `agent_backends` registry.
*   **Coupled Side-Effects**: `coding_agent` performs direct file I/O:
    ```python
    target_path.write_text(updated, encoding="utf-8")
    ```
    This needs to be extracted into a `filesystem.write` tool action.

### `skyforce/runtime/context_hub.py`
*   **Clean Implementation**: The `ContextHub` is a relatively clean implementation of a local RAG/Search index using basic string matching.
*   **Improvement Area**: `search` uses a simple `q in text.lower()`. This will break down for complex queries. It should integrate with a proper semantic retrieval backend.

### `skyforce/runtime/retrieval.py`
*   **Fallback Logic**: The fallback logic for missing search results (defaulting to "guide" or random files) is brittle. The retrieval layer should cleanly signal "no context found" rather than injecting random documentation.

## Conclusion and Recommendations

The `skyforce` codebase serves as an MVP/prototype for the `morphOS` vision but requires significant refactoring to align with the P1 milestones.

**Next Concrete Steps (In Priority Order):**
1.  **Resolve Missing Dependencies**: Provide or implement `models.py`, `policy_engine.py`, and `agent_backends.py` so the orchestrator can run.
2.  **Event Taxonomy**: Introduce an `EventBus` and `MorphOSEvent` dataclasses to replace dict-based event tracking.
3.  **Tool Registry Extraction**: Strip side-effects out of `agents.py` and move them into a managed `ToolRegistry` with approval-aware `ToolAction` wrappers.
4.  **Action Contracts**: Standardize how the Orchestrator invokes Agents using `ActionRequest` and `ActionResponse` contracts.