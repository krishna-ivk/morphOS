# Profile Doctrine Portfolio Scorecard Decision Binding Spec

## Purpose

This spec defines how a reconciled doctrine portfolio scorecard posture binds into real portfolio decisions.

The scorecard is not meant to become a vague dashboard that people glance at and then ignore. It also is not meant to silently overrule governance, policy, or workflow-level evidence. Instead, the scorecard must have a clear and limited decision role:

- when it is only advisory
- when it raises review expectations
- when it constrains launch or expansion decisions
- when it can act as a gate input
- when it must not be used to decide anything on its own

This spec turns scorecard posture into explicit decision-binding semantics.

## Core Principle

The doctrine portfolio scorecard may influence decisions only through declared binding modes.

There is no such thing as "the scorecard looked bad so we stopped the wave" unless the scorecard posture was bound into the relevant decision class by policy or doctrine.

Likewise, there is no such thing as "the scorecard looked healthy so we approved it" unless the scorecard was only one allowed input among the other required evidence families.

## Decision Binding Goals

The binding model exists to ensure:

- scorecard usage is predictable
- operators know when scorecard posture matters operationally
- governance decisions cannot hide behind dashboard language
- maturity posture can shape planning without pretending to be direct runtime truth
- stronger doctrine claims require stronger scorecard posture where appropriate
- low-confidence scorecards cannot be used as if they were authoritative gates

## Non-Goals

This spec does not define:

- how the scorecard is calibrated
- how the scorecard is published
- how reconciliation works internally
- workflow-level acceptance or policy gating

Those are defined in separate specs. This document only defines how the resulting reconciled scorecard posture participates in decisions.

## Binding Inputs

A binding decision may reference:

- current reconciled scorecard posture
- scorecard freshness
- scorecard confidence and caveats
- trend direction
- unresolved disputes
- active exceptions
- linked portfolio intervention posture

The scorecard must be consumed in its reconciled form, not from raw publication fragments or stale snapshots.

## Decision Classes

The scorecard may bind into the following decision classes:

- planning prioritization
- doctrine change prioritization
- wave launch readiness
- wave expansion readiness
- intervention continuation or step-down
- doctrine freeze eligibility
- doctrine maturity advancement claims
- doctrine recovery or reentry expansion claims
- portfolio-level governance attention

The scorecard must not directly decide:

- code correctness
- run-level acceptance
- live production changes
- tool-action approval
- workflow-level policy exceptions

Those decisions may use doctrine posture as context, but the portfolio scorecard cannot replace direct evidence for them.

## Binding Modes

Each decision class must declare one binding mode.

### `informational`

The scorecard is visible but does not affect the outcome.

Use when:

- operators should remain aware of doctrine posture
- decisions are primarily local or runtime-specific
- the cost of overbinding would distort execution

### `advisory`

The scorecard may shape discussion, prioritization, or caution level, but decision-makers may proceed without extra approval if they document why scorecard posture did not materially change the decision.

Use when:

- doctrine posture matters, but not enough to constrain action
- human judgment should stay primary

### `review_biasing`

The scorecard does not decide the outcome, but poor or ambiguous scorecard posture automatically raises the review level, increases evidence expectations, or triggers additional cross-checks.

Use when:

- the platform wants to be more careful under weak doctrine posture
- stronger scrutiny is appropriate without becoming a hard stop

### `constraint`

The scorecard defines the allowed operating envelope for the decision. A weak scorecard may force a narrower scope, smaller wave, slower rollout, or limited claim set, even if it does not fully block the decision.

Use when:

- the decision should remain possible under weaker posture
- but its scope or confidence claims must be reduced

### `gate_input`

The scorecard is a required input into a gate, and an insufficient scorecard posture can block the decision unless an approved exception exists.

Use when:

- the platform is making a higher-order doctrine claim
- the decision depends on cross-wave or portfolio-level stability
- proceeding under weak doctrine posture would create hidden systemic risk

## Binding Strength

Binding strength must depend on:

- decision criticality
- doctrine maturity involved
- freshness of the scorecard
- confidence of the reconciled scorecard
- current intervention or failsafe posture

Higher-risk decisions require stronger binding. Lower-confidence scorecards cannot be used as strong gates unless governance explicitly accepts the weakness through a documented exception.

## Decision Binding Matrix

Recommended defaults:

- planning prioritization: `advisory`
- doctrine change prioritization: `review_biasing`
- wave launch readiness: `constraint`
- wave expansion readiness: `gate_input`
- intervention continuation or step-down: `gate_input`
- doctrine freeze eligibility: `review_biasing`
- doctrine maturity advancement claims: `gate_input`
- doctrine recovery or reentry expansion claims: `gate_input`
- portfolio-level governance attention: `constraint`

