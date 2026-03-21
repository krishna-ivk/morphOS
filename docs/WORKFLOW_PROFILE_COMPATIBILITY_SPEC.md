# Workflow Profile Compatibility Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow packs and registries
- workflow acceptance profiles
- tool registries and action discovery
- policy hooks at workflow boundaries

What is still missing is the compatibility layer between those assets.

Right now the platform can describe:

- a workflow template
- an acceptance profile
- a tool surface
- a policy posture

But it still needs a clear way to answer:

- which combinations are valid?
- which are only partially supported?
- which should be blocked before a run starts?

This spec defines that compatibility layer.

## Executive Summary

Compatibility should not be inferred from naming convention or operator memory.

For `morphOS`, the correct posture is:

- declare compatibility explicitly
- validate composition before execution
- surface incompatibility as an operator-visible fact
- separate hard incompatibility from reviewable mismatch
- version compatibility alongside the assets themselves

The goal is safer workflow selection, more portable packs, and less hidden drift.

## Core Design Goals

- prevent invalid workflow and profile combinations from reaching execution
- make pack composition inspectable and version-aware
- distinguish compatibility failure from acceptance failure
- support gradual evolution without silent breakage
- keep compatibility visible to the runtime and operators

## Compatibility Principle

Every reusable workflow asset should declare what it expects from the environment around it.

That includes:

- runtime capabilities
- supported execution modes
- compatible acceptance profiles
- required tool families
- policy and governance assumptions

If those expectations are not met, the system should say so before execution begins.

## What Compatibility Covers

The first useful compatibility model should cover:

- workflow template to acceptance profile compatibility
- workflow template to tool-family compatibility
- workflow pack to runtime compatibility
- workflow template to execution-mode compatibility
- workflow template to policy-hook availability
- workflow template to governance requirement compatibility

This should be enough to stop most invalid compositions early.

## Canonical Compatibility Objects

`morphOS` should support at least:

- `CompatibilityContract`
- `CompatibilityAssessment`
- `CompatibilityVerdict`
- `CompatibilityException`
- `CompatibilityMatrix`

Suggested meanings:

- `CompatibilityContract`
  - declared expectations for a reusable asset
- `CompatibilityAssessment`
  - actual comparison against the current environment
- `CompatibilityVerdict`
  - final compatibility result
- `CompatibilityException`
  - governed override for a non-default pairing
- `CompatibilityMatrix`
  - indexed view of supported combinations

## Compatibility Verdicts

The system should converge on a small shared set of verdicts:

- `compatible`
- `compatible_with_warnings`
- `review_required`
- `incompatible`
- `unsupported`

Suggested meanings:

- `compatible`
  - expected combination with no known blockers
- `compatible_with_warnings`
  - usable, but some constraints or caveats apply
- `review_required`
  - composition may work, but requires governed approval
- `incompatible`
  - the combination should not execute as composed
- `unsupported`
  - the platform does not currently implement the required capability

## Workflow Template Compatibility Contract

Each workflow template should be able to declare at least:

- `supported_acceptance_profile_ids`
- `supported_execution_modes`
- `required_tool_families`
- `required_policy_hooks`
- `required_governance_categories`
- `required_runtime_features`
- `incompatible_tags`

This keeps compatibility close to the template rather than scattering it across notes.

## Acceptance Profile Compatibility

Acceptance profiles should declare what workflow shapes they are valid for.

Examples:

- an `analysis_only` profile should not attach to a promotion workflow
- an `equivalence_transfer` profile should not attach to a simple incident triage workflow
- a `high_risk_feature` profile may require policy hooks and approval categories that a lightweight workflow does not expose

Compatibility should check:

- target phases
- evidence families
- required eval categories
- governance requirements
- mode assumptions

## Tool Family Compatibility

Workflows should declare the tool families they require or forbid.

Examples:

- a `feature_pipeline` may require source-read, source-write, test, and review-packet tool families
- a `repo_evaluation` workflow may forbid mutation-capable tool families by default
- a promotion workflow may require governed live-action tool families but only after validation and review

