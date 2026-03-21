# Profile Doctrine Portfolio Reentry Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio intervention
- profile doctrine portfolio exit criteria
- profile doctrine portfolio health

What is still missing is the transition back into ordinary portfolio management after intervention has stepped down or closed.

The platform still needs clear answers to these questions:

- how does the doctrine portfolio return to normal operating posture after coordinated intervention?
- what should still be monitored during the early post-intervention period?
- how do we avoid an abrupt handoff from strategic correction back to routine management?

This spec defines that portfolio-reentry layer.

## Executive Summary

Closing an intervention is not the same as instantly becoming ordinary again.

Portfolio reentry should define the controlled return from extraordinary coordination back to normal doctrine portfolio management.

For `morphOS`, the correct posture is:

- treat post-intervention return as a governed transition
- preserve temporary observation while ordinary management resumes
- restore planning and confidence in stages where appropriate
- keep the option to re-escalate if weakness returns quickly

The goal is to make the move back to ordinary portfolio management deliberate instead of abrupt.

## Core Design Goals

- define how the portfolio resumes ordinary management after intervention
- preserve transitional monitoring without keeping intervention artificially alive
- restore ordinary planning confidence in a staged and visible way
- support rapid re-escalation if the portfolio weakens again
- preserve an auditable record of the reentry path

## Reentry Principle

After a portfolio intervention ends, the doctrine portfolio should not immediately lose all transitional context.

Reentry should therefore:

- resume ordinary management deliberately
- preserve short-lived observation and caution where justified
- prove that stability persists without strategic intervention

Intervention closure answers, "can we stand down?"
Portfolio reentry answers, "how do we return to normal safely?"

## What This Spec Covers

The first useful portfolio-reentry model should cover:

- reentry stages
- post-intervention observation posture
- restoration of ordinary planning confidence
- re-escalation triggers during reentry
- required artifacts and governance

This is enough to make post-intervention normalization disciplined instead of casual.

## Canonical Reentry Objects

`morphOS` should support at least:

- `DoctrinePortfolioReentryPlan`
- `DoctrinePortfolioReentryStage`
- `DoctrinePortfolioReentryAssessment`
- `DoctrinePortfolioReentryDecision`
- `DoctrinePortfolioReentryRecord`

Suggested meanings:

- `DoctrinePortfolioReentryPlan`
  - the intended transition from closed intervention back to normal portfolio management
- `DoctrinePortfolioReentryStage`
  - the current post-intervention normalization posture
- `DoctrinePortfolioReentryAssessment`
  - analysis of whether the portfolio is normalizing successfully
- `DoctrinePortfolioReentryDecision`
  - the official step or completion decision for reentry
- `DoctrinePortfolioReentryRecord`
  - durable history of the portfolio’s return to ordinary management

## Reentry Preconditions

Portfolio reentry should begin only when:

- an intervention has reached partial or full exit
- current residual risks are documented
- ordinary portfolio owners are clear
- post-intervention observation expectations are defined

This keeps reentry from being an implicit afterthought.

## Reentry Stages

The first useful reentry stages should include:

- `handoff_prepared`
- `observed_normalization`
- `ordinary_management_with_watchpoints`
- `fully_normalized`

Suggested meanings:

- `handoff_prepared`
  - intervention is ending and ordinary portfolio ownership is being resumed
- `observed_normalization`
  - ordinary management is active again, but the portfolio is still under explicit transitional watch
- `ordinary_management_with_watchpoints`
  - the portfolio is mostly normal, but a small number of temporary watchpoints remain
- `fully_normalized`
  - no special post-intervention posture remains at the portfolio level

These stages separate “intervention ended” from “normalization complete.”

## Transitional Observation

Reentry should preserve observation for a defined period or evidence window.

The first useful observation targets should include:

- recently stabilized doctrine clusters
- formerly critical workflow families
- wave planning assumptions that were narrowed during intervention
- doctrine areas that remain locally active even after portfolio closure

