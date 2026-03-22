# Profile Doctrine Portfolio Scorecard Queue Discipline Spec

## Purpose

This spec defines how scorecard-driven portfolio handoffs are ordered, aged, revisited, escalated, and closed once they enter an operator queue.

The earlier specs already define:

- how scorecard posture is interpreted
- how it binds into decisions
- what action protocol is triggered
- where automation must stop
- how operator handoff packets are created

This document defines the queue behavior after handoff creation.

## Core Principle

A doctrine handoff queue is not just a storage list. It is an operational control surface.

Queue discipline must ensure that:

- urgent items do not get buried
- stale items do not masquerade as current work
- blocked items remain visible
- repeated deferrals become visible doctrine signals
- operator attention is aligned with real portfolio risk

Without explicit queue discipline, even well-formed handoffs decay into administrative noise.

## Goals

This queue discipline exists to ensure:

- scorecard handoffs remain actionable
- response order matches portfolio risk and authority need
- queue backlog does not hide doctrine weakness
- stale and superseded packets are actively managed
- escalation from queue delay is predictable and auditable

## Non-Goals

This spec does not define:

- user-interface layout
- general ticketing behavior outside doctrine portfolio work
- workflow runtime job queues
- code review queues

This applies only to doctrine portfolio scorecard handoffs.

## Queue Item

Each queue item must reference a canonical handoff packet and extend it with queue state.

Required queue fields:

- queue item id
- handoff packet id
- current queue state
- priority band
- severity posture
- authority requirement
- insertion time
- last touch time
- freshness expiry
- defer count
- reassignment count
- escalation status

## Queue States

Allowed queue states:

- `new`
- `triaged`
- `awaiting_action`
- `awaiting_authority`
- `deferred`
- `blocked`
- `stale`
- `superseded`
- `closed`

These states should be stable across all queue surfaces.

## State Meanings

### `new`

The handoff has entered the queue but has not yet been reviewed for ordering and ownership.

### `triaged`

The item has been classified, prioritized, and routed, but no final operator action has yet been taken.

### `awaiting_action`

The right owner is known and the next decision or review is expected from that owner.

### `awaiting_authority`

The item is blocked on a higher authority class than the current queue owner can provide.

### `deferred`

The item has been intentionally delayed with a stated reason and revisit condition.

### `blocked`

The item cannot move because a dependency is missing, such as fresh reconciliation, required evidence, or policy clarification.

### `stale`

The item has aged past safe decision use and must be refreshed, reassessed, or replaced before action continues.

### `superseded`

The item is no longer current because a newer packet, refreshed packet, or changed posture replaced it.

### `closed`

The item has completed with a recorded disposition and is no longer active.

## Priority Bands

Each item must be assigned one priority band:

- `P0_critical`
- `P1_high`
- `P2_normal`
- `P3_watch`

Priority band is not the same as severity, though severity strongly influences it.

## Priority Inputs

Priority should be derived from:

- handoff severity
- action protocol level
- decision-blocking effect
- authority scarcity
- intervention posture
- trend direction
- queue age
- number of prior deferrals

Repeatedly deferred items should trend upward in priority unless explicitly justified otherwise.

## Default Priority Guidance

Recommended defaults:

- `portfolio_risk` + `L4_systemic_escalation` -> `P0_critical`
- `decision_blocking` + `approval_required` -> `P1_high`
- `time_sensitive` + `review_required` -> `P1_high`
- `informational` + `auto_assist_only` -> `P2_normal` or `P3_watch`

The queue must still allow local adjustment when context justifies it.

## Queue Ordering Rules

Default queue ordering should consider, in order:

1. priority band
2. severity posture
3. freshness risk
4. time already waiting
5. intervention relevance
6. authority availability risk

This ensures the queue reflects operational danger rather than simple first-in-first-out order.

## Aging Rules

Every active queue item must age against at least two clocks:

- response clock
- freshness clock

The response clock measures how long the item has waited for attention.

The freshness clock measures how long the linked scorecard and evidence remain safe to act upon.

An item may still be young in response time but already unsafe because freshness expired.

