# Profile Doctrine Portfolio Scorecard SLA And Breach Response Spec

## Purpose

This spec defines the service expectations for scorecard-driven portfolio handoffs and the required response when those expectations are breached.

The earlier specs already define:

- how scorecard posture is interpreted
- how portfolio actions are triggered
- where automation stops
- how operator handoffs are created
- how those handoffs are managed in queue

This document defines the time-and-response contract for that queue.

## Core Principle

A queue without service expectations slowly normalizes delay.

The doctrine portfolio should make delay visible, measurable, and actionable. A missed response target is not just a scheduling inconvenience. It is a potential doctrine-governance failure signal.

The platform should therefore treat response expectations as:

- explicit
- risk-sensitive
- auditable
- tied to breach actions

## Goals

This SLA model exists to ensure:

- scorecard handoffs have clear service expectations
- urgent doctrine work receives timely attention
- breaches trigger predictable operational response
- chronic delay becomes a visible portfolio signal
- queue performance feeds doctrine health honestly

## Non-Goals

This spec does not define:

- human employment schedules
- global company paging policy
- runtime execution latency
- non-doctrine queues

This applies only to doctrine portfolio scorecard handoffs and their operator workflow.

## SLA Objects

Each active queue item must carry one SLA profile.

Minimum SLA fields:

- SLA class
- initial response target
- ownership target
- decision target
- freshness compatibility window
- breach thresholds
- required breach actions

An SLA profile may be inherited from doctrine policy, intervention posture, or a specific decision class.

## SLA Classes

Allowed default SLA classes:

- `watch`
- `standard`
- `urgent`
- `critical`

These classes should stay simple and stable across surfaces.

## SLA Class Intent

### `watch`

Used for low-risk, low-urgency, largely informational scorecard items.

Expected behavior:

- visible in queue
- reviewed in normal cadence
- not expected to interrupt active work

### `standard`

Used for ordinary doctrine handoffs that need real ownership and timely review, but are not yet actively threatening a wave or governance posture.

Expected behavior:

- prompt triage
- named ownership
- decision before freshness risk becomes material

### `urgent`

Used for decision-blocking or time-sensitive doctrine work where delay is itself a growing risk.

Expected behavior:

- rapid ownership
- quick routing to correct authority
- breach visibility in the same operating cycle

### `critical`

Used for portfolio-risk or wave-risk doctrine items where delay may materially worsen risk posture or allow hidden instability to persist.

Expected behavior:

- immediate visibility
- rapid authority engagement
- automatic breach escalation if response stalls

## SLA Targets

Every SLA profile should define at least three targets:

- `acknowledge_by`
- `own_by`
- `decide_by`

### `acknowledge_by`

The time by which the queue item must be noticed and triaged.

### `own_by`

The time by which a responsible operator or authority path must be assigned.

### `decide_by`

The time by which the item should reach a valid next disposition:

- decision
- defer with rule
- reassessment
- escalation
- closure

This does not always require final closure, but it does require meaningful forward movement.

## Freshness Compatibility

SLA targets must never exceed the freshness compatibility window of the linked scorecard and evidence without explicit reassessment logic.

If the decision target would naturally fall after freshness expiry, the system must:

- shorten the target
- require early refresh
- or mark the item as needing reassessment before decision

This prevents an SLA that quietly encourages stale decision-making.

## Default Mapping

Recommended defaults:

- `P3_watch` + informational posture -> `watch`
- `P2_normal` + ordinary review -> `standard`
- `P1_high` + decision-blocking or review-required -> `urgent`
- `P0_critical` + portfolio-risk or intervention-sensitive -> `critical`

The queue may refine this based on intervention posture, authority scarcity, and freshness pressure.

## Breach Types

An item may breach in different ways:

- `acknowledgement_breach`
- `ownership_breach`
- `decision_breach`
- `freshness_breach`
- `repeat_defer_breach`

These breach types must be tracked separately because they indicate different operational failures.

## Acknowledgement Breach

This means the item was not triaged in time.

This usually signals:

- queue overload
- poor routing
- weak visibility

Required default response:

- raise queue visibility
- increase priority if warranted
- record breach

## Ownership Breach

This means the item did not get a clear owner or authority path in time.

This usually signals:

- authority ambiguity
- staffing or capacity mismatch
- escalation friction

Required default response:

- route to stronger queue review
- force ownership clarification
- record breach with authority context

## Decision Breach

This means the item did not meaningfully progress by the decision target.

This usually signals:

- decision avoidance
- unresolved conflict
- overloaded authority path

Required default response:

