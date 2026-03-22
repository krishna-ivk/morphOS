# P0 Program and Approval Execution Spec

## Origin & Influence
- **Source Influence**: `openai/symphony`, `wavezync/durable`, `morphOS` buildability plan
- **Local Owner(s)**: `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live`

## Core Concept
The abstract workflow language means nothing if it cannot execute natively and pause precisely at human intervention gates.

## Program Steps (`skyforce-harness`)
When `skyforce-symphony` evaluates a `program` node in a workflow tree:
1. A strongly-typed `DurableExecutionRequest` payload is transmitted to the `Harness` context.
2. `Harness` evaluates the sandboxing rules and runs the command (e.g. `npm run test`).
3. It emits an `ExecutionReceipt` confirming the `exit_code`, `duration_ms`, and `stdout_ref`.

## Approval Steps (`layer-8 / Human-in-the-Loop`)
When `symphony` hits an `approval` node:
1. Execution is instantly yielded using the `wavezync/durable` lifecycle patterns.
2. The UI (`sky-force-command-centre-live`) polls or is pushed the associated `approval_packet.json`.
3. The orchestration thread is suspended entirely (zero CPU churn) until a trusted `WorkspaceAdmin` injects an `ApprovalDecision` payload back into the bus.
