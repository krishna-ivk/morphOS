# Profile Doctrine Portfolio Scorecard Capacity Recovery Spec

## Purpose

This spec defines how the doctrine portfolio should recover when repeated scorecard queue breaches reveal real capacity limits rather than isolated operator delay.

The earlier specs already define:

- how scorecard handoffs are queued
- how queue service expectations are measured
- how breaches are detected and escalated

This document defines what happens when those breaches indicate a sustained capacity problem.

## Core Principle

A capacity problem should trigger recovery behavior, not just repeated breach recording.

Once the portfolio can see that doctrine review, approval, or governance capacity is persistently insufficient, the system must respond in a structured way:

- stabilize
- narrow scope
- protect critical work
- restore service
- learn from the overload

Without a recovery model, the platform will normalize breach churn and slowly lose trust in its own governance posture.

## Goals

This recovery model exists to ensure:

- repeated queue breaches produce a real operational response
- doctrine work is prioritized under constraint
- service restoration is intentional and measurable
- overload does not silently weaken governance or freshness discipline
- capacity failure becomes a portfolio learning input

## Non-Goals

This spec does not define:

- hiring or staffing policy
- runtime compute autoscaling
- workflow execution concurrency
- non-doctrine operational recovery

This applies only to doctrine portfolio scorecard handling capacity.

## Recovery Trigger Classes

Capacity recovery may be triggered by:

- sustained acknowledgement breaches
- sustained ownership breaches
- sustained decision breaches
- rising freshness breaches
- repeated defer breaches
- persistent high-priority backlog
- authority bottlenecks

The trigger should look for patterns over time, not only isolated incidents.

## Recovery Entry Conditions

The system should enter capacity recovery when one or more of these conditions hold:

- breach rate exceeds tolerated baseline across multiple review windows
- critical or urgent items are repeatedly missing decision targets
- freshness breaches begin affecting decision-critical items
- queue health shows backlog growth without matching closure recovery
- a specific authority lane becomes the dominant bottleneck

Recovery entry should be explicit and recorded, not inferred informally.

## Recovery Modes

Allowed recovery modes:

- `watch_recovery`
- `local_recovery`
- `portfolio_recovery`
- `authority_recovery`

### `watch_recovery`

Used when early warning signs appear but the queue is still mostly functional.

Goal:

- prevent deterioration
- tighten observation
- reduce avoidable queue churn

### `local_recovery`

Used when one doctrine area or one queue slice is overloaded but the whole portfolio is not yet in distress.

Goal:

- stabilize the affected slice
- protect neighboring capacity
- avoid unnecessary portfolio-wide disruption

### `portfolio_recovery`

Used when overload is broad enough that queue discipline, SLA posture, and handoff health are degrading across multiple doctrine areas.

Goal:

- restore safe portfolio handling
- narrow active surface area
- protect critical governance work

### `authority_recovery`

Used when the bottleneck is concentrated in a specific approval or authority lane.

Goal:

- reduce authority choke points
- preserve decision integrity
- keep the queue from piling up behind a single constrained role

## Recovery Stages

Every recovery mode should move through these stages:

1. detect
2. stabilize
3. constrain
4. restore
5. exit_or_escalate

### `detect`

Confirm that the problem is real and not just a one-off spike.

### `stabilize`

Stop the system from making the overload worse.

### `constrain`

Reduce inflow, narrow queue scope, and protect the most important work.

### `restore`

Rebuild queue health and response capability.

### `exit_or_escalate`

Either return to normal posture or escalate if recovery is failing.

## Stabilization Actions

Allowed stabilization actions:

- raise visibility of overloaded queue slices
- freeze low-priority intake into affected doctrine lanes
- reclassify watch items to slower treatment
- increase automation only for safe clerical tasks
- require stricter defer discipline
- surface bottleneck authority lanes explicitly

Stabilization should reduce chaos without silently weakening governance.

## Constraint Actions

Allowed constraint actions:

- pause non-critical doctrine improvements
- narrow review scope to critical and urgent items
- defer low-risk watch work into later cadence
- require explicit justification for new exception work
- slow or pause non-essential maturity claims

The purpose of constraint is to protect the queue’s ability to handle high-risk doctrine decisions safely.

## Restoration Actions

Allowed restoration actions:

- rebalance ownership across reviewers where permitted
- add structured review blocks for the bottleneck queue
- clear stale items through reassessment or supersession
- refresh aging packets before they become repeated breach sources
- reduce avoidable packet churn through better routing

Restoration should improve throughput without compromising authority or freshness rules.

## Authority Bottleneck Handling

If overload is concentrated in one authority path:

- route preparatory work to lower layers where safe
- bundle related approvals when policy allows
- surface authority scarcity in queue ranking
- consider narrower scope decisions that require less scarce authority

The system must not reduce authority requirements just to clear backlog faster.

## Intake Control

During recovery, the platform may apply intake controls such as:

- watch-only admission for low-risk items
- delayed admission for non-urgent doctrine changes
- stricter thresholds for opening new remediation tracks
- mandatory triage before creating approval-bound items

Intake control must be explicit, temporary, and reversible.

## Interaction With SLA

Recovery mode may change how the platform behaves around SLA, but it must not hide breaches.

Allowed effects:

- more aggressive prioritization of urgent items
- explicit widening of some low-priority targets if doctrine policy allows
- stronger breach escalation for critical items

Disallowed effect:

- silently redefining missed service as acceptable without a governed change

## Interaction With Queue Discipline

Recovery mode should feed queue discipline by:

- changing ordering weights toward critical items
- tightening defer scrutiny
- increasing visibility of stale-risk items
- accelerating supersession of obviously outdated packets

Recovery must make the queue more honest, not merely quieter.

## Interaction With Automation Boundary

Recovery may expand `auto_allowed` only for:

- clerical routing
- packet refresh requests
- record generation
- watchlist maintenance

Recovery must not use automation as a hidden substitute for human doctrine judgment.

## Recovery Success Criteria

Recovery should be considered successful only when:

- breach rate declines materially
- freshness breaches stop affecting active decision work
- urgent and critical items return to safer response posture
- backlog growth stabilizes or reverses
- the bottleneck authority path is no longer degrading the queue

Success should be evidence-based, not declared because the queue "feels calmer."

## Failed Recovery Signals

Recovery should be escalated if:

- critical breaches continue during recovery
- freshness breaches remain common
- constrained scope still does not restore service
- authority bottlenecks remain unresolved
- deferred low-priority work starts becoming systemic backlog risk

Failed recovery is itself a portfolio governance signal.

## Exit Conditions

Recovery may exit when:

- the triggering patterns remain below threshold for a sustained review window
- urgent and critical items are no longer breaching at abnormal rates
- recovery constraints can be safely relaxed
- queue health signals show stable restoration

Exit must be explicit and recorded so later retrospectives can evaluate whether recovery really worked.

## Required Artifacts

Each recovery episode must record:

- recovery mode
- trigger pattern
- entry time
- constrained doctrine scope
- actions taken
- authority bottlenecks identified
- restoration metrics
- exit or escalation outcome

These artifacts should feed portfolio learning and doctrine load planning.

## Observability Signals

The recovery system should emit at least:

- active recovery mode
- duration in recovery
- backlog trend during recovery
- breach trend during recovery
- freshness breach count during recovery
- authority bottleneck concentration
- deferred work carried out of recovery

These signals should remain visible until the system fully exits recovery.

## Anti-Patterns

Avoid these failures:

- treating overload as normal and never entering recovery
- using recovery as an excuse to weaken governance permanently
- hiding SLA breaches while recovery is active
- widening queue scope before service is stable
- assuming lower queue volume means successful recovery if stale risk increased
- allowing authority bottlenecks to remain invisible during recovery

## Adoption Sequence

Recommended rollout:

1. detect sustained overload patterns
2. define and surface explicit recovery modes
3. connect recovery to queue ordering, intake control, and bottleneck visibility
4. add exit and failed-recovery escalation logic

## Open Questions

Later refinement may be needed for:

- whether doctrine areas need separate recovery thresholds
- how recovery should interact with wave launch posture
- whether some recovery actions should auto-open portfolio review
- how to convert repeated recovery episodes into structural doctrine changes

## Summary

Repeated scorecard queue breaches should not remain a passive metric. They should trigger a disciplined recovery loop.

This spec defines that loop through recovery modes, staged actions, intake control, authority bottleneck handling, restoration criteria, and explicit exit rules so doctrine portfolio overload becomes manageable, visible, and learnable instead of chronic background instability.
