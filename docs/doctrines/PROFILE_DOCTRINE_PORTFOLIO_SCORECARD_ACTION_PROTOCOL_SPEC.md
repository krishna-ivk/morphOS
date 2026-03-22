# Profile Doctrine Portfolio Scorecard Action Protocol Spec

## Purpose

This spec defines what concrete portfolio actions should happen once a doctrine portfolio scorecard outcome is known and its decision-binding role has been determined.

The previous specs establish:

- how the scorecard is calibrated
- how it is governed and published
- how it is reconciled
- how it binds into decisions

This document answers the next operational question:

what do operators and the platform actually do after a scorecard outcome becomes decision-relevant?

## Core Principle

A scorecard outcome is useful only if it produces a predictable operational response.

The platform should not stop at saying:

- the scorecard is weak
- the scorecard is constrained
- the scorecard triggered review

Instead, those outcomes must map to a bounded action protocol that tells the system:

- what to review
- what to narrow
- what to pause
- what to escalate
- what to monitor
- what to revisit later

## Goals

The action protocol exists to ensure:

- scorecard-driven decisions are operationally consistent
- similar doctrine conditions lead to similar responses
- action stays proportional to the posture
- scorecard outcomes do not create hidden or improvised governance
- operators know the next expected move
- audit and retrospective work can compare intended action vs actual response

## Non-Goals

This spec does not define:

- how the scorecard is computed
- how binding modes are chosen
- workflow-level runtime actions
- code-level remediation

This is a portfolio action protocol, not a runtime or implementation playbook.

## Action Inputs

The action protocol may use:

- reconciled scorecard posture
- scorecard binding outcome
- scorecard freshness and confidence
- active caveats
- trend direction
- intervention posture
- failsafe or degraded-governance posture
- open exceptions
- linked decision class

Actions must be based on the reconciled current posture, not an outdated publication snapshot.

## Action Families

Every scorecard-driven response must fall into one or more of these action families:

- `observe`
- `review`
- `constrain`
- `escalate`
- `pause`
- `reassess`
- `remediate`
- `record`

These families may be combined, but the system should avoid inventing ad hoc action types outside them.

## `observe`

Observation actions are light-touch responses used when the scorecard posture is not strong enough to justify deeper operational changes.

Typical observation actions:

- mark the decision as scorecard-aware
- place the doctrine area on a watchlist
- increase review cadence visibility
- attach caveats to planning or launch summaries

Use `observe` when the scorecard is:

- informational
- advisory
- weak but not worsening
- still within normal tolerance

## `review`

Review actions increase scrutiny without yet changing operating scope.

Typical review actions:

- require an additional cross-area review
- require human confirmation before a forward-looking claim
- add evidence checks before the decision completes
- route the decision through a higher review queue

Use `review` when the scorecard:

- triggers `review_biasing`
- is stale enough to weaken confidence
- is under dispute
- shows ambiguous or unstable trend

## `constrain`

Constraint actions narrow the allowed move instead of blocking it outright.

Typical constraint actions:

- reduce wave size
- narrow doctrine claims
- limit reentry scope
- require a smaller pilot before expansion
- prohibit broader publication of maturity claims

Use `constrain` when the scorecard:

- binds as `constraint`
- is healthy enough to proceed only with reduced scope
- is improving but not yet strong enough for broad claims

## `escalate`

Escalation actions raise the issue into a higher authority or broader governance lane.

Typical escalation actions:

- route to portfolio review
- require workspace-admin attention
- require super-admin review for systemic claims
- trigger intervention review intake

Use `escalate` when the scorecard:

- blocks a higher-order decision
- shows systemic weakness
- conflicts with a requested forward move
- is repeatedly overridden

## `pause`

Pause actions temporarily stop the affected portfolio decision path until the posture improves or an authority resolves the issue.

Typical pause actions:

- hold wave launch recommendation
- freeze expansion approval
- block intervention exit
- defer maturity advancement review

Use `pause` when the scorecard:

- acts as `gate_input` and fails sufficiency
- is materially stale for the decision window
- is contradicted by unresolved disputes or major caveats

## `reassess`

Reassessment actions explicitly require a near-term re-evaluation.

Typical reassessment actions:

- refresh the scorecard
- request a reconciliation rerun
- reopen the supporting evidence set
- schedule a short-horizon follow-up review

Use `reassess` when the issue is:

- uncertainty-driven
- freshness-driven
- caused by missing evidence rather than clear weakness

## `remediate`

Remediation actions target the doctrine weakness itself rather than only its immediate decision impact.

Typical remediation actions:

- open change-management intake
- trigger calibration review
- require simulation before future claims
- require broader evidence collection
- start a doctrine recovery plan

Use `remediate` when repeated scorecard outcomes show:

- structural weakness
- chronic overrides
- repeated low-confidence publication
- recurring conflict between doctrine and actual usage

## `record`

Recording actions are mandatory for every scorecard-driven response.

Typical record actions:

- persist the action protocol outcome
- store the triggered action families
- link the decision, scorecard snapshot, and exception references
- capture follow-up deadlines

No scorecard-driven decision is complete without a durable record of what action protocol was applied.

