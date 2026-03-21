# Workspace Admin Governance Spec

## Why This Spec Exists

`morphOS` already freezes:

- `workspace_admin`
- `super_admin`
- `workspace`
- `global`

It also already states the high-level routing rule:

- workspace-scoped risky actions default to `workspace_admin`
- cross-workspace, global-policy, or exception-path actions escalate to `super_admin`

What is still missing is the governance model around those roles.

This spec defines that model.

## Executive Summary

The platform should not treat human authority as a vague “someone approves this.”

It should use a clear governance split:

- `workspace_admin`
  - owns risky decisions inside a workspace boundary
- `super_admin`
  - owns global exceptions, cross-workspace risk, and policy-breaking paths

The goal is not bureaucracy.
The goal is to make approval, escalation, override, and audit behavior predictable.

## Core Design Goals

- make approval authority legible to operators and agents
- keep local workspace decisions local where possible
- prevent workspace-scoped roles from silently making global exceptions
- preserve auditability for overrides, escalations, and rejections
- align approval behavior with policy hooks, validation posture, and promotion readiness

## Governance Principle

Authority should follow blast radius.

If the likely impact is contained to one workspace, prefer `workspace_admin`.
If the likely impact crosses workspaces, affects global policy, or changes platform trust posture, require `super_admin`.

This keeps governance proportional to the risk.

## Canonical Roles

### Workspace Admin

Primary purpose:

- govern risky but local work inside a workspace

Typical responsibilities:

- approve workspace-scoped risky actions
- review blocked work in that workspace
- decide on local promotion readiness where policy allows
- inspect workspace delivery status and evidence
- reject or request rework for local risky flows

### Super Admin

Primary purpose:

- govern global, cross-workspace, or exception-path decisions

Typical responsibilities:

- approve global overrides
- decide cross-workspace exception paths
- approve or reject policy-breaking actions that are even eligible for override
- govern unusually risky promotion or rollout paths
- resolve authority conflicts when workspace-level decision is insufficient

## Canonical Scopes

### Workspace Scope

Use when:

- the affected run belongs to one workspace
- the approval concerns only that workspace's artifacts, tools, and delivery posture
- no global policy exception is required

### Global Scope

Use when:

- the action affects multiple workspaces
- the action changes or bypasses global policy
- the action can alter shared platform posture
- the approval acts as an exception beyond normal workspace rights

## Governance Objects

The governance model should work through explicit objects, not loose chat approvals.

Minimum objects:

- `ApprovalRequest`
- `ApprovalDecision`
- `AuthorityContext`
- `OverrideRecord`
- `EscalationRecord`

These should connect cleanly to:

- policy findings
- validation posture
- summary pyramid artifacts
- promotion posture

## Approval Routing Rules

### Default Local Rule

If an action is risky but contained to one workspace, route to `workspace_admin`.

Examples:

- approving a local risky tool action
- accepting a workspace-scoped validation exception
- deciding on local promotion into source review

### Global Escalation Rule

Escalate to `super_admin` when:

- the action crosses workspace boundaries
- the action requires a global policy exception
- the action changes trust posture for shared systems
- the action affects multiple teams or tenants
- the workspace admin lacks legal authority to decide

### No-Silent-Escalation Rule

If escalation occurs, the system should emit a visible escalation artifact and event.
It should never quietly re-route authority without making that obvious.

## Approval Categories

The system should distinguish approval categories rather than treating all approvals as the same.

Suggested categories:

- `risk_acceptance`
- `policy_exception`
- `live_action_authorization`
- `promotion_authorization`
- `rework_override`
- `scope_exception`

Different categories may have different routing defaults.

## What Workspace Admins May Approve

Default allowed categories:

- workspace-scoped risky actions
- local review outcomes
- local promotion into review-ready state
- bounded live actions that do not violate global policy
- local rework or retry exception decisions

Default forbidden categories:

- global policy exceptions
- cross-workspace data or state changes
- shared-system trust changes
- platform-wide rollout exceptions

## What Super Admins May Approve

Default allowed categories:

- global policy exceptions that are explicitly overridable
- cross-workspace exception paths
- protected global live actions
- high-risk promotion exceptions
- authority conflict resolution

Super admins should not automatically bypass evidence requirements.
They govern exceptions, not magical shortcuts.

## Override Semantics

Some policy blocks may be overridable.
Some may not.

The system should distinguish:

- `hard_block`
  - never overridable
- `reviewable_block`
  - requires structured review first
- `approvable_exception`
  - may be overridden by the correct authority

Every override should record:

- actor id
- actor role
- scope
- rationale
- linked evidence
- expiration or permanence when relevant

## Rejection Semantics

Rejection is also a governance action and should be explicit.

A rejection should capture:

- what was denied
- who denied it
- why it was denied
- whether rework is allowed
- whether escalation is still possible

This prevents rejected runs from becoming ambiguous dead ends.

## Escalation Semantics

Escalation should be a first-class transition, not a note in a summary.

Escalation should capture:

- source authority level
- target authority level
- reason for escalation
- blocking rule or risk category
- current delivery posture

Common escalation reasons:

- global policy exception required
- multiple workspaces affected
- uncertainty about authority boundary
- unusual risk concentration

## Relationship To Policy Hooks

Governance and policy are related but different.

Policy decides:

- whether the system may proceed normally

Governance decides:

- whether an exception or approval may legally and operationally clear the path

That means:

- policy may emit `require_approval`
- governance determines which role may answer
- the answer does not erase the original policy record

## Relationship To Validation And Promotion

Validation, approval, and promotion should stay connected.

Governance should not allow:

- approval with no evidence
- promotion with unresolved blocking validation findings unless an explicit exception path exists
- hidden local approvals for global-risk decisions

The promotion packet should reference approval decisions explicitly when approval was required.

## Relationship To Execution Mode

In `interactive` mode:

- governance may be surfaced earlier, while scope and intent are still being shaped

In `factory` mode:

- governance should appear at named boundaries with deterministic routing

The authority rules stay the same in both modes.
Only the interruption pattern changes.

## Required Events

The event taxonomy should support at least:

- `approval.requested`
- `approval.approved`
- `approval.rejected`
- `approval.escalated`
- `approval.overridden`

Each event should include:

- `run_id`
- `issue_identifier` when present
- authority scope
- required approver role
- decider role when resolved
- approval category

## Required Artifacts

Governance actions should emit durable artifacts.

Suggested baseline:

- `approvals/approval_packet.json`
- `approvals/decision.json`
- `approvals/escalation.json`
- `approvals/override_record.json`

These artifacts should feed:

- review surfaces
- promotion posture
- summary rendering
- audit history

## Operator Surface Expectations

Operator views should make the following obvious:

- who is allowed to decide
- why this authority is required
- whether the issue is workspace-scoped or global
- whether escalation has already happened
- whether the current decision is terminal

Avoid vague labels like:

- `needs approval`

Prefer explicit labels like:

- `awaiting workspace admin approval`
- `escalated to super admin`
- `blocked by non-overridable policy`

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define authority, approval category, escalation, and override contracts
- `skyforce-symphony` should route approval requests using workspace vs global scope rules
- `skyforce-command-centre` should show explicit authority context and escalation state
- `skyforce-harness` should preserve approval-related evidence refs in receipts when relevant

## Recommended First Implementation Slice

The first useful slice should be narrow and high-value:

1. define approval category and escalation contracts
2. implement workspace-vs-global routing
3. emit `approval.escalated` when authority changes
4. show `workspace_admin` vs `super_admin` on approval cards
5. record override metadata for exception paths

That is enough to make governance visible and enforceable without overbuilding org structure.

## Recommended Next Specs

This spec should be followed by:

1. `PARALLEL_WORKSPACE_EXECUTION_SPEC.md`
2. `SEMPORT_ADOPTION_BOUNDARY_SPEC.md`
3. `CODE_INTELLIGENCE_RETRIEVAL_SPEC.md`

Together, those would push the remaining multi-agent, upstream-porting, and retrieval gaps forward.
