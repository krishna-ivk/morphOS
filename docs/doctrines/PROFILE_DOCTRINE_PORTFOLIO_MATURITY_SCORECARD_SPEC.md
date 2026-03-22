# Profile Doctrine Portfolio Maturity Scorecard Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine maturity and regression models
- profile doctrine portfolio health, baseline, and review cadence
- portfolio authority, audit, continuity, and recovery posture

What is still missing is a compact rollup that summarizes how mature the doctrine portfolio is across these dimensions without forcing operators to read the full doctrine graph every time.

The platform still needs clear answers to these questions:

- how mature is the doctrine portfolio overall?
- which dimensions of doctrine governance are strong, weak, or still emerging?
- how can operators compare portfolio maturity over time without flattening everything into a meaningless single number?

This spec defines that portfolio maturity-scorecard layer.

## Executive Summary

The doctrine portfolio needs more than raw health signals and many individual specs.

It also needs a scorecard that summarizes current maturity across a small set of important governance dimensions.

For `morphOS`, the correct posture is:

- use a multi-dimension scorecard, not one oversimplified number
- let operators see maturity by area as well as in aggregate
- tie maturity judgments to current evidence, not historical prestige
- use the scorecard to guide prioritization, not to replace judgment

The goal is to make doctrine portfolio maturity legible without making it shallow.

## Core Design Goals

- define a concise maturity rollup for doctrine portfolio stewardship
- keep the rollup dimension-based instead of misleadingly monolithic
- connect maturity posture to evidence already defined elsewhere
- support comparison across time, areas, and waves
- preserve drill-down from scorecard to underlying reasons

## Scorecard Principle

A maturity scorecard should summarize the doctrine portfolio, not pretend to be the doctrine portfolio.

It should therefore:

- compress current maturity into a few important dimensions
- stay traceable to evidence
- highlight where confidence is deserved and where it is not

The scorecard is a navigation aid, not a substitute for real review.

## What This Spec Covers

The first useful scorecard model should cover:

- maturity dimensions
- maturity levels per dimension
- rollup rules
- scorecard update cadence
- required artifacts and operator visibility

This is enough to make doctrine portfolio maturity visible and actionable.

## Canonical Scorecard Objects

`morphOS` should support at least:

- `DoctrinePortfolioMaturityScorecard`
- `DoctrineMaturityDimension`
- `DoctrineMaturityLevel`
- `DoctrineMaturityRollup`
- `DoctrineMaturityScorecardRecord`

Suggested meanings:

- `DoctrinePortfolioMaturityScorecard`
  - the compact multidimensional maturity view for the doctrine portfolio
- `DoctrineMaturityDimension`
  - one important category of doctrine governance quality
- `DoctrineMaturityLevel`
  - the current maturity posture within that dimension
- `DoctrineMaturityRollup`
  - the aggregate interpretation across dimensions
- `DoctrineMaturityScorecardRecord`
  - durable history of scorecard updates and changes

## First Useful Maturity Dimensions

The first useful maturity dimensions should include:

- `health_and_freshness`
- `review_and_cadence`
- `decision_authority`
- `auditability`
- `continuity_and_resilience`
- `portfolio_operability`

Suggested meanings:

- `health_and_freshness`
  - how current, stable, and healthy doctrine is
- `review_and_cadence`
  - how well the portfolio is being reviewed at the intended rhythm
- `decision_authority`
  - how clearly and correctly decision rights are working
- `auditability`
  - how reliably doctrine decisions are captured and explainable later
- `continuity_and_resilience`
  - how safely doctrine governance behaves under disruption and recovers afterward
- `portfolio_operability`
  - how well baseline stewardship, triage, escalation, and load management function together

These dimensions match the main governance surfaces the docs now define.

## First Useful Maturity Levels

The first useful maturity levels should include:

- `fragile`
- `emerging`
- `reliable`
- `strong`

Suggested meanings:

- `fragile`
  - the dimension depends too much on ad hoc behavior or has obvious weak control
- `emerging`
  - the dimension exists, but is still inconsistent or lightly proven
