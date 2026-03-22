# P1 Policy Hooks Spec

## Origin & Influence
- **Source Influence**: `morphOS` policy model
- **Local Owner(s)**: `skyforce-core`, `skyforce-symphony`, `skyforce-harness`

## Core Concept
Safety, compliance, and approval semantics must be mechanically enforced at runtime boundaries, not just written in markdown doctrines.

A Policy Hook is a synchronous runtime boundary that executes before a step or phase is allowed to transition state.

## Implementation Boundaries
1. **Intake Hook (`skyforce-core`)**: 
   - Before a `work_order.json` is accepted, check the payload shape, workspace identity, and admission posture.
2. **Command Evaluation Hook (`skyforce-harness`)**:
   - Before executing a shell command requested by an agent, inspect the command posture. If the command attempts network egress to unauthorized domains or file-system reads outside the workspace context, block it completely.
3. **Promotion Hook (`skyforce-symphony`)**:
   - Before merging code back into the source repository, the durable engine MUST halt and emit an approval request whenever promotion posture requires human review.

## Multi-Repo Responsibilities
- `skyforce-harness` enforces strictly local OS-level hooks (file write blocking, command denylists).
- `skyforce-core` provides the shared TypeScript `PolicyRule` interface.
- `skyforce-symphony` enforces abstract workflow-level hooks (forcing the workflow to pause and yield to `wavezync/durable` until a human operator clicks "Override").

`P1` needs only a small verdict language:

- `allow`
- `warn`
- `block`
- `require_review`
- `require_approval`

`P1` should prefer a small repeatable hook set over a large speculative policy lattice.

## Repo Responsibilities

### `skyforce-core`

Defines the shared hook result types and policy contract shapes.

### `skyforce-symphony`

Invokes the hooks at the orchestration boundaries and respects their verdicts.

### `skyforce-harness`

Enforces the execution hook at the command boundary.

### `skyforce-command-centre`

Projects policy-blocked or approval-required state to operators without inventing alternate meanings.

## P1 Success Condition

This spec is successful when:

1. the `P0` golden path has named policy checkpoints
2. execution and promotion can be blocked deterministically
3. approval posture is enforced by the runtime, not just expected socially

## Bottom Line

`P1` policy hooks are where the factory becomes governable. The important thing is not how many hooks exist, but that the same ones fire every time.
