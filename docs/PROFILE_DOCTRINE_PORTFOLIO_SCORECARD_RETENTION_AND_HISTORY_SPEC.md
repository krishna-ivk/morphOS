# Profile Doctrine Portfolio Scorecard Retention And History Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio maturity scorecard
- profile doctrine portfolio scorecard calibration
- profile doctrine portfolio scorecard publication

What is still missing is the longitudinal history model for how scorecard snapshots are retained, compared, aged, and used over time.

The platform still needs clear answers to these questions:

- how long should doctrine scorecard snapshots be kept?
- how should historical scorecards be compared without losing their context?
- how do we preserve trend trust while preventing stale snapshots from being mistaken for current truth?

This spec defines that portfolio scorecard-retention and history layer.

## Executive Summary

If the scorecard is supposed to show maturity over time, then the platform needs a governed history of scorecard states.

Retention and history should define how `morphOS`:

- stores scorecard snapshots
- compares them across review periods and waves
- marks old scorecards as historical rather than current
- preserves trend interpretability over time

For `morphOS`, the correct posture is:

- keep enough scorecard history to support real trend analysis
- preserve the context around historical ratings
- prevent stale snapshots from being reused as current evidence
- connect retention policy to publication, calibration, and review cadence

The goal is to make doctrine maturity trends durable, reviewable, and hard to misuse.

## Core Design Goals

- define how scorecard history is retained and aged
- preserve comparability across time without stripping context
- support trustworthy longitudinal trend analysis
- distinguish current scorecard truth from historical snapshots
- keep scorecard history useful for review, calibration, and learning

## Retention Principle

Scorecard history should preserve decision-grade learning without pretending that old snapshots are still current posture.

Retention and history should therefore:

- preserve historical snapshots with their original context
- clearly mark whether a snapshot is current, superseded, or stale
- support trend analysis without flattening away dispute, calibration, or publication posture

History should inform the present, not silently replace it.

## What This Spec Covers

The first useful retention-and-history model should cover:

- scorecard snapshot lifecycle
- retention classes
- historical comparison rules
- trend integrity rules
- required artifacts and operator visibility

This is enough to make scorecard history durable and trustworthy.

## Canonical History Objects

`morphOS` should support at least:

- `DoctrineScorecardSnapshot`
- `DoctrineScorecardHistoryWindow`
- `DoctrineScorecardRetentionClass`
- `DoctrineScorecardTrendComparison`
- `DoctrineScorecardHistoryRecord`

Suggested meanings:

- `DoctrineScorecardSnapshot`
  - one published or governed scorecard state at a point in time
- `DoctrineScorecardHistoryWindow`
  - a bounded period used for comparing scorecard movement
- `DoctrineScorecardRetentionClass`
  - the retention and access posture for a scorecard snapshot
- `DoctrineScorecardTrendComparison`
  - a structured comparison between scorecard states
- `DoctrineScorecardHistoryRecord`
  - durable history of scorecard storage, aging, and comparison

## First Useful Retention Classes

The first useful retention classes should include:

- `active_current`
- `recent_history`
- `wave_history`
- `archived_history`

Suggested meanings:

- `active_current`
  - the current authoritative scorecard for operational use
- `recent_history`
  - recent prior snapshots still useful for ordinary comparison and review
- `wave_history`
  - snapshots tied to wave-readiness or post-wave milestones
- `archived_history`
  - older scorecard history retained mainly for long-term learning and audit

These classes help separate immediate operational value from long-term reference value.

## Snapshot Lifecycle

The first useful snapshot lifecycle should include:

- created
- published
- superseded
- historical
- archived

Suggested meanings:

- `created`
  - the scorecard state has been formed but is not yet the operative published version
- `published`
  - the scorecard is the current view for its intended audience
- `superseded`
  - a newer scorecard has replaced it operationally
- `historical`
  - the scorecard is retained for comparison but not for current decision claims
- `archived`
  - the scorecard is retained mainly for long-horizon analysis, audit, or institutional memory

