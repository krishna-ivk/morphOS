# Super-Admin Global Authority Model Spec

This document details the specifications for the `Super-Admin Global Authority Model` feature as prioritized in the `morphOS v0 Implementation Board`.

## Why This Spec Exists
While the `Workspace-Scoped Admin Model` handles the day-to-day operations within a bounded delivery surface, the software factory requires a higher level of governance for cross-workspace policy, audit, and platform evolution.

A global authority model is required to:
*   Enforce compliance boundaries.
*   Roll out new skills, agents, and tool integrations across the platform safely.
*   Override workspace-level decisions during exceptional circumstances.

## 1. Governance Model Overview

### 1.1 The Super-Admin
A **Super-Admin** is a designated human operator with platform-wide authority. They are not tied to a specific workspace. They are responsible for:
*   Creating workspaces and assigning Workspace Admins.
*   Defining and enforcing global policy (e.g., "No deployment tools during holiday freezes").
*   Approving the rollout of new global skills, tools, and risky capabilities.
*   Auditing visibility across all workspaces.
*   Providing approval overrides for exceptional cases (e.g., an incident response overriding a workspace freeze).

### 1.2 The Control Split
*   **Workspace Admins**: Handle routine micro-approvals for their assigned workspaces.
*   **Super-Admins**: Do not routinely micro-approve actions unless an escalation path is triggered or a global policy exception is requested.

## 2. Technical Implementation Blueprint

### 2.1 Global Configuration
The concept of a Super-Admin must be introduced to the authentication and authorization layers of `sky-force-command-centre-live` and enforced by `skyforce-core`.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class GlobalRole:
    user_id: str
    role: str  # "super_admin", "auditor"

@dataclass
class GlobalConfig:
    global_policies: List[str] = field(default_factory=list) # e.g. ["deny:deployment.execute:*"]
    roles: List[GlobalRole] = field(default_factory=list)
    allowed_global_tools: List[str] = field(default_factory=list)

    def is_super_admin(self, user_id: str) -> bool:
        return any(role.user_id == user_id and role.role == "super_admin" for role in self.roles)
```

### 2.2 Orchestrator Integration (`skyforce-symphony`)
The `Orchestrator` must support global overrides and routing rules.

```python
class Orchestrator:
    def _load_global_config(self) -> GlobalConfig:
        # Load from disk or database
        pass

    def apply_approval(self, run_id: str, decision: str, reason: str, user_id: str) -> RunState:
        state, run_dir = self._load_run(run_id)
        workspace = self._load_workspace(state.context["workspace_id"])
        global_config = self._load_global_config()

        # Super-Admin override
        if global_config.is_super_admin(user_id):
            # Log the override explicitly in the audit trail
            self._append_event(run_dir, {
                "event_type": "approval.override",
                "run_id": run_id,
                "user_id": user_id,
                "reason": reason
            })
            # ... process decision logic ...
            return state

        if not workspace.is_admin(user_id):
            raise PermissionError(f"User '{user_id}' is not an admin for workspace '{workspace.workspace_id}'.")

        # ... process decision logic ...
        return state
```

### 2.3 Policy Engine Evaluation
The `PolicyEngine` must evaluate global policies *before* workspace policies.

```python
class PolicyEngine:
    def check_tool_execution(self, tool_action: ToolAction, context: Dict[str, Any], workspace: WorkspaceConfig, global_config: GlobalConfig) -> PolicyDecision:
        tool_family = tool_action.descriptor.action_family

        # 1. Evaluate global policies first (e.g., holiday freeze)
        for policy in global_config.global_policies:
            if policy.startswith("deny:") and fnmatch.fnmatch(tool_family, policy[5:]):
                return PolicyDecision(allowed=False, reason=f"Tool family '{tool_family}' is blocked by global policy.")

        # 2. Evaluate workspace policies
        # ...

        # ... other rules ...
        return PolicyDecision(allowed=True)
```

### 2.4 Command Centre Live (UI)
The `sky-force-command-centre-live` UI must differentiate views based on global roles:
1.  **Global Audit Dashboard**: Provide Super-Admins with a cross-workspace view of all blocked runs, active escalations, and system health metrics.
2.  **Platform Configuration**: Allow Super-Admins to manage the `GlobalConfig`, adding users to roles and managing the global tool registry.
3.  **Exception Handling UI**: Clearly mark runs where a Super-Admin has provided an override in the timeline and audit logs.

## 3. Workflow Examples

### Global Policy Block
1.  **Super-Admin**: Adds `"deny:deployment.execute:*"` to the `GlobalConfig` during a system freeze.
2.  **Agent (Coding)**: Attempts to execute a deployment tool in a valid, allowed workspace.
3.  **Symphony**: The `PolicyEngine` evaluates the global policy and blocks the execution, marking the run as `failed` (or escalating it depending on workflow rules).
4.  **Workspace Admin**: Sees the run failed due to a global policy violation. They cannot override this block.

### Super-Admin Override
1.  **Agent (Coding)**: Attempts a risky change. The workspace `PolicyEngine` requires an approval gate.
2.  **Workspace Admin**: Is unavailable or offline. The run is blocked.
3.  **Super-Admin**: Sees the escalated run in the Global Audit Dashboard. Understands the urgency, clicks "Override and Approve", and provides a justification.
4.  **Symphony**: Bypasses the workspace admin check, logs an `approval.override` event, and resumes the run.