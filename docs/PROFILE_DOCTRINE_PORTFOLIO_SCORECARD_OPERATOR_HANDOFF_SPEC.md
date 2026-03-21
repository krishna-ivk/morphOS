# Profile Doctrine Portfolio Scorecard Operator Handoff Spec

## Purpose

This spec defines how scorecard-driven portfolio actions are handed off to operators once automation reaches a review, approval, or human-only boundary.

The previous specs define:

- how the doctrine scorecard is interpreted
- how it binds into portfolio decisions
- what action protocol it should trigger
- which parts of that protocol may be automated

This document defines the final operational bridge:

how the system hands the matter to a human without losing context, authority clarity, or momentum.

## Core Principle

A handoff is successful only when the next operator can understand:

- what happened
- why it matters
- what the system already did
- what authority is required next
- what decision is now expected

The platform should not force operators to reconstruct the scorecard posture from raw evidence or scattered artifacts.

## Goals

This handoff model exists to ensure:

- automated and semi-automated scorecard actions do not stall at human boundaries
- operators receive the minimum complete context needed to act
- authority and urgency are visible immediately
- handoffs are auditable and repeatable
- review and approval work feels like continuation, not restart

## Non-Goals

This spec does not define:

- how operator interfaces are visually designed
- how scorecards are calculated
- workflow-level coding handoffs
- general incident-management handoffs outside doctrine portfolio work

This is only about portfolio-level scorecard action handoff.

## Handoff Triggers

A handoff must be created when a scorecard-driven action reaches any of these conditions:

- `review_required`
- `approval_required`
- `human_only`
- automation blocked by ambiguity
- automation blocked by stale or disputed scorecard posture
- automation blocked by intervention or failsafe policy

The system may also create a handoff proactively when a repeated low-confidence pattern suggests operator attention before a hard gate is hit.

## Handoff Packet

Every scorecard operator handoff must be represented as a structured packet.

Minimum packet fields:

- handoff id
- doctrine area or portfolio scope
- triggering scorecard snapshot reference
- current reconciled scorecard posture
- binding outcome
- action protocol level
- automation class
- reason handoff is required
- requested operator action
- required authority class
- urgency or response window
- linked evidence references
- open caveats or disputes
- prior automated actions already taken

This packet should be the canonical handoff object across all surfaces.

## Requested Operator Actions

The handoff must clearly classify what the operator is being asked to do.

Allowed request types:

- `review_and_confirm`
- `review_and_modify`
- `approve_or_reject`
- `escalate_authority`
- `resolve_dispute`
- `set_exception_disposition`
- `choose_scope_constraint`
- `defer_with_reason`
- `request_more_evidence`

The system should not hand off with vague asks such as "please check" or "needs attention."

## Authority Cues

Every handoff must state:

- who may act
- who may only review
- whether the current operator can complete the action
- whether escalation is mandatory

Authority cues should be based on the existing portfolio authority model, not local habit.

Typical authority labels:

- portfolio reviewer
- doctrine owner
- workspace admin
- super-admin
- intervention owner

## Handoff Severity

Each handoff must carry one severity posture:

- `informational`
- `time_sensitive`
- `decision_blocking`
- `portfolio_risk`

This posture should be derived from:

- protocol level
- decision class
- trend direction
- exception presence
- intervention posture

Severity affects routing, response expectations, and inbox ordering.

## Handoff Freshness

A handoff must include freshness markers for:

- the scorecard snapshot
- linked evidence
- the packet itself

If the handoff becomes stale before action is taken, the system must either:

- refresh it
- flag it as requiring reassessment
- withdraw it and issue a new handoff packet

Operators should not unknowingly act on stale handoffs.

## Handoff Composition Rules

A good handoff must include:

- one-sentence statement of the issue
- one-sentence statement of why the system stopped
- one clear requested action
- one authority statement
- one urgency statement

Then it may include supporting detail:

- caveats
- disputes
- trend notes
- previous exceptions
- related intervention context

This ordering keeps the handoff readable under time pressure.

## Automation Disclosure

