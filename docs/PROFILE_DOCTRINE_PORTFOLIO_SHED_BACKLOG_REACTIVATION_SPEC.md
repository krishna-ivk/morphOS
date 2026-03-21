# Profile Doctrine Portfolio Shed Backlog Reactivation Spec

## Purpose

This spec defines how intentionally shed doctrine portfolio work returns to active handling after overload posture eases.

The earlier specs already define:

- capacity recovery
- load shedding
- queue discipline
- SLA and breach handling

This document defines the reactivation path for shed backlog so deferred or suppressed scorecard work can return safely and honestly.

## Core Principle

Reactivating shed work is not the same as simply putting old items back at the top of the queue.

A safe reactivation process must account for:

- changed doctrine posture
- changed freshness
- accumulated queue risk
- current capacity
- whether the original work is still worth doing

The system should avoid both extremes:

- forgetting shed work ever existed
- flooding the queue with stale work all at once

## Goals

This reactivation model exists to ensure:

- intentionally shed work returns through a governed path
- critical current work is not destabilized by backlog reintroduction
- stale or obsolete shed items are filtered before re-entry
- residual risk from prior shedding remains visible
- backlog recovery becomes measurable and learnable

## Non-Goals

This spec does not define:

- general backlog management outside doctrine portfolio work
- runtime job replay
- product-feature backlog resurrection
- staffing policy

This applies only to doctrine portfolio work that was intentionally shed.

## Reactivation Preconditions

Shed backlog reactivation should begin only when:

- the active overload posture has narrowed or exited
- protected queue classes are no longer in unstable breach posture
- current capacity can absorb some additional work
- reactivation has an explicit plan rather than ad hoc reopening

Reactivation must not begin merely because the shedding flag has been removed.

## Reactivation Modes

Allowed reactivation modes:

- `watch_reactivation`
- `staged_reactivation`
- `targeted_reactivation`
- `full_reactivation`

### `watch_reactivation`

Used when the system is not yet ready to fully restore work but wants to reintroduce visibility and reassessment.

Typical effect:

- surface shed backlog for review
- refresh prioritization
- do not yet fully reactivate execution

### `staged_reactivation`

Used when backlog should return gradually over multiple review windows.

Typical effect:

- restore limited slices of shed work
- cap the number of reactivated items per window
- evaluate queue health after each tranche

### `targeted_reactivation`

Used when only some shed work is worth restoring, based on current need, freshness, or doctrine importance.

Typical effect:

- reactivate selected doctrine areas or work classes
- leave lower-value shed work deferred or retired

### `full_reactivation`

Used when the system has capacity and posture confidence to restore all remaining shed work that still has value.

Typical effect:

- reopen all still-valid shed items under normal queue discipline
- preserve historical shed markers

## Reactivation Stages

Every reactivation flow should move through these stages:

1. inventory
2. filter
3. refresh
4. prioritize
5. reintroduce
6. observe

### `inventory`

Enumerate all shed work that is eligible for review.

### `filter`

Remove work that is obsolete, redundant, or no longer worth restoring.

### `refresh`

Update posture, freshness, and dependency status before the item becomes active again.

### `prioritize`

Assign reactivation order using current doctrine risk, not the old queue order alone.

### `reintroduce`

Place the selected work back into active queue handling with explicit reactivation markers.

### `observe`

Monitor whether reactivation is destabilizing active service.

## Reactivation Eligibility

An item is eligible for reactivation only if:

- the underlying doctrine question still matters
- the item is not superseded by newer work
- the item can be refreshed or revalidated
- reactivation would not violate current policy posture

Items that fail these checks should not be blindly reintroduced.

## Reactivation Outcomes

Each shed item must resolve into one of these reactivation outcomes:

- `reactivate_now`
- `reactivate_later`
- `reactivate_after_refresh`
- `merge_into_newer_item`
- `retire_with_history`

This keeps the backlog honest and prevents silent disappearance.

## Filtering Rules

Before reactivation, the system should filter out items that are:

- obsolete due to doctrine changes
- replaced by newer scorecard packets
- no longer relevant because the decision window passed
- too stale to justify restoration without full reassessment
- lower value than the cost of recovery

Filtering should be explicit and recorded.

## Refresh Rules

