# Pyramid Summary Rendering Spec

## Why This Spec Exists

`morphOS` already freezes the minimum summary artifact names:

- `summaries/status.txt`
- `summaries/summary_short.md`
- `summaries/summary_full.md`
- `summaries/evidence.json`

It also now defines:

- validation guardrails
- digital twin validation
- software-factory control flow

What is still missing is a rendering contract for how the same underlying truth should appear at different levels of detail.

This spec defines that summary pyramid.

## Executive Summary

The platform should not create separate, drifting summaries for every surface.

Instead, each run should produce one pyramid of summaries that share the same evidence base and differ only in:

- size
- audience
- rendering style
- allowed level of interpretation

The summary pyramid should let the system move cleanly between:

- one-line posture
- short delivery recap
- full narrative
- machine-readable evidence

without changing the underlying facts.

## Core Design Goals

- keep all summary surfaces anchored to the same evidence
- allow humans and agents to zoom in and out without contradiction
- make closeout deterministic even when agents omit some summary layers
- separate fact rendering from speculative interpretation
- support CLI, operator UI, approvals, and promotion with one model

## The Pyramid Model

The summary pyramid has four canonical layers.

### Layer 1: Status Line

Artifact:

- `summaries/status.txt`

Purpose:

- one-line posture for machines and humans

Audience:

- CLI
- dashboards
- queue views
- automation filters

Allowed content:

- run id
- current posture
- current or terminal step
- concise readiness signal

This layer should be extremely stable and low-noise.

### Layer 2: Short Summary

Artifact:

- `summaries/summary_short.md`

Purpose:

- fast human-readable recap of what happened and what matters next

Audience:

- issue views
- operator summaries
- handoff notes
- delivery notifications

Allowed content:

- objective
- major outcome
- important blockers or risks
- next action
- short validation posture

This layer should normally fit into a quick skim.

### Layer 3: Full Summary

Artifact:

- `summaries/summary_full.md`

Purpose:

- expanded narrative with enough detail for inspection, review, and recovery

Audience:

- operators
- reviewers
- future agents resuming the run
- promotion and incident analysis flows

Allowed content:

- original objective
- major steps taken
- findings
- validation and twin outcomes
- approvals or review context
- unresolved risks
- recommended next actions

This layer may be narrative, but it must stay evidence-linked.

### Layer 4: Evidence Layer

Artifact:

- `summaries/evidence.json`

Purpose:

- machine-readable truth backing the human-rendered layers

Audience:

- runtimes
- validators
- promotion logic
- deterministic closeout
- advanced operator detail views

Required role:

- point to receipts, validation artifacts, approval packets, and other references that support the human summaries

This layer is the ground truth substrate for the rest of the pyramid.

## Shared Evidence Rule

Every summary layer above `evidence.json` must be derivable from the same underlying evidence set.

That means:

- `status.txt` cannot claim readiness unsupported by evidence
- `summary_short.md` cannot hide blocking findings present in evidence
- `summary_full.md` cannot invent actions or approvals not reflected in artifacts

If a surface wants a friendlier phrasing, it may re-render the truth.
It may not rewrite the truth.

## Canonical Summary Inputs

The pyramid should render from stable inputs such as:

- workflow run metadata
- current control-flow state
- execution receipts
- validation artifacts
- twin verdict artifacts
- approval packet artifacts
- promotion posture
- key changed artifact references

The summary system should prefer references over free-text-only memory.

## Summary Rendering Rules

### Rule 1: Compress, Do Not Mutate

Higher layers may compress lower layers.
They may not silently change the meaning.

### Rule 2: Preserve Blocking Truth

Any blocking validation, review, or approval issue must appear in all relevant human-facing layers.

### Rule 3: Prefer Stable Labels

Render summary state using stable delivery terms where possible, such as:

- `Quality Checks`
- `Review Queue`
- `awaiting approval`
- `ready for promotion`

### Rule 4: Separate Facts From Recommendations

Summaries may include a recommended next action, but they should distinguish:

- what happened
- what is true now
- what should happen next

### Rule 5: Deterministic Backfill Is Allowed

If an agent fails to emit `summary_short.md` or `evidence.json`, deterministic closeout may synthesize missing layers from existing artifacts.

### Rule 6: One Run, One Summary Pyramid

Different surfaces may render the pyramid differently, but they should not fork it into unrelated narratives.

## Suggested Content Contract By Layer

### `status.txt`

Suggested structure:

- `run_id`
- `posture`
- `current_step`
- `readiness`

Example shape:

- `run=abc123 posture=review_required step=quality_checks readiness=not_ready`

### `summary_short.md`

Suggested sections:

- objective
- current posture
- outcome
- blockers or risks
- next action

### `summary_full.md`

Suggested sections:

- objective and scope
- execution path
- implementation or analysis outcomes
- validation and twin results
- approvals and review state
- artifacts and evidence references
- open risks
- recommended next action

### `evidence.json`

Suggested fields in addition to the frozen minimum keys:

- `run_id`
- `issue_identifier`
- `summary_generated_at`
- `receipt_artifact_refs`
- `validation_artifact_refs`
- `twin_artifact_refs`
- `approval_artifact_refs`
- `promotion_artifact_refs`
- `current_posture`
- `current_step`

## Audience-Specific Rendering

The same pyramid may be rendered differently by surface.

### CLI

Should emphasize:

- status line
- compact short summary
- exact artifact refs when asked

### Command Centre

Should emphasize:

- short summary
- blockers
- quality-check posture
- review and approval state

### Approval Flows

Should emphasize:

- risk
- requested decision
- evidence refs
- concise summary of why the decision is needed

### Promotion Flows

Should emphasize:

- readiness
- validation support
- approval state
- artifact completeness

## Relationship To Validation And Twins

The pyramid must incorporate validation and digital twin results consistently.

That means:

- twin mode or live mode should be visible where materially relevant
- fidelity labels should appear in full summary when they affect confidence
- blocking validation findings must appear in short and full summaries
- review-required outcomes must be represented across the pyramid

## Summary Freshness

Every summary layer should be attributable to a generation moment.

Recommended metadata:

- generation timestamp
- source artifact set or hash
- renderer identity
- whether the summary was human-authored, agent-authored, or deterministic backfill

This is important when runs are resumed or reviewed later.

## Deterministic Closeout Responsibilities

Deterministic closeout should be able to:

- detect missing layers
- regenerate renderable layers from evidence
- refuse to mark a run complete when the evidence layer is missing or inconsistent
- preserve provenance of backfilled summaries

This keeps summary quality from depending entirely on the last agent that touched the run.

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define summary renderer contracts and evidence input shapes
- `skyforce-harness` should emit cleaner evidence refs for deterministic summary generation
- `skyforce-symphony` should trigger summary regeneration at stable checkpoints
- `skyforce-command-centre` should render the same pyramid at multiple zoom levels instead of inventing surface-local summaries

## Recommended First Implementation Slice

The first useful slice should be narrow:

1. standardize `status.txt`, `summary_short.md`, and `evidence.json`
2. build a deterministic renderer that consumes receipts and validation artifacts
3. render the same short summary in CLI and command-centre
4. defer richer `summary_full.md` composition until the evidence substrate is stable

## Recommended Next Specs

This spec should be followed by:

1. `POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md`
2. `GENE_TRANSFUSION_EQUIVALENCE_SPEC.md`
3. `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`

Together, those close the remaining gaps between truthful rendering, safe execution control, and reusable behavioral transfer.
