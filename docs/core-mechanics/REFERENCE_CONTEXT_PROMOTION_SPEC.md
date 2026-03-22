# Reference Context Promotion Spec

## Why This Spec Exists

`morphOS` already defines:

- reference context as a distinct layer
- runtime attachment of Context Hub retrieval
- persistent memory as a separate layer
- upstream drift monitoring for source freshness

What is still missing is the controlled path between those layers:

- when can repeatedly useful reference context become durable memory?
- what gets promoted?
- what must remain only a reference?

This spec defines that promotion path.

## Executive Summary

Reference context should not automatically become memory just because it was useful once.

Promotion should happen only when:

- the context has repeated operational value
- provenance is clear
- trust posture is acceptable
- drift risk is understood
- a governed promotion rule is satisfied

The correct posture is:

- keep references as references by default
- promote stable lessons and usage guidance deliberately
- preserve linkage back to source references and annotations

This protects the architecture boundary while still letting the system learn.

## Core Design Goals

- preserve the distinction between external grounding and local memory
- let recurring high-value reference insights become reusable knowledge
- ensure promoted knowledge remains attributable and reviewable
- prevent low-trust or stale references from silently becoming memory
- support demotion or reevaluation when upstream drift appears

## What May Be Promoted

Good promotion candidates include:

- repeated annotation themes
- stable usage cautions
- version-specific operational lessons
- validated migration guidance
- recurring provider quirks with strong provenance

These are not raw docs.
They are distilled, governed lessons derived from reference usage.

## What Must Not Be Promoted Directly

The system should not directly promote:

- full external documents
- low-trust machine summaries with no review
- one-off run notes
- transient operational state
- unverified annotations

Those remain reference context or operational context, not memory.

## Promotion Principle

Promote the lesson, not the whole source.

That means a promoted memory record should capture:

- the distilled reusable knowledge
- why it matters
- where it came from
- how trustworthy it is

It should not simply duplicate the source material wholesale.

## Promotion Triggers

Reference-context promotion should be considered when one or more of these are true:

- the same reference or annotation is repeatedly attached across runs
- the same usage note appears in successful validation or review packets
- operators repeatedly rely on the same reference-grounded caveat
- the lesson has become part of stable workflow guidance

Repeated use alone is not enough.
Trust and freshness still matter.

## Canonical Promotion Objects

`morphOS` should support at least:

- `ReferencePromotionCandidate`
- `PromotionRationale`
- `PromotionAssessment`
- `PromotionDecision`
- `PromotedMemoryLink`

Suggested meanings:

- `ReferencePromotionCandidate`
  - a candidate lesson derived from reference use
- `PromotionRationale`
  - why the system believes promotion is useful
- `PromotionAssessment`
  - trust, freshness, and reuse analysis
- `PromotionDecision`
  - governed result of the promotion process
- `PromotedMemoryLink`
  - linkage from the new memory record back to its source references

## Promotion Criteria

The first useful criteria should include:

- repeated operational use
- clear source attribution
- acceptable trust label
- acceptable access label for the target memory scope
- no unresolved drift warning
- lesson is reusable beyond one run

If these are not met, promotion should not proceed.

## Trust Rules

Promotion should be trust-aware.

Suggested trust handling:

- `verified`
  - may be strong promotion input
- `curated`
  - promotable with assessment
- `annotated`
  - promotable if annotation provenance is strong
- `unverified`
  - usually not promotable without human review
- `machine-derived`
  - requires explicit review or promotion gating

Trust should affect promotion posture, not be ignored once the lesson seems useful.

## Drift Rules

Promoted knowledge must remain linked to upstream drift posture.

If the source reference later drifts:

- the promoted memory may need reevaluation
- confidence may be reduced
- the memory may be marked stale or demoted

This keeps promotion from creating frozen folklore detached from reality.

## Access Rules

Promotion should preserve or tighten access boundaries, not weaken them.

Examples:

- `operator-only` reference guidance should not silently become `public` memory
- local-only or restricted context may produce memory with the same or stricter access posture

Access labels should be evaluated explicitly during promotion.

## Promotion Path

The healthy path should be:

1. reference context is retrieved and used
2. repeated useful annotations or citations accumulate
3. a promotion candidate is created
4. promotion assessment checks trust, reuse, access, and drift posture
5. a governed decision accepts, rejects, or defers promotion
6. the resulting memory record is linked back to source references

The memory record should remain a local lesson, not a replacement for the source.

## Relationship To Annotations

Annotations are often the bridge between reference context and memory.

Human-authored or well-governed annotations may become strong promotion inputs.
Machine-derived annotations should generally be:

- reviewed
- confidence-scored
- promoted only with explicit acceptance

This keeps annotation usefulness without letting annotation volume become memory spam.

## Relationship To Persistent Memory

Promoted records belong in persistent memory because they have crossed the threshold from:

- “useful reference item”

to:

- “reusable lesson the system should retain”

But the promoted record should still keep:

- source refs
- annotation refs
- review or approval provenance
- drift linkage

## Relationship To Acceptance

Promotion itself should be an acceptance surface.

Acceptance should answer:

- is this lesson mature enough to become reusable memory?

Good inputs include:

- evals on reuse frequency or correctness
- review of the distilled lesson
- trust and drift posture

## Relationship To Review Automation

Review automation may help:

- detect promotion candidates
- assemble promotion packets
- validate source attribution
- flag stale or drift-sensitive candidates

But the actual promotion decision should remain governed according to risk and trust posture.

## Required Artifacts

Promotion should emit durable artifacts.

Suggested baseline:

- `reference-promotion/candidates.json`
- `reference-promotion/assessments.json`
- `reference-promotion/decisions.json`
- `reference-promotion/promoted_links.json`

These artifacts should feed:

- persistent memory creation
- audit history
- drift reevaluation
- operator review

## Required Events

The event taxonomy should support at least:

- `reference_promotion.candidate_created`
- `reference_promotion.assessed`
- `reference_promotion.accepted`
- `reference_promotion.rejected`
- `reference_promotion.reevaluation_required`

Each event should include:

- source context refs
- trust posture
- access posture
- resulting memory target when accepted

## Operator Surface Expectations

Operator views should be able to show:

- what source references produced the promoted lesson
- whether the lesson is fresh or drift-sensitive
- who approved or reviewed the promotion
- what memory record was created

This keeps promoted memory explainable.

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define promotion candidate, assessment, and promoted-memory-link contracts
- future context or memory subsystem should implement the promotion workflow
- `skyforce-symphony` may surface repeated reference use as promotion candidates
- `skyforce-command-centre` should expose promotion candidates and drift-sensitive memory posture where operators need it

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define promotion candidate and promoted-memory-link contracts
2. support human-reviewed promotion of repeated annotations first
3. preserve source refs, trust labels, and drift linkage in the promoted record
4. keep promoted memory scoped and provenance-rich
5. defer bulk automatic promotion until the evaluation and drift layers mature

That is enough to make learning possible without blurring context and memory.

## Recommended Next Specs

This spec should be followed by:

1. `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
2. `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`
3. `MEMORY_GOVERNANCE_RETENTION_SPEC.md`

Together, those continue reusable acceptance patterns, drift response, and long-term memory discipline.
