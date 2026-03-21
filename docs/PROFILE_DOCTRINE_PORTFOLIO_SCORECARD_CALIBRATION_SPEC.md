# Profile Doctrine Portfolio Scorecard Calibration Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio maturity scorecard
- profile doctrine portfolio review cadence
- portfolio decision audit and authority posture

What is still missing is the calibration model that keeps maturity scorecards honest, comparable, and resistant to inflation.

The platform still needs clear answers to these questions:

- how are maturity scorecard judgments kept consistent over time?
- how do we prevent scorecards from drifting into optimism, politics, or local interpretation bias?
- what review process keeps dimension ratings evidence-backed instead of aspirational?

This spec defines that portfolio scorecard-calibration layer.

## Executive Summary

A maturity scorecard is only useful if people can trust it.

Calibration should define how `morphOS` keeps scorecard ratings:

- comparable across time
- grounded in evidence
- resistant to inflation
- reviewable when challenged

For `morphOS`, the correct posture is:

- calibrate maturity ratings explicitly
- require evidence before upward claims
- allow downward correction when reality weakens
- treat calibration as ongoing governance, not one-time setup

The goal is to prevent the scorecard from becoming a vanity dashboard.

## Core Design Goals

- define a reliable calibration process for maturity scorecards
- reduce local interpretation drift across dimensions
- make maturity upgrades and downgrades evidence-backed
- preserve trust in scorecard comparisons over time
- keep the scorecard useful for governance rather than presentation theater

## Calibration Principle

The scorecard should reflect demonstrated maturity, not desired maturity.

Calibration should therefore:

- tie ratings to observable evidence
- prefer conservative interpretation when evidence is weak or ambiguous
- revisit ratings when operations contradict prior claims

Calibration is what keeps the scorecard honest enough to matter.

## What This Spec Covers

The first useful calibration model should cover:

- calibration anchors
- rating review rules
- challenge and correction paths
- consistency checks across dimensions
- required artifacts and operator visibility

This is enough to keep maturity scoring from drifting into opinion.

## Canonical Calibration Objects

`morphOS` should support at least:

- `DoctrineScorecardCalibrationRule`
- `DoctrineScorecardAnchor`
- `DoctrineScorecardCalibrationReview`
- `DoctrineScorecardCalibrationDispute`
- `DoctrineScorecardCalibrationRecord`

Suggested meanings:

- `DoctrineScorecardCalibrationRule`
  - the rule that constrains how maturity ratings are assigned or changed
- `DoctrineScorecardAnchor`
  - a concrete evidence pattern associated with a maturity level in a dimension
- `DoctrineScorecardCalibrationReview`
  - a review of whether the current scorecard ratings remain justified
- `DoctrineScorecardCalibrationDispute`
  - a challenge to a scorecard rating or interpretation
- `DoctrineScorecardCalibrationRecord`
  - durable history of calibration changes and reasoning

## Calibration Anchors

The first useful calibration anchors should include:

- review rhythm evidence
- decision audit completeness
- authority conflict frequency
- continuity and failsafe recovery quality
- baseline and intervention performance evidence

These anchors should connect maturity claims to real operating behavior, not abstract confidence.

## Upward Rating Rules

The first useful upward rating rules should include:

- require repeated evidence, not one clean period
- require no unresolved contradiction from audit or health signals
- require that stronger claims hold at the intended operating scope

This prevents fast optimism after brief improvement.

## Downward Rating Rules

The first useful downward rating rules should include:

- allow downgrades when real operations no longer support current claims
- prefer honest regression over preserving prestige
- use repeated contradiction or material control weakness as sufficient cause to narrow ratings

This keeps the scorecard adaptive to reality.

## Consistency Checks

Calibration should also check for internal inconsistency.

Examples:

- `auditability` should not be rated strong if audit completeness is repeatedly missing
- `continuity_and_resilience` should not be rated strong if failsafe recovery remains fragile
- `portfolio_operability` should not be strong while capacity pressure is routinely overloaded

These checks keep one dimension from overclaiming against the others.

## Relationship To Review Cadence

Calibration should run on a recurring rhythm.

Examples:

- weekly review may confirm or question current ratings
- post-wave review may provide stronger evidence for recalibration
- major intervention entry or exit should trigger calibration attention

This keeps the scorecard current enough to remain credible.

## Relationship To Audit

Audit trails should be key calibration input.

Examples:

- repeated reversals may reveal overstated authority maturity
- missing decision follow-up may weaken operability or auditability claims
- clean, explainable decisions can support stronger maturity ratings

This ties calibration to actual governance behavior.

## Relationship To Disputes

Scorecard ratings should be challengeable.

Suggested posture:

- allow operators or governance to dispute ratings with evidence
- require calibration review when the dispute is material
- record whether the rating stands, narrows, or widens after review

This helps stop scorecards from becoming unquestionable folklore.

## Relationship To Portfolio Learning

Calibration should improve the scorecard over time.

Examples:

- if one dimension is repeatedly overestimated, tighten its calibration anchor
- if two dimensions are always confusingly coupled, clarify their distinction

This helps the scorecard itself mature.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current maturity dimension ratings
- why each rating is believed
- whether any rating is under calibration review or dispute
- recent rating changes and what triggered them
- which dimensions are weakest because of calibration evidence, not opinion

This keeps the scorecard explainable rather than decorative.

## Required Artifacts

The first useful calibration artifacts should include:

- `scorecard_calibration_rules.md`
- `scorecard_calibration_reviews.json`
- `scorecard_calibration_disputes.json`
- `scorecard_calibration_changes.json`

Suggested contents:

- `scorecard_calibration_rules.md`
  - explicit anchors and interpretation rules for maturity ratings
- `scorecard_calibration_reviews.json`
  - completed calibration checks and their outcomes
- `scorecard_calibration_disputes.json`
  - open and resolved rating disputes
- `scorecard_calibration_changes.json`
  - historical record of rating changes and their justification

## First Useful Outcomes

The first useful calibration outcomes should include:

- `rating_confirmed`
- `rating_narrowed`
- `rating_strengthened`
- `rating_under_review`
- `calibration_rule_needs_tightening`

These outcomes make the scorecard’s own governance visible.

## Governance Expectations

Calibration should preserve trust in the scorecard without making it heavyweight theater.

Suggested posture:

- calibrate more carefully where the scorecard influences strategic decisions
- keep the burden of upward claims higher than the burden of cautious doubt
- ensure that scorecard confidence never outruns the evidence behind it

## Non-Goals

This spec does not define:

- a rigid mathematical scoring model for all dimensions
- elimination of judgment from maturity assessment
- a scorecard that replaces detailed portfolio review

It only defines how maturity scorecard judgments remain trustworthy and comparable over time.

## Bottom Line

`morphOS` should calibrate its doctrine portfolio scorecard deliberately.

If the scorecard is going to shape attention and confidence, the platform should ensure those maturity ratings are anchored in evidence, challengeable, and willing to narrow when reality no longer supports them.
