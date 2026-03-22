# Profile Doctrine Portfolio Exit Criteria Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio health
- profile doctrine portfolio intervention
- doctrine-level recovery, renewal, and recertification behavior

What is still missing is the portfolio-level decision model for when coordinated intervention is actually complete.

The platform still needs clear answers to these questions:

- when can a portfolio intervention safely end?
- what evidence is enough to return from strategic correction to ordinary doctrine management?
- how do we prevent interventions from ending too early or dragging on without justification?

This spec defines that portfolio exit-criteria layer.

## Executive Summary

Portfolio intervention should not end just because attention fades.

It should end because the portfolio has actually improved enough to justify returning to ordinary management posture.

For `morphOS`, the correct posture is:

- require explicit exit criteria at the start of intervention
- assess those criteria using current portfolio evidence
- end intervention only when strategic risk has narrowed sufficiently
- preserve the option to step down gradually instead of switching instantly to normal posture

The goal is to make portfolio recovery explicit, durable, and honest.

## Core Design Goals

- define how portfolio interventions conclude
- require evidence-based exit decisions rather than intuition
- distinguish partial stabilization from true exit readiness
- connect exit decisions to planning, freeze posture, and governance
- preserve a durable record of why intervention ended

## Exit Principle

Portfolio intervention should end only when the reasons it began are no longer strong enough to justify coordinated extraordinary handling.

Exit should therefore:

- evaluate current portfolio posture against the original intervention triggers
- confirm that concentrated or systemic weakness has materially narrowed
- preserve caution where localized recovery is still incomplete

Ending intervention is not the same as proving the portfolio is perfect.
It means ordinary management is once again sufficient.

## What This Spec Covers

The first useful portfolio-exit model should cover:

- exit criteria categories
- evidence needed to satisfy them
- partial versus full exit decisions
- relationship to ongoing local doctrine work
- required artifacts and governance

This is enough to make portfolio intervention closure disciplined instead of vague.

## Canonical Exit Objects

`morphOS` should support at least:

- `DoctrinePortfolioExitCriteria`
- `DoctrinePortfolioExitAssessment`
- `DoctrinePortfolioExitDecision`
- `DoctrinePortfolioExitStage`
- `DoctrinePortfolioExitRecord`

Suggested meanings:

- `DoctrinePortfolioExitCriteria`
  - the defined conditions for ending or stepping down an active intervention
- `DoctrinePortfolioExitAssessment`
  - analysis of whether those conditions have been met
- `DoctrinePortfolioExitDecision`
  - the official decision to continue, step down, or exit intervention
- `DoctrinePortfolioExitStage`
  - the current closure posture for the intervention
- `DoctrinePortfolioExitRecord`
  - durable history of exit evaluation and decision making

## Exit Stages

The first useful exit stages should include:

- `not_ready`
- `partial_exit_ready`
- `step_down_active`
- `full_exit_ready`
- `closed`

Suggested meanings:

- `not_ready`
  - portfolio conditions do not yet justify reducing intervention
- `partial_exit_ready`
  - some strategic constraints may be relaxed, but not all
- `step_down_active`
  - the intervention is being reduced in a controlled way
- `full_exit_ready`
  - coordinated extraordinary handling is no longer needed
- `closed`
  - the portfolio has returned to ordinary doctrine management posture

These stages separate shrinking intervention from fully ending it.

## Exit Criteria Categories

The first useful exit criteria categories should include:

- trigger resolution
- risk concentration reduction
- planning confidence recovery
- governance confidence recovery
- local doctrine continuity

Suggested meanings:

- `trigger resolution`
  - the original portfolio intervention triggers have materially weakened
- `risk concentration reduction`
  - clustered doctrine weakness is no longer strategically concentrated
- `planning confidence recovery`
  - wave and freeze planning can proceed without extraordinary portfolio constraints
- `governance confidence recovery`
  - governance no longer requires the active strategic intervention posture