These defaults may be overridden only through governed doctrine change, not informal operator habit.

## Scorecard Sufficiency

For a scorecard to bind into a decision above `advisory`, it must be:

- current enough for the decision window
- reconciled
- free of unresolved severe contradiction
- published with visible caveats
- linked to its supporting evidence set

If any of those conditions fail, the binding level must automatically degrade:

- `gate_input` becomes `review_biasing`
- `constraint` becomes `advisory`
- `review_biasing` becomes `informational`

This prevents weak scorecard posture from silently behaving like a hard truth.

## Binding Outcomes

When a scorecard binds into a decision, the decision output must explicitly record one of these postures:

- `scorecard_not_material`
- `scorecard_supported`
- `scorecard_supported_with_caveats`
- `scorecard_triggered_higher_review`
- `scorecard_constrained_scope`
- `scorecard_blocked_without_exception`
- `scorecard_overridden_by_exception`

This keeps later audits honest about what role the scorecard actually played.

## Exceptions

If a decision proceeds against the normal scorecard binding outcome, the system must require:

- an approved exception or override route
- an explanation of why the scorecard was insufficient, incomplete, or superseded
- a time-bound scope for the exception
- a follow-up obligation if repeated exceptions suggest doctrine drift

Repeated scorecard overrides are a doctrine signal and must feed:

- scorecard calibration review
- recommendation review
- doctrine conflict review
- possible change-management intake

## Interaction With Governance

Scorecard binding never removes authority from the proper decision-maker.

Instead, it shapes what that decision-maker is allowed to claim or approve without extra process. For example:

- a workspace admin may still make a local decision
- but may not approve a broader maturity claim if scorecard binding requires a stronger portfolio posture

This means scorecard binding constrains the decision envelope, not the identity of authority by itself.

## Interaction With Portfolio Intervention

If the doctrine portfolio is under active intervention:

- scorecard binding strength should increase, not decrease
- decisions that are normally `constraint` may temporarily act as `gate_input`
- reentry and expansion decisions must use the most recent reconciled scorecard posture

If the portfolio is in failsafe or degraded governance mode:

- scorecard binding may narrow to `advisory` if the scorecard itself has low confidence
- but decision-makers must then widen human review, not proceed casually

## Interaction With Trend

A stable but declining scorecard should not be treated the same as a stable and improving scorecard when binding into decisions such as:

- wave expansion
- maturity advancement
- intervention exit
- portfolio reentry

Trend does not replace current posture, but it must shape confidence in forward-looking claims.

## Required Artifacts

Every bound decision must persist:

- the scorecard snapshot reference used
- binding mode used
- scorecard sufficiency assessment
- any downgraded binding due to stale or weak posture
- final decision outcome
- exception reference if applicable

This artifact linkage must be preserved for audit and retrospective review.

## Operator Guidance

Operators should interpret scorecard binding in a simple way:

- `informational`: notice it
- `advisory`: consider it
- `review_biasing`: review more carefully because of it
- `constraint`: narrow the allowed move because of it
- `gate_input`: do not proceed without satisfying it or formally overriding it

This simple ladder should be consistent across all operator surfaces.

## Anti-Patterns

Avoid these failures:

- treating publication views as if they were the canonical scorecard truth
- using a stale scorecard as a hard gate
- treating scorecard health as proof of runtime or code correctness
- ignoring repeated overrides that show poor binding fit
- allowing a scorecard to silently become a veto without declared binding mode
- using scorecard weakness as a vague excuse for unrelated delivery failures

## Adoption Sequence

Recommended rollout order:

1. bind scorecards as `advisory` for planning and review posture
2. adopt `constraint` for wave readiness and governance attention
3. adopt `gate_input` for maturity advancement, recovery expansion, and intervention exit
4. refine bindings only after observing exceptions, disputes, and override frequency

This keeps the platform from overbinding too early.

## Open Questions

The following may require later refinement:

- whether different doctrine areas need different default binding matrices
- whether scorecard trend should have explicit numeric impact on decision posture
- how automated recommendation systems should precompute likely binding outcomes
- whether some portfolio decisions should require multiple consecutive healthy scorecards before expansion

## Summary

The doctrine portfolio scorecard becomes operationally useful only when its role in decisions is explicit.

This spec defines that role through declared binding modes, sufficiency rules, downgrade behavior, exception handling, and auditability. The result is a scorecard that meaningfully shapes portfolio decisions without pretending to be direct runtime truth or bypassing governance.
