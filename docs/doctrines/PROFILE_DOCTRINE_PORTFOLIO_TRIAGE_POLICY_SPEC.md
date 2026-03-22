# Profile Doctrine Portfolio Triage Policy Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio baseline
- profile doctrine portfolio SLO and alerting
- profile doctrine portfolio capacity and load

What is still missing is the decision policy for choosing what doctrine work gets handled first when portfolio demand exceeds comfortable stewardship capacity.

The platform still needs clear answers to these questions:

- how should doctrine work be prioritized when many signals compete at once?
- what should be handled immediately, and what can safely wait?
- how do operators avoid inconsistent or purely intuitive triage under load?

This spec defines that portfolio triage-policy layer.

## Executive Summary

Portfolio health, alerts, and load only become operationally useful if they drive clear prioritization decisions.

Triage policy should define how the platform chooses among competing doctrine work under real constraint.

For `morphOS`, the correct posture is:

- triage according to strategic impact, risk, and time sensitivity
- make deferral explicit rather than accidental
- preserve consistency across routine stewardship, elevated watch, and intervention readiness
- document why some doctrine work is prioritized over other work

The goal is to keep doctrine operations disciplined when everything cannot be handled at once.

## Core Design Goals

- define a consistent doctrine-work prioritization policy
- distinguish urgent, important, and safely deferrable work
- connect triage decisions to health, alerts, and capacity posture
- make tradeoffs visible and auditable
- reduce arbitrary operator variance under load

## Triage Principle

When doctrine work demand exceeds comfortable handling capacity, the platform should not rely on intuition alone.

Triage should therefore:

- prioritize by strategic consequence, not noise
- protect planning confidence and risk containment first
- allow lower-impact work to defer deliberately

Triage is not just sorting a queue.
It is deciding how limited doctrine attention should be spent responsibly.

## What This Spec Covers

The first useful triage model should cover:

- doctrine work priority classes
- triage factors
- defer-versus-act rules
- queue ordering under load
- required artifacts and operator visibility

This is enough to make doctrine portfolio work ordering consistent and governable.

## Canonical Triage Objects

`morphOS` should support at least:

- `DoctrineTriagePolicy`
- `DoctrineTriageFactor`
- `DoctrineTriageDecision`
- `DoctrinePriorityClass`
- `DoctrineTriageRecord`

Suggested meanings:

- `DoctrineTriagePolicy`
  - the rule set for prioritizing competing doctrine work
- `DoctrineTriageFactor`
  - one input used to evaluate urgency and importance
- `DoctrineTriageDecision`
  - the official priority or deferral outcome for a work item
- `DoctrinePriorityClass`
  - the assigned action class for a piece of doctrine work
- `DoctrineTriageRecord`
  - durable history of triage outcomes and rationale

## First Useful Priority Classes

The first useful priority classes should include:

- `immediate`
- `next_cycle`
- `planned`
- `defer_with_watch`

Suggested meanings:

- `immediate`
  - should be handled now because delay materially increases risk or weakens active planning confidence
- `next_cycle`
  - should be addressed in the next focused doctrine cycle or wave
- `planned`
  - important but can wait within ordinary stewardship planning
- `defer_with_watch`
  - currently safe to postpone if the item remains visible and monitored

These classes help avoid false binary choices between “urgent” and “ignored.”

## Triage Factors

The first useful triage factors should include:

- strategic dependency
- alert severity
- freshness risk
- backlog age
- clustering
- governance sensitivity
- planning or freeze impact

Suggested meanings:

- `strategic dependency`
  - how much important work relies on this doctrine area
- `alert severity`
  - how urgent the current operational signal is
- `freshness risk`
  - how close the doctrine is to undermining trust claims through aging
- `backlog age`
  - how long the item has already gone without resolution
- `clustering`
  - whether similar issues are concentrating in one family or area
- `governance sensitivity`
  - whether the item affects policy, approval, or organizational risk
- `planning or freeze impact`
  - whether delay degrades active planning confidence

These factors help the queue reflect real consequence instead of simple timestamp order.

## Immediate Class Rules

Use `immediate` when:

