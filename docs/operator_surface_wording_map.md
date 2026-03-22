# morphOS v0 Operator Surface Wording Map

This is the Wave 1 Agent D inventory artifact.

It is an inventory-only handoff.
No final UI wiring or naming migration is included here.

## Scope Reviewed

- `sky-force-command-centre-live`
- user-facing `skyforce-core` CLI surfaces

## Stable Terms Ready For Rollout

These frozen terms now have enough upstream support to be used consistently later:

- execution mode:
  - `interactive`
  - `factory`
- authority role:
  - `workspace_admin`
  - `super_admin`
- authority scope:
  - `workspace`
  - `global`
- summary artifacts:
  - `status.txt`
  - `summary_short.md`
  - `summary_full.md`
  - `evidence.json`

## Current Surface Inventory

### Command Centre Live

Current user-facing concepts already present:

- readiness labels
- pending approvals
- validation summaries
- summary sync
- durable refresh, resume, cancel
- issue-level approval queue
- validation evidence display

Current language still too protocol-heavy or mixed:

- `workflow`
- `directive`
- `checkpoint`
- `durable`
- `publish`
- `sync`

Wave 2 migration target:

- keep `workflow` where it truly means workflow selection or step progress
- prefer delivery-facing labels over raw protocol nouns in operator summaries
- keep low-level terms available in detail views, not primary labels

### Sky CLI

Current user-facing concepts already present:

- `sky status`
- `sky workflows`
- `sky inspect`
- `sky summary`
- `sky approvals`
- `sky durable`
- `sky publish-summary`

Current language still too protocol-heavy or mixed:

- `workflow runtime action`
- `workflow directive`
- `durable execution`
- `checkpoint artifact`
- `summary publish`

Wave 2 migration target:

- keep exact technical names in detailed inspect output
- introduce shorter delivery-first labels in summaries and readiness lines
- surface approval authority and execution mode explicitly

## Missing Surface Fields Now Available Upstream

The following fields now exist upstream in Wave 1 handoffs and should be surfaced in Wave 2:

- `workflow_run.execution_mode`
- `workflow_run.execution_mode_source`
- `workflow_run.workspace_id`
- `workflow_run.workspace_admin_id`
- `approval_context.authority_scope`
- `approval_context.required_approver_role`
- `approval_context.approval_target_id`

## Recommended Label Mapping For Wave 2

Use these primary labels in operator-facing summaries where possible:

| Current mixed term | Preferred operator term |
|---|---|
| durable execution | long-running step |
| directive | approval or operator action |
| checkpoint | recovery point |
| summary publish | summary sync |
| workflow runtime action | current step action |
| blocked approval_pending | awaiting approval |

## Do Not Rename Yet

Do not rename these in Wave 1:

- artifact file names
- event names
- contract field names
- CLI commands

Wave 1 inventory should only prepare the map, not mutate stable technical interfaces.

## Highest-Value UI Additions For Wave 2

- show execution mode on issue and dashboard views
- show authority role and scope on approval cards
- show workspace ownership on run detail views
- distinguish delivery summary from low-level technical detail

## Handoff Packet

- `scope_completed`
  - inventoried current command-centre and CLI wording and mapped the highest-value delivery-language upgrades
- `files_changed`
  - `morphOS/docs/operator_surface_wording_map.md`
  - `morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md`
  - `morphOS/docs/README.md`
  - `skyforce-core/packages/contracts/src/index.ts`
- `contracts_relied_on`
  - `morphOS/docs/contract_freeze_notes.md`
  - `morphOS/docs/orchestration_state_handoff.md`
  - `morphOS/docs/runner_receipt_examples.md`
- `events_changed`
  - none
- `artifacts_emitted`
  - `morphOS/docs/operator_surface_wording_map.md`
- `open_blockers`
  - command-centre and CLI still need actual Wave 2 UI wording changes
  - not all current operator payloads expose the new fields yet
- `next_owner`
  - Agent A or contract implementation follow-up in `skyforce-core`, then Agent D Wave 2 UI rollout
