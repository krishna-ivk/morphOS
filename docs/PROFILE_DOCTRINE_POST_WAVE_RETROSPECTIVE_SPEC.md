# Profile Doctrine Post Wave Retrospective Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine wave launch
- workflow profile observability
- workflow profile change management

What is still missing is the structured learning loop after a wave completes.

The platform still needs clear answers to these questions:

- what evidence should be reviewed after a doctrine wave?
- which signals matter most when judging whether the doctrine held up?
- how do retrospective findings become change requests, simulations, or future freeze criteria?

This spec defines that retrospective layer.

## Executive Summary

A wave should not end with only “it shipped” or “it hurt.”

For `morphOS`, the correct posture is:

- review doctrine performance after the wave with structured evidence
- distinguish transient wave noise from real doctrine gaps
- convert findings into the right next step:
  - change request
  - simulation request
  - freeze-criteria update
  - no action

The goal is to make each wave improve the doctrine without overreacting to every rough edge.

## Core Design Goals

- create a repeatable post-wave review process
- turn observability and incident signals into actionable learning
- avoid both complacency and overcorrection
- preserve traceability from wave evidence to doctrinal change or non-change
- improve future freeze, launch, and recommendation quality

## Retrospective Principle

The purpose of a retrospective is not to relitigate every decision.

It is to answer:

- did the doctrine perform as intended?
- where did it create friction?
- where did it fail to contain risk?
- what should we carry forward into the next wave?

## What This Spec Covers

The first useful retrospective model should cover:

- wave-level doctrine performance review
- review of exceptions, conflicts, and stop signals
- interpretation of observability trends
- conversion of findings into follow-up actions

This is enough to close the learning loop after a wave.

## Canonical Retrospective Objects

`morphOS` should support at least:

- `ProfileDoctrineRetrospectiveRequest`
- `WaveDoctrineRetrospectivePacket`
- `RetrospectiveFinding`
- `RetrospectiveDecision`
- `RetrospectiveFollowup`

Suggested meanings:

- `ProfileDoctrineRetrospectiveRequest`
  - request to run a post-wave doctrine review
- `WaveDoctrineRetrospectivePacket`
  - the evidence bundle for the completed wave
- `RetrospectiveFinding`
  - a doctrine-relevant conclusion from the review
- `RetrospectiveDecision`
  - the chosen next action for that finding
- `RetrospectiveFollowup`
  - a concrete resulting task such as simulation, change request, or freeze update

## Required Retrospective Inputs

The first useful retrospective packet should include:

- wave doctrine lock package
- override summary
- doctrine conflict summary
- stop-signal incidents
- active-run pause and termination summary
- recommendation backlog created during the wave
- reopen requests and outcomes

This gives the review enough evidence to judge doctrine performance honestly.

## Finding Categories

The first useful retrospective finding categories should include:

- `doctrine_held`
- `doctrine_friction`
- `doctrine_gap`
- `doctrine_overconstraint`
- `doctrine_instability_signal`

Examples:

- a doctrine held with only expected low-rate exceptions
- a doctrine created friction but not enough to justify change
- a doctrine gap caused repeated overrides or stop signals
- a doctrine overconstrained otherwise healthy workflows
- a doctrine showed instability under real wave pressure

## What Counts As Meaningful Evidence

Retrospectives should weigh evidence such as:

- override concentration
- unresolved and review-required trends
- active-run intervention rates
- conflict escalation patterns
- stop-the-wave events
- recommendation quality and acceptance signals

Single anecdotes may matter, but they should not dominate without corroboration.

## Decision Outcomes

The first useful retrospective decisions should include:

- `no_change`
- `queue_simulation`
- `create_change_request`
- `update_freeze_criteria`
- `tighten_exception_policy`
- `relax_overconstraint`

This keeps the output actionable instead of purely narrative.

## No-Change Is A Valid Result

Not every wave should cause doctrine edits.

Sometimes the right result is:

- doctrine performed acceptably
- friction was expected or temporary
- evidence is insufficient for a change

This protects the system from churn driven by post-wave anxiety.

## Simulation Followups

Simulation is appropriate when:

- evidence suggests a better profile may exist
- the wave exposed friction but not enough proof for immediate doctrine change
- a repeated override pattern looks promising but unproven

This gives the system a safe next step before rewriting doctrine.

## Change Request Followups

A retrospective should recommend doctrine change when:

- repeated wave evidence shows the current profile is wrong or incomplete
- stop signals or severe conflict patterns indicate genuine doctrine failure
- repeated local exceptions point to a platform-wide gap

This keeps major doctrine evolution evidence-backed.

## Freeze-Criteria Followups

Some waves should teach the platform how to freeze better next time.

Examples:

- freeze happened too early and hid serious doctrine churn
- freeze happened too late and caused avoidable uncertainty
- override or conflict thresholds were too loose or too strict

These learnings should update the freeze model, not just profile content.

## Relationship To Recommendations

Recommendations generated during the wave should be reviewed in hindsight.

Questions include:

- which recommendations were accurate?
- which were noisy or low-value?
- which should become simulations or change requests?

This helps improve recommendation quality over time.

## Relationship To Active Runs

Active-run incidents during the wave are key retrospective evidence.

Useful questions include:

- did doctrine contribute to pauses or terminations?
- did doctrine prevent worse outcomes?
- were run interventions proportional and understandable?

This helps separate operational turbulence from doctrinal weakness.

## Operator Surface Requirements

Operator surfaces should be able to show:

- completed-wave doctrine packet
- key findings and evidence
- chosen follow-up decisions
- what will change before the next wave

This makes retrospective conclusions visible and actionable.

## Required Events And Artifacts

The first useful retrospective model should emit at least:

- `profile_doctrine_retrospective.requested`
- `profile_doctrine_retrospective.completed`
- `profile_doctrine_retrospective.finding_recorded`
- `profile_doctrine_retrospective.followup_created`

Useful artifacts include:

- `wave_doctrine_retrospective_packet.json`
- `retrospective_findings.md`
- `retrospective_decisions.json`
- `retrospective_followups.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- one retrospective packet per completed wave
- findings across overrides, conflicts, stop signals, and reopen requests
- explicit follow-up decisions into simulation, change request, or no-change
- operator-visible retrospective summary

That is enough to make wave learning systematic before building richer historical comparison across multiple waves.

## Relationship To Other Specs

This spec depends on:

- `PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md`
- `WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md`
- `ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md`

This spec should guide:

- post-wave review rituals
- conversion of wave evidence into doctrine updates
- improvement of freeze and launch criteria
- future multi-wave learning systems
