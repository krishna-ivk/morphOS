# Workspace-Scoped Admin Model Spec

This document defines the technical specifications for implementing the `Workspace-Scoped Admin Model` feature, as outlined in the `morphOS v0 Implementation Board`.

## Why This Spec Exists
The `morphOS` MVP requires a clear governance structure. Every workspace needs a named human authority for approvals, local rules, and escalations. Without this structure, the software factory cannot operate with clear ownership, leading to confused routing, insecure access, and unclear accountability for high-risk actions.

## 1. Governance Model Overview

### 1.1 The Workspace
A **Workspace** is a bounded context for a specific delivery surface, repository group, or project. It has:
*   An isolated environment (e.g., dedicated API keys, permissions, filesystem layout).
*   A set of active runs (`RunState` objects).
*   A defined set of policies and allowed tools.

### 1.2 The Workspace Admin
A **Workspace Admin** is the designated human authority over a specific workspace. They are responsible for:
*   Approving risky actions (e.g., `code.patch`, `git.push`) that occur *within* the workspace.
*   Reviewing blocked or failed runs.
*   Curating local rules, exemplars, and reference contexts.
*   Managing the allowlist for tools and capabilities within their boundary.
*   Deciding what can auto-merge versus what requires review.

## 2. Technical Implementation Blueprint

### 2.1 Workspace Configuration
The concept of a workspace must move from being implicitly defined by `workspace_id` strings to a formally modeled entity in `skyforce-core`.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class WorkspaceRole:
    user_id: str
    role: str  # "admin", "operator", "viewer"

@dataclass
class WorkspaceConfig:
    workspace_id: str
    name: str
    description: str
    roles: List[WorkspaceRole] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list) # e.g. ["git.*", "code.patch", "filesystem.*"]
    auto_merge_paths: List[str] = field(default_factory=list) # Paths that do not require review

    def is_admin(self, user_id: str) -> bool:
        return any(role.user_id == user_id and role.role == "admin" for role in self.roles)
```

### 2.2 Orchestrator Integration (`skyforce-symphony`)
The `Orchestrator` must load the `WorkspaceConfig` when executing a run and enforce role-based access for decisions.

```python
class Orchestrator:
    def _load_workspace(self, workspace_id: str) -> WorkspaceConfig:
        # Load from disk or database
        pass

    def apply_approval(self, run_id: str, decision: str, reason: str, user_id: str) -> RunState:
        state, run_dir = self._load_run(run_id)
        workspace = self._load_workspace(state.context["workspace_id"])

        if not workspace.is_admin(user_id):
            raise PermissionError(f"User '{user_id}' is not an admin for workspace '{workspace.workspace_id}'.")

        # ... apply decision logic ...
        return state
```

### 2.3 Policy Engine Evaluation
The `PolicyEngine` must become aware of the `WorkspaceConfig` when gating tool executions.

```python
class PolicyEngine:
    def check_tool_execution(self, tool_action: ToolAction, context: Dict[str, Any], workspace: WorkspaceConfig) -> PolicyDecision:
        tool_family = tool_action.descriptor.action_family

        # 1. Check if the tool family is explicitly allowed in this workspace
        is_allowed = False
        for pattern in workspace.allowed_tools:
            if fnmatch.fnmatch(tool_family, pattern):
                is_allowed = True
                break

        if not is_allowed:
             return PolicyDecision(allowed=False, reason=f"Tool family '{tool_family}' is not allowed in workspace '{workspace.workspace_id}'.")

        # ... other rules ...
        return PolicyDecision(allowed=True)
```

### 2.4 Command Centre Live (UI)
The `sky-force-command-centre-live` UI must:
1.  **Filter Views**: Ensure users only see active runs and approval queues for workspaces they are a part of.
2.  **Role Enforcement**: Hide the "Approve/Reject" buttons for users who lack the "admin" role for a given workspace.
3.  **Settings Panel**: Provide a dedicated interface for Workspace Admins to manage tool allowlists and auto-merge paths.

## 3. Workflow Examples

### Blocked Tool Approval
1.  **Agent (Coding)**: Attempts to execute a `git.push` `ToolAction` via the `ToolExecutionEngine`.
2.  **Symphony**: Determines the tool requires an explicit `approval_gate`. The run transitions to `pending_approval`. Emits `approval.requested` signal.
3.  **Operator**: Navigates to the Command Centre UI. They are an "operator" but not an "admin". They can view the reason for the block but cannot click "Approve".
4.  **Workspace Admin**: Logs in, sees the blocked run, and clicks "Approve".
5.  **Symphony**: Validates the `user_id` against the `WorkspaceConfig`, processes the decision, and resumes the run.