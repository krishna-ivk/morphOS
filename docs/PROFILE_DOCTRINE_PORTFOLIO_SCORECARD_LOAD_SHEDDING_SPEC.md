# Profile Doctrine Portfolio Scorecard Load Shedding Spec

## Purpose

This spec defines how the doctrine portfolio intentionally reduces, delays, narrows, or suppresses lower-value scorecard work during overload while preserving honesty about risk and governance impact.

The earlier specs already define:

- queue discipline
- SLA and breach handling
- capacity recovery

This document defines a more forceful overload tool:

load shedding.

## Core Principle

When the doctrine portfolio is overloaded, it is better to deliberately drop or delay lower-priority work than to pretend all work is still being handled safely.

Load shedding must therefore be:

- explicit
- policy-bounded
- reversible
- observable
- risk-labeled

The platform should never hide load shedding behind vague phrases like "later review" when the real meaning is "we are intentionally not servicing this class of work right now."

## Goals

This load-shedding model exists to ensure:

- overload response is honest
- critical doctrine work remains protected
- lower-value work is reduced in a controlled way
- deferred risk remains visible
- shedding decisions become learnable portfolio signals

## Non-Goals

This spec does not define:

- permanent policy simplification
- human staffing plans
- runtime compute load shedding
- product-feature triage outside doctrine portfolio operations

This applies only to doctrine portfolio scorecard handling load.

## Load Shedding Triggers

Load shedding may be triggered by:

- sustained queue overload
- repeated SLA breaches despite recovery posture
- authority bottlenecks that block critical work
- rising freshness breaches on urgent items
- backlog growth that exceeds closure capacity for multiple review windows

Load shedding should not be the first response to small or temporary spikes.

## Entry Conditions

The system should enter load shedding only when:

- normal queue discipline is insufficient
- SLA breach response is already active
- capacity recovery actions are not enough or not fast enough
- protecting critical doctrine work now requires reducing lower-priority work

Entry should be explicit and recorded as a distinct posture.

## Shedding Modes

Allowed load-shedding modes:

- `watch_shedding`
- `selective_shedding`
- `protective_shedding`
- `emergency_shedding`

### `watch_shedding`

Used when the platform needs minor reduction in low-value work to protect normal flow.

Typical effect:

- delay or batch watch-level items
- reduce non-urgent refresh activity

### `selective_shedding`

Used when one or more doctrine lanes must intentionally reduce intake and follow-up to preserve important work.

Typical effect:

- defer low-risk reviews
- suppress non-essential maturity maintenance
- pause low-value recommendation generation

### `protective_shedding`

Used when urgent and critical doctrine work is at risk and the platform must aggressively narrow lower-priority handling.

Typical effect:

- suspend watch-level action entirely
- convert many standard items into later backlog
- stop optional portfolio hygiene work

### `emergency_shedding`

Used when queue health, freshness, or authority bottlenecks are severe enough that only the smallest critical doctrine surface can be served safely.

Typical effect:

- handle only critical governance and blocking items
- freeze most other scorecard-driven work
- require explicit recovery before wider service resumes

## Sheddable Work Classes

Load shedding may apply only to work classes that are policy-approved as shed-capable.

Typical shed-capable work:

- low-risk watch items
- advisory-only follow-up
- non-urgent recommendation generation
- non-critical doctrine hygiene
- optional review enrichment
- low-priority historical refresh work

Typical non-sheddable work:

- critical intervention decisions
- urgent blocking governance actions
- freshness repair for active high-risk decisions
- required authority routing for live portfolio risk
- exception review that directly affects decision integrity

## Shedding Actions

Allowed shedding actions:

- delay
- batch
- downgrade to watch-only
- narrow review depth
- suppress optional artifact generation
- pause intake
- pause follow-up creation
- close as intentionally unserviced with risk marker

Every shedding action must be explicitly classified. The system should not use vague backlog drift as implicit shedding.

## Risk Labeling

Every shed item must carry a risk label such as:

- `low_risk_delayed`
- `visibility_reduced`
- `freshness_deferred`
- `followup_suppressed`
- `unserviced_by_policy`

This ensures the portfolio can later distinguish intentional shedding from accidental neglect.

## Selection Rules

Work should be considered for shedding based on:

- priority band
- severity posture
- decision criticality
- freshness sensitivity
- authority scarcity
- intervention relevance
- reversibility of later recovery

