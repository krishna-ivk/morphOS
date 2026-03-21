# Profile Doctrine Portfolio Scorecard Exception Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio scorecard governance
- profile doctrine portfolio scorecard publication
- profile doctrine portfolio scorecard consumption policy

What is still missing is the exception model for rare cases where the scorecard itself needs a temporary deviation from its normal governance, calibration, publication, or consumption rules.

The platform still needs clear answers to these questions:

- what happens when normal scorecard rules do not cleanly fit a real portfolio situation?
- how can the platform permit a temporary deviation without weakening scorecard trust?
- how do we stop one-off scorecard exceptions from silently becoming normal scorecard behavior?

This spec defines that portfolio scorecard-exception layer.

## Executive Summary

If the scorecard is important, then the scorecard itself also needs governed exception handling.

Scorecard exceptions should define how `morphOS` handles rare cases involving:

- unusual publication posture
- temporary calibration deviation
- constrained or expanded consumption rules
- special scorecard routing or approval

For `morphOS`, the correct posture is:

- treat scorecard exceptions as explicit, narrow, and temporary
- require stronger visibility than ordinary scorecard changes
- connect every exception back to governance, audit, and later normalization
- prevent scorecard exceptions from rewriting baseline scorecard doctrine by accident

The goal is to absorb unusual scorecard cases without making the scorecard itself unreliable.

## Core Design Goals

- define how scorecard-specific exceptions are recognized and governed
- preserve trust in scorecard truth during unusual handling
- prevent exceptional scorecard treatment from becoming hidden baseline behavior
- connect scorecard exceptions to authority, publication, and consumption policy
- preserve clear audit and follow-up for every scorecard exception

## Exception Principle

A scorecard exception is not a license to ignore scorecard governance.

It is a governed acknowledgment that:

- a rare case does not fit the normal scorecard rules cleanly, or
- following them literally would create disproportionate confusion, risk, or delay

Scorecard exceptions should therefore:

- be explicit
- be bounded
- be reviewable

The scorecard should bend carefully, not silently.

## What This Spec Covers

The first useful scorecard-exception model should cover:

- exception classes
- exception scope rules
- temporary disposition types
- follow-up and normalization rules
- required artifacts and operator visibility

This is enough to make unusual scorecard cases governable without weakening the scorecard system.

## Canonical Scorecard Exception Objects

`morphOS` should support at least:

- `DoctrineScorecardException`
- `DoctrineScorecardExceptionClass`
- `DoctrineScorecardExceptionDisposition`
- `DoctrineScorecardExceptionFollowup`
- `DoctrineScorecardExceptionRecord`

Suggested meanings:

- `DoctrineScorecardException`
  - a scorecard case that does not fit ordinary governance, calibration, publication, or consumption rules cleanly
- `DoctrineScorecardExceptionClass`
  - the type of scorecard exception involved
- `DoctrineScorecardExceptionDisposition`
  - the approved temporary handling outcome
- `DoctrineScorecardExceptionFollowup`
  - the later work needed to close, normalize, or learn from the exception
- `DoctrineScorecardExceptionRecord`
  - durable history of the scorecard exception and its handling

## First Useful Scorecard Exception Classes

The first useful exception classes should include:

- `publication_exception`
- `calibration_exception`
- `consumption_exception`
- `authority_exception`
- `novel_scorecard_case`

Suggested meanings:

- `publication_exception`
  - a scorecard must be shown in an unusual form or audience boundary for a bounded reason
- `calibration_exception`
  - a normal calibration path does not fit the current scorecard situation cleanly
- `consumption_exception`
  - scorecard use for a given decision needs a temporary stricter or broader rule
- `authority_exception`
  - ordinary scorecard approval or ownership routing is not sufficient in the current case
- `novel_scorecard_case`
  - a materially new scorecard situation exists that normal rules do not yet cover

These classes keep scorecard exceptions understandable instead of vague.

## Exception Scope Rules

Every scorecard exception should define its scope explicitly.

The first useful scope dimensions should include:

- affected scorecard view or dimension
- affected audience or role
- allowed duration
- allowed publication or consumption change
- required follow-up review

This prevents temporary scorecard deviations from spreading informally.

## Exception Dispositions

The first useful scorecard exception dispositions should include:

- `temporary_scorecard_override`
- `temporary_publication_restriction`
- `temporary_consumption_constraint`
- `special_review_required`
- `normalize_to_standard_rule`

Suggested meanings:

- `temporary_scorecard_override`
  - allow a narrow scorecard deviation for a defined reason and period
