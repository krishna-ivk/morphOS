# Policy Hooks At Workflow Boundaries Spec

## Why This Spec Exists

`morphOS` already defines:

- software-factory control flow
- validation guardrails
- digital twin validation
- summary rendering
- authority roles and approval routing

What is still missing is a clear answer to this question:

Where, exactly, does policy get to stop, defer, allow, or escalate work?

This spec defines those workflow-boundary hooks.

## Executive Summary

Policy should not behave like a vague background filter.
It should intervene at named workflow boundaries.

For `morphOS`, the correct model is:

- workflows define semantic phases
- policy defines allowed transitions and action posture at boundary points
- approvals resolve some policy blocks, but not all of them
- Durable preserves blocked and deferred execution state
- Symphony uses policy verdicts to choose the next legal step

The result is a system where policy is explicit, auditable, and predictable.

## Core Design Goals

- make policy intervention points visible to humans and runtimes
- separate validation failure from policy denial
- keep authorization distinct from orchestration meaning
- ensure high-risk actions are gated before execution, not explained afterward
- support both deterministic factory execution and human-in-the-loop escalation

## Policy As Boundary Control

Policy should be evaluated at workflow boundaries, not just at arbitrary low-level events.

The key idea is:

- work happens inside phases
- policy decides whether work may cross certain phase boundaries or perform certain risky actions inside them

This keeps policy aligned to delivery flow instead of turning it into scattered rule checks.

## Canonical Boundary Hooks

`morphOS` should define these first-class policy hook points:

1. `intake_policy_gate`
2. `plan_policy_gate`
3. `assignment_policy_gate`
4. `tool_policy_gate`
5. `execution_policy_gate`
6. `validation_policy_gate`
7. `review_policy_gate`
8. `promotion_policy_gate`
9. `live_action_policy_gate`
10. `closeout_policy_gate`

Each hook should have:

- trigger conditions
- expected inputs
- allowed policy verdicts
- required artifact or event outputs

## Hook Meanings

### 1. Intake Policy Gate

Purpose:

- reject malformed, out-of-scope, or unauthorized work before planning begins

Examples:

- missing workspace scope
- unsupported request type
- unsafe seed content
- restricted tenant or workspace target

### 2. Plan Policy Gate

Purpose:

- evaluate whether the proposed plan is allowed to proceed

Examples:

- disallowed target repo
- required approval not yet requested
- forbidden workflow archetype
- missing risk classification

### 3. Assignment Policy Gate

Purpose:

- determine whether selected agents, tools, and connectivity posture are acceptable

Examples:

- coding agent not allowed in sensitive workspace
- required capability missing
- restricted tool assigned to low-trust archetype
- online-write posture not allowed

### 4. Tool Policy Gate

Purpose:

- approve, deny, or defer access to a specific tool action

Examples:

- external write requires approval
- filesystem mutation forbidden outside workspace
- deployment command blocked in factory mode
- network access not allowed under current connectivity posture

### 5. Execution Policy Gate

Purpose:

- guard high-risk execution transitions during work

Examples:

- repeated retries exceed policy budget
- execution attempts to cross repo boundary
- sandbox posture becomes insufficient
- sensitive file paths are touched

### 6. Validation Policy Gate

Purpose:

- decide whether validation posture is sufficient to continue

Examples:

- required quality checks not run
- twin validation required before live integration action
- policy-sensitive findings require review even if tests pass
- evidence artifact incomplete

### 7. Review Policy Gate

Purpose:

- determine whether review is required and who may decide

Examples:

- workspace admin can approve local risky action
- super admin required for global exception
- policy block cannot be cleared by ordinary review

### 8. Promotion Policy Gate

Purpose:

- decide whether validated work may become promotion-ready

Examples:

- approval packet missing
- validation passed but protected target requires extra signoff
- source or target repo mismatch
- artifact completeness not satisfied

### 9. Live Action Policy Gate

Purpose:

- separate safe twin success from permission to touch real systems

Examples:

- Linear update allowed in twin but not live
- Slack escalation allowed only for on-call-approved workflows
- GitHub merge action requires terminal approval state

### 10. Closeout Policy Gate

Purpose:

- ensure runs do not silently close without required evidence

Examples:

- missing summary artifacts
- required audit references absent
- quarantined artifacts unresolved
- unresolved policy block still present

## Allowed Policy Verdicts

Policy hooks should converge on a small set of shared verdicts:

- `allow`
- `warn`
- `defer`
- `block`
- `reject`
- `kill`
- `require_review`
- `require_approval`

Suggested meanings:

- `allow`
  - proceed normally
- `warn`
  - proceed, but record a visible policy finding
- `defer`
  - hold execution until a condition changes
- `block`
  - stop transition at this boundary
- `reject`
  - deny the requested action or transition as invalid
- `kill`
  - terminate the active execution path
- `require_review`
  - route to review gate
- `require_approval`
  - route to approval flow with required authority context

## Boundary Inputs

Each policy evaluation should receive structured inputs rather than vague prompts.

Minimum categories:

- workflow run identity
- execution mode
- workspace and authority scope
- current factory phase
- requested transition or tool action
- risk posture
- validation posture
- twin or live execution mode when relevant
- artifact completeness
- retry and checkpoint state

Policy quality depends on stable inputs.

## Policy Findings Versus Validation Findings

Policy findings and validation findings should be kept distinct.

Validation asks:

- did the work behave correctly?

Policy asks:

- is the system allowed to proceed?

Examples:

- tests can pass while policy blocks deployment
- twin validation can pass while live action remains forbidden
- code can compile while a secret scan blocks promotion

Operator surfaces should show both, not collapse one into the other.

## Approval Is Not The Same As Policy

Approvals are a resolution path for some policy conditions.
They are not the policy system itself.

That means:

- some policy blocks are absolute and cannot be approved away
- some policy blocks become `require_approval`
- some approvals satisfy review posture but do not bypass validation requirements

This keeps human authority inside a governed boundary instead of making it a universal override.

## Factory Mode vs Interactive Mode

In `factory` mode:

- policy should prefer deterministic verdicts
- defer or block before risky live actions
- route to approval only when needed

In `interactive` mode:

- policy may surface warnings and require review earlier
- the operator may choose a different plan or tool path

The same hooks exist in both modes.
The difference is how aggressively the runtime keeps going before human interruption.

## Relationship To Symphony And Durable

The healthy split should be:

- Symphony owns workflow meaning and next-step selection
- Durable owns paused, deferred, blocked, and resumable execution truth
- policy produces the verdict that constrains legal next moves

That means:

- policy must not become the orchestrator
- Symphony must not silently bypass policy hooks
- Durable must preserve the blocked or deferred state created by policy decisions

## Required Events

The event taxonomy should support policy-aware flow with at least:

- `policy.evaluated`
- `policy.blocked`
- `policy.deferred`
- `policy.review_required`
- `policy.approval_required`
- `policy.warned`

Each event should include:

- `run_id`
- boundary hook name
- verdict
- rule id or policy source
- affected action or transition

## Required Artifacts

Policy should emit durable artifacts when it materially alters flow.

Suggested baseline:

- `policy/evaluations.jsonl`
- `policy/latest_verdict.json`
- `policy/pending_requirements.json`
- `policy/quarantine_manifest.json` when quarantine exists

These artifacts should feed:

- summary pyramid rendering
- review packets
- promotion posture
- operator inspection

## Recommended Policy Questions By Boundary

### Before Entering A Phase

- is the next phase allowed?
- is the actor authorized?
- are required prerequisites present?

### Before Using A Tool

- is this tool action allowed here?
- does it need review or approval?
- is twin mode required first?

### Before Promotion Or Closeout

- is the evidence complete?
- is the approval state sufficient?
- are unresolved policy blocks still active?

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define policy verdict, policy finding, and boundary-hook enums
- `skyforce-symphony` should call policy hooks at named factory boundaries and route accordingly
- `skyforce-harness` should surface tool-action and execution metadata in a policy-consumable shape
- `skyforce-command-centre-live` should show `blocked_at`, policy verdicts, and approval requirements as first-class delivery state
- `skyforce-api-gateway` should stabilize those policy and approval projections for operator clients

## Recommended First Implementation Slice

The first useful slice should be narrow and high-leverage:

1. implement `tool_policy_gate`, `validation_policy_gate`, and `promotion_policy_gate`
2. support verdicts `allow`, `block`, `require_review`, and `require_approval`
3. emit `policy.blocked` and `policy.approval_required`
4. render named blocked boundaries in operator views

That is enough to make policy visible without overbuilding the first pass.

## Recommended Next Specs

This spec should be followed by:

1. `GENE_TRANSFUSION_EQUIVALENCE_SPEC.md`
2. `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`
3. `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

Together, those would round out behavioral reuse, execution-mode control, and governance authority.
