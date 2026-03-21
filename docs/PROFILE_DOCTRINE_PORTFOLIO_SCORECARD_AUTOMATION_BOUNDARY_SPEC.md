# Profile Doctrine Portfolio Scorecard Automation Boundary Spec

## Purpose

This spec defines which scorecard-driven portfolio actions may be automated, which require human review, and which must remain explicitly governed.

The earlier specs already define:

- what the scorecard means
- how it is reconciled
- how it binds into decisions
- what action protocol it should trigger

This document defines the next boundary:

how far the platform may go automatically once a scorecard-based action is triggered.

## Core Principle

Automation is allowed only where the action is narrow, reversible, evidence-backed, and low-risk.

Automation must stop where an action:

- changes authority posture
- broadens or narrows governance scope materially
- creates strategic portfolio commitments
- weakens a required gate
- depends on ambiguous interpretation

The scorecard system should automate clerical and bounded coordination work before it automates judgment-heavy doctrine decisions.

## Goals

This automation boundary exists to ensure:

- scorecard-driven automation is predictable
- operators know which moves the platform may take on its own
- automation does not silently become governance
- review and escalation remain meaningful
- the system can move quickly on low-risk follow-up without overreaching

## Non-Goals

This spec does not define:

- how scorecards are calculated
- how action protocol levels are chosen
- workflow-level task automation
- live production automation

This is only about portfolio-level doctrine scorecard responses.

## Automation Classes

Every scorecard-driven action must be assigned one automation class:

- `auto_allowed`
- `auto_assist_only`
- `review_required`
- `approval_required`
- `human_only`

These classes must be attached to the action protocol outcome before execution begins.

## `auto_allowed`

The platform may execute the action without waiting for human input, as long as the action remains inside a declared safe envelope.

Typical examples:

- attaching caveats to an internal portfolio summary
- creating a watch item
- scheduling a reassessment reminder
- recording protocol artifacts
- routing an item into an existing review queue

Use `auto_allowed` only when the action is:

- reversible
- non-claim-making
- low-impact
- already described by deterministic rules

## `auto_assist_only`

The platform may prepare, draft, gather, or route, but may not finalize the action.

Typical examples:

- drafting an escalation packet
- prebuilding a review agenda
- collecting linked evidence
- drafting a remediation intake

This class is useful when the system can reduce human effort without taking the final action itself.

## `review_required`

The platform may detect and assemble the action, but a human reviewer must confirm before the action becomes active.

Typical examples:

- applying a narrower wave recommendation
- marking a doctrine area as constrained for the next review window
- initiating broader trend investigation

Use `review_required` when the action changes operating posture but does not require a formal approval chain.

## `approval_required`

The platform may not execute until the correct authority explicitly approves.

Typical examples:

- blocking an expansion path based on scorecard posture
- stepping down a doctrine claim
- changing portfolio intervention posture
- overriding a weak scorecard through exception

Use `approval_required` when the action changes governance posture, commitment scope, or cross-wave claims.

## `human_only`

The platform may surface the issue, but it must not even draft or pre-stage the decision as if the system is taking it.

Typical examples:

- strategic tradeoff adjudication between doctrine areas
- deciding whether weak scorecard posture is acceptable for a special case without precedent
- making a portfolio-wide confidence statement under dispute

Use `human_only` when ambiguity is high or when the act itself carries governance weight.

## Safe Automation Envelope

An action may be `auto_allowed` only if all of the following are true:

- the triggering condition is deterministic
- the action is bounded in scope
- the action is reversible
- the action does not weaken a gate
- the action does not broaden authority claims
- the action does not create a new exception
- the action can be fully recorded and explained

If any of these conditions fail, the automation class must be raised to a more restrictive level.

## Default Automation Mapping

Recommended defaults:

- `observe` -> `auto_allowed`
- `record` -> `auto_allowed`
- `reassess` -> `auto_allowed` or `auto_assist_only`
- `review` -> `auto_assist_only` or `review_required`
- `constrain` -> `review_required`
- `pause` -> `review_required` or `approval_required`
- `escalate` -> `auto_assist_only` or `approval_required`
- `remediate` -> `auto_assist_only` or `review_required`

The platform should default to the more restrictive class whenever doubt exists.

## Protocol-Level Guidance