- delay threatens current planning or freeze posture
- critical doctrine alerts are active
- capacity overload is causing strategic doctrine work to slip
- the item is part of a concentrated risk cluster that is still worsening

These items should preempt ordinary routine work.

## Next-Cycle Class Rules

Use `next_cycle` when:

- the item is materially important
- delay is acceptable briefly but not for long
- the work belongs in the next deliberate doctrine maintenance or renewal wave

This class is useful for important work that is not yet emergency work.

## Planned Class Rules

Use `planned` when:

- the item is valuable but stable enough to schedule normally
- no active strategic pressure requires immediate acceleration
- the doctrine area is not meaningfully degrading current planning confidence

This keeps the queue from treating all useful work as urgent.

## Defer-With-Watch Rules

Use `defer_with_watch` when:

- the item is safe to postpone for now
- the consequences of waiting are limited and visible
- a watchpoint or reminder is sufficient to prevent silent neglect

Deferral should never mean disappearance.

## Relationship To Capacity And Load

Triage policy should activate most strongly when the portfolio is busy, strained, or overloaded.

Examples:

- `within_capacity` may allow broader planned work
- `strained` should tighten the bar for immediate and next-cycle work
- `overloaded` should favor strategic containment and explicitly defer lower-value maintenance

This helps the queue adapt to real operating conditions.

## Relationship To SLO And Alerting

Alerts should influence triage, but not replace it.

Examples:

- repeated `warning` items in one area may move next-cycle work upward
- `high` or `critical` alerts may move work into the immediate class
- quiet but aging backlog may still deserve attention even without a current alert

This prevents the portfolio from only chasing the loudest signal.

## Relationship To Baseline And Intervention

Triage should bridge ordinary stewardship and strategic response.

Examples:

- in baseline posture, triage keeps routine work healthy
- in elevated watch, triage should protect the portfolio from sliding into intervention
- during intervention review, triage should make clear which items are driving strategic concern

This makes prioritization useful across the full lifecycle.

## Relationship To Governance

Governance-sensitive work should be triaged with attention to consequence, not ceremony.

Suggested posture:

- governance-sensitive work may rise in priority when delay risks compliance or approval integrity
- governance routing overhead should not crowd out all substantive doctrine work
- triage decisions affecting strategic governance posture should be visible and auditable

## Operator Surface Requirements

Operator surfaces should be able to show:

- current triage queue
- assigned priority classes
- rationale for high-priority items
- explicitly deferred items and why they were deferred
- whether triage is stable or being distorted by overload

This helps operators trust the ordering rather than guessing at it.

## Required Artifacts

The first useful triage artifacts should include:

- `doctrine_triage_queue.md`
- `doctrine_triage_decisions.json`
- `doctrine_triage_summary.md`
- `deferred_doctrine_watchpoints.json`

Suggested contents:

- `doctrine_triage_queue.md`
  - current ordered doctrine work list by priority class
- `doctrine_triage_decisions.json`
  - machine-readable record of triage outcomes and rationale
- `doctrine_triage_summary.md`
  - high-level explanation of current doctrine prioritization posture
- `deferred_doctrine_watchpoints.json`
  - deferred items that remain under active observation

## First Useful Outcomes

The first useful triage outcomes should include:

- `handle_now`
- `schedule_next_cycle`
- `keep_in_normal_plan`
- `defer_with_watch`
- `escalate_to_portfolio_review`

These outcomes connect prioritization to visible action.

## Governance Expectations

Triage policy should support judgment, not automate it away.

Suggested posture:

- ordinary triage can remain within normal portfolio ownership
- strategically important triage choices should be visible to governance
- repeated deferral of the same sensitive items should become auditable

## Non-Goals

This spec does not define:

- a universal numeric priority formula
- staffing or budget decisions outside doctrine work
- replacement of operator judgment with rigid queue automation

It only defines how doctrine work should be prioritized consistently under real portfolio pressure.

## Bottom Line

`morphOS` should treat doctrine triage as a policy, not a mood.

When many doctrine signals compete at once, the platform should know what must happen now, what belongs in the next cycle, what can stay planned, and what may safely defer with watchpoints.
