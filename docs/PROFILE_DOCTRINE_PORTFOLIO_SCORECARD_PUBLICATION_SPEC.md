# Profile Doctrine Portfolio Scorecard Publication Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio maturity scorecard
- profile doctrine portfolio scorecard calibration
- profile doctrine portfolio scorecard governance

What is still missing is the publication model for how the scorecard should be presented to different audiences, surfaces, and decision contexts.

The platform still needs clear answers to these questions:

- who should see which version of the doctrine portfolio scorecard?
- how much detail should be shown in each surface?
- how should confidence, caveats, and disputed scorecard posture be communicated when the scorecard is published?

This spec defines that portfolio scorecard-publication layer.

## Executive Summary

A governed scorecard is only useful if it is published in the right form to the right audience.

Publication should define how `morphOS` presents scorecard posture across:

- operator surfaces
- portfolio reviews
- wave-readiness and post-wave reviews
- governance and admin views

For `morphOS`, the correct posture is:

- publish the same core truth at different levels of detail
- keep caveats and confidence visible wherever the scorecard is shown
- avoid over-sharing raw internal detail where a summarized view is more appropriate
- prevent publication from flattening nuanced maturity posture into false certainty

The goal is to make the scorecard legible, useful, and honest across different contexts.

## Core Design Goals

- define audience-specific scorecard publication forms
- preserve consistency across surfaces while adapting detail level
- ensure caveats and disputes survive publication
- connect publication to authority, governance, and confidence posture
- prevent publication drift from creating conflicting versions of truth

## Publication Principle

The doctrine portfolio should have one scorecard truth, but not one rendering for all purposes.

Publication should therefore:

- keep the underlying scorecard canonical
- vary presentation by audience and context
- preserve current confidence and dispute posture in every published form

Publication is about shaping access and comprehension, not changing the score itself.

## What This Spec Covers

The first useful publication model should cover:

- audience classes
- publication views
- confidence and caveat rendering
- freshness and staleness markers
- required artifacts and surface behavior

This is enough to make the scorecard usable across the portfolio operating system.

## Canonical Publication Objects

`morphOS` should support at least:

- `DoctrineScorecardPublicationView`
- `DoctrineScorecardAudienceClass`
- `DoctrineScorecardPublicationSnapshot`
- `DoctrineScorecardConfidenceLabel`
- `DoctrineScorecardPublicationRecord`

Suggested meanings:

- `DoctrineScorecardPublicationView`
  - one audience-specific rendering of the canonical scorecard
- `DoctrineScorecardAudienceClass`
  - a role or surface category that consumes the scorecard
- `DoctrineScorecardPublicationSnapshot`
  - the published state of the scorecard at a point in time
- `DoctrineScorecardConfidenceLabel`
  - the explicit confidence or caveat posture attached to the publication
- `DoctrineScorecardPublicationRecord`
  - durable history of what scorecard view was published where and when

## First Useful Audience Classes

The first useful audience classes should include:

- `operator`
- `portfolio_authority`
- `workspace_admin`
- `executive_or_summary_view`

Suggested meanings:

- `operator`
  - needs actionable detail, weak dimensions, and current watchpoints
- `portfolio_authority`
  - needs dimension posture plus current constraints and likely interventions
- `workspace_admin`
  - needs governance-grade detail including disputes, caveats, and calibration posture
- `executive_or_summary_view`
  - needs a concise, high-level maturity picture with explicit caveats, not raw internals

These classes allow the same truth to be presented in different useful forms.

## First Useful Publication Views

The first useful publication views should include:

- `compact_summary`
- `dimension_detail`
- `governance_detail`
- `wave_context_view`

Suggested meanings:

- `compact_summary`
  - short multidimensional rollup for fast scanning
- `dimension_detail`
  - maturity by dimension with current constraints and trend movement
- `governance_detail`
  - detailed view including disputes, calibration review, and authority context
