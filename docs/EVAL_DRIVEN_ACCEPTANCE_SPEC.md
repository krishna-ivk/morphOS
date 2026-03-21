# Eval Driven Acceptance Spec

## Why This Spec Exists

`morphOS` already defines:

- validation guardrails
- review loop automation
- token economy observability

What is still missing is a clear acceptance model:

- what evidence is sufficient to accept work?
- how do evals contribute to that decision?
- when does acceptance remain human or governed even after strong eval results?

This spec defines that model.

## Executive Summary

Acceptance should not be based on narrative confidence or ad hoc reviewer intuition alone.

It should be driven by a combination of:

- validation evidence
- eval results
- policy posture
- review and governance context

The correct posture is:

- evals strengthen acceptance confidence
- evals do not erase policy or approval boundaries
- acceptance remains evidence-backed and auditable

This makes the platform more systematic without pretending every decision can be fully automated.

## Core Design Goals

- make acceptance criteria explicit and reusable
- separate passing checks from being truly acceptable to ship or promote
- use evals as structured evidence, not as vague “AI confidence”
- preserve governance and review where judgment or authority is still required
- let workflows define acceptance surfaces without reinventing them every time

## What Acceptance Is

Acceptance is the decision that a run, slice, or artifact is good enough to advance to the next meaningful delivery posture.

Examples:

- ready to leave validation
- ready to leave review
- ready for promotion
- accepted as equivalent
- accepted as fit for operator use

Acceptance is a delivery decision, not just a test result.

## What It Is Not

Acceptance is not:

- a synonym for “tests passed”
- a synonym for “review happened”
- a synonym for “nothing obviously failed”

It should integrate multiple evidence streams.

## Canonical Acceptance Inputs

The system should consider at least these input families:

- structural validation results
- behavioral validation results
- policy findings
- review packet posture
- approval state
- eval results
- summary and evidence consistency
- promotion posture

This keeps acceptance grounded in the actual delivery loop.

## What Evals Are In This Context

For `morphOS`, evals are structured assessments that measure whether the work satisfies an expected behavior, quality bar, or acceptance property.

Examples:

- scenario-based behavior scoring
- rubric-based output evaluation
- contract compliance evaluation
- regression acceptance checks
- review-packet quality evaluation

Evals are stronger than intuition but broader than simple binary tests.

## Eval Categories

The first useful categories should be:

- `behavior_eval`
- `contract_eval`
- `summary_eval`
- `review_packet_eval`
- `policy_posture_eval`
- `equivalence_eval`

Different categories support different acceptance decisions.

## Acceptance Levels

The system should support at least these acceptance levels:

- `accepted_for_progression`
- `accepted_with_noted_risk`
- `not_accepted`
- `insufficient_evidence`
- `requires_governed_decision`

Suggested meanings:

- `accepted_for_progression`
  - the work may move to the next intended delivery state
- `accepted_with_noted_risk`
  - acceptable, but some non-blocking concerns remain visible
- `not_accepted`
  - the work should not progress
- `insufficient_evidence`
  - more proof is required before deciding
- `requires_governed_decision`
  - evidence may be sufficient technically, but authority or risk posture still requires human or governed decision

## Eval-Driven Acceptance Rule

Evals should contribute directly to acceptance only when:

- the eval category is relevant to the acceptance decision
- the underlying evidence is current
- the eval inputs are attributable
- the eval result is not contradicted by blocking policy or review findings

This prevents evals from becoming a magical override.

## Canonical Acceptance Questions

Every acceptance decision should answer:

1. what are we accepting?
2. for which next posture is it acceptable?
3. what evidence supports that decision?
4. what evals were considered?
5. what blockers still exist, if any?
6. does governance or approval still need to weigh in?

## Acceptance Surface By Phase

### Validation Phase

Acceptance question:

- is the work acceptable to leave quality checks?

Strong inputs:

- validation results
- behavior evals
- policy posture

### Review Phase

Acceptance question:

- is the work acceptable for reviewer disposition or governed decision?

Strong inputs:

- review packet quality
- summary consistency
- evidence completeness

### Promotion Phase

Acceptance question:

- is the work acceptable to propose, promote, or release?

Strong inputs:

- validation outcomes
- acceptance evals
- approval state
- policy posture

## Eval Confidence And Freshness

Each eval result should capture:

- eval category
- target artifact or run
- confidence or score
- input artifact refs
- evaluation timestamp
- evaluator identity

Stale evals should not quietly support new acceptance decisions after the underlying evidence changes.

## Acceptance And Review Automation

Review automation may prepare acceptance packets and even suggest acceptance posture.

But it should not auto-accept risky or ambiguous work unless:

- the workflow explicitly allows it
- the eval category is sufficient
- governance and policy permit it

This keeps automation supportive rather than overreaching.

## Acceptance And Governance

Some acceptance decisions remain governed even with strong eval results.

Examples:

- global exception path
- risky live action
- promotion into protected targets
- policy-sensitive drift acceptance

In these cases, evals inform the decision.
They do not replace the decider.

## Acceptance And Token Economy

Acceptance should also consider whether the run reached its result credibly.

Examples:

- strong results reached with efficient evidence-backed flow may be easier to trust
- noisy or waste-heavy runs may warrant more scrutiny even if nominal checks passed

This does not make cost the main criterion.
It makes acceptance more context-aware.

## Required Acceptance Objects

`morphOS` should support at least:

- `AcceptanceDecision`
- `AcceptanceCriterion`
- `EvalResult`
- `AcceptancePacket`
- `AcceptanceVerdict`

Suggested meanings:

- `AcceptanceCriterion`
  - a defined condition for acceptable progression
- `EvalResult`
  - structured evaluation output
- `AcceptancePacket`
  - assembled evidence used for acceptance
- `AcceptanceDecision`
  - the recorded acceptance outcome
- `AcceptanceVerdict`
  - the final posture from the accepted levels above

## Required Events

The event taxonomy should support at least:

- `acceptance.evaluated`
- `acceptance.accepted`
- `acceptance.rejected`
- `acceptance.insufficient_evidence`
- `acceptance.governed_decision_required`

Each event should include:

- `run_id`
- optional `slice_id`
- acceptance target
- acceptance level
- supporting eval categories

## Required Artifacts

Acceptance should emit durable artifacts.

Suggested baseline:

- `acceptance/criteria.json`
- `acceptance/eval_results.json`
- `acceptance/packet.json`
- `acceptance/decision.json`
- `acceptance/noted_risks.json`

These artifacts should feed:

- promotion posture
- review surfaces
- audit history
- later learning and workflow refinement

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define acceptance criteria, eval result, and acceptance decision contracts
- `skyforce-symphony` should evaluate acceptance posture at validation, review, and promotion transitions
- `skyforce-harness` should emit eval-ready evidence and structured outputs
- `skyforce-command-centre` should show acceptance posture distinctly from raw validation pass or fail

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define acceptance packet and decision contracts
2. support behavior, contract, and review-packet eval categories first
3. tie acceptance to validation and promotion transitions
4. surface `insufficient_evidence` distinctly from `not_accepted`
5. keep governed decisions explicit even when evals are strong

That is enough to make acceptance more systematic without overbuilding a full eval platform first.

## Recommended Next Specs

This spec should be followed by:

1. `UPSTREAM_DRIFT_MONITORING_SPEC.md`
2. `REFERENCE_CONTEXT_PROMOTION_SPEC.md`
3. `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`

Together, those continue drift management, memory promotion, and reusable workflow-level acceptance patterns.
