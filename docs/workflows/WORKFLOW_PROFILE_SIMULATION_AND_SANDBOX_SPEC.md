# Workflow Profile Simulation And Sandbox Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile recommendation
- workflow profile change management
- digital twin validation

What is still missing is the safe test lane for trying profile candidates before they affect real workflow selection.

The platform still needs clear answers to these questions:

- how do we test a candidate profile or override without making it active?
- how do we compare a recommended profile against the current one safely?
- what kind of sandbox or simulation evidence is required before rollout?

This spec defines that simulation layer.

## Executive Summary

Profile doctrine should be testable before it becomes active.

For `morphOS`, the correct posture is:

- run candidate profiles in a sandbox or simulated selection lane
- compare candidate outcomes to the current active profile behavior
- capture evidence before activating a new profile or accepting a risky override pattern
- keep simulation separate from live authority and real workflow mutation

The goal is to validate profile changes safely rather than trusting theory alone.

## Core Design Goals

- provide a safe environment for testing profile candidates
- let operators compare candidate and current profile behavior
- reduce rollout risk for new profiles, recommendations, and override patterns
- preserve simulation evidence for change management and review
- keep simulation advisory unless separately approved for activation

## Simulation Principle

A profile candidate should be able to prove itself before it changes real workflow resolution.

That means:

- simulate profile resolution with the candidate profile
- simulate downstream workflow posture where useful
- compare outcomes against the current active baseline

Simulation should help answer:

- would this profile fit better?
- what warnings or blocks would change?
- would it reduce or increase override pressure?

## What This Spec Covers

The first useful simulation model should cover:

- candidate acceptance-profile evaluation
- candidate policy-profile evaluation
- comparison of current versus candidate resolved contracts
- override candidate rehearsal
- recommendation validation

This is enough to de-risk most profile changes.

## Canonical Simulation Objects

`morphOS` should support at least:

- `WorkflowProfileSimulationRequest`
- `WorkflowProfileSimulationScenario`
- `WorkflowProfileSimulationRun`
- `WorkflowProfileComparisonResult`
- `WorkflowProfileSimulationVerdict`

Suggested meanings:

- `WorkflowProfileSimulationRequest`
  - request to test one or more profile candidates
- `WorkflowProfileSimulationScenario`
  - the workflow, mode, workspace, and governance context used for the test
- `WorkflowProfileSimulationRun`
  - execution of the simulated resolution or workflow posture evaluation
- `WorkflowProfileComparisonResult`
  - delta between baseline and candidate behavior
- `WorkflowProfileSimulationVerdict`
  - advisory conclusion about the candidate profile

## Simulation Modes

The first useful simulation modes should include:

- `resolution_only`
- `resolution_plus_posture`
- `sandboxed_run_replay`

Suggested meanings:

- `resolution_only`
  - compare resolved contracts without simulating broader workflow execution
- `resolution_plus_posture`
  - compare resolution plus expected policy and acceptance posture changes
- `sandboxed_run_replay`
  - replay a representative prior run or scenario through the candidate profile in a safe environment

These modes let the platform start small and grow deeper where needed.

## Baseline Versus Candidate Comparison

Every useful simulation should compare at least:

- current active profile set
- candidate profile set
- resolution verdict
- warning and review posture
- override likelihood
- expected governance or approval changes

This keeps simulation comparative, not just descriptive.

## Sandbox Boundaries

Profile simulation should stay inside a sandboxed evaluation lane.

That means:

- no live external side effects
- no activation of the candidate profile by accident
- no mutation of real workflow defaults
- no hidden promotion of a recommendation into doctrine

If broader behavior needs testing, it should use digital twins or other safe replay surfaces.

## Simulation Inputs

The minimum useful inputs should include:

- workflow template
- workflow pack
- execution mode
- workspace and governance context
- baseline resolved profile set
- candidate profile or candidate change
- representative prior run context when available

This makes simulation grounded in realistic conditions.

## Simulation Evidence

Simulation should produce evidence such as:

- resolved-contract differences
- compatibility changes
- policy finding changes
- acceptance target changes
- override pressure changes
- active-run reevaluation implications

This evidence should be retained for review and change management.

## Recommendation Validation

Recommendations should often be validated through simulation before they influence real selection behavior.

Examples:

- a suggested stricter policy profile can be simulated against recent runs
- a candidate acceptance profile can be checked for reduced warning or override frequency
- a proposed workspace-default profile can be tested against representative workflows

This keeps recommendations evidence-backed.

## Override Rehearsal

Override patterns that may become doctrine should be rehearsed through simulation.

Examples:

- a repeated single-run override can be tested as a candidate default
- a recurring mode exception can be evaluated for broader safety

This helps distinguish a real missing rule from a one-off operator preference.

## Relationship To Digital Twins

When profile behavior materially affects external-system actions, simulation should be able to connect to twin-backed validation.

Examples:

- a policy-profile candidate that changes live-action posture can be exercised against a twin
- a promotion-related acceptance profile can be rehearsed against simulated review and approval flows

Twins provide safe behavioral proof when profile simulation needs more than resolution-only comparison.

## Relationship To Change Management

Simulation should feed change management directly.

Good uses include:

- supporting approval of a risky profile change
- reducing uncertainty during staged rollout
- deciding whether a recommendation should become a real change request

Simulation is evidence, not a substitute for governance.

## Simulation Verdicts

The first useful verdicts should include:

- `candidate_improves_fit`
- `candidate_equivalent`
- `candidate_increases_risk`
- `candidate_requires_review`
- `candidate_not_supported`

These verdicts should remain advisory unless a separate governance step acts on them.

## Operator Surface Requirements

Operator surfaces should be able to show:

- baseline versus candidate profile set
- simulated resolution differences
- confidence and verdict
- whether simulation used only resolution or a deeper sandbox replay
- linked recommendation or change request when relevant

This helps people understand what was actually tested.

## Required Events And Artifacts

The first useful simulation model should emit at least:

- `workflow_profile_simulation.requested`
- `workflow_profile_simulation.completed`
- `workflow_profile_simulation.comparison_generated`
- `workflow_profile_simulation.verdict_emitted`

Useful artifacts include:

- `workflow_profile_simulation_request.json`
- `workflow_profile_simulation_run.json`
- `workflow_profile_comparison_result.json`
- `workflow_profile_simulation_verdict.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- resolution-only simulation for candidate profiles
- baseline versus candidate comparison output
- recommendation validation against recent representative runs
- operator-visible simulation summaries

That is enough to make profile experimentation safer before building deeper replay and twin-coupled simulation lanes.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md`
- `DIGITAL_TWIN_VALIDATION_SPEC.md`

This spec should guide:

- sandbox tooling for profile experiments
- evidence gathering before activation
- recommendation validation workflows
- future replay and twin-integrated profile testing
