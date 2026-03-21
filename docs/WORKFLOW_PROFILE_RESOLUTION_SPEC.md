# Workflow Profile Resolution Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow acceptance profiles
- workflow policy profiles
- workflow profile compatibility

What is still missing is the deterministic selection step that turns those reusable assets into one active run contract.

The platform still needs clear answers to these questions:

- which profile wins when pack defaults, template overrides, and workspace context differ?
- how do execution mode and governance posture affect the chosen profile set?
- what is the single resolved profile contract the runtime actually executes against?

This spec defines that resolution model.

## Executive Summary

Reusable profiles are useful only if the runtime can resolve them deterministically.

For `morphOS`, the correct posture is:

- resolve acceptance and policy profiles before execution starts
- combine pack defaults, template overrides, compatibility results, and runtime context explicitly
- emit one resolved workflow contract for the run
- make every override and selection reason inspectable

The goal is selection behavior that is predictable, auditable, and easy to reason about.

## Core Design Goals

- prevent ambiguous or implicit profile selection
- make workflow behavior reproducible across runs
- keep resolution aligned with compatibility, governance, and mode semantics
- support inheritance without hidden precedence rules
- give operators a clear view of why a specific profile set became active

## Resolution Principle

Each run should have one active resolved workflow contract.

That contract should include at least:

- the selected workflow template
- the resolved acceptance profile
- the resolved policy profile
- the compatibility verdicts that allowed the selection
- the mode and governance context used during resolution

The runtime should execute against the resolved contract, not against scattered partial defaults.

## What Resolution Must Consider

The first useful resolution model should consider:

- pack-level profile defaults
- template-level profile declarations
- template-specific overrides
- execution mode
- workspace or tenant governance posture
- compatibility verdicts
- migration or deprecation state
- operator-provided explicit selection when allowed

This is enough to avoid most hidden selection drift.

## Canonical Resolution Objects

`morphOS` should support at least:

- `ProfileResolutionRequest`
- `ProfileResolutionContext`
- `ResolvedWorkflowContract`
- `ResolutionTrace`
- `ResolutionVerdict`

Suggested meanings:

- `ProfileResolutionRequest`
  - requested workflow selection with optional profile preferences
- `ProfileResolutionContext`
  - execution mode, governance, workspace, runtime, and compatibility context
- `ResolvedWorkflowContract`
  - final active workflow, acceptance, and policy contract for the run
- `ResolutionTrace`
  - explanation of how the final selection was derived
- `ResolutionVerdict`
  - whether resolution succeeded, needs review, or failed

## Resolution Verdicts

The system should converge on a small shared set of verdicts:

- `resolved`
- `resolved_with_warnings`
- `review_required`
- `unresolved`

Suggested meanings:

- `resolved`
  - one clear active contract was selected
- `resolved_with_warnings`
  - selection succeeded, but caveats or downgraded posture apply
- `review_required`
  - selection is plausible, but governed or operator choice is required
- `unresolved`
  - no safe active contract could be formed

## Resolution Inputs

The minimum useful inputs should include:

- `workflow_template_id`
- `workflow_pack_id`
- `execution_mode`
- `workspace_id`
- `tenant_or_scope`
- `runtime_feature_snapshot`
- `governance_snapshot`
- `requested_acceptance_profile_id` when explicitly provided
- `requested_policy_profile_id` when explicitly provided

This keeps resolution explicit instead of magical.

## Resolution Order

The first useful resolution order should be:

1. choose the candidate workflow template
2. load pack-level defaults
3. apply template-level declared profiles
4. apply template-specific overrides
5. apply mode-sensitive adjustments
6. apply governance and workspace constraints
7. run compatibility checks
8. emit the final resolved contract or a review-required result

This gives inheritance and context a clear precedence path.

## Precedence Rules

When multiple sources provide conflicting profile guidance, the first useful precedence should be:

1. hard compatibility and governance constraints
2. explicit template-level requirements
3. template overrides over pack defaults
4. explicit operator choice only when compatible and permitted
5. pack defaults as fallback

