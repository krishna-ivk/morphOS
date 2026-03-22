# Profile Doctrine Portfolio Health Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine trust decay
- profile doctrine renewal and recertification
- profile doctrine maturity, recovery, and reentry behavior

What is still missing is the portfolio-level view across many doctrine areas at once.

The platform still needs clear answers to these questions:

- how healthy is the doctrine portfolio overall?
- which doctrine areas are stable, aging, recovering, or at risk?
- how should operators prioritize attention when multiple doctrine areas need action at the same time?

This spec defines that portfolio-health layer.

## Executive Summary

Individual doctrine specs explain how one doctrine area behaves.

Portfolio health should explain how the full doctrine set looks in aggregate.

For `morphOS`, the correct posture is:

- roll up doctrine health without hiding important local detail
- make it easy to spot concentration of risk, decay, or active recovery
- distinguish between isolated weakness and portfolio-wide instability
- support prioritization of renewal, recovery, and governance attention

The goal is to help operators see whether doctrine is broadly healthy, uneven, or drifting into strategic risk.

## Core Design Goals

- define a clear health model across many doctrine areas
- support prioritization instead of only passive observation
- distinguish local issues from systemic portfolio weakness
- connect portfolio health to wave planning, freeze posture, and change management
- preserve drill-down from aggregate health to specific doctrine evidence

## Portfolio Health Principle

The doctrine portfolio should be managed like a living system, not a pile of isolated documents.

Portfolio health should therefore:

- combine local doctrine state into a readable whole
- preserve the importance of freshness, maturity, recovery, and active risk
- show concentration of issues, not just counts

Strong doctrine in one area should not hide serious weakness in another.
But one weak area should also not automatically imply total portfolio failure.

## What This Spec Covers

The first useful portfolio-health model should cover:

- doctrine health categories
- portfolio rollups
- concentration and spread of risk
- prioritization rules
- operator surfaces and artifacts

This is enough to make the doctrine set governable as a portfolio.

## Canonical Portfolio Objects

`morphOS` should support at least:

- `DoctrineHealthState`
- `DoctrinePortfolioHealthSnapshot`
- `DoctrinePortfolioRiskCluster`
- `DoctrinePortfolioPriorityQueue`
- `DoctrinePortfolioHealthRecord`

Suggested meanings:

- `DoctrineHealthState`
  - the current posture of one doctrine area
- `DoctrinePortfolioHealthSnapshot`
  - aggregate view of the doctrine portfolio at a point in time
- `DoctrinePortfolioRiskCluster`
  - a set of related doctrine areas showing similar instability, decay, or dependency pressure
- `DoctrinePortfolioPriorityQueue`
  - the current ordered list of doctrine areas needing action
- `DoctrinePortfolioHealthRecord`
  - durable history of portfolio health changes over time

## Doctrine Health Categories

The first useful doctrine health categories should include:

- `stable`
- `aging`
- `renewal_in_progress`
- `recovery_in_progress`
- `expansion_monitored`
- `at_risk`
- `critical`

Suggested meanings:

- `stable`
  - doctrine is currently healthy and fresh enough for ordinary use
- `aging`
  - doctrine is still usable, but confidence is narrowing
- `renewal_in_progress`
  - doctrine is actively being refreshed or recertified
- `recovery_in_progress`
  - doctrine is recovering from regression or stronger confidence loss
- `expansion_monitored`
  - doctrine is healthy enough for staged reentry but still under active observation
- `at_risk`
  - doctrine has meaningful weakness that requires prioritization
- `critical`
  - doctrine weakness materially threatens strategic trust or wave planning

These categories make the portfolio understandable without losing nuance.

## Portfolio Rollup Dimensions

The first useful portfolio rollups should include:

- count by health category
- count by maturity stage
- count by freshness state
- count by governance sensitivity
- count by workflow or domain dependency

This helps the platform see not just "how many problems," but "what kind of problems."

## Concentration Versus Spread

Portfolio health should distinguish:

- isolated issues
- clustered issues in one domain
- broad cross-portfolio degradation

Examples:

- one doctrine area in recovery is manageable
- many doctrine areas aging in the same workflow family may indicate systemic neglect
- many critical doctrine areas across unrelated domains may indicate portfolio-wide instability

This prevents shallow interpretation of health counts.

## Priority Rules

The first useful prioritization factors should include:

- current severity
- strategic dependency
- breadth of affected workflows or waves
- governance sensitivity
- whether weakness is spreading or recurring

Priority should reflect operational importance, not just raw count.

## Relationship To Wave Planning

Portfolio health should influence wave planning.

Examples:

- concentrated doctrine weakness in a release-critical area may justify narrower launch posture
- broad portfolio aging may argue for a renewal wave before aggressive expansion
- stable portfolio posture may support stronger freeze confidence

This helps planning stay aligned with doctrine reality.

## Relationship To Freeze Posture

Freeze confidence should reflect portfolio health, not only local doctrine confidence.

Examples:

- a healthy portfolio supports stronger system-wide freeze claims
- multiple at-risk doctrine areas may require narrower or shorter freeze assumptions
- critical clusters should be visible before freeze is declared stable

## Relationship To Change Management

Portfolio health should guide doctrine change work.

Examples:

- repeated aging in one doctrine family may justify proactive refresh or simplification
- recurring recovery cycles in a category may justify deeper redesign rather than repeated patching

This makes doctrine maintenance strategic instead of ad hoc.

## Relationship To Governance

Portfolio health should help governance bodies focus attention.

Examples:

- workspace-level operators may handle isolated aging
- cross-workspace clusters may require stronger review
- portfolio-wide critical posture may need higher-level intervention

This gives governance a portfolio view rather than only case-by-case visibility.

## Operator Surface Requirements

Operator surfaces should be able to show:

- overall portfolio health posture
- doctrine areas by category
- top priority doctrine areas needing action
- risk clusters and spread patterns
- trend over time
- effect on waves, freezes, and planning confidence

This should support both quick scanning and drill-down.

## Required Artifacts

The first useful portfolio-health artifacts should include:

- `portfolio_health_snapshot.json`
- `portfolio_health_summary.md`
- `portfolio_priority_queue.md`
- `portfolio_risk_clusters.json`

Suggested contents:

- `portfolio_health_snapshot.json`
  - machine-readable current doctrine states, counts, and trends
- `portfolio_health_summary.md`
  - high-level interpretation of portfolio health and current posture
- `portfolio_priority_queue.md`
  - ordered list of doctrine areas needing renewal, recovery, or governance attention
- `portfolio_risk_clusters.json`
  - grouped areas with related risk patterns or dependencies

## Portfolio Health Outcomes

The first useful portfolio-level outcomes should include:

- `healthy`
- `healthy_with_watchpoints`
- `uneven_requires_prioritization`
- `strategically_constrained`
- `portfolio_intervention_required`

These outcomes help summarize whether the doctrine system is merely busy or strategically threatened.

## Governance Expectations

Portfolio health should support, not replace, local doctrine decisions.

Suggested posture:

- local decisions still happen at the doctrine level
- portfolio health influences prioritization, attention, and higher-level intervention
- broader governance review should be triggered when portfolio posture becomes strategically constrained or critical

## Non-Goals

This spec does not define:

- the internal details of every doctrine state machine
- one universal scoring formula for all doctrine areas
- replacement of local doctrine evidence with aggregate metrics

It only defines how the doctrine system should be observed and managed as a portfolio.

## Bottom Line

`morphOS` should treat doctrine as a portfolio, not just a collection of separate specs.

Operators should be able to see where doctrine is strong, where it is aging, where it is recovering, and where concentrated weakness threatens broader platform confidence.
