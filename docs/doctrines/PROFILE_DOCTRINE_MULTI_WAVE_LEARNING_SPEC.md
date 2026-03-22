# Profile Doctrine Multi Wave Learning Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine post wave retrospective
- workflow profile observability
- profile doctrine stability and freeze

What is still missing is the way learning accumulates across multiple waves instead of staying trapped in one retrospective at a time.

The platform still needs clear answers to these questions:

- how do we compare doctrine performance across waves?
- when does a recurring pattern become a strategic doctrine signal?
- how should multi-wave evidence influence future freeze, launch, and change decisions?

This spec defines that multi-wave learning layer.

## Executive Summary

One wave can teach us something.
Several waves can teach us whether that lesson is real.

For `morphOS`, the correct posture is:

- accumulate doctrine evidence across waves
- compare recurring patterns instead of overreacting to one cycle
- identify durable signals for doctrine change, freeze tuning, or simulation investment
- keep local anomalies distinct from platform-wide learning

The goal is doctrine that improves from repeated evidence, not just the loudest recent wave.

## Core Design Goals

- turn multiple wave retrospectives into durable learning
- distinguish recurring signals from one-off turbulence
- improve doctrine change quality with longitudinal evidence
- support smarter freeze and launch behavior over time
- preserve visibility into both platform-wide and local learning patterns

## Multi Wave Learning Principle

A single wave is a data point.
A doctrine trend should usually require more than one data point.

That means:

- repeated patterns should matter more than isolated incidents
- doctrine changes should gain confidence when multiple waves agree
- freeze and launch rules should be tuned from cross-wave evidence, not just post-wave emotion

## What This Spec Covers

The first useful multi-wave model should cover:

- aggregation of retrospective findings
- recurring override and conflict patterns across waves
- recurring freeze and stop-signal patterns
- doctrine learning signals by workflow class and workspace

This is enough to move from reactive iteration to strategic improvement.

## Canonical Multi Wave Objects

`morphOS` should support at least:

- `MultiWaveDoctrineDataset`
- `DoctrineTrendSignal`
- `DoctrineTrendAssessment`
- `MultiWaveLearningDecision`
- `DoctrineLearningBacklog`

Suggested meanings:

- `MultiWaveDoctrineDataset`
  - accumulated retrospective and observability evidence across waves
- `DoctrineTrendSignal`
  - repeated doctrine-relevant pattern spanning multiple waves
- `DoctrineTrendAssessment`
  - structured evaluation of whether the pattern is meaningful
- `MultiWaveLearningDecision`
  - what action to take based on the trend
- `DoctrineLearningBacklog`
  - durable backlog of unresolved multi-wave lessons

## What Counts As A Multi Wave Signal

Useful multi-wave signals include:

- same profile override pattern appearing across multiple waves
- same doctrine conflict recurring even after local fixes
- repeated stop-the-wave signals of the same category
- repeated overconstraint or friction findings for one workflow class
- repeated successful outcomes after a particular doctrine adjustment

A real doctrine trend should survive more than one cycle.

## Aggregation Dimensions

Multi-wave learning should support aggregation by:

- workflow template
- workflow pack
- workspace
- execution mode
- governance scope
- profile version
- wave identifier

This makes it possible to distinguish:

- platform-wide doctrine gaps
- local workspace quirks
- mode-specific tensions

## Trend Categories

The first useful trend categories should include:

- `recurring_friction`
- `recurring_gap`
- `recurring_overconstraint`
- `freeze_instability_pattern`
- `successful_adjustment_pattern`

Examples:

- the same policy profile causes recurring review bottlenecks
- the same acceptance gap appears every wave for one workflow class
- a new freeze rule consistently reduces wave churn

## Evidence Thresholds

Multi-wave learning should use thresholds before calling something a strategic signal.

The first useful thresholds should consider:

- number of waves affected
- consistency of the pattern
- severity of the impact
- scope of affected workflows or workspaces

This keeps the system from turning noise into doctrine.

## Strategic Decisions

The first useful multi-wave decisions should include:

- `raise_change_priority`
- `require_simulation_before_next_wave`
- `update_freeze_rule`
- `update_launch_monitoring_rule`
- `no_action_yet`

This keeps longitudinal learning concrete.

## Relationship To Retrospectives

Retrospectives answer:

- what did this wave teach us?

Multi-wave learning answers:

- what has the last several waves taught us together?

This keeps short-cycle learning and long-cycle learning distinct but connected.

## Relationship To Change Management

Multi-wave evidence should strongly influence change priority.

Examples:

- a gap seen in one wave may stay low priority
- the same gap seen in three waves may justify urgent doctrine change

This helps allocate attention toward the most persistent problems.

## Relationship To Freeze And Launch

Multi-wave learning should improve:

- freeze criteria
- stop-the-wave thresholds
- monitoring plans
- exception posture during waves

This lets the platform become better at operating each new wave.

## Relationship To Recommendations

Recommendations should become more credible when multi-wave evidence supports them.

Examples:

- a low-confidence recommendation in one wave may become high-confidence after repeated confirmation
- noisy recommendations can be downgraded when later waves do not support them

This helps improve recommendation quality over time.

## Operator Surface Requirements

Operator surfaces should be able to show:

- top recurring doctrine issues across waves
- trend direction by workflow class
- which findings are getting better or worse
- what multi-wave signals have already turned into doctrine changes

This makes longitudinal learning visible instead of buried in old documents.

## Required Events And Artifacts

The first useful multi-wave model should emit at least:

- `profile_doctrine_multi_wave.dataset_updated`
- `profile_doctrine_multi_wave.trend_detected`
- `profile_doctrine_multi_wave.trend_assessed`
- `profile_doctrine_multi_wave.decision_recorded`

Useful artifacts include:

- `multi_wave_doctrine_dataset.json`
- `doctrine_trend_assessment.json`
- `multi_wave_learning_decisions.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- aggregation of retrospective findings across named waves
- recurring override, conflict, and stop-signal pattern detection
- operator-visible trend summary
- backlog entries for cross-wave doctrine issues

That is enough to give the doctrine memory across waves before building richer forecasting or automated prioritization.

## Relationship To Other Specs

This spec depends on:

- `PROFILE_DOCTRINE_POST_WAVE_RETROSPECTIVE_SPEC.md`
- `WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md`
- `PROFILE_DOCTRINE_STABILITY_AND_FREEZE_SPEC.md`
- `PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`

This spec should guide:

- multi-wave doctrine reviews
- longer-horizon prioritization
- freeze and launch rule tuning
- strategic learning across release cycles