This prevents convenience defaults from overriding hard safety boundaries.

## Acceptance Profile Resolution

Acceptance profile resolution should answer:

- which profile class applies to this workflow and mode?
- are the required evidence and governance assumptions supported?
- did compatibility downgrade the available set?

If multiple acceptance profiles remain viable, the runtime should prefer:

- the template-declared profile
- otherwise the pack default
- otherwise the highest-compatible profile with the narrowest ambiguity

## Policy Profile Resolution

Policy profile resolution should answer:

- which required policy hooks are available?
- which action-family restrictions fit this environment?
- which approval and exception posture matches governance reality?

If multiple policy profiles remain viable, the runtime should prefer:

- the template-declared profile
- otherwise the pack default
- otherwise the most restrictive compatible profile that still supports the workflow purpose

This biases toward safety when resolution is ambiguous.

## Mode-Sensitive Resolution

Execution mode should influence profile selection directly.

Examples:

- `factory` mode may resolve to stricter acceptance and policy profiles
- `interactive` mode may allow exploratory profiles with narrower live-action posture
- some profiles may be excluded entirely in one mode

Mode should be part of the resolution contract, not an afterthought.

## Governance-Sensitive Resolution

Resolution should account for authority reality before the run starts.

Examples:

- a workflow requiring workspace-admin approval may be unresolved in a context where only super-admin can approve the relevant category
- a local workspace flow may resolve differently from a cross-workspace flow
- a policy profile allowing reviewable exceptions may be incompatible where the governance model disallows them

This keeps the resolved contract honest about real authority.

## Compatibility As A Gate

Compatibility does not pick the profile by itself.
It acts as the boundary that removes unsafe candidates.

Resolution should use compatibility results to:

- drop incompatible profile candidates
- downgrade to review-required when only marginal fits remain
- explain why a requested profile was not selected

This keeps profile selection and compatibility tightly linked without merging them conceptually.

## Explicit Operator Selection

Operators may sometimes request a specific profile.

That request should be treated as:

- advisory by default
- binding only when policy allows it and compatibility is satisfied

If an operator-requested profile is rejected, the runtime should explain:

- what blocked it
- which profile was chosen instead
- whether review could change the outcome

## Resolution Trace

Every resolved contract should produce a trace that shows:

- candidate profiles considered
- which ones were excluded and why
- defaults and overrides applied
- compatibility findings used
- governance or mode adjustments applied

This is critical for operator trust and debugging.

## Runtime Use

At runtime, the resolved workflow contract should answer:

- which acceptance profile is active?
- which policy profile is active?
- what compatibility warnings still matter?
- what governance posture applies?
- whether execution is fully resolved or still review-gated

This gives the runtime one canonical contract to execute against.

## Operator Use

Operator surfaces should be able to show:

- selected workflow template
- resolved acceptance profile
- resolved policy profile
- warnings or review requirements
- the resolution trace summary

This helps people understand how the system arrived at the active workflow posture.

## Required Events And Artifacts

The first useful resolution model should emit at least:

- `workflow_profile_resolution.requested`
- `workflow_profile_resolution.resolved`
- `workflow_profile_resolution.review_required`
- `workflow_profile_resolution.failed`

Useful artifacts include:

- `resolved_workflow_contract.json`
- `profile_resolution_trace.json`
- `profile_resolution_verdict.json`

## First Implementation Slice

The first implementation slice should stay narrow.

Start with:

- pack default plus template override resolution
- mode-sensitive profile selection
- compatibility-gated candidate pruning
- operator-visible resolved contract output

That is enough to make workflow profile selection deterministic before adding deeper inheritance trees and cross-pack profile resolution.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
- `WORKFLOW_POLICY_PROFILE_SPEC.md`
- `WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md`
- `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- workflow launch preflight
- operator workflow selection UX
- future profile linting and migration tooling
- durable recording of active workflow contracts
