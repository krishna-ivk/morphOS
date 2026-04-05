# P0 Factory Spine Implementation Checklist

## Purpose

This checklist turns the [P0 factory spine recovery plan](P0_FACTORY_SPINE_RECOVERY_PLAN.md) into concrete implementation work across the active Skyforce repos.

The target is one successful end-to-end transaction:

`Intake -> Plan -> Code -> Harness Test -> Approval -> Merge`

## Completion Standard

This checklist is done only when:

- one real seed becomes a valid `work_order`
- one planner-generated path drives real code execution
- one harness receipt is consumed for retry or approval
- one human approval packet is used in the flow
- one change merges through the governed path

## Repo Map

- [morphOS](/home/vashista/skyforce/morphOS): doctrine source and MVP contract source
- [skyforce-core](/home/vashista/skyforce/skyforce-core): shared contracts and sync/runtime helpers
- [skyforce-symphony](/home/vashista/skyforce/skyforce-symphony): orchestration and workflow planning
- [skyforce-harness](/home/vashista/skyforce/skyforce-harness): execution and receipt loop
- [skyforce-api-gateway](/home/vashista/skyforce/skyforce-api-gateway): backend adapter and operator-facing API layer
- [skyforce-command-centre-live](/home/vashista/skyforce/skyforce-command-centre-live): primary approval and operator surface
- [skyforce-command-centre](/home/vashista/skyforce/skyforce-command-centre): transitional compatibility UI

## Phase 1: Golden Path Seed

### Select One Tiny Task

- choose one small feature or bug fix in one repo
- prefer a change with:
  - 1-3 files
  - one obvious validation command
  - low release risk

### Define the Golden Seed

- create one canonical seed packet
- confirm the target workflow type:
  - `feature_delivery` or `bug_fix`
- confirm the target repo

### Exit Condition

- the team agrees on the single golden-path seed and target repo

## Phase 2: Intake And Work Order

### `morphOS`

- use [WORK_ORDER_SCHEMA_SPEC.md](../../core-mechanics/WORK_ORDER_SCHEMA_SPEC.md) as the intake contract
- keep the schema minimal for the first run

### `skyforce-core`

- ensure shared contracts expose the minimum work-order fields needed for:
  - workflow type
  - target repo
  - execution mode
  - acceptance posture
  - governance posture

### Implementation Tasks

- create a real `work_order.json` for the golden seed
- validate that Symphony can consume it without manual translation

### Exit Condition

- one valid `work_order.json` is created and consumed by orchestration

## Phase 3: Planner To Coder Path

### `skyforce-symphony`

- map `work_order.request.work_type` to one concrete workflow path
- produce one minimal execution plan
- assign at least:
  - `planner`
  - `coder`
  - `validator`
- emit task or execution envelope data that Harness can consume directly

### `morphOS`

- use [AGENT_ARCHETYPES_SPEC.md](../../architecture/AGENT_ARCHETYPES_SPEC.md) only as role constraint
- do not expand archetype doctrine during this phase

### Exit Condition

- one planner output drives one coder task without manual reshaping

## Phase 4: Coder Execution Boundary

### `skyforce-harness`

- run the coder step inside the safest currently available execution boundary
- if containerization is not ready, define one explicit temporary bounded path and document it
- preserve:
  - cwd
  - command
  - changed files
  - exit status

### `skyforce-core`

- keep execution envelope and receipt fields minimal but complete

### Critical Requirement

- no silent unrestricted execution assumptions
- every run must leave a receipt trail

### Exit Condition

- one coder task executes and produces a structured receipt

## Phase 5: Validation And Retry

### `skyforce-harness`

- run one real validation command
- emit one structured receipt with:
  - pass/fail
  - changed files
  - artifact refs
  - validation status

### `skyforce-symphony`

- if validation fails:
  - allow one bounded retry
  - optionally allow one second retry
  - then escalate

### `morphOS`

- use [EXECUTION_RECEIPT_SCHEMA_SPEC.md](../../core-mechanics/EXECUTION_RECEIPT_SCHEMA_SPEC.md) as the target contract
- do not widen receipt doctrine beyond what the code path consumes

### Exit Condition

- failed validation returns a receipt and re-enters one bounded retry loop

## Phase 6: Approval Packet And Operator Loop

### `skyforce-command-centre-live`

- display or accept one approval packet
- show:
  - decision request
  - authority requirement
  - evidence refs
  - risk summary

### `skyforce-api-gateway`

- normalize approval packet and action responses for operator clients
- keep operator HTTP contracts stable while runtime repos evolve

### `skyforce-core`

- ensure the approval packet contract is usable in the operator surface

### `morphOS`

- use [APPROVAL_PACKET_SCHEMA_SPEC.md](../../core-mechanics/APPROVAL_PACKET_SCHEMA_SPEC.md) as the minimum packet contract

### Exit Condition

- one real approval packet is created and answered by a human

## Phase 7: Merge Path

### `skyforce-symphony`

- take approved outcome back into orchestration
- move the run into merge-ready state

### Target Repo

- merge the golden-path change through the governed path
- preserve run artifacts and summary outputs

### Exit Condition

- one real change merges after approval

## Phase 8: Minimal Telemetry

### Required Minimum

- run id
- current phase
- last receipt status
- retry count
- approval pending state
- final disposition

### Suggested Placement

- lightweight event stream or timeline in Command Centre Live
- filesystem artifacts remain the audit trail

### Exit Condition

- the golden-path run can be observed without reading raw files only

## Phase 9: Second Run

### Purpose

- prove the first run was not luck

### Requirement

- run a second tiny task through the same spine
- allow only small fixes to the spine between run one and run two

### Exit Condition

- two successful runs without redesigning the whole factory

## Stop Rules

Pause new doctrine work if:

- the planner-to-coder handoff is still manual
- receipts are not driving retries
- approval packets are not used in practice
- merge still depends on human glue outside the intended path

## Non-Goals During This Checklist

Do not expand:

- profile doctrine suites
- scorecard governance
- multi-wave learning
- advanced portfolio controls
- broad semport theory

unless they directly unblock one checklist item above.

## Suggested Ownership

- `morphOS`: contract corrections only
- `skyforce-core`: shared payloads and helper types
- `skyforce-symphony`: workflow selection, orchestration, retry routing
- `skyforce-harness`: execution boundary and receipt emission
- `skyforce-api-gateway`: operator-facing API normalization and response handling
- `skyforce-command-centre-live`: approval packet rendering and response capture

## Summary

This checklist converts the P0 recovery plan into an implementation sequence that can produce the first real factory transaction. The rule for this phase is simple: prove the line works before expanding the doctrine around it.