## Aging Thresholds

Each queue item should carry threshold markers:

- `attention_due`
- `risk_of_stale`
- `stale_at`
- `escalate_if_unowned`

Thresholds should be based on severity, protocol level, and authority requirement.

Higher-risk items should age faster.

## Defer Discipline

Deferral is allowed only with:

- explicit reason
- explicit revisit date or trigger
- statement of whether refresh is required before revisit

Deferral must not freeze the aging model completely. Deferred items should continue to accumulate queue history and become candidates for escalation if repeatedly postponed.

## Deferral Limits

The queue should track:

- total defer count
- consecutive defers without material progress
- average defer duration

Repeated deferrals should trigger:

- queue health alerts
- doctrine observability signals
- possible escalation to portfolio review

## Reassignment Discipline

Reassignment is allowed when:

- authority mismatch is discovered
- workload balancing is needed
- intervention ownership changes
- better subject-matter fit is required

Reassignment must preserve:

- original packet context
- age history
- prior queue events
- current urgency

Reassignment must not be used to "reset the clock."

## Blocked Item Rules

Blocked items must clearly state:

- what is missing
- who owns the missing dependency
- whether action is waiting on evidence, authority, or policy
- expected unblock path

Blocked items should remain visible in queue reporting and must not disappear behind closed items.

## Staleness Handling

When a queue item becomes stale, the queue must force one of these outcomes:

- refresh and continue
- return for reassessment
- supersede with a new packet
- close as no longer actionable

No stale item should remain silently actionable.

## Supersession Rules

An item should move to `superseded` when:

- a refreshed packet replaces it
- scorecard reconciliation materially changes the posture
- the linked decision path has changed enough that the old request no longer applies

Superseded items must remain visible in history but should leave active ordering.

## Escalation From Queue Behavior

Queue behavior itself may trigger escalation.

Escalation should be considered when:

- a high-priority item remains unowned
- repeated deferrals indicate decision avoidance
- stale items accumulate in a doctrine area
- blocked items reveal structural dependency problems
- handoff volume exceeds review capacity persistently

This keeps queue dysfunction from hiding as a simple operational inconvenience.

## Queue Health Signals

The queue should emit at least these signals:

- oldest active item age
- count of stale items
- count of blocked items
- defer rate
- reassignment rate
- approval wait time
- closure rate
- supersession rate

These signals should feed broader portfolio observability.

## Operator Expectations

Operators should be able to tell at a glance:

- what demands action now
- what is waiting on authority
- what is becoming unsafe due to staleness
- what is repeatedly deferred
- what is blocked for structural reasons

The queue should communicate posture, not just volume.

## Required Artifacts

Each queue item must preserve:

- queue state transitions
- priority changes
- defer events
- reassignment events
- stale and supersession events
- final closure outcome
- timestamps for all major transitions

This history is required for audit, retrospectives, and doctrine load analysis.

## Surface Expectations

Any queue surface should clearly render:

- priority band
- severity posture
- current state
- freshness risk
- authority requirement
- next due time
- reason for block or defer if present

The goal is to make queue risk legible without opening every packet.

## Anti-Patterns

Avoid these failures:

- treating queue order as simple FIFO
- allowing deferral without a revisit rule
- resetting age on reassignment
- leaving stale packets in actionable states
- hiding blocked items from active reporting
- treating superseded items as completed success

## Adoption Sequence

Recommended rollout:

1. standardize queue states and priority bands
2. add response and freshness clocks
3. enforce defer and staleness rules
4. connect queue dysfunction to escalation and observability

## Open Questions

Later refinement may be needed for:

- whether doctrine areas need different aging curves
- how queue order should adapt under sustained overload
- whether some low-risk items can auto-close after supersession
- how queue discipline should interact with operator locale and working hours

## Summary

The scorecard handoff queue is where doctrine work either remains alive or quietly decays.

This spec defines queue discipline through stable states, priority bands, aging rules, defer and reassignment controls, stale and supersession handling, and queue-health signals so scorecard-driven operator work stays visible, timely, and governable.