- `reliable`
  - the dimension works consistently under ordinary conditions
- `strong`
  - the dimension is stable, evidence-backed, and resilient even under pressure

These levels are simple enough to read but still directional.

## Rollup Principle

The rollup should summarize without hiding weak dimensions.

Suggested posture:

- no single strong dimension should erase a fragile one
- the rollup should surface the weakest strategically important dimensions
- overall maturity should be constrained by unresolved fragility in core governance areas

This keeps the scorecard honest.

## Relationship To Health And Baseline

The scorecard should use health and baseline posture as core inputs.

Examples:

- repeated aging and weak freshness coverage should lower `health_and_freshness`
- unstable baseline stewardship should lower `portfolio_operability`

This prevents the scorecard from drifting away from operational reality.

## Relationship To Review Cadence

Cadence performance should shape maturity directly.

Examples:

- missed weekly or wave-readiness reviews should lower `review_and_cadence`
- restored recurring review discipline should improve that dimension over time

This rewards actual governance rhythm, not just declared intent.

## Relationship To Authority And Audit

Authority clarity and audit completeness should each shape maturity.

Examples:

- repeated authority conflicts should lower `decision_authority`
- weak decision traceability should lower `auditability`
- clean routing and auditable decision trails should support higher maturity

This keeps the scorecard grounded in real control quality.

## Relationship To Continuity And Recovery

Disruption behavior should influence maturity, not just normal-day behavior.

Examples:

- poor failsafe posture should lower `continuity_and_resilience`
- clean restoration from degraded governance should improve it

This keeps resilience from being invisible until a crisis hits.

## Relationship To Portfolio Learning

The scorecard should help point to where the portfolio most needs improvement.

Examples:

- if auditability is reliable but cadence is emerging, improvement work should focus on rhythm rather than logging
- if continuity is fragile, the platform should not overclaim governance maturity overall

This makes the scorecard actionable, not decorative.

## Update Cadence

The scorecard should be updated on a recurring but meaningful basis.

The first useful update points should include:

- weekly portfolio review
- wave-readiness review
- post-wave review
- major intervention entry or exit

This keeps the scorecard current enough to matter without becoming noisy.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current maturity by dimension
- overall rollup posture
- trend since the last major review
- the weakest dimensions currently constraining portfolio maturity
- links to the evidence behind each dimension

This makes the scorecard useful for both scanning and drill-down.

## Required Artifacts

The first useful scorecard artifacts should include:

- `doctrine_maturity_scorecard.json`
- `doctrine_maturity_summary.md`
- `doctrine_maturity_dimension_trends.json`
- `doctrine_maturity_constraints.md`

Suggested contents:

- `doctrine_maturity_scorecard.json`
  - machine-readable current maturity by dimension and rollup
- `doctrine_maturity_summary.md`
  - high-level explanation of current maturity posture and recent movement
- `doctrine_maturity_dimension_trends.json`
  - change history across scorecard dimensions
- `doctrine_maturity_constraints.md`
  - what currently prevents stronger overall maturity claims

## First Useful Outcomes

The first useful scorecard outcomes should include:

- `maturity_holding`
- `maturity_improving`
- `maturity_constrained`
- `maturity_regressing`
- `targeted_strengthening_required`

These outcomes help the scorecard point toward action.

## Governance Expectations

The scorecard should support judgment without becoming political theater.

Suggested posture:

- use the scorecard to focus attention, not to reward vanity
- do not let one summary label replace evidence-based review
- keep scorecard updates tied to real operational signals and review outputs

## Non-Goals

This spec does not define:

- a universal single-number doctrine score
- compensation or performance management systems
- replacement of portfolio review with dashboards alone

It only defines a compact, multidimensional maturity summary for doctrine portfolio governance.

## Bottom Line

`morphOS` should give the doctrine portfolio a maturity scorecard that is compact, multidimensional, and evidence-backed.

Operators should be able to see where the portfolio is strong, where it is merely emerging, where it is fragile, and what is currently limiting stronger maturity claims.
