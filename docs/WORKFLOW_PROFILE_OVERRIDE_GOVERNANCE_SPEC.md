# Workflow Profile Override Governance Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile resolution
- workflow policy profiles
- workspace admin governance

What is still missing is the governance model for changing the resolved workflow contract by exception.

The platform still needs clear answers to these questions:

- when may an operator override the resolved profile set?
- who is allowed to approve that override?
- how long does an override remain valid?

This spec defines that governance layer.

## Executive Summary

Manual overrides should exist, but they should not behave like silent shortcuts around the resolution model.

For `morphOS`, the correct posture is:

- treat profile overrides as governed exceptions
- scope them tightly
- require explicit authority and rationale
- time-bound them by default
- preserve a full audit trail

The goal is flexibility without dissolving profile discipline.

## Core Design Goals

- allow justified exceptions without undermining deterministic resolution
- prevent casual or hidden override drift
- align override approval with blast radius and governance scope
- make override duration and impact explicit
- keep operators and runtimes aware of the active exception posture

## Override Principle

The resolved workflow contract is the default truth for a run.

An override is a governed exception that temporarily or deliberately changes one part of that truth.

Overrides should be:

- explicit
- narrow
- reviewable
- expiring unless there is a strong reason otherwise

## What May Be Overridden

The first useful override surface should allow controlled exceptions for:

- selected acceptance profile
- selected policy profile
- mode-sensitive profile branch
- specific review or approval posture where the workflow policy allows it

The system should not assume every field of the resolved contract is overrideable.

## What Should Usually Not Be Overridden

The default non-overrideable categories should include:

- hard compatibility failures
- missing required policy hooks
- forbidden governance scope crossings
- non-overridable policy blocks
- unavailable runtime features the workflow fundamentally requires

These should remain hard stops unless another spec explicitly allows exception paths.

## Canonical Override Objects

`morphOS` should support at least:

- `WorkflowProfileOverrideRequest`
- `WorkflowProfileOverrideAssessment`
- `WorkflowProfileOverrideDecision`
- `WorkflowProfileOverrideRecord`
- `OverrideExpiry`

Suggested meanings:

- `WorkflowProfileOverrideRequest`
  - requested change to the resolved workflow contract
- `WorkflowProfileOverrideAssessment`
  - evaluation of compatibility, governance, and blast radius
- `WorkflowProfileOverrideDecision`
  - approved, rejected, or escalated result
- `WorkflowProfileOverrideRecord`
  - durable record of the active or historical override
- `OverrideExpiry`
  - expiration condition for the override

## Override Categories

The first useful override categories should include:

- `profile_substitution`
- `profile_downgrade`
- `profile_escalation`
- `mode_exception`
- `governance_exception`

Examples:

- substituting a different acceptance profile
- selecting a stricter policy profile than the default
- allowing an interactive branch where factory mode was the default
- requesting a temporary governance exception for one run

## Scope Rules

Every override should declare its scope clearly.

Useful scopes include:

- `single_run`
- `workflow_template_in_workspace`
- `workspace_default_temporary`
- `global_exception`

Default rule:

- prefer the narrowest scope that solves the problem

Broader scopes should require stronger authority.

## Authority Rules

Authority should follow blast radius.

Suggested posture:

- single-workspace, single-run overrides may go to `workspace_admin`
- cross-workspace or global exceptions escalate to `super_admin`
- policy-shape overrides that alter shared trust posture generally require `super_admin`

Overrides should never silently bypass the normal authority split.

## Approval Criteria

An override request should be evaluated against at least:

- compatibility impact
- policy impact
- governance impact
- workflow risk class
- evidence and rationale quality
- whether a safer non-override path exists

If the request only bypasses discipline without necessity, it should be rejected.

## Expiration Rules

Overrides should expire by default.

Useful expiration models include:

- end of current run
- fixed time window
- until migration completes
- until a blocking dependency is restored

Permanent overrides should be rare and usually indicate that the base profiles need revision instead.

## Renewal Rules

Renewal should not happen silently.

If an override must continue:

- renew it explicitly
- reassess its original rationale
- check whether the base profile model should be updated instead

Repeated renewal is a signal that the exception may actually be a missing productized rule.

## Override Effects On Resolution

Overrides should not replace the resolution process.

Instead, the healthy flow is:

1. normal profile resolution runs
2. an override request is assessed
3. if approved, the override is applied as a governed overlay
4. the resolved workflow contract records both the base contract and override delta

This preserves the original truth while making the exception visible.

## Override Traceability

Every active override should expose:

- base resolved profile set
- fields changed by the override
- approving actor and authority
- rationale
- scope
- expiration

This should be visible in operator surfaces and durable records.

## Relationship To Compatibility

Overrides may narrow or substitute among compatible options.

Overrides should not normally:

- invent compatibility where none exists
- ignore missing runtime requirements
- bypass hard governance mismatches

If an override attempts one of those, it should be rejected or escalated under a different exception process.

## Relationship To Policy Profiles

Policy profile overrides are especially sensitive because they can change what actions are legal or reviewable.

That means:

- stricter policy-profile overrides are often safer
- looser policy-profile overrides require stronger justification
- exception posture changes should be treated as governance events

This keeps policy integrity intact.

## Relationship To Acceptance Profiles

Acceptance profile overrides may change what evidence is considered sufficient.

That means:

- weaker acceptance-profile overrides should be treated carefully
- stronger acceptance-profile overrides may be acceptable for cautionary runs
- promotion-related acceptance overrides should usually require governance review

This keeps “good enough” from drifting silently.

## Relationship To Active Runs

If an override is applied after a run has started, it should also trigger active-run reevaluation.

Examples:

- a looser policy profile may require new approval
- a substituted acceptance profile may require replanning or new evidence
- an expired override may pause the run until re-resolution occurs

Overrides and active-run posture should remain synchronized.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current base resolved contract
- active override delta
- authority and rationale
- expiration status
- whether the override is pending, active, rejected, or expired

This helps avoid “why is this run behaving differently?” confusion.

## Required Events And Artifacts

The first useful override model should emit at least:

- `workflow_profile_override.requested`
- `workflow_profile_override.approved`
- `workflow_profile_override.rejected`
- `workflow_profile_override.expired`
- `workflow_profile_override.renewed`

Useful artifacts include:

- `workflow_profile_override_request.json`
- `workflow_profile_override_assessment.json`
- `workflow_profile_override_record.json`

## First Implementation Slice

The first implementation slice should stay narrow and practical.

Start with:

- single-run override requests
- scope-aware authority routing
- expiration support
- resolved-contract overlay recording
- operator-visible override status and rationale

That is enough to make overrides governable before building broader workspace-default or global exception tooling.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_POLICY_PROFILE_SPEC.md`
- `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`
- `ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md`

This spec should guide:

- operator override UX
- override audit logs
- future exception analytics
- migration from repeated exceptions into first-class profile changes
