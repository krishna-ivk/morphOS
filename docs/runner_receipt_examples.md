# morphOS v0 Runner Receipt Examples

This is the Wave 1 Agent C handoff artifact.

It captures the first stable Harness receipt and evidence shape for downstream use.

## What Landed

Harness consumption now emits a richer execution receipt and a paired evidence artifact.

Implemented in `skyforce-harness`:

- stable `run_id` and `task_execution_id` projection from the execution envelope
- `workflow_run` payload with:
  - `execution_mode`
  - `execution_mode_source`
  - `execution_mode_locked`
  - `workspace_id`
  - `workspace_admin_id`
- `approval_context` payload with:
  - `approval_state`
  - `authority_scope`
  - `required_approver_role`
  - `approval_target_id`
- `validation_handoff` payload with summary-artifact expectations
- paired artifact emission:
  - execution receipt JSON
  - evidence JSON

## Stable Receipt Shape

The receipt now includes these stable top-level areas:

- `receipt_id`
- `run_id`
- `task_execution_id`
- `workflow_run`
- `tool_action`
- `approval_context`
- `validation_handoff`
- `result_artifact_refs`

## Stable Artifact Outputs

For each consumed envelope, Harness now writes:

- `<issue>.result.json`
- `<issue>.evidence.json`

The receipt references both artifacts through `result_artifact_refs`.
The validation handoff references the evidence artifact through `evidence_ref`.

## Stable Next Actions

Harness now emits deterministic next actions:

- `program-runner-dispatch`
- `await-approval`
- `ready-for-runner`
- `inspect-only`

## Downstream Expectations

### For Agent D

You can now inventory and later render these fields in operator surfaces:

- `workflow_run.execution_mode`
- `workflow_run.workspace_id`
- `approval_context.authority_scope`
- `approval_context.required_approver_role`
- `validation_handoff.status`

### For Agent E

You can now rely on the receipt/evidence pair as the first stable Harness-side inputs for promotion and closeout work:

- receipt artifact ref
- evidence artifact ref
- approval context
- validation handoff state
- summary artifact expectations

## Files Changed In Harness

- `skyforce-harness/scripts/consume-execution-envelope.mjs`
- `skyforce-harness/scripts/test-consume-execution-envelope.mjs`
- `skyforce-harness/package.json`

## Validation

Passed:

- `npm run test:consume-envelope`
- `npm run smoke`

## Remaining Gaps

- Harness still writes planned receipts and evidence, not true native command execution results yet
- result artifacts do not yet include real validation outputs from program execution
- promotion packet generation is still pending in later waves
- shared `skyforce-core` contracts still need to encode these fields formally

## Handoff Packet

- `scope_completed`
  - aligned Harness receipt and evidence outputs with Wave 1 execution-mode, authority, and validation-handoff needs
- `files_changed`
  - `skyforce-harness/scripts/consume-execution-envelope.mjs`
  - `skyforce-harness/scripts/test-consume-execution-envelope.mjs`
  - `skyforce-harness/package.json`
- `contracts_relied_on`
  - `morphOS/docs/contract_freeze_notes.md`
  - `morphOS/docs/orchestration_state_handoff.md`
- `events_changed`
  - none; this handoff focused on receipt and artifact shape
- `artifacts_emitted`
  - `morphOS/docs/runner_receipt_examples.md`
- `open_blockers`
  - true native command execution is still pending
  - shared contract code in `skyforce-core` still needs formal field adoption
- `next_owner`
  - Agent D for operator inventory and later UI rollout