This helps catch quick relapse without keeping the full intervention alive.

## Restoration Of Ordinary Confidence

Reentry should also define how normal confidence returns.

Examples:

- restore normal planning assumptions gradually if they were constrained during intervention
- preserve explicit caveats during early observed normalization
- remove temporary watchpoints only after the portfolio shows stable ordinary behavior

This keeps restored confidence evidence-backed.

## Relationship To Portfolio Health

Portfolio reentry should reconnect intervention history back to ordinary health monitoring.

Suggested posture:

- portfolio health snapshots should continue through reentry without losing trend continuity
- reentry should appear as a transitional health posture, not a data reset
- normalization should be visible in the same portfolio health system used before intervention

## Relationship To Wave Planning

Reentry should influence wave planning until normalization is complete.

Examples:

- waves during observed normalization may still carry narrow watchpoints
- ordinary planning confidence should return fully only after reentry matures
- quick relapse during a post-intervention wave should support re-escalation

## Relationship To Freeze Posture

Reentry should also affect freeze posture.

Examples:

- early reentry may still require explicit portfolio caveats in freeze claims
- fully normalized posture should mean those special caveats are no longer needed

This keeps freeze confidence aligned with actual portfolio recovery.

## Relationship To Governance

Governance should help ensure reentry is real, not ceremonial.

Examples:

- stronger interventions may require explicit confirmation that ordinary ownership has resumed cleanly
- reentry completion should be auditable
- rapid relapse should support quicker re-escalation without ambiguity

## Re-Escalation Triggers

The first useful re-escalation triggers during reentry should include:

- renewed clustering of doctrine weakness
- sudden loss of planning confidence after constraints are relaxed
- multiple doctrine areas reentering recovery or renewal unexpectedly
- temporary watchpoints worsening instead of fading

These triggers should allow the platform to step back toward intervention if needed.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current reentry stage
- remaining portfolio watchpoints
- whether planning confidence is fully restored or still conditional
- what would trigger re-escalation
- how close the portfolio is to full normalization

This makes post-intervention recovery visible and governable.

## Required Artifacts

The first useful reentry artifacts should include:

- `portfolio_reentry_plan.md`
- `portfolio_reentry_assessment.md`
- `portfolio_reentry_status.json`
- `portfolio_reentry_summary.md`

Suggested contents:

- `portfolio_reentry_plan.md`
  - handoff posture, observation scope, remaining caveats, and normalization targets
- `portfolio_reentry_assessment.md`
  - whether the portfolio is reentering ordinary management successfully
- `portfolio_reentry_status.json`
  - machine-readable stage, watchpoints, confidence posture, and re-escalation triggers
- `portfolio_reentry_summary.md`
  - high-level explanation of current post-intervention posture

## Reentry Outcomes

The first useful portfolio reentry outcomes should include:

- `continue_observed_normalization`
- `ordinary_management_with_watchpoints`
- `fully_normalized`
- `hold_current_reentry_stage`
- `re_escalate_to_intervention`

These outcomes make post-intervention posture explicit and reversible.

## Governance Expectations

The stronger the original intervention, the stronger the expected reentry confirmation.

Suggested posture:

- smaller interventions may return to ordinary management with proportionate review
- broader stabilization efforts may require explicit step-down and normalization confirmation
- portfolios recovering from strategic pause should have clear reentry approval and re-escalation rules

## Non-Goals

This spec does not define:

- the original intervention trigger model
- the full portfolio-health scoring system
- every local doctrine follow-up task after intervention

It only defines how the portfolio safely returns from intervention posture to ordinary management.

## Bottom Line

`morphOS` should treat portfolio reentry as a real transition, not a silent reset.

After intervention ends, the portfolio should normalize through visible watchpoints, staged confidence restoration, and clear re-escalation rules before it is treated as fully ordinary again.