- `wave_context_view`
  - scorecard rendering tied to current wave-readiness or post-wave decision context

These views cover most real publication needs without multiplying truth sources.

## Confidence And Caveat Labels

The first useful publication labels should include:

- `stable`
- `under_review`
- `constrained`
- `disputed`
- `stale_publication`

Suggested meanings:

- `stable`
  - the published scorecard posture is current and not materially contested
- `under_review`
  - active recalibration or review may change this posture
- `constrained`
  - maturity posture is limited by known weak dimensions or recent disruption
- `disputed`
  - one or more scorecard dimensions are materially challenged
- `stale_publication`
  - the published rendering is no longer current enough for strong planning confidence

These labels help preserve honesty when the scorecard is reused widely.

## Relationship To Governance

Publication should reflect scorecard governance, not bypass it.

Suggested posture:

- published views should show whether the scorecard is settled or contested
- material disputes should not disappear in summary views
- publication should never outrun the latest approved scorecard state

This keeps publication trustworthy.

## Relationship To Calibration

Publication should also preserve calibration posture.

Examples:

- if a dimension is under calibration review, the published view should say so
- if ratings were recently narrowed, the trend should remain visible
- if calibration confidence is weak, summary views should not imply stable maturity

This prevents the scorecard from looking firmer than it really is.

## Relationship To Review Cadence

Publication should align with review rhythm.

Examples:

- weekly portfolio review may publish updated dimension detail
- wave-readiness review may publish a wave-context view
- post-wave review may publish changed trend posture or constraints

This keeps the scorecard current where it matters most.

## Relationship To Authority And Access

Different audiences should see different depth, but not different truth.

Suggested posture:

- deeper governance views may expose more operational detail
- summary audiences may see compressed but still caveated views
- restricted details should not appear in summary publication if they exceed the audience’s need or access scope

This keeps publication useful without flattening access control.

## Freshness And Staleness

Published scorecards should carry freshness markers.

The first useful freshness markers should include:

- publication timestamp
- last review source
- whether publication predates a material dispute or intervention event

This helps users know whether the scorecard is current enough for their decision.

## Operator Surface Requirements

Operator surfaces should be able to show:

- which publication view is being shown
- publication freshness and confidence label
- links to deeper detail where allowed
- whether the current view omits governance detail by design
- whether a newer scorecard state exists

This makes the publication layer explicit rather than invisible.

## Required Artifacts

The first useful publication artifacts should include:

- `scorecard_publications.json`
- `scorecard_publication_views.md`
- `scorecard_publication_freshness.json`
- `scorecard_confidence_labels.json`

Suggested contents:

- `scorecard_publications.json`
  - machine-readable list of current and recent published scorecard snapshots
- `scorecard_publication_views.md`
  - definitions of audience-specific views and content boundaries
- `scorecard_publication_freshness.json`
  - current freshness, last update source, and staleness posture by publication
- `scorecard_confidence_labels.json`
  - confidence and caveat labels associated with each published view

## First Useful Outcomes

The first useful publication outcomes should include:

- `publish_current_view`
- `publish_with_caveat`
- `publish_limited_summary`
- `hold_publication_pending_review`
- `mark_publication_stale`

These outcomes make publication behavior governed and visible.

## Governance Expectations

Publication should never turn a nuanced governance signal into false marketing.

Suggested posture:

- summary views should remain honest about weakness
- contested scorecards should remain visibly contested
- publication should support decision quality, not cosmetic confidence

## Non-Goals

This spec does not define:

- external PR or public website messaging
- low-level UI implementation details
- replacement of full scorecard evidence with summary labels alone

It only defines how the doctrine portfolio scorecard should be published across internal audiences and operating surfaces.

## Bottom Line

`morphOS` should publish one canonical doctrine scorecard truth in several governed views.

Different audiences may see different levels of detail, but every publication should preserve freshness, confidence, and caveat posture so maturity is communicated clearly without being overstated.
