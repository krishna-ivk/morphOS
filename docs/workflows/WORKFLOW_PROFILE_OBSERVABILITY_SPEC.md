# Workflow Profile Observability Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile resolution
- workflow profile override governance
- workflow profile change management

What is still missing is the observability model for how profiles behave in practice.

The platform still needs clear answers to these questions:

- which profiles are actually being selected?
- where are incompatibilities, overrides, and review-required outcomes clustering?
- is the profile doctrine matching real workflow behavior?

This spec defines that observability layer.

## Executive Summary

Profiles should not only be governable.
They should also be measurable.

For `morphOS`, the correct posture is:

- observe how profiles are selected and used
- track where profile resolution fails or requires review
- measure override frequency and repeated exception patterns
- surface rollout and deprecation impact over time

The goal is to make profile doctrine evidence-backed instead of purely editorial.

## Core Design Goals

- make workflow profile behavior visible to operators and platform owners
- detect mismatch between designed profiles and actual usage
- identify where overrides or incompatibilities signal missing doctrine
- support safe rollout and deprecation decisions with real evidence
- connect profile behavior to workflow outcomes without blurring distinct concerns

## Observability Principle

If profiles shape runtime behavior, they should leave a measurable trail.

That trail should show:

- what was selected
- why it was selected
- what was overridden
- where it failed to fit
- what outcomes followed

Observability is how the platform learns whether its profile system is working.

## What This Spec Covers

The first useful observability model should cover:

- profile selection frequency
- resolution outcomes and warning rates
- incompatibility and review-required patterns
- override rates and renewal patterns
- staged rollout and deprecation impact

This is enough to guide profile improvement.

## Canonical Observability Objects

`morphOS` should support at least:

- `WorkflowProfileSelectionEvent`
- `WorkflowProfileOutcomeRecord`
- `WorkflowProfileOverrideMetric`
- `WorkflowProfileRolloutMetric`
- `WorkflowProfileObservabilitySnapshot`

Suggested meanings:

- `WorkflowProfileSelectionEvent`
  - a recorded profile resolution and selection event
- `WorkflowProfileOutcomeRecord`
  - downstream run outcome tied back to the selected profiles
- `WorkflowProfileOverrideMetric`
  - summarized override frequency and posture data
- `WorkflowProfileRolloutMetric`
  - rollout or deprecation impact measurements
- `WorkflowProfileObservabilitySnapshot`
  - aggregated view over a time window

## Core Questions To Answer

The first useful dashboards or reports should answer:

- which acceptance profiles are most common?
- which policy profiles generate the most review-required outcomes?
- which workflows frequently need overrides?
- which profile combinations correlate with blocked or restarted runs?
- are staged profile rollouts reducing or increasing intervention load?

These questions help convert profile governance into operational feedback.

## Selection Metrics

Useful selection metrics include:

- profile selection count by workflow template
- profile selection count by execution mode
- pack default versus template override usage
- operator-requested versus auto-resolved selection rate
- resolved versus resolved-with-warnings rate

This shows what the platform is really choosing, not just what it claims to support.

## Resolution Health Metrics

Useful resolution-health metrics include:

- `review_required` rate
- `unresolved` rate
- warning frequency by workflow class
- incompatibility reason frequency
- average candidate pruning count during resolution

These metrics show where profile resolution is smooth or brittle.

## Override Metrics

Useful override metrics include:

- override request rate by workflow class
- approval rate versus rejection rate
- override scope distribution
- override renewal frequency
- repeated override patterns by profile pair

High override concentration is often a sign that base profile doctrine needs revision.

## Change Management Metrics

Useful change-management metrics include:

- profile change request volume
- draft-to-active lead time
- staged rollout success rate
- deprecation adoption rate
- repeated rollback or hesitation patterns

This helps measure whether the profile system can evolve cleanly.

## Outcome Linkage

Observability should connect profile choices to workflow outcomes without claiming false causality.

Useful linked outcomes include:

- promotion-readiness rate
- review-block rate
- restart rate
- termination rate
- active-run reevaluation frequency

The system should present these as correlations and signals unless stronger causal proof exists.

## Rollout And Deprecation Observability

Staged and deprecated profiles should be tracked explicitly.

Useful rollout metrics include:

- new-profile adoption rate
- warning-rate change after rollout
- override-rate change after rollout
- unresolved-rate change after rollout

Useful deprecation metrics include:

- deprecated profile selection count
- deprecated profile override count
- lingering dependency count by workspace

This helps determine when a deprecated profile can actually retire.

## Workspace And Scope Views

Observability should support views by:

- workflow template
- workflow pack
- workspace
- execution mode
- governance scope
- profile version

This makes it easier to distinguish local anomalies from platform-wide patterns.

## Operator Surface Requirements

Operator surfaces should be able to show:

- currently selected profile mix
- top incompatibility reasons
- override hotspots
- staged rollout health
- deprecated profile usage

This helps platform owners see whether the doctrine is being followed or fought.

## Signals For Productizing Exceptions

Repeated exceptions should become visible as candidate doctrine updates.

The first useful signals include:

- same override repeated across multiple runs
- same resolution warning pattern recurring by workflow template
- same workspace repeatedly requesting a non-default profile
- staged rollout consistently improving outcome posture

These signals should feed profile change management.

## Required Events And Artifacts

The first useful observability model should emit at least:

- `workflow_profile.selected`
- `workflow_profile.resolution_warning`
- `workflow_profile.override_applied`
- `workflow_profile.override_expired`
- `workflow_profile.rollout_stage_changed`
- `workflow_profile.deprecated_usage_observed`

Useful artifacts include:

- `workflow_profile_selection_event.json`
- `workflow_profile_outcome_record.json`
- `workflow_profile_observability_snapshot.json`

## First Implementation Slice

The first implementation slice should stay intentionally narrow.

Start with:

- selection and resolution verdict counters
- override request and renewal counters
- rollout-stage adoption counts
- deprecated-profile usage counts
- operator-visible top reasons for review-required and unresolved outcomes

That is enough to make the profile system inspectable before building richer comparative analytics and historical trend tooling.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md`
- `TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md`

This spec should guide:

- profile dashboards
- rollout health reporting
- doctrine tuning from real usage
- future exception-mining and profile recommendation tooling