## Protocol Levels

The action protocol should support five standardized levels:

- `L0_notice`
- `L1_review`
- `L2_constraint`
- `L3_gate_pause`
- `L4_systemic_escalation`

### `L0_notice`

Expected actions:

- `observe`
- `record`

Used when:

- scorecard posture is advisory only
- no direct restriction is needed

### `L1_review`

Expected actions:

- `review`
- `record`
- optional `reassess`

Used when:

- scorecard weakness or ambiguity should increase scrutiny
- broader action would be disproportionate

### `L2_constraint`

Expected actions:

- `constrain`
- `review`
- `record`

Used when:

- forward progress is still acceptable
- but scope or claims must be narrowed

### `L3_gate_pause`

Expected actions:

- `pause`
- `escalate` or `reassess`
- `record`

Used when:

- scorecard posture is insufficient for the decision class
- a required gate input fails

### `L4_systemic_escalation`

Expected actions:

- `escalate`
- `remediate`
- `record`
- usually `pause`

Used when:

- the problem looks portfolio-wide
- repeated issues show doctrine instability
- intervention posture may need to change

## Mapping From Binding Outcomes

Recommended default mapping:

- `scorecard_not_material` -> `L0_notice`
- `scorecard_supported` -> `L0_notice`
- `scorecard_supported_with_caveats` -> `L1_review`
- `scorecard_triggered_higher_review` -> `L1_review`
- `scorecard_constrained_scope` -> `L2_constraint`
- `scorecard_blocked_without_exception` -> `L3_gate_pause`
- `scorecard_overridden_by_exception` -> `L2_constraint` or `L4_systemic_escalation`

If exception use becomes frequent, the platform should prefer `L4_systemic_escalation` over repeatedly staying at `L2_constraint`.

## Time Horizon

Every action protocol must declare its time horizon:

- `immediate`
- `current_cycle`
- `next_review_window`
- `multi_wave_followup`

This prevents vague follow-up language such as "watch this later" without an actual review expectation.

## Scope

Every action protocol must declare scope:

- single doctrine area
- related doctrine cluster
- current wave only
- current and next wave
- whole portfolio

The scorecard may justify strong action in a narrow scope without yet justifying whole-portfolio claims.

## Interaction With Exceptions

If a scorecard-based decision is overridden through exception:

- the action protocol must still execute
- the exception does not erase observation, review, or remediation duties
- the protocol must record that the final action was modified by exception

An exception may change whether work proceeds, but it must not erase the evidence that the underlying doctrine posture was weak.

## Interaction With Trend

Trend should modify action intensity:

- improving trend may shorten pause duration or favor `reassess`
- declining trend may strengthen `constraint` into `pause`
- unstable trend may increase review cadence even if current posture looks acceptable

Trend modifies the protocol. It does not replace the current scorecard state.

## Interaction With Portfolio Intervention

If the portfolio is already under intervention:

- `L1_review` may be treated operationally like `L2_constraint`
- `L2_constraint` may require explicit intervention-owner review
- `L3_gate_pause` may escalate directly into intervention governance

This ensures the same scorecard signal is interpreted more carefully under already elevated doctrine risk.

## Required Artifacts

Each action protocol invocation must record:

- decision reference
- scorecard snapshot reference
- binding outcome
- protocol level
- triggered action families
- scope
- time horizon
- authority owner
- due follow-up dates
- exception linkage if any

These records must be durable enough for audit, wave retrospective, and doctrine change analysis.

## Operator Guidance

Operators should be able to interpret the levels simply:

- `L0_notice`: be aware
- `L1_review`: inspect more carefully
- `L2_constraint`: proceed narrowly
- `L3_gate_pause`: stop and resolve
- `L4_systemic_escalation`: treat as a broader doctrine problem

This interpretation should remain stable across dashboards, reviews, and governance workflows.

## Anti-Patterns

Avoid these failures:

- using the scorecard to trigger vague action without a protocol level
- escalating everything that is merely cautionary
- treating a pause as if it were remediation
- using exceptions to skip recording the underlying weakness
- failing to distinguish local doctrine weakness from systemic portfolio instability
- letting action scope silently expand beyond what the scorecard justified

## Adoption Sequence

Recommended rollout:

1. map scorecard outcomes to `L0_notice`, `L1_review`, and `L2_constraint`
2. introduce `L3_gate_pause` for maturity, expansion, and intervention-exit decisions
3. introduce `L4_systemic_escalation` only after intervention governance is stable
4. refine mappings using override frequency, drift signals, and retrospective findings

## Open Questions

Later refinement may be needed for:

- whether action protocol levels should differ by doctrine area
- how automated scheduling should create reassessment tasks
- whether some action families should automatically emit operator inbox items
- how action protocol outcomes should influence future scorecard recommendations

## Summary

The doctrine portfolio scorecard becomes operationally meaningful only when its outcomes produce predictable actions.

This spec defines that action protocol through standardized action families, protocol levels, mapping defaults, scope and time-horizon rules, and durable recording requirements. The result is a scorecard system that not only informs decisions, but also produces clear, reviewable next moves.
