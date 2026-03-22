# P0 Durable Lifecycle Spec

## Origin & Influence
- **Source Influence**: `wavezync/durable`
- **Local Owner(s)**: `skyforce-symphony`, `skyforce-core`

## Core Concept
Long-running factory work needs survivability. If an agent task takes 35 minutes, or a human approval takes 3 days, the system cannot rely on Node.js process memory.

## Capabilities Imported from `wavezync/durable`
1. **Durable Checkpoints**: Before any step executes, its inputs and intended commands are written to persistent storage (`CheckpointRecord`). If the machine reboots, `symphony` reads the last checkpoint and resumes execution.
2. **Retry Policies (Exponential Backoff)**: If a network request or container spin-up fails with a transient error, the durable engine reschedules the execution block automatically without resetting the entire workflow.
3. **Cancel Lifecycle**: If the user hits "Cancel Run" from the Command Centre, the durable engine safely propagates a `SIGTERM` or `cancellation_token` to the nested agent subprocess, records the cancelled state, and halts the workflow branch securely.

## Implementation Boundaries
We do not adopt `wavezync/durable` blindly. Its capabilities are wrapped behind local `packages/contracts` so `morphOS` retains the primary authority over what an "approval" and a "checkpoint" actually means to the operator.