- force operator review of blockage reason
- consider escalation
- record breach for doctrine observability

## Freshness Breach

This means the queue has allowed an item to outlive safe evidence posture.

This is especially important because it means the queue is now carrying unsafe decision material.

Required default response:

- move to `stale` or reassessment path
- block direct decision from old packet
- record freshness breach explicitly

## Repeat Defer Breach

This means the item has been deferred often enough that delay itself is now part of the doctrine signal.

Required default response:

- raise queue review priority
- require defer justification review
- consider escalation to portfolio review

## Breach Severity

Every breach should carry its own severity:

- `minor`
- `material`
- `systemic`

Severity should depend on:

- SLA class
- affected decision class
- intervention posture
- whether the breach is isolated or repeated
- whether freshness was compromised

## Breach Response Levels

Recommended response levels:

- `B0_record_only`
- `B1_notify_and_reprioritize`
- `B2_escalate_queue_attention`
- `B3_escalate_authority`
- `B4_trigger_portfolio_intervention_review`

These levels should scale with breach severity and recurrence.

## Default Breach Actions

Recommended defaults:

- minor acknowledgement breach -> `B1_notify_and_reprioritize`
- material ownership breach -> `B2_escalate_queue_attention`
- material decision breach -> `B3_escalate_authority`
- freshness breach on urgent or critical item -> `B3_escalate_authority`
- repeated critical breaches in one doctrine area -> `B4_trigger_portfolio_intervention_review`

These defaults may be tightened during intervention posture.

## Auto Response Rules

The platform may automatically perform low-risk breach responses such as:

- marking breach state
- reprioritizing a queue item
- sending queue visibility signals
- requesting reassessment for freshness breach

The platform should not automatically:

- approve an exception because of breach pressure
- suppress a gate because SLA was missed
- declare a doctrine area healthy because a queue was cleared

Breaches may justify more attention, not weaker governance.

## Interaction With Intervention

Under active intervention:

- SLA classes should tend to tighten
- breach severity should ratchet upward faster
- repeated breaches should more quickly trigger governance review

This reflects the fact that delayed doctrine attention is more dangerous in already elevated conditions.

## Interaction With Failsafe

In degraded governance or failsafe posture:

- some SLA targets may widen due to reduced capability
- but breach recording must become more explicit, not less
- confidence in closure claims should narrow

Failsafe posture explains some delay. It does not erase the portfolio signal of delay.

## Interaction With Queue Discipline

SLA posture must feed queue ordering and queue health.

Specifically:

- breached items should become more visible
- repeated breach patterns should feed queue-health alerts
- unresolved breach clusters should influence capacity and escalation review

Queue discipline and SLA management must operate as one loop, not two disconnected systems.

## Required Artifacts

Every breach event must preserve:

- queue item id
- handoff packet id
- breached target type
- breach timestamp
- breach severity
- response level
- actions taken
- whether the item later recovered

This is required for audit, retrospective analysis, and doctrine portfolio health review.

## Recovery From Breach

When an item returns to healthy handling after breach, the system should record:

- breach cleared
- current posture
- whether freshness was restored
- whether escalation remains open

Clearing a breach must not erase breach history.

## Portfolio Signals

The SLA system should emit at least these rollups:

- breach count by doctrine area
- breach count by SLA class
- percentage of stale-causing breaches
- mean acknowledgement delay
- mean ownership delay
- mean decision delay
- repeat-defer breach rate
- unresolved breach count

These should feed broader doctrine portfolio observability and scorecard interpretation.

## Anti-Patterns

Avoid these failures:

- setting SLA targets without breach actions
- hiding freshness breach inside generic delay metrics
- widening targets informally without doctrine change
- clearing breaches without showing whether stale posture was fixed
- treating breach pressure as justification to weaken gates
- assuming queue volume alone explains repeated breach patterns

## Adoption Sequence

Recommended rollout:

1. define SLA classes and breach types
2. connect queue items to acknowledge, own, and decide targets
3. enforce freshness breach handling
4. connect repeated breaches to escalation and intervention review

## Open Questions

Later refinement may be needed for:

- whether doctrine areas need separate SLA baselines
- how to model non-working-hour effects without hiding real risk
- whether some breaches should auto-open change-management intake
- how SLA posture should influence future scorecard recommendations

## Summary

The doctrine queue needs more than ordering. It needs explicit service expectations and a truthful response when those expectations fail.

This spec defines that contract through SLA classes, target types, breach types, breach response levels, and recovery artifacts so delay in scorecard-driven doctrine work becomes a visible, governable portfolio signal instead of a quiet operational habit.