This keeps current truth and historical truth clearly separated.

## Historical Comparison Rules

The first useful comparison rules should include:

- compare like publication scope where possible
- preserve calibration and dispute context during comparison
- distinguish real maturity movement from changed scoring rules
- record whether differences reflect posture change, evidence change, or calibration change

These rules keep trend analysis honest.

## Trend Integrity

Trend reporting should preserve why a score changed, not just that it changed.

Examples:

- a dimension may improve because operations improved
- a dimension may narrow because calibration got stricter
- an apparent drop may reflect newly surfaced evidence, not a sudden operational collapse

This helps operators interpret history intelligently rather than theatrically.

## Relationship To Calibration

History should preserve calibration context.

Examples:

- store whether a scorecard was published before or after a calibration rule change
- flag trend comparisons that cross a significant calibration change
- preserve disputes and calibration reviews that materially affected rating movement

This keeps trend claims from becoming misleading.

## Relationship To Publication

Publication and retention should work together.

Suggested posture:

- published scorecards become history when superseded
- historical scorecards should retain their original publication view and confidence labels
- a stale publication should remain visible as stale, not disappear into ambiguity

This helps each audience interpret old scorecards correctly.

## Relationship To Review Cadence

Cadence should define the main rhythm of scorecard history.

Examples:

- weekly portfolio reviews may create recent-history snapshots
- wave reviews may create wave-history anchors
- major intervention entry or exit may justify preserving milestone snapshots explicitly

This makes scorecard history aligned with real portfolio events.

## Relationship To Learning And Audit

Scorecard history should serve both learning and accountability.

Examples:

- long-term trend review can reveal repeated governance weakness
- audit review can show whether maturity claims were repeatedly overstated
- intervention retrospectives can compare scorecard posture before, during, and after disruption

This makes history practically useful instead of decorative storage.

## Staleness And Misuse Prevention

Historical scorecards should not be easily mistaken for current posture.

The first useful protections should include:

- explicit stale markers
- clear publication timestamps
- linkage to current scorecard state
- warning when a historical scorecard predates major disputes or governance change

This reduces the risk of citing the wrong maturity truth.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current scorecard and recent history side by side
- whether a viewed scorecard is current, superseded, or archived
- trend movement by dimension
- whether a comparison is complicated by calibration or dispute changes
- links from history into the current scorecard state

This makes scorecard history usable, not just stored.

## Required Artifacts

The first useful retention-and-history artifacts should include:

- `scorecard_history_index.json`
- `scorecard_snapshots/`
- `scorecard_trend_comparisons.json`
- `scorecard_history_summary.md`

Suggested contents:

- `scorecard_history_index.json`
  - machine-readable index of current and historical scorecard snapshots
- `scorecard_snapshots/`
  - stored scorecard snapshots with metadata and publication posture
- `scorecard_trend_comparisons.json`
  - structured comparisons across meaningful review windows
- `scorecard_history_summary.md`
  - high-level interpretation of maturity movement over time

## First Useful Outcomes

The first useful retention-and-history outcomes should include:

- `retain_as_recent_history`
- `promote_to_wave_history`
- `archive_snapshot`
- `flag_comparison_context_shift`
- `mark_snapshot_stale_for_operational_use`

These outcomes make history governance visible and actionable.

## Governance Expectations

Scorecard history should preserve institutional memory without creating historical confusion.

Suggested posture:

- current operational decisions should always anchor on current scorecard truth
- historical scorecards should remain available for comparison and audit
- retention should favor explainability over bulk accumulation without context

## Non-Goals

This spec does not define:

- the low-level storage engine
- broad document retention policy for the whole platform
- replacement of current scorecard governance with historical trend narratives

It only defines how doctrine maturity scorecard states are retained, aged, compared, and kept trustworthy over time.

## Bottom Line

`morphOS` should treat scorecard history as a governed timeline, not a pile of old snapshots.

Historical scorecards should remain usable for trend analysis, audit, and learning, while still being clearly separated from the current scorecard truth that governs present decisions.