Tool compatibility should be checked before selection, not discovered mid-run.

## Runtime Feature Compatibility

Workflow packs should declare runtime features they depend on.

Examples:

- parallel slice execution
- approval checkpoint persistence
- digital twin validation support
- Context Hub reference lookup
- governed live-action gates

If the runtime lacks a required feature, the workflow should be visibly unsupported.

## Execution Mode Compatibility

Not every workflow behaves correctly in every mode.

Examples:

- `factory` mode may be supported only when the workflow has sufficient policy hooks and acceptance automation
- `interactive` mode may be required for ambiguous exploratory workflows
- some workflows may support both but attach different acceptance profiles depending on mode

Compatibility should express these differences explicitly.

## Policy Hook Compatibility

Some workflows assume that specific policy hooks exist.

Examples:

- promotion workflows may require `promotion_policy_gate`
- live integration workflows may require `live_action_policy_gate`
- risky tool paths may require `tool_policy_gate` and `execution_policy_gate`

If those hooks are unavailable, the workflow should be incompatible or review-required.

## Governance Compatibility

Workflow composition should also account for governance expectations.

Examples:

- a workflow that assumes workspace-admin approval is incompatible in an environment where only super-admin approval exists for that action class
- a cross-workspace workflow cannot be treated as compatible with a profile designed for purely local approvals
- a protected rollout workflow may require governance categories not present in a lightweight pack

Governance mismatch should be visible before the run begins.

## Version Compatibility

Compatibility should be version-aware.

That means:

- workflow packs should declare compatible profile versions
- profiles should declare compatible template versions or classes
- tool registries should expose supported action-family versions where needed
- compatibility assessments should record the versions actually evaluated

Without this, pack evolution will drift silently.

## Compatibility Matrix

The platform should maintain a machine-readable compatibility matrix.

A useful v0 matrix should answer:

- which profiles fit which templates?
- which templates require which tool families?
- which packs are usable on the current runtime?
- which combinations are deprecated or review-only?

This matrix should be operator-visible and runtime-queryable.

## Selection And Preflight Use

Compatibility should be checked during preflight, before workflow launch.

The healthy flow is:

1. candidate workflow templates are selected
2. candidate acceptance profiles are attached
3. required tool families and runtime features are compared
4. policy and governance assumptions are checked
5. a compatibility verdict is emitted
6. only compatible or explicitly approved combinations proceed

Compatibility is a precondition, not a postmortem explanation.

## Exceptions And Overrides

Some mismatches may be reviewable rather than strictly blocked.

Examples:

- temporary pack version skew during migration
- a governed trial of a new acceptance profile
- an operator-approved local deviation with clear blast radius

These cases should use `CompatibilityException` records with:

- rationale
- scope
- expiration
- approving authority
- linked evidence

Compatibility exceptions should never become invisible defaults.

## Operator Surface Requirements

Operator surfaces should be able to show:

- active workflow template
- attached acceptance profile
- compatibility verdict
- missing requirements
- warning conditions
- whether a compatibility exception is active

This helps people understand why a workflow is available, blocked, or review-only.

## Required Events And Artifacts

The first useful compatibility model should emit at least:

- `compatibility.assessed`
- `compatibility.blocked`
- `compatibility.review_required`
- `compatibility.exception_granted`
- `compatibility.exception_expired`

Useful artifacts include:

- `compatibility_assessment.json`
- `compatibility_matrix.json`
- `compatibility_exception.json`

## First Implementation Slice

The first implementation slice should stay narrow.

Start with:

- workflow template to acceptance profile compatibility
- workflow template to execution-mode compatibility
- workflow template to required tool-family compatibility
- pack to runtime-feature compatibility
- operator-visible compatibility verdicts at preflight

That is enough to prevent the most common invalid compositions before modeling every edge case.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
- `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
- `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
- `POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md`
- `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- workflow preflight validation
- pack installation checks
- operator-facing workflow selection
- future pack migration and deprecation tooling