Recommended defaults by action protocol level:

- `L0_notice` -> mostly `auto_allowed`
- `L1_review` -> mostly `auto_assist_only`
- `L2_constraint` -> mostly `review_required`
- `L3_gate_pause` -> mostly `approval_required`
- `L4_systemic_escalation` -> `approval_required` or `human_only`

This keeps automation aligned with the seriousness of the posture.

## Actions That Should Usually Be Automated

These are strong candidates for `auto_allowed`:

- writing scorecard action records
- updating watch queues
- attaching freshness or caveat labels
- scheduling follow-up review reminders
- routing packets to already-defined review lanes
- refreshing internal references to the current reconciled scorecard snapshot

These actions are low-risk because they preserve or surface posture rather than reinterpret it.

## Actions That Should Usually Stay Human-Governed

These should usually be `review_required`, `approval_required`, or `human_only`:

- changing wave scope
- approving or blocking doctrine expansion
- ending intervention based on scorecard improvement
- converting weak posture into an exception
- making portfolio-wide maturity claims
- materially downgrading a doctrine area’s standing

These actions shape portfolio direction and cannot be safely reduced to clerical automation.

## Drafting vs Acting

The system may often draft more than it may act.

For example, the platform may:

- draft a remediation packet
- gather evidence for a review
- propose a constrained scope

without being allowed to:

- open the remediation formally
- impose the constrained scope
- declare the review outcome

This distinction should be explicit in all operator surfaces.

## Interaction With Exceptions

Any action that:

- creates an exception
- widens an exception
- extends an exception
- treats an exception as precedent

must never be `auto_allowed`.

At minimum it must be `approval_required`, and in ambiguous cases it should be `human_only`.

## Interaction With Drift and Freshness

Automation should become more conservative when:

- the scorecard is stale
- the underlying evidence is aging
- upstream drift signals are active
- reconciliation confidence is low
- disputes are unresolved

Weak confidence should narrow automation even if the action would normally be low-risk.

## Interaction With Intervention and Failsafe

If the doctrine portfolio is under intervention or degraded governance:

- automation classes should ratchet upward
- previously `auto_allowed` actions may become `auto_assist_only`
- previously `review_required` actions may become `approval_required`

This reflects the fact that the environment is already abnormal.

## Operator Responsibilities

When automation is permitted, operators still remain responsible for:

- noticing repeated automation patterns that signal doctrine mismatch
- reviewing whether the automation class remains appropriate
- challenging automation that has become de facto governance

Automation should reduce operational drag, not reduce accountability.

## Required Artifacts

Every scorecard-driven action must record:

- action protocol level
- action family
- assigned automation class
- reason for that automation class
- whether the action was auto-executed, drafted, reviewed, approved, or rejected
- any later override or escalation

This record is required for automation audit and later doctrine refinement.

## Surface Expectations

Operator surfaces should clearly distinguish:

- automated completion
- drafted recommendation
- pending review
- pending approval
- human-only decision needed

The platform should never make a human-governed action look as if it already happened automatically.

## Anti-Patterns

Avoid these failures:

- automating scope constraints without visible human review
- treating drafted escalations as actual escalations
- automatically extending exceptions because similar cases happened before
- auto-pausing major portfolio decisions from weak or stale scorecards without the required authority path
- hiding automation class from operators
- letting convenience push a judgment-heavy action into `auto_allowed`

## Adoption Sequence

Recommended rollout:

1. automate `record`, `observe`, and simple `reassess` actions
2. add auto-assisted drafting for reviews, escalations, and remediation packets
3. allow human-confirmed constraint actions only after audit trails are stable
4. keep exception handling, posture changes, and major portfolio decisions governed even in mature phases

## Open Questions

Later refinement may be needed for:

- whether some doctrine areas can safely support more aggressive automation
- how automation classes should interact with workload and operator availability
- whether repeated reviewer confirmations can graduate a narrow action from `review_required` to `auto_assist_only`
- how action automation should surface in observability dashboards

## Summary

The scorecard action system should automate bounded follow-up work, not automate doctrine judgment by accident.

This spec defines that boundary through explicit automation classes, safe-envelope rules, escalation behavior, and artifact requirements so the platform can move quickly on low-risk scorecard responses while preserving meaningful human and governance control over strategic portfolio actions.