The platform should always prefer shedding work that:

- is lowest risk
- is easiest to recover later
- does not distort current governance truth

## Order Of Shedding

Recommended shedding order:

1. optional artifact and enrichment work
2. advisory-only follow-up
3. watch-level and low-priority review work
4. non-urgent standard work
5. only in emergency posture, narrowly constrained standard work with explicit risk labels

Critical and urgent decision-integrity work should be the last surface ever considered and normally should not be shed at all.

## Interaction With Queue Discipline

Shedding must be visible in the queue model.

Queue items affected by shedding should be marked as:

- `shed_delayed`
- `shed_batched`
- `shed_suppressed`
- `shed_closed_with_risk`

These may be represented as queue annotations or queue states, but the posture must remain queryable and auditable.

## Interaction With SLA

Load shedding may change service expectations for affected low-priority work, but it must not hide service loss.

Allowed behavior:

- apply a different declared SLA profile for shed work
- explicitly suspend SLA on paused optional work

Disallowed behavior:

- silently missing the original SLA and pretending it was never applicable

Shed work must still preserve timing truth.

## Interaction With Capacity Recovery

Load shedding is a stronger tool inside capacity recovery, not a separate excuse to avoid recovery.

When load shedding activates:

- capacity recovery should remain active
- shedding should help restore service to protected work
- the system should keep measuring whether shedding is actually working

If shedding does not improve critical queue health, the portfolio should escalate rather than remain in indefinite reduced service.

## Interaction With Automation

Automation may assist load shedding only for clerical actions such as:

- tagging affected items
- reclassifying SLA posture
- suppressing optional packet generation
- batching low-priority queue entries

Automation must not decide on its own to shed non-shed-capable work.

## Recovery From Shedding

When the system exits shedding posture, it must decide what happens to affected items:

- restore for active handling
- refresh before reactivation
- keep deferred for later wave
- permanently close with historical risk marker

Exiting shedding is not just "turning service back on." It requires a deliberate recovery path for previously reduced work.

## Success Criteria

Load shedding should be considered effective only if:

- critical and urgent doctrine work becomes safer
- breach rates decline in the protected classes
- freshness loss in protected classes reduces
- queue overload becomes more manageable

If these improvements do not appear, shedding may be harming visibility more than helping service.

## Failure Signals

Shedding should be reconsidered or escalated if:

- protected work still breaches heavily
- shed backlog becomes a major future risk
- decision-quality signals decline
- operators stop understanding what is or is not being serviced
- emergency shedding lasts longer than intended without restoration plan

Indefinite shedding is a sign of unresolved structural capacity problems.

## Required Artifacts

Each shedding episode must record:

- shedding mode
- trigger conditions
- work classes affected
- actions applied
- risk labels used
- entry and exit time
- observed impact on protected work
- residual backlog carried forward

This record is required for audit and portfolio learning.

## Observability Signals

The shedding system should emit at least:

- count of shed items by class
- percentage of queue affected by shedding
- protected-work breach rate before and after shedding
- duration in shedding mode
- residual shed backlog after exit
- number of items permanently closed with risk marker

These signals should remain visible during and after shedding.

## Anti-Patterns

Avoid these failures:

- silently shedding work through neglect
- treating shedding as a permanent operating model
- shedding critical decision-integrity work to make metrics look cleaner
- removing historical evidence that work was intentionally unserviced
- using shedding to mask poor routing or weak authority design
- resuming from shedding without a reactivation plan

## Adoption Sequence

Recommended rollout:

1. define shed-capable and non-shed-capable work classes
2. add explicit shedding modes and risk labels
3. connect shedding to queue and SLA visibility
4. require exit and reactivation rules for all shedding episodes

## Open Questions

Later refinement may be needed for:

- whether some doctrine areas need custom shedding hierarchies
- when a shed backlog should automatically trigger doctrine change-management review
- how long emergency shedding may persist before mandatory escalation
- how to expose shedding posture in operator dashboards without creating confusion

## Summary

When overload becomes real, the doctrine portfolio needs a way to intentionally reduce lower-value work without lying to itself.

This spec defines that mechanism through explicit shedding modes, sheddable work classes, risk labels, queue and SLA visibility, and recovery rules so overload handling remains governed, visible, and strategically honest.
