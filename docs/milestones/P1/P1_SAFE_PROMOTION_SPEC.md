# P1 Safe Promotion Spec

## Origin & Influence
- **Source Influence**: `morphOS` MVP, StrongDM `validation`
- **Local Owner(s)**: `skyforce-core`, `skyforce-symphony`

## Core Concept
A factory loop is completely meaningless if it only runs tests inside a sandbox. It must safely propose or promote validated outputs back into the real `git` source tree.

## The Promotion Lifecycle
1. **Isolated Execution**: Agents clone the target repository into an ephemeral, workspace-isolated `tmp` directory.
2. **Deterministic Validation**: Agents execute `npm run build` and `npm run test` local to the ephemeral workspace.
3. **The Yield**: `skyforce-symphony` intercepts the successful validation receipt and yields to `wavezync/durable` for a human approval gate (`promotion_gate`).
4. **The Promotion (`skyforce-core`)**: Once the Workspace Admin approves the run, `skyforce-core` executes an authenticated `git` operation:
   - Committing the changes on a new branch.
   - Pushing the branch to the remote origin.
   - Opening a Pull Request automatically populated with the `ExecutionReceipt` as proof of validity.

## Minimum Promotion Inputs

Any promotion request should carry at least:

- `task_execution_id` or equivalent final step id
- validation receipt
- approval state
- target repo and branch

## Multi-Repo Responsibilities
- `skyforce-symphony`: Orchestrates exactly WHEN the promotion can occur (post-human-approval).
- `skyforce-core`: Orchestrates HOW the promotion occurs. It securely manages the GitHub/GitLab access tokens and executes the authenticated API calls to open the PR. `Harness` and `Symphony` never touch the production access tokens.
- `skyforce-harness`: Preserves the execution and validation evidence that promotion depends on.
- `sky-force-command-centre-live`: Projects promotion readiness, approval posture, and final promotion state to operators.

## Repo Responsibilities

### `skyforce-symphony`

Owns promotion readiness and promotion gating.

### `skyforce-harness`

Owns evidence that the isolated execution completed and validated.

### `skyforce-core`

Owns the shared promotion contract and any common helper logic.

### `skyforce-command-centre`

Owns the operator-facing promotion request and status projection.

## P1 Success Condition

`P1` safe promotion is good enough when:

1. the system can distinguish validated output from promoted output
2. promotion requires explicit readiness and policy posture
3. a human can inspect promotion evidence before approving where needed

## Bottom Line

The factory is not done when it proves a change works in isolation. It is done when it can promote that change safely and traceably back to the source repository.
