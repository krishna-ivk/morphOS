# Validation Guardrails And Review Loop Spec

## Why This Spec Exists

`morphOS` already defines workflow phases, receipts, summaries, approvals, and promotion posture.
What is still missing is a single contract for how the system proves that work is acceptable before it moves forward.

This spec defines that contract.

It turns validation from "run some tests near the end" into a governed loop with:

- deterministic machine checks
- structured review routing
- bounded rework
- evidence-rich promotion posture

It is informed by the current `morphOS` delivery spine, `runner_receipt_examples.md`, and the validation-oriented gene-transfusion ideas in repositories such as `tdd-guard`, `agent-reviews`, and `openreview`.

## Executive Summary

Every delivery run must pass through a `Quality Checks` loop before it can enter the `Review Queue` or become promotion-ready.

Validation is not one thing.
It is a layered system:

1. structural validation
2. behavioral validation
3. policy validation
4. summary and evidence validation
5. human review when required

Each layer emits receipts, findings, and artifacts.
Failures do not silently disappear.
They either:

- trigger bounded automated rework
- route to review or approval
- mark the run as not promotion-ready

## Core Design Goals

- make quality checks deterministic enough to trust in factory mode
- keep validation evidence legible for humans
- avoid endless agent retry loops
- distinguish machine failure from review concern
- ensure promotion is based on evidence, not narrative confidence
- preserve compatibility with existing receipt, summary, and approval artifacts

## Validation As A Delivery Phase

Within the software-factory control flow, validation sits after implementation work and before promotion.
It is not a single step.
It is a loop with explicit entry and exit conditions.

The loop begins when execution produces a candidate output:

- code change
- configuration change
- generated artifact
- analysis result that claims completion

The loop ends only when one of these states is reached:

- `validation_passed`
- `validation_failed`
- `review_required`
- `approval_required`

## Validation Layers

### 1. Structural Validation

Structural validation checks whether the output is shaped correctly and is buildable enough to continue.

Examples:

- files compile
- formatting passes
- required files exist
- schema contracts validate
- output artifacts are present
- workflow-required receipts were emitted

This layer should be fast and deterministic.

### 2. Behavioral Validation

Behavioral validation checks whether the change behaves correctly.

Examples:

- unit tests
- integration tests
- replay tests
- contract tests
- fixture-based scenario runs
- regression checks for changed code paths

Behavioral validation is the primary proof layer for code changes.

### 3. Policy Validation

Policy validation checks whether the result is safe and allowed to proceed.

Examples:

- forbidden secret exposure
- unsafe tool usage
- missing approval for protected operations
- environment or connectivity violations
- prohibited file or branch mutations

Policy validation may fail even when tests pass.

### 4. Summary And Evidence Validation

The system must validate its own explanation artifacts before closeout.

Required artifact families include:

- `summaries/status.txt`
- `summaries/summary_short.md`
- `summaries/summary_full.md`
- `summaries/evidence.json`
- `approvals/approval_packet.json` when approval is involved

This layer checks that:

- required summary files exist
- evidence references resolve
- receipts point to real artifacts
- findings and outcomes are represented consistently
- promotion posture is supported by evidence

### 5. Human Review

Human review is not the default answer to every failure.
It is used when machine validation cannot safely decide.

Typical review triggers:

- repeated failed rework attempts
- high-risk areas
- policy-sensitive changes
- ambiguous validation output
- low-confidence auto-fixes
- promotion into protected environments

This human-facing stage maps to the `Review Queue` terminology already preferred by morphOS operator surfaces.

## Canonical Validation States

Validation engines, runtimes, and operator surfaces should converge on these states:

- `validation.pending`
- `validation.running`
- `validation.passed`
- `validation.failed`
- `validation.rework_requested`
- `validation.review_required`
- `validation.approval_required`
- `validation.skipped`

`validation.skipped` is only valid when a workflow explicitly permits it.
It must never be used as a silent fallback.

## Findings Model

Validation should emit structured findings rather than free-form complaints.

Each finding should capture:

- `finding_id`
- `category`
- `severity`
- `source`
- `summary`
- `evidence_refs`
- `suggested_rework`
- `blocking`

Suggested categories:

- `compile`
- `test`
- `contract`
- `policy`
- `security`
- `artifact`
- `summary`
- `review`

Suggested severities:

- `info`
- `warning`
- `error`
- `critical`

Only blocking findings should prevent promotion.

## Rework Loop

The validation system may request automatic rework, but the loop must be bounded.

Required rules:

- every automated rework attempt increments a visible counter
- workflows must define a maximum retry count
- repeated failures of the same class should escalate rather than loop forever
- each rework attempt must produce a new receipt and evidence delta
- the system should preserve failed validation artifacts for comparison

When the retry budget is exhausted, the run must move to:

- `review_required`, or
- `validation_failed`

## Review Loop

The review loop sits above raw validation.
Its job is to convert findings and evidence into a disposition.

Supported review outcomes:

- `accepted`
- `changes_requested`
- `blocked`
- `approval_required`

The review packet should include:

- current objective
- changed artifact set
- validation summary
- blocking findings
- evidence references
- promotion posture
- recommended next action

When possible, the review loop should consume the same receipts and summary artifacts that power machine closeout.
The system should not require humans to reconstruct the run from scratch.

## Required Validation Artifacts

Every validation-capable workflow should define output locations for:

- machine-readable validation results
- summarized validation status
- finding list
- artifact references
- rework-attempt count
- review packet when escalation occurs

Suggested baseline layout:

- `validation/results.json`
- `validation/findings.json`
- `validation/status.txt`
- `validation/rework_history.json`
- `reviews/review_packet.json`

These do not replace the summary pyramid.
They feed it.

## Receipts And Event Alignment

Validation must align with the frozen event and receipt direction already present in `morphOS`.

At minimum, the system should support:

- `validation.started`
- `validation.completed`
- `validation.failed`
- `validation.rework_requested`
- `validation.review_requested`
- `validation.approval_requested`

Receipts emitted during this phase should capture:

- validation tool or program used
- scope of validation
- artifact references
- findings summary
- pass/fail disposition
- whether rework was triggered

## Factory Mode vs Interactive Mode

In `factory` mode, validation should aggressively prefer deterministic checks and bounded rework before interrupting a human.

In `interactive` mode, the system may surface findings earlier and invite guidance sooner.

The underlying evidence model should stay the same across both modes.
Only the interruption strategy changes.

## Promotion Rule

No run may be marked promotion-ready unless:

- blocking validation findings are absent
- required validation artifacts exist
- summary and evidence artifacts are consistent
- required reviews or approvals are resolved

Narrative confidence is not enough.
Promotion posture must be evidence-backed.

## What This Changes For Skyforce

This spec implies concrete follow-on work across the runtime repos:

- `skyforce-core` should define shared finding, validation result, and review packet contracts
- `skyforce-harness` should emit stable validation receipts and artifact references
- `skyforce-symphony` should treat validation as a first-class loop with retry budgeting and escalation
- `skyforce-command-centre-live` should expose `Quality Checks`, findings, and `Review Queue` status clearly to operators
- `skyforce-api-gateway` should normalize those review and validation surfaces for operator clients

## Recommended Next Specs

This spec should be followed by:

1. `DIGITAL_TWIN_VALIDATION_SPEC.md`
2. `PYRAMID_SUMMARY_RENDERING_SPEC.md`
3. `POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md`

Together, those documents would complete the path from "did the run work?" to "can we trust what it says, and can we safely promote it?"
