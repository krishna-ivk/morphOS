# Workflow Acceptance Profile Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow packs and templates
- eval-driven acceptance
- validation guardrails

What is still missing is the reusable workflow-level layer that ties those together.

This spec defines that layer.

## Executive Summary

Acceptance should not be reinvented separately for every run of the same workflow.

Instead, each workflow template should be able to declare an `Acceptance Profile` that states:

- what evidence matters
- which eval categories apply
- what minimum acceptance posture is needed at each phase
- when governance is still required

The result is:

- workflow-specific acceptance discipline
- less ad hoc decision-making
- more portable and reviewable delivery behavior

## Core Design Goals

- make acceptance reusable at the workflow level
- reduce per-run ambiguity about what “good enough” means
- keep acceptance logic aligned with workflow purpose and risk
- allow different workflows to have different acceptance expectations
- preserve policy and governance boundaries even when profiles are strong

## What A Workflow Acceptance Profile Is

A `WorkflowAcceptanceProfile` is a declarative acceptance contract attached to a workflow template or workflow pack.

It should define:

- acceptance targets
- required evidence families
- required eval categories
- disallowed blocker conditions
- governance or approval requirements

This profile does not replace runtime judgment.
It gives the runtime and reviewers a reusable rule surface.

## What It Is Not

A workflow acceptance profile is not:

- a guarantee that every run will pass
- a replacement for validation artifacts
- a replacement for governance
- a static checklist detached from the workflow’s actual evidence

It is a reusable acceptance scaffold.

## Canonical Acceptance Targets

The first useful targets should be:

- `validation_exit`
- `review_entry`
- `promotion_readiness`
- `release_readiness`
- `equivalence_readiness`

Different workflows may use only a subset of these.

## Profile Structure

Each profile should declare at least:

- `profile_id`
- `workflow_template_id`
- `risk_class`
- `acceptance_targets`
- `required_evidence_families`
- `required_eval_categories`
- `blocking_conditions`
- `governance_requirements`
- `supported_execution_modes`

This makes profiles portable and inspectable.

## Evidence Families

Profiles should refer to stable evidence families rather than ad hoc notes.

Suggested families:

- `validation_results`
- `findings`
- `summary_evidence`
- `review_packet`
- `approval_packet`
- `twin_verdicts`
- `equivalence_verdicts`
- `promotion_packet`

This keeps profiles aligned with the existing artifact system.

## Eval Categories Per Workflow

Different workflows should be able to require different eval mixes.

Examples:

### Feature Delivery Workflow

Likely evals:

- `behavior_eval`
- `contract_eval`
- `review_packet_eval`

### Promotion Workflow

Likely evals:

- `summary_eval`
- `policy_posture_eval`
- `behavior_eval`

### Equivalence Workflow

Likely evals:

- `equivalence_eval`
- `contract_eval`

## Blocking Conditions

Profiles should declare what blocks acceptance by default.

Examples:

- blocking validation findings remain
- required eval category missing
- required evidence family missing
- policy block unresolved
- approval state non-terminal where approval is required

This prevents workflow-specific acceptance from drifting into vague judgment.

## Governance Requirements

Profiles should be able to declare when governed decisions are still required.

Examples:

- workspace-admin approval required before promotion
- super-admin decision required for global exception flows
- no automatic acceptance for protected targets

This keeps workflow profiles honest about authority.

## Mode Sensitivity

Profiles may vary by execution mode.

Examples:

- in `factory` mode, promotion readiness may require stricter eval completeness
- in `interactive` mode, validation exit may allow exploratory continuation without claiming promotion readiness

Profiles should express this explicitly rather than relying on informal interpretation.

## Profile Inheritance

Workflow packs should be able to provide:

- a base acceptance profile
- template-specific overrides

This allows:

- shared doctrine across a workflow family
- tighter rules for riskier templates

Without inheritance, acceptance logic will become repetitive quickly.

## Suggested Profile Classes

The first useful profile classes should be:

- `standard_feature`
- `high_risk_feature`
- `promotion_path`
- `analysis_only`
- `equivalence_transfer`

These classes are not required, but they may help pack authors reuse patterns.

## Runtime Use

At runtime, the profile should help answer:

- what evidence do we still need?
- which evals are missing?
- can this run leave validation?
- can this run enter review or promotion?
- is governed approval still mandatory?

This lets the runtime enforce workflow-specific acceptance consistently.

## Operator Use

Operator surfaces should be able to show:

- which acceptance profile is active
- what evidence is still missing
- what blockers remain
- whether the next step is governed, automatic, or blocked

This helps operators understand why similar-looking runs may have different acceptance posture.

## Relationship To Workflow Packs

Acceptance profiles belong naturally beside workflow templates and packs.

That means:

- profiles should be versioned with workflows
- profile changes should be part of pack compatibility review
- profile trust should follow workflow pack trust posture

Profiles should not float around as undocumented side rules.

## Relationship To Acceptance Decisions

The workflow profile defines:

- what should be true for acceptance

The actual acceptance decision records:

- what was true in this run

This preserves the distinction between reusable rule and run-specific evidence.

## Relationship To Drift

If upstream drift affects assumptions behind a profile:

- the profile may need reevaluation
- target acceptance rules may need tightening
- eval categories may need to change

Profiles should therefore remain linked to upstream-sensitive assumptions where relevant.

## Required Artifacts

Workflow acceptance profiles should emit or define durable artifacts such as:

- `acceptance-profiles/<profile_id>.json`
- `acceptance-profiles/<profile_id>.md`
- `acceptance-profiles/<profile_id>/criteria.json`
- `acceptance-profiles/<profile_id>/governance_rules.json`

These artifacts should be part of workflow pack governance.

## Required Events

The event taxonomy should support at least:

- `acceptance.profile_applied`
- `acceptance.profile_blocked`
- `acceptance.profile_satisfied`
- `acceptance.profile_reevaluation_required`

Each event should include:

- `run_id`
- `workflow_template_id`
- `profile_id`
- current acceptance target

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define workflow acceptance profile contracts
- `skyforce-symphony` should apply profiles during validation, review, and promotion transitions
- workflow packs should ship profile metadata alongside templates
- `skyforce-command-centre` should surface active profile, missing evidence, and acceptance blockers clearly

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define `WorkflowAcceptanceProfile` and profile-target contracts
2. attach one acceptance profile to the core feature-delivery workflow
3. require evidence family and eval category checks for validation exit and promotion readiness
4. expose profile-driven blockers in operator views
5. keep governance requirements explicit in the profile

That is enough to make workflow-level acceptance reusable without building a huge policy matrix first.

## Recommended Next Specs

This spec should be followed by:

1. `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`
2. `MEMORY_GOVERNANCE_RETENTION_SPEC.md`
3. `WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md`

Together, those continue operational response, memory discipline, and workflow-pack governance refinement.
