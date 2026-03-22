# Profile Doctrine Portfolio Exception Handling Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio decision authority
- profile doctrine portfolio escalation policy
- profile doctrine portfolio review cadence

What is still missing is the handling model for doctrine portfolio cases that do not fit normal queueing, cadence, routing, or baseline governance assumptions.

The platform still needs clear answers to these questions:

- what should happen when a doctrine issue does not fit the normal portfolio rules cleanly?
- how should the platform handle urgent or unusual cases without weakening governance discipline?
- how do we make exceptions explicit instead of allowing them to become invisible precedent?

This spec defines that portfolio exception-handling layer.

## Executive Summary

No governance model is complete unless it defines how exceptions are handled.

Exception handling should give `morphOS` a controlled way to manage doctrine portfolio cases that are:

- unusual
- ambiguous
- time-sensitive
- cross-boundary
- not well-covered by ordinary policy

For `morphOS`, the correct posture is:

- treat exceptions as governed deviations, not informal shortcuts
- require explicit classification, rationale, and follow-up
- keep exceptions rare, visible, and auditable
- prevent one-off exceptions from silently redefining the baseline

The goal is to absorb unusual doctrine cases without letting the governance model erode.

## Core Design Goals

- define how doctrine exceptions are recognized and handled
- preserve governance integrity under unusual conditions
- prevent ad hoc exception handling from becoming shadow policy
- connect exceptions to authority, audit, and later doctrine improvement
- keep exception handling proportional and temporary where possible

## Exception Principle

An exception is not a loophole.

It is a governed recognition that:

- the ordinary rules do not fully fit the present case, or
- following them literally would create disproportionate risk or harm

Exception handling should therefore:

- remain explicit
- remain scoped
- remain reviewable

The system should treat an exception as a special operating condition, not as permission to stop being disciplined.

## What This Spec Covers

The first useful exception-handling model should cover:

- exception types
- exception classification
- temporary handling posture
- follow-up and normalization rules
- required artifacts and operator visibility

This is enough to make unusual doctrine cases governable without normalizing them.

## Canonical Exception Objects

`morphOS` should support at least:

- `DoctrinePortfolioException`
- `DoctrineExceptionClass`
- `DoctrineExceptionDisposition`
- `DoctrineExceptionFollowup`
- `DoctrineExceptionRecord`

Suggested meanings:

- `DoctrinePortfolioException`
  - a doctrine portfolio case that does not fit ordinary handling cleanly
- `DoctrineExceptionClass`
  - the type of exception involved
- `DoctrineExceptionDisposition`
  - the approved temporary handling outcome
- `DoctrineExceptionFollowup`
  - the required later action to close, normalize, or incorporate lessons
- `DoctrineExceptionRecord`
  - durable history of the exception and its handling

## First Useful Exception Classes

The first useful exception classes should include:

- `policy_gap`
- `authority_gap`
- `time_critical_override`
- `cross_boundary_case`
- `novel_case`

Suggested meanings:

- `policy_gap`
  - ordinary doctrine rules do not cover the case clearly enough
- `authority_gap`
  - normal ownership or routing is ambiguous or insufficient
- `time_critical_override`
  - ordinary process is too slow for the consequence of delay
- `cross_boundary_case`
  - the issue spans more scopes or domains than the baseline model assumed
- `novel_case`
  - the situation is materially new and does not yet have a trustworthy handling pattern

These classes help exceptions stay legible instead of becoming generic “special cases.”

## Exception Detection

The first useful signals that a doctrine case may be an exception should include:

- no clear decision route exists
- normal authority is disputed or obviously insufficient
- following the normal cadence would create material avoidable risk
- the case crosses portfolio boundaries not covered by current rules
- operators are repeatedly improvising around the same type of issue

These are signs that the platform needs exception handling, not silent improvisation.

## Exception Dispositions

The first useful exception dispositions should include:

