# Execution Receipt Schema Spec

## Purpose

This spec defines the canonical `execution_receipt` artifact for software-factory work.

The execution receipt is the structured proof of what an archetype or workflow step actually did.

It should answer:

- what was attempted
- what changed
- what validations ran
- what succeeded or failed
- what artifacts were produced

## Core Principle

A receipt is an evidence artifact, not a narrative summary.

## Canonical File Location

Recommended location:

- `artifacts/execution_receipt.json`

## Schema Shape

```json
{
  "schema_version": "1.0",
  "receipt_id": "rcpt_...",
  "created_at": "2026-03-21T00:00:00Z",
  "work_order_ref": "seed/work_order.json",
  "run_ref": "run_state.json",
  "producer": {},
  "execution": {},
  "changes": {},
  "validation": {},
  "outputs": {},
  "status": {},
  "annotations": {}
}
```

## Required Fields

Required top-level fields:

- `schema_version`
- `receipt_id`
- `created_at`
- `producer`
- `execution`
- `status`

## Producer Archetypes

Allowed `archetype` values:

- `planner`
- `coder`
- `reviewer`
- `validator`
- `releaser`
- `operator_liaison`

## Execution Kinds

Allowed `execution_kind` values:

- `planning_step`
- `task_slice`
- `review_step`
- `validation_step`
- `promotion_step`
- `handoff_step`

## Validation Status

Allowed `validation_status` values:

- `passed`
- `failed`
- `partial`
- `not_run`

## Execution Status

Allowed `execution_status` values:

- `succeeded`
- `succeeded_with_warnings`
- `failed`
- `blocked`
- `partial`

## Receipt Invariants

The `execution_receipt` must:

- describe actual execution, not intended work
- disclose failure or incompleteness honestly
- link to produced artifacts where possible
- be attributable to a producing archetype or step

## Summary

The `execution_receipt` is the machine-readable evidence of what a factory step actually did. It gives later review, validation, approval, and retrospective work a stable proof artifact instead of scattered logs or narrative summaries.
