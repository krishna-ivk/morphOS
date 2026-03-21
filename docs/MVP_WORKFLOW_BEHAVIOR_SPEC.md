# MVP Workflow Behavior Spec

## Purpose

This spec defines the behavioral expectations for the five core AI software factory MVP workflows:

- feature delivery
- bug fix
- repo evaluation
- release preparation
- incident triage

## Core Principle

The YAML templates may remain the executable source of truth, but the MVP still needs a stable behavioral contract so operators and downstream systems know what each workflow means.

## Shared Workflow Expectations

All five MVP workflows must:

- begin from a normalized `work_order`
- select a compatible acceptance and policy posture
- emit the summary pyramid
- produce execution receipts for meaningful execution steps
- use approval packets where governed decisions are required
- preserve filesystem-first run artifacts

## Feature Delivery

Expected flow:
1. normalize seed into `work_order`
2. plan feature scope and decomposition
3. implement changes
4. review and validate
5. prepare promotion or release packet if applicable
6. emit summaries and receipts

## Bug Fix

Expected flow:
1. normalize bug seed into `work_order`
2. identify affected scope and likely root cause
3. implement fix
4. verify regression protection
5. emit bounded fix evidence and summaries

## Repo Evaluation

Expected flow:
1. normalize evaluation request into `work_order`
2. inspect repo structure, tests, workflows, and signals
3. identify findings, risks, and readiness posture
4. produce evaluation summary and evidence bundle

## Release Preparation

Expected flow:
1. normalize release request into `work_order`
2. gather candidate scope and dependency posture
3. validate release readiness and evidence completeness
4. package release-facing artifacts
5. request required approvals

## Incident Triage

Expected flow:
1. normalize incident seed into `work_order`
2. assess severity, uncertainty, and impacted scope
3. collect immediate evidence and likely causes
4. recommend containment or next-step actions
5. route governed actions to operators if needed

## Workflow Selection Rules

The factory should choose among these workflows primarily from `work_order.request.work_type`.

Suggested mapping:

- `feature_delivery` -> feature delivery workflow
- `bug_fix` -> bug fix workflow
- `repo_evaluation` -> repo evaluation workflow
- `release_preparation` -> release preparation workflow
- `incident_triage` -> incident triage workflow

## Completion Expectations

A workflow is not complete merely because agents stopped acting.

Completion requires:

- required artifacts emitted
- required gates satisfied or explicitly deferred
- summary pyramid present
- run disposition recorded honestly

## Summary

The five MVP workflows need explicit behavioral contracts, not just template files. This spec defines those contracts so workflow selection, archetype use, gates, and required artifacts remain predictable across the software factory MVP.