- `temporary_override`
- `temporary_route_expansion`
- `escalate_for_special_review`
- `hold_until_policy_clarified`
- `normalize_into_standard_path`

Suggested meanings:

- `temporary_override`
  - allow a limited deviation from the normal path for a defined reason and duration
- `temporary_route_expansion`
  - widen decision routing for this case without redefining the general model
- `escalate_for_special_review`
  - require a dedicated review path because the case is too novel or consequential
- `hold_until_policy_clarified`
  - pause action where acting without clearer doctrine would be too risky
- `normalize_into_standard_path`
  - determine that the case was unusual in appearance but still fits an existing route after analysis

These dispositions keep exception handling both flexible and bounded.

## Scope Limits

Every exception should be explicitly scoped.

The first useful scope dimensions should include:

- affected doctrine area
- allowed duration
- allowed decision types
- allowed authority expansion
- required follow-up review

This prevents exceptions from quietly becoming permanent.

## Relationship To Authority

Exception handling should not bypass authority discipline.

Suggested posture:

- exceptions may widen or alter routing temporarily
- the authority used for the exception should still be explicit
- unclear authority should itself be treated as an exception signal, not ignored

This keeps exception handling compatible with the decision-authority model.

## Relationship To Escalation

Some exceptions should escalate immediately.

Examples:

- time-critical overrides with strategic consequence
- novel cases affecting multiple areas
- policy gaps that block safe action on important doctrine work

This makes exceptions a structured input into escalation, not a competing path around it.

## Relationship To Audit

Every meaningful exception should be auditable.

Examples:

- record why the ordinary path did not fit
- record who approved the exception posture
- record what follow-up is required before the case is considered closed

This ensures exceptions teach the system instead of disappearing into lore.

## Relationship To Baseline Doctrine Improvement

Repeated exceptions should be treated as signals that the baseline doctrine is incomplete.

Examples:

- recurring policy-gap exceptions may require a new spec or rule
- repeated time-critical overrides may show the normal cadence is too slow in one domain
- repeated authority-gap exceptions may show routing needs redesign

This keeps exceptions from becoming permanent shadow policy.

## Operator Surface Requirements

Operator surfaces should be able to show:

- active doctrine exceptions
- exception class and current disposition
- current scope and expiration posture
- whether the exception is isolated or recurring
- follow-up needed to close or normalize the case

This makes exceptional handling visible and governable.

## Required Artifacts

The first useful exception-handling artifacts should include:

- `doctrine_exceptions.json`
- `doctrine_exception_summary.md`
- `exception_followups.json`
- `recurring_exceptions.json`

Suggested contents:

- `doctrine_exceptions.json`
  - machine-readable list of active and recent doctrine exceptions
- `doctrine_exception_summary.md`
  - high-level explanation of why exceptions exist and what posture they require
- `exception_followups.json`
  - required actions to close, review, or normalize exceptions
- `recurring_exceptions.json`
  - repeated exception patterns that may indicate doctrine gaps

## First Useful Outcomes

The first useful exception-handling outcomes should include:

- `approve_temporary_exception`
- `route_to_special_review`
- `reject_exception_request`
- `close_exception`
- `promote_exception_learning_into_doctrine`

These outcomes keep exceptions actionable and bounded.

## Governance Expectations

Exception handling should preserve discipline under pressure.

Suggested posture:

- routine operations should not rely on exceptions
- meaningful exceptions should always leave an audit trail
- repeated or strategic exceptions should be reviewed for doctrine improvement, not normalized informally

## Non-Goals

This spec does not define:

- every possible rare case in advance
- a blanket emergency-powers model across the whole platform
- replacement of baseline governance with constant exceptions

It only defines how unusual doctrine portfolio cases should be handled explicitly, safely, and temporarily.

## Bottom Line

`morphOS` should treat doctrine exceptions as governed deviations, not informal workarounds.

When a portfolio case does not fit the normal rules, the platform should classify it, scope it, route it, audit it, and learn from it without letting the exception silently rewrite the baseline.