Shed items should usually not return directly to active handling without some refresh step.

Refresh may include:

- posture refresh
- scorecard reconciliation refresh
- freshness validation
- authority check
- dependency recheck

The deeper the time spent in shed posture, the stronger the refresh expectation should be.

## Prioritization Rules

Reactivated work should be prioritized using:

- current doctrine criticality
- residual risk from prior shedding
- freshness sensitivity
- current intervention posture
- value of restoring the work now
- current queue load

The old pre-shedding priority is informative, but not sufficient by itself.

## Reactivation Rate Limits

The platform should define rate limits for reactivation such as:

- number of items per review window
- percentage of queue capacity reserved for reactivated work
- maximum simultaneous reactivation lanes

These limits help prevent backlog re-entry from recreating the original overload.

## Interaction With Queue Discipline

Reactivated items must carry visible markers such as:

- `reactivated_from_shed`
- `reactivation_refresh_required`
- `reactivation_priority_adjusted`

These markers should remain queryable so operators know the item is returning from overload history rather than appearing as fresh ordinary work.

## Interaction With SLA

Reactivated work must receive an explicit SLA posture.

Allowed approaches:

- assign a fresh SLA based on current priority
- apply a special reactivation SLA if policy defines one
- require refresh before any new decision target starts

Disallowed approach:

- pretending the original pre-shedding SLA still ran continuously during shedding

SLA truth must reflect the fact that service was intentionally reduced.

## Interaction With Capacity Recovery

If capacity recovery remains active:

- reactivation should usually be staged, not full
- restored items should enter only as the system proves service stability
- failed reactivation should feed back into recovery posture

The system should not treat reactivation as proof that recovery is complete.

## Interaction With Load Shedding

Reactivation must preserve the historical fact that the item was shed.

That means:

- risk labels remain in history
- reactivation does not erase shedding duration
- future retrospectives can still see the original reduction decision

This preserves strategic honesty about overload tradeoffs.

## Success Criteria

Reactivation should be considered successful only if:

- active queue health remains stable
- reintroduced work receives meaningful progress
- critical work does not regress
- stale or obsolete items are filtered rather than blindly reopened
- restored backlog declines in a controlled way

Success means backlog recovery without renewing overload.

## Failure Signals

Reactivation should be slowed, paused, or reversed if:

- breach rates rise again in protected work
- reactivated items dominate queue attention without real progress
- stale reactivated items create repeated reassessment churn
- authority bottlenecks reappear
- operators lose clarity about current vs historical risk

Failure to reactivate well is a portfolio planning signal, not just a queue problem.

## Required Artifacts

Each reactivation cycle must record:

- reactivation mode
- set of candidate shed items
- filter decisions
- refresh actions
- reactivated item count
- reactivation rate limits used
- observed impact on active queue health
- backlog remaining after the cycle

These records should feed doctrine load learning and future shedding policy.

## Observability Signals

The reactivation system should emit at least:

- number of items reactivated
- number retired or merged instead of reactivated
- percentage of reactivated items needing refresh
- breach rate among reactivated items
- effect on overall queue health
- time spent in shed posture before reactivation

These signals should remain visible across the full reactivation period.

## Anti-Patterns

Avoid these failures:

- dumping all shed work back into the queue at once
- reopening stale items without refresh
- erasing the fact that an item was previously shed
- measuring reactivation success only by reopened count
- reactivating low-value work before current critical work is stable
- treating retirement of obsolete shed work as failure

## Adoption Sequence

Recommended rollout:

1. add inventory and filter rules for shed backlog
2. require explicit reactivation outcomes per item
3. introduce staged reactivation with rate limits
4. connect reactivation impact to queue health and recovery posture

## Open Questions

Later refinement may be needed for:

- whether different doctrine areas need different reactivation rate limits
- when old shed work should auto-retire instead of asking for review
- how reactivation should interact with wave boundaries
- whether repeated reactivate-and-re-shed patterns should trigger doctrine change review

## Summary

Intentional shedding only works if the platform also has an honest and controlled way to bring work back.

This spec defines that return path through reactivation modes, refresh and filter rules, rate limits, historical markers, and queue-health checks so shed backlog can re-enter safely without recreating the original overload or losing its history.
