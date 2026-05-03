# Human Authority Model Spec

## Purpose

This spec defines the authority boundaries for human roles within the software factory. It establishes which roles are permitted to perform sensitive operations like approving code changes, promoting releases, or modifying factory policy.

## Roles & Identity

The model recognizes the following core human roles:

- `super_admin`: Global authority. Can override any policy, approve any promotion, and manage global factory configuration.
- `admin`: Workspace-level authority. Can approve promotions and resolve directives within their assigned workspace.
- `operator`: (Future) Execution-level authority. Can trigger and monitor runs but cannot bypass major safety gates.
- `observer`: Read-only access to factory observability.

## Authority Matrix (P1/V1)

| Action Family | Action | Allowed Roles (Workspace Scope) | Allowed Roles (Global Scope) |
| :--- | :--- | :--- | :--- |
| **Directives** | Resolve Directive | `admin`, `super_admin` | `super_admin` |
| **Approvals** | Approve/Reject Packet | `admin`, `super_admin` | `super_admin` |
| **Durable** | Refresh/Resume/Cancel | `admin`, `super_admin` | `super_admin` |
| **Promotion** | Preview Promotion | (Any authenticated operator) | (Any authenticated operator) |
| **Promotion** | Apply Promotion | `admin`, `super_admin` | `super_admin` |
| **Governed Merge** | Land Changes | `admin`, `super_admin` | `super_admin` |
| **Factory Run** | Manual Run Trigger | (Any authenticated operator) | `super_admin` |

## Enforcement Mechanism

Authority is enforced at two levels:

1. **Gateway Policy Hook (`skyforce-api-gateway`)**:
   - Every sensitive POST/PATCH mutation must invoke `evaluate_policy_hook`.
   - The hook validates the `operator_role` from the signed `operator_claim`.
   - The result is persisted in the `OperatorActionReceipt`.

2. **Orchestration Boundary (`skyforce-symphony`)**:
   - Symphony emits directives that specify the `required_approver_role`.
   - Decisions are only accepted if the deciding role satisfies the requirement.

## Signed Proof of Authority

Operators must provide a signed `operator_claim` for all authoritative actions. This claim includes:
- `operator_identity`
- `operator_role`
- `workspace_id`

The gateway verifies the signature using the `SKYFORCE_OPERATOR_CLAIM_SECRET`.

## Future Extensions (P2+)

- **Granular Permissions**: Moving from role-based to capability-based access control (e.g., `can_land`, `can_approve_security_critical`).
- **Escalation Paths**: Automated escalation from `admin` to `super_admin` when a policy threshold (e.g., risk score) is exceeded.
- **Quorum Approvals**: Requirement for multiple independent admins to approve high-risk promotions.
