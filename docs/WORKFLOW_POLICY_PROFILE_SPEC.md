# Workflow Policy Profile Spec

## Why This Spec Exists

`morphOS` already defines:

- policy hooks at workflow boundaries
- workflow acceptance profiles
- workflow profile compatibility

What is still missing is the reusable workflow-level policy contract that sits beside acceptance.

The platform still needs clear answers to these questions:

- which policy gates are required for a workflow?
- which action classes are restricted, reviewable, or forbidden?
- what approval posture should a workflow assume by default?

This spec defines that reusable policy layer.

## Executive Summary

Policy should not be reinvented from scratch for every run of the same workflow.

For `morphOS`, the correct posture is:

- attach a reusable `WorkflowPolicyProfile` to each workflow template or pack
- declare required policy hooks and action restrictions explicitly
- make approval and exception posture visible before execution starts
- allow controlled variation by workflow risk and execution mode

The goal is workflow-specific policy discipline without scattering rules across prompts, templates, and operator memory.

## Core Design Goals

- make policy expectations reusable at the workflow level
- reduce ambiguity about what a workflow is allowed to do
- keep workflow intent aligned with approval and restriction posture
- support different policy shapes for different workflow classes
- preserve compatibility with governance and runtime policy evaluation

## What A Workflow Policy Profile Is

A `WorkflowPolicyProfile` is a declarative policy contract attached to a workflow template or workflow pack.

It should define:

- required policy hooks
- allowed and restricted action families
- approval posture
- exception posture
- escalation expectations

This profile does not replace runtime policy evaluation.
It tells the runtime what policy shape the workflow assumes.

## What It Is Not

A workflow policy profile is not:

- the full dynamic policy engine
- a guarantee that every action will be allowed
- a replacement for governance review
- a hidden prompt convention

It is a reusable policy scaffold for one workflow family.

## Canonical Policy Targets

The first useful targets should include:

- `planning`
- `assignment`
- `execution`
- `validation`
- `promotion`
- `live_action`
- `closeout`

Different workflows may use only a subset of these.

## Profile Structure

Each profile should declare at least:

- `policy_profile_id`
- `workflow_template_id` or `workflow_class`
- `risk_class`
- `required_policy_hooks`
- `restricted_action_families`
- `approval_requirements`
- `exception_rules`
- `supported_execution_modes`
- `governance_requirements`

This makes policy profiles portable and inspectable.

## Required Policy Hooks

Policy profiles should be able to declare which boundary hooks must exist.

Examples:

- a feature-delivery workflow may require `tool_policy_gate`, `validation_policy_gate`, and `promotion_policy_gate`
- a live-integration workflow may additionally require `live_action_policy_gate`
- an analysis-only workflow may not need `promotion_policy_gate`

If a required hook is missing, the workflow should be incompatible or review-required.

## Action Family Restrictions

Policy profiles should define default posture by action family.

Useful postures include:

- `allowed`
- `allowed_with_review`
- `allowed_with_approval`
- `blocked`

Examples:

- analysis-only workflows may block source mutation and live-action families
- promotion workflows may allow live-action families only with approval
- high-risk workflows may require review for deployment or external-write actions

## Approval Requirements

Policy profiles should be able to express:

- when approval is required
- which approval category applies
- whether `workspace_admin` is sufficient
- when `super_admin` escalation is mandatory

This keeps workflow-level policy honest about authority requirements.

## Exception Rules

Not every workflow should allow the same exceptions.

Profiles should be able to define:

- which policy blocks are reviewable
- which may become approvable exceptions
- which remain hard blocks

Examples:

- a protected rollout workflow may allow almost no exceptions
- an exploratory analysis workflow may allow broader reviewable exceptions

## Mode Sensitivity

Policy profiles may vary by execution mode.

Examples:

- in `factory` mode, write-capable actions may require stricter predeclared approval posture
- in `interactive` mode, exploratory reads may be broader while live actions remain tightly controlled

These differences should be explicit rather than implied.

## Profile Inheritance

Workflow packs should be able to provide:

- a base policy profile
- template-specific overrides

This allows:

- common policy doctrine across a workflow family
- stricter rules for higher-risk templates

Without inheritance, policy rules will become repetitive quickly.

## Suggested Profile Classes

The first useful profile classes should be:

- `analysis_safe`
- `standard_delivery`
- `high_risk_delivery`
- `promotion_controlled`
- `live_integration_guarded`

These are optional, but they help pack authors reuse patterns.

## Runtime Use

At runtime, the profile should help answer:

- which policy hooks must be present?
- which action families are allowed right now?
- when is approval mandatory?
- can a review clear this block?
- does this workflow permit the requested live action at all?

This lets the runtime apply workflow-specific policy posture consistently.

## Operator Use

Operator surfaces should be able to show:

- which policy profile is active
- which actions are blocked or approval-gated
- what review or escalation posture applies
- whether a requested action violates the workflow’s intended policy shape

This helps operators understand why similar workflows behave differently.

## Relationship To Workflow Packs

Policy profiles belong naturally beside workflow templates, packs, and acceptance profiles.

That means:

- profiles should be versioned with workflows
- profile changes should be part of pack compatibility review
- profile trust should follow workflow pack trust posture

Policy profiles should not float around as undocumented side rules.

## Relationship To Acceptance Profiles

Acceptance profiles and policy profiles are complementary:

- acceptance profiles say what evidence and posture are needed to progress
- policy profiles say what actions, hooks, and approvals are allowed or required

Together they define what “good enough” means and what “allowed to proceed” means.

They should remain distinct but composable.

## Relationship To Compatibility

Compatibility checks should validate:

- the workflow template can use the chosen policy profile
- required policy hooks exist
- governance requirements match the environment
- execution-mode assumptions are satisfied

This prevents a workflow from selecting a policy profile it cannot actually support.

## Relationship To Governance

Policy profiles should declare when governance is expected, not replace it.

Examples:

- a profile may require workspace-admin approval for promotion
- a profile may state that live-action exceptions always escalate to super-admin
- a profile may declare some action families non-overridable

This keeps governance explicit at the workflow level.

## Canonical Policy Findings At Profile Level

The first useful reusable policy findings should include:

- missing required hook
- forbidden action family requested
- approval category missing
- unsupported exception request
- governance mismatch

These findings should be operator-visible and machine-readable.

## Required Events And Artifacts

The first useful policy-profile model should emit at least:

- `workflow_policy_profile.selected`
- `workflow_policy_profile.incompatible`
- `workflow_policy_profile.approval_required`
- `workflow_policy_profile.exception_denied`

Useful artifacts include:

- `workflow_policy_profile.json`
- `policy_profile_assessment.json`
- `policy_profile_finding.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- profile attachment to workflow templates
- required policy-hook declarations
- action-family posture declarations
- approval category and governance requirements
- operator-visible profile selection and incompatibility reasons

That is enough to make workflow-level policy reusable before building deeper inheritance and exception tooling.

## Relationship To Other Specs

This spec depends on:

- `POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md`
- `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
- `WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`
- `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`

This spec should guide:

- workflow pack authoring
- policy preflight checks
- approval-routing defaults
- future workflow policy linting and migration tools