- `temporary_publication_restriction`
  - narrow publication while the scorecard posture is unusually sensitive or unsettled
- `temporary_consumption_constraint`
  - restrict how the scorecard may be used for certain decisions until normal posture returns
- `special_review_required`
  - require a dedicated review path because the scorecard case is too novel or consequential
- `normalize_to_standard_rule`
  - determine that the case can return to ordinary scorecard rules after clarification

These dispositions keep scorecard exceptions both practical and bounded.

## Relationship To Governance

Scorecard exceptions should strengthen governance visibility, not reduce it.

Suggested posture:

- scorecard exceptions should route through explicit authority
- material scorecard exceptions should not be silently approved by ordinary editing
- a scorecard exception should always remain visibly exceptional

This protects trust in the scorecard system itself.

## Relationship To Calibration

Calibration-related exceptions should be especially careful.

Examples:

- if a dimension cannot yet be calibrated normally, publication should show that explicitly
- temporary calibration deviation should not be mistaken for a settled stronger claim
- repeated calibration exceptions may indicate the calibration model itself needs improvement

This keeps exceptions from corrupting maturity interpretation.

## Relationship To Publication

Scorecard publication exceptions should preserve honesty across surfaces.

Examples:

- special summary suppression for a disputed dimension should remain visible as a publication exception
- restricted publication should not create two contradictory scorecard truths
- unusual publication should always point back to canonical scorecard state

This prevents publication exceptions from becoming misleading.

## Relationship To Consumption Policy

Scorecard use exceptions should remain narrow and visible.

Examples:

- a temporary ban on relying on one dimension for governance decisions
- a temporary requirement for deeper validation before using a normally sufficient scorecard view
- bounded exceptional use in a wave context with explicit caution

This keeps scorecard use policy coherent under unusual conditions.

## Relationship To Audit And History

Scorecard exceptions should always be auditable and retained in history.

Examples:

- record when and why the scorecard exception was approved
- record what scorecard truth, view, or rule was temporarily altered
- record whether the exception later closed, normalized, or changed the baseline

This ensures exceptions create learning instead of lore.

## Relationship To Baseline Improvement

Repeated scorecard exceptions should trigger doctrine improvement.

Examples:

- recurring publication exceptions may indicate a missing audience model
- recurring calibration exceptions may indicate weak anchors
- recurring consumption exceptions may indicate scorecard use rules are too brittle

This keeps scorecard governance adaptive.

## Operator Surface Requirements

Operator surfaces should be able to show:

- active scorecard exceptions
- affected scorecard views or dimensions
- current exception disposition and duration
- whether the exception affects publication, calibration, or consumption
- required follow-up before the exception closes

This makes exceptional scorecard handling visible and bounded.

## Required Artifacts

The first useful scorecard-exception artifacts should include:

- `scorecard_exceptions.json`
- `scorecard_exception_summary.md`
- `scorecard_exception_followups.json`
- `recurring_scorecard_exceptions.json`

Suggested contents:

- `scorecard_exceptions.json`
  - machine-readable list of active and recent scorecard exceptions
- `scorecard_exception_summary.md`
  - high-level explanation of why scorecard exceptions exist and what they currently change
- `scorecard_exception_followups.json`
  - required actions to close, normalize, or learn from scorecard exceptions
- `recurring_scorecard_exceptions.json`
  - repeated scorecard exception patterns that may indicate design gaps

## First Useful Outcomes

The first useful scorecard-exception outcomes should include:

- `approve_temporary_scorecard_exception`
- `restrict_scorecard_use_temporarily`
- `hold_scorecard_publication_until_review`
- `close_scorecard_exception`
- `promote_exception_learning_into_scorecard_policy`

These outcomes keep the scorecard exception path actionable and finite.

## Governance Expectations

Scorecard exceptions should remain rarer and more visible than ordinary scorecard changes.

Suggested posture:

- if scorecard exceptions become routine, the baseline model is probably incomplete
- exceptions should always preserve freshness, caveat, and authority truth
- no scorecard exception should quietly create a stronger claim than the evidence supports

## Non-Goals

This spec does not define:

- every possible scorecard anomaly in advance
- replacement of scorecard governance with a permanent exception system
- external communication policy for public artifacts

It only defines how unusual scorecard cases should be handled explicitly, safely, and temporarily.

## Bottom Line

`morphOS` should govern scorecard exceptions as carefully as scorecard rules.

When the scorecard itself needs unusual handling, the platform should classify, scope, route, audit, and close that exception explicitly so trust in the scorecard system remains stronger than the convenience of the moment.
