# Profile Doctrine Portfolio Baseline Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio health
- profile doctrine portfolio intervention, exit, and reentry
- doctrine-level recovery, renewal, decay, and recertification behavior

What is still missing is the steady-state operating model for the doctrine portfolio when no extraordinary intervention is active.

The platform still needs clear answers to these questions:

- what does normal doctrine portfolio management look like?
- what should be monitored continuously even when the portfolio is healthy?
- how should the platform distinguish ordinary maintenance from strategic intervention?

This spec defines that portfolio-baseline layer.

## Executive Summary

Most of the time, the doctrine portfolio should not be under extraordinary intervention.

Baseline portfolio management should define the ordinary posture for:

- monitoring health
- prioritizing routine maintenance
- preserving freshness and maturity
- surfacing early warnings before intervention is needed

For `morphOS`, the correct posture is:

- treat baseline management as active stewardship, not passive waiting
- preserve continuous visibility into doctrine freshness, stability, and portfolio trends
- handle ordinary maintenance early so portfolio intervention remains exceptional
- keep clear boundaries between routine baseline operations and strategic correction

The goal is to make the healthy state explicit, governable, and sustainable.

## Core Design Goals

- define the normal operating posture for the doctrine portfolio
- distinguish routine stewardship from extraordinary intervention
- support early detection of decay, clustering, and drift
- connect baseline management to planning and freeze confidence
- preserve an auditable steady-state management model

## Baseline Principle

Healthy doctrine does not maintain itself automatically.

Baseline management should therefore:

- continuously observe the portfolio
- prioritize routine refresh and maintenance before issues compound
- keep ordinary planning confidence aligned with current doctrine health

Baseline is not “nothing happening.”
It is disciplined, low-drama stewardship.

## What This Spec Covers

The first useful baseline model should cover:

- ordinary doctrine portfolio activities
- baseline health monitoring
- routine prioritization
- maintenance and refresh posture
- relationship to intervention triggers

This is enough to define what good day-to-day doctrine operations look like.

## Canonical Baseline Objects

`morphOS` should support at least:

- `DoctrinePortfolioBaselineState`
- `DoctrinePortfolioBaselineSnapshot`
- `DoctrinePortfolioRoutinePriorityQueue`
- `DoctrinePortfolioWatchpoint`
- `DoctrinePortfolioBaselineRecord`

Suggested meanings:

- `DoctrinePortfolioBaselineState`
  - the current steady-state posture of the portfolio when no extraordinary intervention is active
- `DoctrinePortfolioBaselineSnapshot`
  - the ordinary operating view of portfolio health and maintenance needs
- `DoctrinePortfolioRoutinePriorityQueue`
  - current routine doctrine work ordered by importance
- `DoctrinePortfolioWatchpoint`
  - an early warning signal that does not yet justify intervention
- `DoctrinePortfolioBaselineRecord`
  - durable history of baseline portfolio observations and actions

## Baseline States

The first useful baseline states should include:

- `healthy`
- `healthy_with_watchpoints`
- `routine_maintenance_active`
- `elevated_watch`

Suggested meanings:

- `healthy`
  - the portfolio is broadly stable and ordinary stewardship is sufficient
- `healthy_with_watchpoints`
  - the portfolio is still stable, but one or more early-warning conditions are visible
- `routine_maintenance_active`
  - ordinary refresh, renewal, or cleanup work is underway without strategic intervention
- `elevated_watch`
  - baseline management is still in control, but conditions are close enough to intervention thresholds that stronger observation is justified

These states help define steady-state posture before intervention begins.

## Baseline Activities

The first useful baseline activities should include:

- monitoring portfolio health snapshots
- refreshing aging doctrine before it becomes stale
- tracking watchpoints and recurring weak signals
- prioritizing routine doctrine maintenance
- keeping planning and freeze posture aligned with current portfolio reality

This defines active stewardship without invoking emergency posture.

## Watchpoints

Baseline management should preserve early-warning signals.

The first useful watchpoints should include:

- aging doctrine clusters
- rising override pressure in one family
- repeating small governance exceptions
- repeated freshness refresh needs in the same area
- planning caveats that keep resurfacing

Watchpoints should help the platform act early without treating every weak signal as crisis.

## Routine Prioritization

Baseline management should include routine prioritization, not only observation.

The first useful prioritization factors should include:

- strategic dependency
- evidence freshness
- repetition of low-severity signals
- concentration in one domain
- cost of waiting

This allows ordinary maintenance to stay intentional.

## Relationship To Intervention

Baseline management should make intervention exceptional, not mysterious.

Suggested posture:

- baseline handles ordinary maintenance and watchpoints
- elevated watch may prepare the platform for possible intervention
- intervention begins only when baseline stewardship is no longer enough

This keeps the boundary between normal operations and strategic correction clear.

## Relationship To Planning

Baseline posture should still influence planning.

Examples:

- a healthy portfolio supports ordinary planning confidence
- healthy-with-watchpoints may preserve planning confidence while recording explicit caveats
- elevated watch may narrow assumptions even before intervention begins

This keeps planning grounded in the real portfolio state.

## Relationship To Freeze Posture

Baseline management should also shape freeze confidence.

Examples:

- healthy portfolio posture supports ordinary freeze claims
- elevated watch may justify narrower freeze confidence without full intervention
- recurring watchpoints may signal the need for pre-freeze maintenance work

This helps prevent late surprises.

## Relationship To Governance

Baseline management should make governance calmer and more strategic.

Examples:

- routine doctrine work should not require extraordinary governance every time
- governance should still see the watchpoints that matter
- repeated baseline watchpoints may justify a deeper governance review before intervention is necessary

## Operator Surface Requirements

Operator surfaces should be able to show:

- current baseline state
- current routine priorities
- active watchpoints
- freshness and maturity trends
- whether the portfolio is drifting toward intervention thresholds

This gives operators a useful steady-state dashboard, not only an incident dashboard.

## Required Artifacts

The first useful baseline artifacts should include:

- `portfolio_baseline_snapshot.json`
- `portfolio_baseline_summary.md`
- `portfolio_routine_priority_queue.md`
- `portfolio_watchpoints.json`

Suggested contents:

- `portfolio_baseline_snapshot.json`
  - machine-readable view of steady-state doctrine posture
- `portfolio_baseline_summary.md`
  - high-level interpretation of current ordinary portfolio health
- `portfolio_routine_priority_queue.md`
  - ordered routine doctrine work
- `portfolio_watchpoints.json`
  - current early-warning signals and their trends

## Baseline Outcomes

The first useful baseline outcomes should include:

- `continue_normal_stewardship`
- `maintain_watchpoints`
- `prioritize_routine_refresh`
- `shift_to_elevated_watch`
- `recommend_portfolio_intervention`

These outcomes make baseline management active and explicit.

## Governance Expectations

Baseline management should be lightweight but real.

Suggested posture:

- routine stewardship should stay mostly within ordinary portfolio ownership
- elevated watch or intervention recommendation should become more visible to governance
- governance should be able to audit how the platform stayed healthy before crisis emerged

## Non-Goals

This spec does not define:

- the intervention lifecycle itself
- every doctrine-level state machine
- a universal numeric scoring formula for steady-state health

It only defines the ordinary operating posture for a doctrine portfolio that is not under active strategic intervention.

## Bottom Line

`morphOS` should treat baseline doctrine portfolio management as active stewardship.

When the portfolio is healthy, the platform should still observe, refresh, prioritize, and watch for drift so that intervention stays exceptional rather than routine.
