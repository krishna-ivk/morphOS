# Approval Packet Schema Spec

## Purpose

This spec defines the canonical `approval_packet` artifact for governed review and approval boundaries in the software factory MVP.

An approval packet is not a button click. It is a structured artifact that explains:

- what decision is being requested
- why approval is needed
- what evidence supports the request
- what risks remain
- who may decide

## Core Principle

Approval must be reviewable without reconstructing the entire run.

## Canonical File Location

Recommended location:

- `artifacts/approval_packet.json`

## Schema Shape

```json
{
  "schema_version": "1.0",
  "approval_id": "ap_...",
  "created_at": "2026-03-21T00:00:00Z",
  "work_order_ref": "seed/work_order.json",
  "run_ref": "run_state.json",
  "decision": {},
  "authority": {},
  "evidence": {},
  "risk": {},
  "alternatives": [],
  "requested_outcome": {},
  "annotations": {}
}
```

## Required Fields

Required top-level fields:

- `schema_version`
- `approval_id`
- `created_at`
- `decision`
- `authority`
- `evidence`
- `risk`
- `requested_outcome`

## Decision Kinds

Allowed `decision_kind` values:

- `plan_gate`
- `scope_change`
- `policy_exception`
- `promotion`
- `release`
- `incident_action`
- `other_governed_action`

## Authority Values

Allowed `required_authority` values:

- `reviewer`
- `doctrine_owner`
- `workspace_admin`
- `super_admin`
- `release_authority`
- `intervention_owner`

## Evidence Status

Allowed `evidence_status` values:

- `complete`
- `partial`
- `insufficient`

## Requested Dispositions

Allowed `requested_disposition` values:

- `approve`
- `approve_with_conditions`
- `reject`
- `request_changes`
- `defer`

## Packet Invariants

The `approval_packet` must:

- be understandable without replaying the whole run
- state the authority requirement clearly
- show whether evidence is complete or partial
- disclose residual risks honestly
- define the requested disposition explicitly

## Summary

The `approval_packet` is the structured contract for governed factory decisions. It gives the approver a bounded artifact that explains the decision request, authority posture, evidence, risk, and requested outcome without reducing approval to a button press.
