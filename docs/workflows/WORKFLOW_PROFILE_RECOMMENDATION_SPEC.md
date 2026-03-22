# Workflow Profile Recommendation Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile observability
- workflow profile resolution
- workflow profile change management

What is still missing is the advisory layer that turns usage evidence into profile suggestions.

The platform still needs clear answers to these questions:

- when should the system suggest a different acceptance or policy profile?
- what evidence should support that suggestion?
- how do recommendations stay advisory without bypassing governance?

This spec defines that recommendation layer.

## Executive Summary

The platform should learn from profile behavior, but it should not silently replace governed resolution with implicit optimization.

For `morphOS`, the correct posture is:

- generate profile recommendations from observability signals
- keep recommendations advisory by default
- attach evidence, confidence, and blast-radius context
- route material recommendations into review or change management

The goal is evidence-backed improvement without turning recommendations into hidden policy.

## Core Design Goals

- make profile recommendations explainable and reviewable
- identify when a different profile may better fit a workflow or workspace
- distinguish tactical suggestions from doctrine-level change proposals
- prevent recommendation engines from bypassing compatibility and governance
- convert repeated evidence into structured improvement paths

## Recommendation Principle

Recommendations should help humans and runtimes see potentially better profile choices.

They should not:

- silently override resolved contracts
- invent compatibility
- weaken governance requirements

Recommendation is advisory intelligence, not automatic authority.

## What This Spec Covers

The first useful recommendation model should cover:

- alternative acceptance profile suggestions
- alternative policy profile suggestions
- workspace-specific profile fit suggestions
- profile change candidate suggestions based on repeated patterns

This is enough to improve profile quality without replacing core governance.

## Canonical Recommendation Objects

`morphOS` should support at least:

- `WorkflowProfileRecommendation`
- `RecommendationEvidence`
- `RecommendationAssessment`
- `RecommendationVerdict`
- `RecommendationDisposition`

Suggested meanings:

- `WorkflowProfileRecommendation`
  - a proposed better-fit profile or profile change path
- `RecommendationEvidence`
  - the signals that support the recommendation
- `RecommendationAssessment`
  - compatibility, risk, and governance analysis of the suggestion
- `RecommendationVerdict`
  - whether the suggestion is safe to show, escalate, or ignore
- `RecommendationDisposition`
  - what happened to the recommendation after review

## Recommendation Types

The first useful recommendation types should include:

- `alternative_profile_for_future_runs`
- `alternative_profile_for_workspace`
- `candidate_profile_change`
- `candidate_override_retirement`

Examples:

- suggest a stricter policy profile for a workflow that repeatedly needs review
- suggest a different acceptance profile for a workspace with stable higher evidence maturity
- suggest turning repeated overrides into a real profile update
- suggest retiring an old profile that is rarely selected and frequently overridden

## Recommendation Inputs

Recommendations should use evidence such as:

- selection frequency
- resolution warnings
- override frequency and renewal patterns
- compatibility outcomes
- rollout performance
- workflow outcome correlations

Recommendations should not rely on a single noisy signal.

## Recommendation Confidence

Every recommendation should carry an explicit confidence level.

Suggested levels:

- `low`
- `medium`
- `high`

Confidence should reflect:

- evidence volume
- consistency of the observed pattern
- stability across workspaces or workflow classes
- absence of strong contradictory signals

## Recommendation Boundaries

Recommendations should never:

- bypass hard compatibility failures
- ignore missing policy hooks
- weaken required governance scope silently
- auto-activate a new profile without the appropriate change path

These are hard guardrails, not preferences.

## Tactical Versus Strategic Recommendations

The platform should distinguish:

- tactical recommendation
  - a suggestion about a better profile choice for upcoming runs
- strategic recommendation
  - a suggestion that the profile system itself should change

Examples:

- tactical: this workspace may fit `high_risk_feature` better than `standard_feature`
- strategic: repeated overrides suggest the base policy profile is incomplete and should be revised

This keeps one-off fit suggestions distinct from doctrine changes.

## Runtime Use

At runtime, recommendations may be used to:

- surface better candidate profiles during workflow selection
- warn operators that the current default is showing poor fit
- suggest review when a more suitable compatible profile exists

Recommendations should remain advisory unless another governed step adopts them.

## Operator Use

Operator surfaces should be able to show:

- recommended profile
- confidence level
- evidence summary
- whether it is tactical or strategic
- whether accepting it would require change management or approval

This helps operators make informed choices without guessing why a recommendation exists.

## Relationship To Resolution

Recommendations should feed into resolution as optional guidance, not as hidden precedence.

That means:

- recommendations may suggest candidate profiles
- resolution still applies compatibility, governance, and precedence rules
- operator-accepted recommendations should still pass through normal resolution

This preserves deterministic runtime behavior.

## Relationship To Overrides

Recommendations should learn from override history.

Examples:

- recurring approved overrides may suggest a better default profile
- recurring rejected overrides may indicate an unhealthy expectation pattern

Recommendations can help reduce future override load, but they should not convert directly into overrides.

## Relationship To Change Management

Strategic recommendations should feed profile change management.

Good triggers include:

- repeated tactical recommendation acceptance
- recurring override patterns across multiple workspaces
- staged rollout evidence showing a new profile consistently performs better

This gives the system a path from observation to governed doctrine update.

## Recommendation Disposition

Recommendations should not disappear without a trace.

Useful dispositions include:

- `shown`
- `accepted_for_review`
- `rejected`
- `converted_to_change_request`
- `expired`

This helps the platform learn whether its recommendation quality is improving.

## Operator Surface Requirements

Operator surfaces should be able to show:

- top recommendations by workflow class
- acceptance versus rejection patterns
- high-confidence recommendation candidates
- recommendations that became real profile changes

This keeps recommendations legible and accountable.

## Required Events And Artifacts

The first useful recommendation model should emit at least:

- `workflow_profile.recommendation_created`
- `workflow_profile.recommendation_shown`
- `workflow_profile.recommendation_accepted_for_review`
- `workflow_profile.recommendation_rejected`
- `workflow_profile.recommendation_converted`

Useful artifacts include:

- `workflow_profile_recommendation.json`
- `workflow_profile_recommendation_assessment.json`
- `workflow_profile_recommendation_disposition.json`

## First Implementation Slice

The first implementation slice should stay intentionally narrow.

Start with:

- recommendation generation from repeated override and warning patterns
- confidence labels
- operator-visible recommendation summaries
- conversion path from high-confidence strategic recommendations into profile change requests

That is enough to make the system advisory and useful before introducing more advanced ranking or learning models.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md`
- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md`

This spec should guide:

- operator recommendation surfaces
- future advisory ranking systems
- doctrine-improvement workflows
- conversion of recurring signals into profile evolution proposals