The handoff must disclose what the platform already did automatically.

Examples:

- recorded the action protocol
- created a watch item
- drafted a remediation packet
- routed to a review queue
- paused a recommendation pending approval

This prevents duplicate work and avoids the false impression that nothing happened yet.

## Recommended Next Moves

The system may suggest next moves, but must separate suggestion from authority.

Suggested moves may include:

- approve current constrained scope
- reject broader expansion and request narrower pilot
- escalate to intervention governance
- request a refreshed reconciliation

Suggestions are advisory. The handoff must not make the platform’s recommendation look like a completed decision.

## Handoff Outcomes

Each handoff should resolve into one of these outcomes:

- `confirmed`
- `modified_and_confirmed`
- `approved`
- `rejected`
- `deferred`
- `escalated`
- `returned_for_reassessment`
- `withdrawn_as_stale`

The final outcome must link back to the original packet for audit and learning.

## Reassignment

If the receiving operator lacks the required authority or context:

- the handoff may be reassigned
- the reassignment must preserve the original packet
- the system should record why reassignment happened

Reassignment should not reset urgency or erase previous context.

## Escalation Handoff

If the handoff itself requires escalation:

- the escalated packet must inherit the prior context
- the new authority should see the original blocking reason
- prior operator observations should remain visible

The system should not create disconnected follow-up packets that lose the earlier trail.

## Defer and Snooze Rules

Operators may defer only when:

- the handoff is not currently decision-blocking, or
- the defer is explicitly authorized by policy

Every defer must include:

- reason
- expected revisit window
- whether fresh scorecard refresh is required before revisit

Repeated defers should feed observability and queue health review.

## Interaction With Exceptions

If a handoff concerns exception handling:

- the handoff must show current exception posture clearly
- it must show whether the requested move creates, extends, narrows, or closes an exception
- it must identify the authority required for that exception move

Exception-related handoffs should always be more explicit than ordinary review handoffs.

## Interaction With Intervention

If the doctrine portfolio is under intervention:

- the handoff should state that intervention posture prominently
- the intervention owner or delegate should be visible as an authority cue when relevant
- recommended moves should be narrower by default

This ensures the operator acts with full awareness of elevated portfolio sensitivity.

## Interaction With Failsafe

If the system is in degraded governance or failsafe mode:

- the handoff must explicitly say that confidence is reduced
- the operator should see which automatic safeguards were disabled or narrowed
- human judgment expectations should be elevated

Failsafe handoffs should be treated as high-context, not lightweight queue items.

## Required Artifacts

Every handoff must persist:

- packet id
- packet contents at issue time
- any later refresh or replacement
- routing history
- operator actions taken
- final disposition
- timestamps for open, act, and close

This is required for audit, response-time review, and doctrine learning.

## Surface Expectations

Any operator surface that renders these handoffs should clearly show:

- issue summary
- required authority
- urgency
- current scorecard posture
- what the system already did
- exact requested action
- due or revisit time

The user should not need to open multiple artifacts just to know what is being asked.

## Anti-Patterns

Avoid these failures:

- creating handoffs with no explicit requested action
- hiding the authority requirement inside supporting detail
- making automation status unclear
- handing off stale scorecard posture as if it were current
- creating a new packet on escalation without linking the old one
- letting deferred handoffs silently disappear

## Adoption Sequence

Recommended rollout:

1. standardize the handoff packet and requested action types
2. make authority and urgency cues mandatory
3. add automated packet refresh or stale withdrawal
4. integrate reassignment, defer tracking, and escalation lineage

## Open Questions

Later refinement may be needed for:

- whether some doctrine areas need richer handoff packet variants
- how much supporting evidence should be embedded vs linked
- how inbox ranking should combine severity and authority scarcity
- when repeated handoff modification should trigger recommendation or doctrine change review

## Summary

The scorecard system only works operationally if its human boundaries are clean.

This spec defines those boundaries through a structured handoff packet, explicit requested actions, authority and severity cues, freshness handling, routing history, and durable outcomes so operators can take over without reconstructing the entire doctrine state from scratch.
