# Profile Doctrine Maturity Model Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine multi wave learning
- profile doctrine stability and freeze
- workflow profile observability

What is still missing is a simple maturity ladder for the doctrine itself.

The platform still needs clear answers to these questions:

- is this profile area still exploratory or already wave-ready?
- what evidence moves doctrine from one maturity level to the next?
- when should operators treat a profile as stable rather than experimental?

This spec defines that maturity model.

## Executive Summary

Not all doctrine is equally mature.

For `morphOS`, the correct posture is:

- classify profile doctrine by maturity stage
- use evidence, not intuition, to move between stages
- make stage visible to operators, change managers, and release planners

The goal is to distinguish ideas we are still learning from doctrine we can reliably ship against.

## Core Design Goals

- give doctrine a shared maturity vocabulary
- prevent immature profile areas from being mistaken for hardened defaults
- help release and freeze decisions reflect actual evidence quality
- guide where simulation, change management, and observation effort should go next
- support clearer planning across multiple waves

## Maturity Principle

Doctrine matures through use, evidence, and repeated validation.

That means:

- early doctrine should be treated cautiously
- doctrine that survives several waves with low friction should be treated more confidently
- maturity should be earned, not assumed

## What This Spec Covers

The first useful maturity model should cover:

- maturity stages for profile doctrine
- evidence needed to advance or regress maturity
- relationship between maturity and freeze or launch readiness

This is enough to make maturity operational.

## Canonical Maturity Objects

`morphOS` should support at least:

- `ProfileDoctrineMaturityRecord`
- `MaturityAssessment`
- `MaturityStage`
- `MaturityTransition`
- `MaturityRegressionSignal`

Suggested meanings:

- `ProfileDoctrineMaturityRecord`
  - current maturity state of a doctrine area or profile family
- `MaturityAssessment`
  - evidence-backed evaluation of maturity
- `MaturityStage`
  - the current maturity level
- `MaturityTransition`
  - the movement from one stage to another
- `MaturityRegressionSignal`
  - evidence that doctrine should move backward in confidence

## Maturity Stages

The first useful stages should include:

- `exploratory`
- `emerging`
- `wave_ready`
- `multi_wave_stable`
- `institutionalized`

Suggested meanings:

- `exploratory`
  - doctrine is still being formed and should not be treated as highly stable
- `emerging`
  - doctrine has some evidence and shape, but still needs more operational proof
- `wave_ready`
  - doctrine is stable enough for a bounded release or implementation wave
- `multi_wave_stable`
  - doctrine has held across multiple waves with acceptable friction
- `institutionalized`
  - doctrine is a hardened platform norm with strong supporting evidence

## Stage Meanings In Practice

### Exploratory

Typical posture:

- frequent change likely
- simulation and recommendation work are high value
- freeze should be rare

### Emerging

Typical posture:

- candidate for staged rollout
- change management still active
- wave launch possible only with caution

### Wave Ready

Typical posture:

- eligible for freeze and wave launch
- exceptions should still be monitored closely

### Multi Wave Stable

Typical posture:

- multiple waves have validated the doctrine
- change should be less frequent and more evidence-heavy

### Institutionalized

Typical posture:

- doctrine is treated as a strong platform norm
- changes require clear evidence and governance
- freeze and launch planning can assume it as a reliable base

## Advancement Signals

Useful advancement signals include:

- consistent resolved behavior
- low unresolved and override rates
- low doctrine-conflict escalation across relevant waves
- successful staged rollouts
- positive multi-wave trend evidence

Advancement should depend on repeated evidence, not optimism.

## Regression Signals

Doctrine should also be able to move backward.

Useful regression signals include:

- repeated stop-the-wave events
- rising override pressure
- recurring doctrine conflict escalation
- freeze instability across multiple waves
- repeated high-severity profile bugs

Maturity is not permanent if the evidence changes.

## Relationship To Freeze And Launch

Maturity should influence what the platform is willing to do.

Suggested posture:

- `exploratory`
  - not a good freeze baseline
- `emerging`
  - freeze only in narrow contexts
- `wave_ready`
  - acceptable for a bounded wave
- `multi_wave_stable`
  - strong candidate for routine wave usage
- `institutionalized`
  - reliable default foundation for broad release planning

This keeps operational confidence aligned with evidence.

## Relationship To Change Management

Maturity should affect how changes are handled.

Examples:

- exploratory doctrine can change more quickly
- institutionalized doctrine should change more carefully
- emerging doctrine may benefit most from simulation before change

This makes change-management posture proportional to maturity.

## Relationship To Recommendations And Simulation

Less mature doctrine should expect:

- more recommendations
- more simulation
- more experimentation

More mature doctrine should expect:

- fewer changes
- higher bar for recommendations to become changes
- stronger emphasis on regression detection

This keeps effort aligned with maturity needs.

## Relationship To Multi Wave Learning

Multi-wave learning is the strongest source of evidence for later maturity stages.

Examples:

- one solid wave may justify `wave_ready`
- several healthy waves may justify `multi_wave_stable`
- broad repeated success plus low friction may justify `institutionalized`

This makes maturity cumulative rather than rhetorical.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current maturity stage
- recent advancement or regression signals
- why the doctrine is at this stage
- what evidence would move it higher or lower

This makes maturity actionable rather than decorative.

## Required Events And Artifacts

The first useful maturity model should emit at least:

- `profile_doctrine_maturity.assessed`
- `profile_doctrine_maturity.advanced`
- `profile_doctrine_maturity.regressed`

Useful artifacts include:

- `profile_doctrine_maturity_record.json`
- `maturity_assessment.json`
- `maturity_transition.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- maturity record per major doctrine area
- simple stage assignment from wave and observability evidence
- operator-visible stage and recent transition rationale
- regression detection for previously stable doctrine

That is enough to make maturity legible before building richer scoring systems or fine-grained subdomain models.

## Relationship To Other Specs

This spec depends on:

- `PROFILE_DOCTRINE_MULTI_WAVE_LEARNING_SPEC.md`
- `PROFILE_DOCTRINE_STABILITY_AND_FREEZE_SPEC.md`
- `WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md`

This spec should guide:

- doctrine maturity dashboards
- freeze eligibility decisions
- prioritization of simulation and change work
- longer-horizon platform planning
