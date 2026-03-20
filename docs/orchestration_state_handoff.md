# morphOS v0 Orchestration State Handoff

This is the Wave 1 Agent B handoff artifact.

It describes the Symphony-side runtime state changes now available to downstream agents after the first orchestration pass.

## What Landed

The orchestration layer now exposes the Wave 1 freeze fields in live Symphony payloads and workflow approval directives.

Implemented in `skyforce-symphony`:

- inferred or declared `execution_mode` in normalized workflow progress
- `execution_mode_source` and `execution_mode_locked` in workflow progress and workflow-run payloads
- `workspace_id` and `workspace_admin_id` propagation in normalized workflow progress and workflow-run payloads
- approval directive payload defaults for:
  - `authority_scope`
  - `required_approver_role`
  - `approval_target_id`
- approval decision payload enrichment for:
  - `decider_role`
  - `authority_scope`

## Downstream Expectations

### For Agent C

Treat these as stable for the current wave:

- workflow runs default to `execution_mode: "factory"` when no declared mode exists
- runtime requests may now carry:
  - `authority_scope`
  - `required_approver_role`
  - `approval_target_id`
  - `execution_mode`
- workflow progress may now carry:
  - `execution_mode`
  - `execution_mode_source`
  - `execution_mode_locked`
  - `workspace_id`
  - `workspace_admin_id`

Harness receipts should preserve these values when they are relevant to approval, validation, evidence, or promotion.

### For Agent D

Treat these as stable UI-facing values for the current wave:

- execution modes:
  - `interactive`
  - `factory`
- authority roles:
  - `workspace_admin`
  - `super_admin`
- authority scopes:
  - `workspace`
  - `global`

Workflow-run payloads now expose the first execution-mode and workspace fields needed for operator inventory and later UI rollout.

## Files Changed In Symphony

- `skyforce-symphony/elixir/lib/symphony_elixir/execution_envelope.ex`
- `skyforce-symphony/elixir/lib/symphony_elixir/workflow_directive_bridge.ex`
- `skyforce-symphony/elixir/lib/symphony_elixir_web/presenter.ex`
- `skyforce-symphony/elixir/test/execution_envelope_test.exs`
- `skyforce-symphony/elixir/test/symphony_elixir/workflow_directive_bridge_test.exs`
- `skyforce-symphony/elixir/test/symphony_elixir/extensions_test.exs`

## Validation

Passed targeted tests:

- `mix test test/execution_envelope_test.exs test/durable_execution_request_test.exs test/symphony_elixir/workflow_directive_bridge_test.exs test/symphony_elixir/extensions_test.exs`
- `mix specs.check`

## Remaining Gaps

- shared contract code in `skyforce-core` still needs to adopt the frozen fields formally
- Symphony still infers `factory` mode by default; true mode selection logic is not implemented yet
- workspace admin identity is surfaced as a field only when provided; no real assignment flow exists yet
- policy hook transitions are not part of this handoff yet

## Handoff Packet

- `scope_completed`
  - exposed Wave 1 execution-mode and authority-routing fields in Symphony runtime payloads and approval directives
- `files_changed`
  - `skyforce-symphony/elixir/lib/symphony_elixir/execution_envelope.ex`
  - `skyforce-symphony/elixir/lib/symphony_elixir/workflow_directive_bridge.ex`
  - `skyforce-symphony/elixir/lib/symphony_elixir_web/presenter.ex`
  - `skyforce-symphony/elixir/test/execution_envelope_test.exs`
  - `skyforce-symphony/elixir/test/symphony_elixir/workflow_directive_bridge_test.exs`
  - `skyforce-symphony/elixir/test/symphony_elixir/extensions_test.exs`
- `contracts_relied_on`
  - `morphOS/docs/contract_freeze_notes.md`
  - `morphOS/docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`
  - `morphOS/docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`
- `events_changed`
  - none yet; this handoff focused on state payload and directive shape alignment
- `artifacts_emitted`
  - `morphOS/docs/orchestration_state_handoff.md`
- `open_blockers`
  - shared contract implementation in `skyforce-core` is still pending
  - runner receipts have not yet adopted the new fields
- `next_owner`
  - Agent C for Harness execution and receipt alignment