- `local doctrine continuity`
  - remaining local doctrine work can continue under ordinary management instead of portfolio exception handling

## Evidence Requirements

The first useful portfolio-exit evidence should include:

- updated portfolio health snapshots
- trend improvement since intervention began
- reduced count or severity of priority doctrine areas
- reduced cluster pressure in strategic workflow families
- current planning and governance posture showing restored confidence

Current evidence matters more than how much effort was spent.

## Partial Exit

Not every intervention should jump directly from active to closed.

Suggested posture:

- use partial exit when broad improvement exists but some portfolio constraints still need to linger
- keep reduced monitoring or narrower planning caveats during step-down
- use full exit only when those special controls are no longer necessary

This keeps closure proportional.

## Relationship To Local Doctrine Work

Portfolio exit should not require every local doctrine area to be perfect.

Suggested posture:

- local doctrine renewal or recovery may continue after portfolio exit
- portfolio intervention can close once those local issues no longer require coordinated strategic handling
- local doctrine areas should retain clear ownership and follow-up plans after closure

This prevents portfolio interventions from becoming unclosable.

## Relationship To Wave Planning

Portfolio exit should affect wave planning posture directly.

Examples:

- `partial_exit_ready` may allow some previously narrowed planning assumptions to relax
- `full_exit_ready` may restore ordinary planning confidence
- `closed` should mean strategic portfolio constraints are no longer shaping wave scope by default

## Relationship To Freeze Posture

Portfolio exit should also affect freeze posture.

Examples:

- partial exit may still require explicit caveats in freeze confidence
- full exit should mean portfolio-level freeze weakening is no longer justified

This keeps freeze posture aligned with actual portfolio stabilization.

## Relationship To Governance

Governance should help decide when intervention can stand down.

Examples:

- broader interventions should require explicit approval to close
- step-down from strategic pause should be governed more carefully than exit from a targeted intervention
- closure should preserve auditability of why broader confidence was restored

## Exit Failure Signals

The first useful signals that exit is premature should include:

- renewed clustering of doctrine weakness during step-down
- planning confidence falling again after constraints relax
- critical doctrine areas reentering recovery or regression
- governance needing to reapply extraordinary oversight immediately

These signals should support pausing or reversing exit.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current exit stage
- active exit criteria and their current status
- remaining blockers to closure
- planning and freeze posture during step-down
- whether exit is stable or at risk of reversal

This makes closure progress visible instead of assumed.

## Required Artifacts

The first useful exit artifacts should include:

- `portfolio_exit_criteria.md`
- `portfolio_exit_assessment.md`
- `portfolio_exit_decision.json`
- `portfolio_exit_summary.md`

Suggested contents:

- `portfolio_exit_criteria.md`
  - defined conditions for partial and full closure
- `portfolio_exit_assessment.md`
  - current assessment of whether those conditions are met
- `portfolio_exit_decision.json`
  - approved exit stage, caveats, monitoring posture, and governance record
- `portfolio_exit_summary.md`
  - high-level explanation of why intervention continues, steps down, or closes

## Exit Outcomes

The first useful portfolio exit outcomes should include:

- `continue_intervention`
- `step_down_with_constraints`
- `partial_exit_granted`
- `full_exit_granted`
- `exit_reversed`

These outcomes make closure posture explicit and reversible.

## Governance Expectations

The broader the original intervention, the stronger the expected closure review.

Suggested posture:

- targeted interventions may close with proportionate strategic review
- portfolio stabilization should require stronger cross-area confirmation
- strategic pause should require explicit high-authority approval for step-down and closure

## Non-Goals

This spec does not define:

- the details of every local doctrine remediation plan
- a universal scoring formula for intervention closure
- automatic closure based only on elapsed time

It only defines how the platform decides that coordinated portfolio intervention is no longer necessary.

## Bottom Line

`morphOS` should end portfolio intervention deliberately, not casually.

The platform should require clear exit criteria, current evidence, and explicit closure decisions before returning from strategic doctrine intervention to ordinary management posture.
