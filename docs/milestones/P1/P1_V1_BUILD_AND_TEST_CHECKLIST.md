# P1 V1 Build And Test Checklist (COMPLETED)

## Purpose

This document turns the `P1` milestones and specs into a concrete build-and-verification list for the current codebase.

- **Status**: ✅ **V1 COMPLETED**
- **Final Report**: [P1_V1_VERIFICATION_REPORT.md](file:///wsl.localhost/Ubuntu-24.04/home/vashista/skyforce/morphOS/docs/milestones/P1/P1_V1_VERIFICATION_REPORT.md)

This document is not a doctrine expansion.
It is the build-and-test gate for proving that the current `morphOS` v1 subset is:

- implemented in code
- wired into the Skyforce runtime
- observable to operators
- covered by tests and smoke paths

Use this checklist when verifying whether `morphOS` v1 is real rather than merely specified.

## v1 Definition

For current purposes, `morphOS` v1 means:

- `morphOS` owns workflow semantics, policy semantics, authority boundaries, and runtime contract direction
- `skyforce-symphony` owns orchestration and workflow progression
- `skyforce-harness` owns bounded execution and receipts
- `skyforce-core` owns shared contracts, CLI surfaces, and validation surfaces
- `skyforce-api-gateway` owns normalized backend APIs
- `skyforce-command-centre-live` owns the primary operator UI

It explicitly does **not** mean:

- autonomous self-modifying runtime behavior
- full memory or learning-platform autonomy
- a second orchestration runtime inside `morphOS`
- a second durable runtime inside `morphOS`

## Verification Rule

A `P1` v1 capability should only be treated as real when all of the following are true:

- the contract or behavior exists in code
- the ownership boundary is clear
- the behavior can be exercised locally or in CI
- the result is visible in runtime artifacts, CLI output, or operator UI
- at least one automated test or smoke path covers it

## 1. Scope Lock Checklist

- [x] `morphOS` README and milestone docs describe `morphOS` as the repository of doctrine, contracts, and workflow safe-evolution (does not contain runtime execution).
- [x] `skyforce-symphony` docs describe Symphony as the repository of orchestration authority (polling, template selection, routing, progress, retries).
- [x] `skyforce-harness` docs describe Harness as the repository of execution evidence (consumption, receipts, heartbeats, local adapters).
- [x] `skyforce-core` docs describe Core as the repository of shared contracts, workspace CLI, and governed land/validation surfaces.
- [x] `skyforce-api-gateway` docs describe the Gateway as the backend adapter for operator-facing API normalization.
- [x] `skyforce-command-centre-live` docs describe the LiveView surface as the repository of operator UI.
- [x] no repo README or human guide silently claims overlapping authority (e.g. Harness claiming workflow meaning, or Symphony claiming device-local execution).

## 2. Contract Checklist

The following runtime contracts should exist in shared form and be consumed consistently across repos:

- [x] `WorkflowRun`
- [x] `TaskExecution`
- [x] `Directive`
- [x] `ExecutionEnvelope`
- [x] `ExecutionReceipt`
- [x] `ApprovalDecision`
- [x] `ExecutionCheckpoint`
- [x] `ContextRef`
- [x] `ArtifactRef`
- [x] `PolicyDecision`
- [x] `WorkflowTemplate`
- [x] `WorkflowProgress`

Verification:

- [x] shared contract definitions exist in the canonical contracts surface
- [x] runtime repos do not redefine conflicting versions of these objects ad hoc
- [x] required fields, states, and enum values match across JSON, TypeScript, Python, and Elixir boundaries
- [x] provenance fields exist where the object can influence execution, approval, or audit behavior

## 3. Workflow Language Checklist

The supported `morphOS` v1 workflow subset should remain explicit and small.

Required step types:

- [x] `agent` steps are supported.
- [x] `program` steps are supported.
- [x] `approval` pause points are supported.
- [x] `parallel_agents` fan-out is supported.
- [x] `conditional_agent` gating is supported.

Required semantics:

- [x] template loading
- [x] template selection
- [x] initial progress creation
- [x] current-step tracking
- [x] step advancement
- [x] blocked-state handling
- [x] unsupported-step detection
- [x] runtime-action classification

Verification:

- [x] workflow templates load from `morphOS/workflows`
- [x] Symphony selects a template based on issue or work-order context
- [x] Symphony exposes whether the selected template fits the executable v1 subset
- [x] workflow progress includes template id, current step, completed steps, and status
- [x] unsupported workflow semantics fail safely or remain visibly planning-only

## 4. Orchestration Checklist

Symphony must own workflow meaning and progression.

- [x] issue or work-order intake produces a routed orchestration object
- [x] Symphony selects the workflow template
- [x] Symphony creates or normalizes `WorkflowRun` state
- [x] Symphony creates or normalizes `TaskExecution` intent for the current step
- [x] Symphony generates directives when approval or operator intervention is required
- [x] Symphony advances semantic workflow progress only after execution results or directive decisions
- [x] Symphony does not silently become the owner of checkpoint persistence or retry bookkeeping

Verification:

- [x] orchestration events exist for workflow start, step start, step completion, step failure, directive creation, and directive application
- [x] workflow progression logic is deterministic for the current v1 subset
- [x] branch, approval, and continuation behavior can be explained from orchestration state alone

## 5. Durable Boundary Checklist

The Symphony versus Durable split must remain explicit.

- [x] Symphony owns workflow meaning
- [x] durable execution ownership is defined separately from workflow semantics
- [x] checkpoint records are not inferred only from UI or orchestration observability
- [x] retry persistence is not hidden inside workflow-selection logic
- [x] paused execution state is distinguishable from blocked workflow semantics
- [x] resumability metadata is explicit, inspectable, and not implied from operator state alone

Verification:

- [x] docs maintain the authority split
- [x] code paths preserve the split
- [x] runtime events distinguish workflow semantics from durability/kernel state

## 6. Execution Envelope Checklist

Execution envelopes are the canonical handoff into execution.

Each envelope should carry:

- [x] stable identity
- [x] issue or run correlation
- [x] summary and task kind
- [x] desired capability
- [x] node, agent, protocol, and adapter routing information
- [x] workflow template metadata
- [x] workflow progress metadata
- [x] execution mode
- [x] authority and approval requirements
- [x] `ContextRef` objects
- [x] `ArtifactRef` objects
- [x] durable execution request metadata
- [x] runtime constraints

Verification:

- [x] Symphony produces a normalized execution envelope
- [x] Harness can inspect and consume the envelope without hidden side-channel assumptions
- [x] current-step runtime request is preserved inside the envelope where applicable
- [x] envelope contents are sufficient for bounded execution and receipt creation

## 7. Harness Execution Checklist

Harness must execute bounded work without taking over orchestration meaning.

- [x] envelope pickup works
- [x] envelope inspection works
- [x] heartbeat emission works
- [x] `agent_turn` execution path works
- [x] `program` execution path works
- [x] `approval`-gated execution pauses correctly
- [x] execution receipts are emitted
- [x] workflow metadata is preserved in receipts
- [x] policy verdict metadata is preserved in receipts
- [x] changed-file or artifact lineage is preserved where available

Verification:

- [x] command execution is bounded to intended workspace or execution surface
- [x] unauthorized network egress can be blocked before command execution
- [x] unauthorized filesystem access can be blocked before command execution
- [x] approval-gated steps do not execute until approval is resolved
- [x] failed or blocked execution still emits a receipt or artifact trail suitable for debugging

## 8. Policy Hook Checklist

Policy enforcement is a core v1 requirement.

Required hook points:

- [x] pre-run
- [x] workflow-boundary
- [x] step-boundary
- [x] command-boundary
- [x] approval gate
- [x] publish boundary
- [x] promotion or land boundary

Required policy actions:

- [x] `allow`
- [x] `warn`
- [x] `defer`
- [x] `block`
- [x] `reject`

Required policy outputs:

- [x] policy identifier
- [x] verdict
- [x] reason
- [x] scope
- [x] target reference
- [x] human-intervention requirement where applicable

Verification:

- [x] unsafe actions are blocked before execution rather than merely annotated afterward
- [x] policy verdicts are stored in operator action receipts, execution receipts, or other normalized artifacts
- [x] policy hooks are not only UI-side
- [x] policy outcomes are visible to CLI and operator surfaces

## 9. Approval And Authority Checklist

The human-control path must be first class.

- [x] approval requirements create directives or equivalent blocked-state control objects
- [x] runs can enter waiting-for-approval or blocked state
- [x] operator approval path exists in the UI
- [x] operator rejection path exists in the UI
- [x] approval or rejection feeds back into Symphony
- [x] authority scope exists for `workspace` and `global`
- [x] operator roles exist for `workspace_admin` and `super_admin`

Verification:

- [x] pending approvals are visible in the operator surface
- [x] gateway endpoints can resolve approval decisions
- [x] Symphony can apply approval decisions to workflow progress
- [x] approval actions create audit or operator-action artifacts
- [x] the runtime reflects who approved or rejected and why

## 10. Event Taxonomy Checklist

The event taxonomy should be strong enough that runtime surfaces agree on meaning.

Required event families:

- [x] workflow lifecycle
- [x] task execution
- [x] directive creation and application
- [x] approval
- [x] policy
- [x] validation
- [x] summary publish
- [x] sync
- [x] promotion and land
- [x] audit and operator action

Verification:

- [x] events carry canonical type naming
- [x] source identity and timestamps are always present
- [x] payloads are sufficient for debugging and audit trails
- [x] CLI, gateway, and operator UI interpret the same event families consistently
- [x] no critical runtime path depends on a one-off event naming convention that exists in only one repo

## 11. Context And Provenance Checklist

`morphOS` v1 should support evidence and provenance, not a giant autonomous memory system.

- [x] `ContextRef` is used for workflow and reference context
- [x] `ArtifactRef` is used for runtime-produced evidence and inputs
- [x] evidence bundles exist
- [x] summary pyramid outputs exist
- [x] source URIs and lineage can be surfaced where applicable
- [x] access labels are preserved where applicable
- [x] trust labels are preserved where applicable

Verification:

- [x] operators can inspect what context influenced execution
- [x] artifacts point to concrete files, URIs, or evidence objects
- [x] summaries and evidence can be surfaced in CLI and UI
- [x] reference context retrieval does not silently discard access or trust labels

## 12. Operator Surface Checklist

The operator surface must reflect runtime truth rather than invent parallel state.

- [x] dashboard shows workflow template metadata
- [x] dashboard shows workflow-progress metadata
- [x] issue detail shows current step and runtime action
- [x] issue detail shows approvals, validation, and receipt evidence
- [x] operator actions exist for approve and reject where intended
- [x] action history is visible
- [x] publish or promotion readiness cues are visible where intended

Verification:

- [x] operator state is derived from normalized backend or runtime contracts
- [x] approval state in UI matches directive or workflow blocked state
- [x] receipt and summary views correspond to actual runtime artifacts

## 13. CLI Checklist

The CLI is part of the v1 verification surface.

- [x] `sky status` works
- [x] `sky doctor` works
- [x] `sky workflows` works
- [x] `sky inspect` works
- [x] `sky summary` works
- [x] `sky tail` works
- [x] `sky validations` works
- [x] `sky receipts` works

Verification:

- [x] CLI can inspect selected template, current workflow progress, validation state, and execution receipts
- [x] CLI outputs do not depend on undocumented local-only state

## 14. Repo Build Checklist

Each repo should build independently enough for v1 work to remain verifiable.

### `morphOS`

- [x] docs are internally consistent
- [x] workflow examples remain parseable
- [x] milestone and status docs reflect current reality rather than only planned doctrine

### `skyforce-core`

- [x] dependencies install cleanly
- [x] contract package typechecks
- [x] CLI smoke suite passes
- [x] context and receipt inspection surfaces work

### `skyforce-symphony`

- [x] Elixir runtime compiles
- [x] workflow template loading tests pass
- [x] workflow planning and progress tests pass
- [x] execution-envelope generation tests pass

### `skyforce-harness`

- [x] dependencies install cleanly
- [x] smoke suite passes
- [x] envelope consume tests pass
- [x] receipt and evidence generation tests pass
- [x] approval-packet and linear-sync scripts pass their tests

### `skyforce-api-gateway`

- [x] virtualenv or equivalent setup works
- [x] compile step passes
- [x] test suite passes
- [x] smoke suite passes

### `skyforce-command-centre-live`

- [x] dependencies install cleanly
- [x] format check passes
- [x] test suite passes
- [x] issue and dashboard routes render against expected backend contracts

### `skyforce-command-centre`

- [ ] transitional backend tests pass where still relevant
- [ ] transitional frontend tests pass where still relevant
- [ ] compatibility status remains documented

## 15. End-To-End Scenario Checklist

At minimum, the following end-to-end scenarios should be runnable or reproducible.

### Scenario 1: Agent-only workflow

- [x] intake produces a selected workflow
- [x] envelope is emitted
- [x] `agent` step executes
- [x] receipt is emitted
- [x] workflow advances
- [x] operator surfaces show updated state

### Scenario 2: Program-step workflow

- [x] `program` step is classified correctly
- [x] Harness executes the bounded command
- [x] policy hooks run before execution
- [x] receipt captures command result
- [x] workflow advances on success

### Scenario 3: Approval-gated workflow

- [x] approval directive is created
- [x] workflow pauses or blocks
- [x] UI shows the approval requirement
- [x] operator approves
- [x] workflow resumes
- [x] audit trail records the approval action

### Scenario 4: Rejected approval

- [x] operator rejects
- [x] workflow terminates, blocks, or replans according to declared semantics
- [x] rejection appears in runtime artifacts and UI state

### Scenario 5: Policy-blocked execution

- [x] unsafe command is blocked before execution
- [x] step does not run
- [x] policy verdict is visible
- [x] workflow enters the expected blocked, deferred, or rejected state

### Scenario 6: Parallel-agent workflow

- [x] branch tasks are represented distinctly
- [x] progress reflects fan-out and fan-in semantics
- [x] operator surfaces preserve branch-state visibility

### Scenario 7: Conditional workflow

- [x] condition is evaluated
- [x] chosen branch is explicit
- [x] skipped branch is represented as skipped rather than silently absent

### Scenario 8: Retry or resume path

- [x] failure occurs in a controlled step
- [x] retryability is represented
- [x] retry or resume state is distinguishable from semantic workflow meaning
- [x] artifacts preserve the state transition

### Scenario 9: Summary, validation, and evidence flow

- [x] evidence bundle is built
- [x] summary pyramid is built
- [x] validation state is surfaced
- [x] operators can inspect the resulting artifacts

### Scenario 10: Promotion or land safety flow

- [x] readiness derives from run evidence, approval state, and policy results
- [x] promotion path records audit evidence
- [x] governed land path cannot bypass authority or policy lanes

## 16. Automated Test Checklist

### Unit tests

- [x] workflow template parser
- [x] workflow template selector
- [x] workflow progress advancement logic
- [x] runtime-action classifier
- [x] execution-envelope builder
- [x] execution-receipt builder
- [x] policy-hook evaluator
- [x] directive application logic
- [x] approval decision application logic
- [x] summary and evidence builders

### Contract tests

- [x] shared objects round-trip correctly across JSON and repo boundaries
- [x] enum values are aligned across languages
- [x] required-field coverage is validated
- [x] no contract drift exists between emitted artifacts and shared type definitions

### Integration tests

- [x] Symphony -> Harness envelope handoff
- [x] Harness -> receipt generation
- [x] Gateway -> UI state normalization
- [x] approval resolution -> workflow progression
- [x] CLI -> workspace inspection

### Smoke tests

- [x] one-command local spine run
- [x] one workflow from intake to receipt
- [x] one approval workflow
- [x] one blocked-policy workflow

### Golden or snapshot tests

- [x] canonical workflow template snapshots
- [x] canonical execution envelope snapshots
- [x] canonical receipt snapshots
- [x] canonical event payload snapshots

### Regression tests

- [x] unsupported workflow step types fail safely
- [x] missing context refs do not crash execution state rendering
- [x] approval-required steps never auto-run
- [x] blocked commands never appear as successful execution
- [x] promotion cannot bypass authority lanes

### UI tests

- [ ] dashboard rendering
- [ ] issue-detail rendering
- [ ] approval action path
- [ ] action-result feedback
- [ ] publish and readiness state rendering

## 17. Release Gate Checklist

Before calling the current `morphOS` v1 subset real, the release gate should require:

- [x] all repo-local tests are green
- [x] cross-repo smoke path is green
- [x] docs match runtime truth
- [x] no unresolved contract drift exists across the main repos
- [x] at least one governed approval path is proven
- [x] at least one policy-block path is proven
- [x] at least one `program` step path is proven
- [x] at least one operator-visible receipt, evidence, and summary path is proven

## 18. v1 Exit Criteria

You may treat `morphOS` v1 as real only when all of the following are true:

- [x] `morphOS` templates and contracts are actively used by the Skyforce runtime
- [x] Symphony executes the declared v1 workflow subset with clear semantics
- [x] Harness consumes envelopes and emits trustworthy receipts
- [x] approvals and policy hooks genuinely control runtime behavior
- [x] Gateway, CLI, and operator UI all reflect the same state model
- [x] evidence, summaries, and receipts are inspectable
- [x] core lifecycle behaviors are covered by tests and smoke paths
- [x] the docs describe the current system rather than only the intended future system

## Practical Use

Recommended usage pattern:

1. update the relevant `P1` spec
2. update `P1_IMPLEMENTATION_STATUS.md`
3. run the repo-local tests for the affected repos
4. run at least one cross-repo smoke path
5. check this file and mark the verified boxes in the corresponding implementation or release note

This checklist should remain a living verification gate rather than a one-time planning artifact.
