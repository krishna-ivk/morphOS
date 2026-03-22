# P0 Golden Path Seed Packet

## Purpose

This document defines the first real golden-path transaction for the P0 factory spine.

The goal is not to prove every morphOS doctrine. The goal is to prove one narrow, believable software-factory loop end to end.

## Selected Golden Path

### Name

`linear_sync_execution_envelope_flow`

### Outcome

Drive one small implementation task through:

`Intake -> Work Order -> Symphony Plan -> Harness Execution -> Receipt -> Command Centre Approval Surface`

For the first run, the merge step may remain manual if the upstream execution path reaches a valid approval-ready state with real artifacts.

## Why This Seed

This is the best current golden path because the implementation already exists in partial form across the active repos:

- [workflow_template_planner.ex](/home/vashista/skyforce/skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_planner.ex)
- [consume-execution-envelope.mjs](/home/vashista/skyforce/skyforce-harness/scripts/consume-execution-envelope.mjs)
- [test_linear_sync.py](/home/vashista/skyforce/skyforce-command-centre/tests/test_linear_sync.py)

It is small enough to finish and real enough to expose the weak parts of the spine.

## Target Repos

- [skyforce-symphony](/home/vashista/skyforce/skyforce-symphony)
- [skyforce-harness](/home/vashista/skyforce/skyforce-harness)
- [skyforce-command-centre](/home/vashista/skyforce/skyforce-command-centre)
- [skyforce-core](/home/vashista/skyforce/skyforce-core)

## Seed Shape

### Work Type

`feature_delivery`

### Execution Mode

`factory`

### Risk Posture

`low`

### Change Budget

- one narrow task
- one runnable command
- one receipt
- one approval-ready outcome

## Concrete User Story

When Symphony selects a workflow template and emits execution-envelope data for a small implementation lane, Harness should be able to consume that envelope, execute the bounded runner command, emit a structured receipt, and expose enough status for Command Centre to create or display the next approval or sync action without manual reshaping.

## Canonical First Task

### Candidate

`Program smoke execution lane`

### Minimal Success Change

Use the existing execution-envelope path to run one small allowlisted command and produce:

- a stable run id
- a stable task execution id
- a receipt with status
- approval context
- artifact or report paths

### Recommended Validation

- Symphony planner test proves the selected workflow exposes the expected current step payload
- Harness test proves the envelope consumer produces the expected receipt and preview output
- Command Centre test proves the resulting event can be turned into a Linear sync intent or approval-facing packet

## Required Input Packet

The golden-path seed should minimally include:

- `work_order.request.work_type`
- `work_order.request.target_repo`
- `work_order.request.execution_mode`
- `work_order.request.summary`
- `work_order.governance.approval_posture`
- `work_order.acceptance.validation_commands`

Reference example:

- [P0_GOLDEN_PATH_WORK_ORDER.json](../../examples/P0_GOLDEN_PATH_WORK_ORDER.json)

## Required Runtime Outputs

The first golden-path run is only accepted if it produces all of these:

- one valid `work_order`
- one planner-selected workflow template
- one execution envelope or equivalent runtime request payload
- one harness execution result
- one structured execution receipt
- one approval-ready or sync-ready operator payload
- one summary trail that a human can inspect quickly

## Explicit Non-Goals

The first golden path does not need to prove:

- multi-agent parallel slicing
- advanced doctrine scorecards
- multi-wave learning
- super-admin governance
- full digital twin rollout
- broad context-hub intelligence

## Exit Criteria

This seed is complete when:

1. a single seed packet can be instantiated as a real `work_order`
2. Symphony can choose the intended workflow path without manual rewriting
3. Harness can run the intended bounded command and emit a receipt
4. Command Centre can surface the next governed action from the produced artifacts
5. the run is understandable from its artifacts without reading raw source code

## Immediate Follow-On

After this seed succeeds once, the next run should stay in the same path family and only vary one dimension:

- different repo, same workflow shape
- same repo, slightly different validation command
- same workflow, one bounded retry after validation failure

That keeps the second run honest and prevents a redesign between attempts.
