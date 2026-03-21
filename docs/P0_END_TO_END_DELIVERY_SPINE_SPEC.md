# P0 End-to-End Delivery Spine Spec

## Origin & Influence
- **Source Influence**: `openai/symphony`, StrongDM `seed` and `validation`, `morphOS` MVP
- **Local Owner(s)**: `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live`, `skyforce-core`

## Core Concept
This spec defines the minimum believable software-factory loop. The core value of `morphOS` is not any single agent, but the continuous, strictly-gated pipeline that an agent traverses.

## The Spine
1. **Ticket (`Intake`)**: A `work_order.json` is generated from an upstream source (Slack, GitHub Issue, Linear).
2. **Workflow (`Planning`)**: `skyforce-symphony` selects a workflow template based on the heuristic of the ticket.
3. **Workspace (`Agent Provisioning`)**: The system maps the task to a bounded execution environment belonging to a specific `workspace_id`.
4. **Code (`Execution`)**: Agents use the `skyforce-harness` sandbox to write and test code iteratively.
5. **Validation (`Handoff`)**: The orchestrator receives an `execution_receipt.json` confirming tests pass deterministically.
6. **Approval (`Review`)**: The system emits an `approval_packet.json` to the human operator via `sky-force-command-centre-live`.
7. **Promotion (`Release`)**: The validated, approved branch is merged and deployed.

## Rules of Engagement
- No phase can be skipped unless explicitly bypassed by a **Super Admin**.
- `skyforce-symphony` is exclusively responsible for routing the state transitions between these phases.
