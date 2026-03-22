# Workflow Profile Change Management Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile resolution
- workflow profile override governance
- pack migration and deprecation

What is still missing is the change-management process for the profile assets themselves.

The platform still needs clear answers to these questions:

- how are acceptance and policy profile changes proposed and reviewed?
- how are risky profile edits rolled out safely?
- when should repeated overrides become a real profile change?

This spec defines that change-management model.

## Executive Summary

Profiles are not static doctrine.
They will evolve as workflows, governance, and runtime capability evolve.

For `morphOS`, the correct posture is:

- treat profile edits as governed configuration changes
- review them with compatibility and rollout awareness
- distinguish draft, approved, active, and deprecated profile states
- promote recurring justified overrides into first-class profile updates when appropriate

The goal is profile evolution without destabilizing workflow behavior.

## Core Design Goals

- make profile changes explicit and auditable
- prevent silent behavior drift caused by profile edits
- align profile updates with compatibility, governance, and active-run safety
- provide a controlled path from one-off exceptions to durable rules
- support gradual rollout for risky or high-impact profile changes

## Change Management Principle

A workflow profile is a reusable contract.

Changing it is not just editing a config file.
It is changing workflow behavior across future runs and sometimes active runs.

That means profile changes should follow a managed lifecycle.

## What This Spec Covers

The first useful change-management model should cover:

- acceptance profile changes
- policy profile changes
- resolution rule changes that affect profile choice
- profile default changes at pack or template level
- conversion of recurring overrides into durable profile updates

This is enough to make the profile system governable as a product surface.

## Canonical Change Objects

`morphOS` should support at least:

- `WorkflowProfileChangeRequest`
- `WorkflowProfileChangeAssessment`
- `WorkflowProfileChangeDecision`
- `WorkflowProfileReleasePlan`
- `WorkflowProfileChangeRecord`

Suggested meanings:

- `WorkflowProfileChangeRequest`
  - proposed modification to a workflow profile or its defaults
- `WorkflowProfileChangeAssessment`
  - compatibility, governance, and blast-radius analysis
- `WorkflowProfileChangeDecision`
  - approval, rejection, or escalation result
- `WorkflowProfileReleasePlan`
  - staged rollout or activation plan for the change
- `WorkflowProfileChangeRecord`
  - durable audit record of what changed and why

## Profile Lifecycle States

The first useful lifecycle states should include:

- `draft`
- `review_required`
- `approved`
- `staged`
- `active`
- `deprecated`
- `retired`

Suggested meanings:

- `draft`
  - proposed but not yet governed
- `review_required`
  - awaiting structured review
- `approved`
  - allowed to proceed into rollout
- `staged`
  - ready for limited activation
- `active`
  - available for normal resolution
- `deprecated`
  - still recognized but no longer preferred
- `retired`
  - not available for new resolution

## What Counts As A Material Change

Not every edit is equally risky.

Material changes include:

- changing required evidence families
- changing required policy hooks
- changing action-family restrictions
- changing approval or exception posture
- changing default resolved profiles
- changing supported execution modes

These should always go through structured assessment.

## Assessment Criteria

Every material profile change should be assessed against at least:

- workflow compatibility impact
- governance impact
- active-run impact
- migration and deprecation implications
- whether current overrides indicate the new rule is justified
- whether a staged rollout is required

This keeps profile editing from becoming speculative configuration churn.

## Source Of Truth For Change Proposals

A profile change request should include:

- the current profile state
- the proposed new state
- rationale
- linked incidents, overrides, or migration drivers
- expected affected workflows and workspaces

This makes the delta explicit instead of relying on “it seemed better.”

## Override Promotion Path

Repeated approved overrides are often a signal.

The system should ask:

- is this override solving a one-time problem?
- or is it evidence that the base profile is wrong or incomplete?

When the same override pattern repeats, the preferred path should be:

- evaluate it as a candidate profile change
- review it with compatibility and governance context
- productize it if justified

This turns exceptions into learning.

## Rollout Modes

The first useful rollout modes should include:

- `immediate_activation`
- `staged_activation`
- `workspace_limited_activation`
- `review_only_preview`

Examples:

- low-risk wording or metadata changes may use immediate activation
- policy-tightening changes may start as staged or workspace-limited
- risky profile rewrites may require preview before they become active defaults

## Staged Rollout Rules

Staging is especially useful when:

- the profile change alters default workflow resolution
- active runs could be affected soon
- governance posture changes materially
- acceptance or policy requirements become stricter

During staging, operator surfaces should show both:

- currently active profile behavior
- upcoming profile behavior

This reduces surprise during rollout.

## Relationship To Active Runs

Profile changes may affect active runs differently from future runs.

Suggested posture:

- future runs should use the new active profile once rollout allows it
- active runs should be reevaluated only when the change materially affects their current posture
- non-material profile edits should not disrupt healthy active runs

This keeps profile evolution from causing gratuitous churn.

## Relationship To Resolution

Profile changes should not bypass the resolution system.

Instead:

- profile changes update what candidates and defaults resolution sees
- resolution continues to produce the final active contract per run
- rollout state controls when the new profile can actually be selected

This preserves separation between authoring and runtime selection.

## Relationship To Migration And Deprecation

A profile change may:

- create a new active profile version
- deprecate an older profile
- require workflow-pack migration review

That means change management should link directly to:

- migration plans
- deprecation notices
- compatibility assessments

Profile change should not happen in isolation from the surrounding ecosystem.

## Authority Rules

Authority should follow blast radius.

Suggested posture:

- workspace-limited profile changes may be reviewable by `workspace_admin` when they do not alter shared global posture
- shared pack defaults, cross-workspace policy shifts, and high-impact profile changes should escalate to `super_admin`

This keeps local adaptation possible without letting local edits silently redefine shared doctrine.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current active profile version
- pending profile changes
- rollout mode and stage
- affected workflows or workspaces
- linked overrides or incidents that motivated the change

This helps operators understand not just current posture, but where the doctrine is moving.

## Required Events And Artifacts

The first useful change-management model should emit at least:

- `workflow_profile_change.requested`
- `workflow_profile_change.review_required`
- `workflow_profile_change.approved`
- `workflow_profile_change.staged`
- `workflow_profile_change.activated`
- `workflow_profile_change.deprecated`

Useful artifacts include:

- `workflow_profile_change_request.json`
- `workflow_profile_change_assessment.json`
- `workflow_profile_release_plan.md`
- `workflow_profile_change_record.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- explicit change requests for policy and acceptance profiles
- compatibility and governance assessment
- staged versus immediate activation
- links from repeated overrides into profile change proposals
- operator-visible pending and active profile versions

That is enough to make profile evolution governable before building richer diff tooling and full rollout automation.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md`
- `PACK_MIGRATION_AND_DEPRECATION_SPEC.md`
- `ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- profile authoring workflow
- rollout of new profile versions
- deprecation of old profiles
- conversion of repeated exceptions into stable doctrine
