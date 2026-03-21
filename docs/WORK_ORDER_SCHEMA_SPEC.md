# Work Order Schema Spec

## Purpose

This spec defines the canonical `work_order` artifact for the morphOS software factory MVP.

The work order is the normalized intake contract that turns raw seeds such as issues, PRDs, bug reports, release requests, incident reports, and operator instructions into one stable machine-readable object that the software factory can plan, route, validate, and audit.

## Core Principle

The software factory should not reason directly from arbitrary seeds once intake has completed.

After intake, the system should operate from a normalized `work_order` that states:

- what is being asked
- what kind of work it is
- what outcome is expected
- what constraints apply
- what authority posture applies
- what evidence and acceptance posture are required

## Canonical File Location

Recommended location inside a run:

- `seed/work_order.json`

## Schema Shape

```json
{
  "schema_version": "1.0",
  "work_order_id": "wo_...",
  "created_at": "2026-03-21T00:00:00Z",
  "source": {},
  "request": {},
  "scope": {},
  "constraints": {},
  "acceptance": {},
  "governance": {},
  "routing": {},
  "references": [],
  "annotations": {}
}
```

## Required Fields

Required top-level fields:

- `schema_version`
- `work_order_id`
- `created_at`
- `source`
- `request`
- `scope`
- `constraints`
- `acceptance`
- `governance`
- `routing`

## `source`

Required fields:

- `seed_kind`
- `origin_system`
- `origin_ref`

Allowed `seed_kind` values:

- `issue`
- `prd`
- `bug_report`
- `release_request`
- `incident`
- `operator_request`
- `mixed`

## `request`

Required fields:

- `title`
- `summary`
- `work_type`
- `desired_outcome`

Allowed `work_type` values for MVP:

- `feature_delivery`
- `bug_fix`
- `repo_evaluation`
- `release_preparation`
- `incident_triage`

## `scope`

Must at least identify:

- `target_repos`

It may also carry:

- `target_surfaces`
- `in_scope`
- `out_of_scope`
- `expected_change_types`

## `constraints`

Must at least identify:

- `execution_mode`

Allowed `execution_mode` values:

- `interactive`
- `factory`

## `acceptance`

Must at least identify:

- `required_outputs`
- `done_definition`

It may also include:

- `acceptance_profile_ref`
- `required_validations`
- `eval_requirements`

## `governance`

Must at least identify:

- `approval_posture`
- `requires_human_review`

## `routing`

Must at least identify:

- `suggested_workflow`

It may also include:

- `suggested_archetypes`
- `parallelizable`
- `delivery_lane`

## Invariants

The `work_order` must:

- represent normalized request truth, not execution truth
- stay stable even if planning changes
- avoid embedding mutable run state
- be sufficient to select a workflow and archetype set
- be auditable back to the original seed

## Validation Rules

The factory should reject or return for clarification a `work_order` if:

- `work_type` is missing
- no target repo can be determined
- governance posture is contradictory
- the desired outcome is not interpretable
- acceptance is too weak to define done

## Summary

The `work_order` is the normalized intake contract for the software factory MVP. It turns raw seeds into one durable artifact that can drive planning, workflow selection, governance, validation, and audit.
