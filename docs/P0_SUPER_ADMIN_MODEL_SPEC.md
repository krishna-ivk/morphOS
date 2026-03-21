# P0 Super-Admin Global Authority Spec

## Origin & Influence
- **Source Influence**: software-factory governance, compliance boundary design
- **Local Owner(s)**: `morphOS`, `skyforce-core`, `sky-force-command-centre-live`

## Core Concept
A global authority model ensuring that the AI factory complies with broad security and integration rules, overarching all individual workspaces.

## Responsibilities
- **Cross-Workspace Policy**: Enforcing rules like "No agents may deploy to production without dual approval" globally.
- **Override Authority**: Unlocking or terminating `DurableExecutionRequest` instances that are rogue or blocked across any workspace.
- **Rollout Control**: Approving new tool capabilities (e.g. giving agents a new `terraform` skill) before Workspace Admins can enable them locally.

## Concrete Implementation (Compliance Boundary Design)
To properly segment compliance, `skyforce-command-centre` and `skyforce-symphony` strictly observe:

1. **Universal Override Execution**: A Super Admin can terminate or forcibly approve any `approval_packet.json` system-wide, regardless of which `workspace_id` owns the orchestration run.
2. **Strict Segregation of Policy Generation**: Workspace Admins govern local feature behavior, but **only** Super Admins define and publish global boundary policies (e.g. data egress, capability deployment).
3. **Read-Only Audit Roles**: Adopting principles from the `interaction_layer_spec`, compliance officers and read-only Super Admins have absolute visibility into global durable states without holding any write/override authority, ensuring segregation of duties.
