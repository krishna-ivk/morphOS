# Tool Execution Engine Spec

This document defines how governed `ToolAction` objects execute through provider
adapters with approval-aware flow and durable result projection.

It extends the existing `ToolAction` contract and registry doctrine into runtime
execution semantics.

It is primarily grounded in:

- `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
- `MORPHOS_V0_RUNTIME_CONTRACTS.md`
- `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
- `EXECUTION_RECEIPT_SCHEMA_SPEC.md`

The goal is to make tool execution:

- policy-safe
- approval-aware
- adapter-driven
- idempotent under retry
- observable by operators
- durable as evidence

without allowing execution adapters to become a shadow policy engine.

## Why This Spec Exists

Current docs already define:

- what tools are (`ToolDescriptor` and registry)
- what a `ToolAction` is as a shared runtime contract
- where control points and approvals live in the factory flow
- how execution evidence should be represented (`execution_receipt`)

What is still under-specified is the exact engine behavior between:

- a planned `ToolAction`
- policy and approval gates
- concrete provider invocation
- durable projection of results back into run state and artifacts

Without this spec:

- adapters can drift into policy decisions
- approval handling becomes provider-specific
- retries create duplicate side effects
- `ToolAction` status transitions become inconsistent
- operator visibility into tool effects weakens

This spec exists to prevent that.

## Executive Summary

The correct execution model is:

1. `ToolAction` is created and correlated to `run_id` and `task_execution_id`.
2. The engine resolves the `ToolDescriptor` from the registry and validates
   invocation shape.
3. Policy and approval posture are evaluated before provider invocation.
4. If approval is required, flow pauses at `pending_approval` through the named
   control path (`tool_gate`) until an `ApprovalDecision` is applied.
5. Once allowed, the engine invokes the selected provider adapter.
6. Adapter output is normalized into a canonical result envelope.
7. The engine projects outcomes into durable artifacts (`result_artifact_refs`,
   receipts, state patches, or events) according to the descriptor's
   `result_projection_kind`.
8. `ToolAction` ends in `completed`, `failed`, or `cancelled` with evidence and
   lineage preserved.

Key rule:

- policy and approvals decide whether execution may happen
- adapters decide how execution happens
- the engine decides how outcomes become durable runtime truth

## Engine Responsibilities And Non-Goals

## Responsibilities

The execution engine should:

- enforce `ToolAction` lifecycle and status transitions from
  `MORPHOS_V0_RUNTIME_CONTRACTS.md`
- resolve `ToolDescriptor` and adapter binding from
  `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
- apply approval-aware gating at `tool_gate` in line with
  `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
- invoke provider adapters with deterministic request envelopes
- normalize provider responses into canonical success/failure structures
- project results into durable artifacts and references
- emit receipt-grade evidence compatible with
  `EXECUTION_RECEIPT_SCHEMA_SPEC.md`
- preserve replay-safe and retry-safe semantics via idempotency controls

## Non-Goals

The execution engine should not:

- define new workflow authority rules outside existing policy and admin doctrine
- perform semantic planning or action decomposition
- own tool discovery doctrine (registry does)
- silently upgrade or bypass approval requirements
- hide provider-side failures behind synthetic success status
- replace validation/review/promotion control points

## ToolAction Lifecycle

The external lifecycle uses the shared statuses defined in
`MORPHOS_V0_RUNTIME_CONTRACTS.md`:

- `planned`
- `pending_approval`
- `running`
- `completed`
- `failed`
- `cancelled`

## Lifecycle Semantics

### `planned`

- `ToolAction` exists but has not passed execution gate checks.
- Request payload reference and tool identity should be stable.

### `pending_approval`

- action is blocked at `tool_gate`
- no provider invocation may occur while in this state
- linked directive/approval context should be discoverable

### `running`

- provider adapter invocation has started
- retries should increment attempt metadata without losing lineage

### `completed`

- provider execution succeeded
- projection completed according to `result_projection_kind`
- `result_artifact_refs` are attached when applicable

### `failed`

- provider call, normalization, or projection failed irrecoverably for current
  policy/retry rules
- failure reason and evidence references should be durable

### `cancelled`

- execution was intentionally stopped (for example approval rejected, run
  aborted, directive cancellation)
- cancellation reason should remain auditable

## Status Transition Rules

Allowed baseline transitions:

- `planned -> pending_approval`
- `planned -> running`
- `pending_approval -> running`
- `pending_approval -> cancelled`
- `running -> completed`
- `running -> failed`
- `running -> cancelled`

Transitions should be monotonic for each attempt and timestamped.

## Approval-Aware Execution Flow

Approval handling should remain system-governed and never adapter-specific.

## Flow

1. Receive `ToolAction` in `planned` with request payload reference.
2. Load `ToolDescriptor` and current policy snapshot.
3. Evaluate whether approval is required from policy + risk posture + workspace
   governance.
4. If approval is required:
   - set `ToolAction.status = pending_approval`
   - link to directive/approval packet context
   - wait for `ApprovalDecision`
5. Apply decision:
   - `approved` -> proceed to `running`
   - `rejected` or `cancelled` -> set `ToolAction.status = cancelled`
   - `deferred` -> remain `pending_approval`
6. Invoke adapter only after allowed posture is explicit.

## Control-Flow Alignment

This flow aligns to named factory control points:

- `tool_gate` for pre-invocation approval/policy blocking
- upstream `plan_gate` and downstream `validation_gate` remain outside adapter
  scope

## Rule

Approval state must be represented as runtime control state, not hidden as a
provider timeout or retry loop.

## Adapter/Provider Boundary

The provider boundary should keep policy and invocation concerns separated.

## Engine Boundary

The engine owns:

- descriptor resolution
- policy/approval gate integration
- lifecycle state updates
- idempotency and retry orchestration
- durable projection and receipt linkage

## Adapter Boundary

Each adapter should own:

- translation from canonical tool request to provider-specific call shape
- provider authentication/transport handling (within allowed runtime context)
- provider response capture and normalization scaffolding
- provider error classification into canonical categories

Adapters should not own:

- approval policy decisions
- cross-tool orchestration
- final authority on `ToolAction` lifecycle semantics

## Provider-Agnostic Request Envelope

Each adapter invocation should receive a canonical envelope containing at least:

- `tool_action_id`
- `run_id`
- `task_execution_id`
- `tool_id` and provider identity
- stable payload reference or payload hash
- attempt number
- idempotency key
- connectivity posture

This preserves consistent tracing across provider kinds (`local_program`,
`mcp_server`, `http_api`, `cli_wrapper`, and others defined by registry
doctrine).

## External Result Artifact Projection

Projection translates raw provider output into runtime-usable, durable evidence.

## Projection Inputs

Projection should use:

- `ToolDescriptor.result_projection_kind`
- normalized adapter result envelope
- execution status and failure class
- current run/task lineage context

## Supported Projection Kinds

As defined by registry doctrine:

- `none`
- `artifact_ref`
- `state_patch`
- `receipt`
- `event_only`

## Projection Rules

- `none`
  - record minimal outcome metadata and status
- `artifact_ref`
  - write or reference durable artifact and attach to `result_artifact_refs`
- `state_patch`
  - emit bounded runtime patch plus provenance link
- `receipt`
  - produce execution evidence compatible with
    `EXECUTION_RECEIPT_SCHEMA_SPEC.md`
- `event_only`
  - emit event stream evidence when durable artifact content is unnecessary

## Receipt Compatibility

When projection includes receipt generation, artifacts should include enough
evidence to satisfy receipt invariants:

- actual work attempted
- changed outputs or declared no-change
- validation posture if run during this action
- final execution status
- attributable producer and timestamps

## Retry, Failure, And Idempotency Rules

## Failure Classes

Failures should be classified at least as:

- `policy_blocked`
- `approval_denied`
- `provider_transient`
- `provider_permanent`
- `projection_failed`
- `runtime_cancelled`

This supports deterministic retry behavior and operator triage.

## Retry Policy

- retries are allowed only for classes marked retryable (typically transient)
- each retry should preserve the same `tool_action_id` and increment attempt
  metadata
- retry limits should be explicit per tool family or workflow profile
- exhaustion of retry budget should end in `failed` with class and evidence

## Idempotency

For side-effecting providers, idempotency keys should be stable per logical
attempt group and include:

- `tool_action_id`
- payload hash
- provider/tool identity

Rule:

- duplicate dispatch with same idempotency key should not create duplicate
  external side effects where provider supports idempotency
- if provider lacks native idempotency, the engine should use local dedupe and
  conservative retry posture

## Cancellation

Cancellation must be explicit and auditable, including:

- cancellation source (approval rejection, operator abort, policy intervention)
- timestamp
- whether provider call had started
- whether compensation or follow-up action is required

## Operator Observability

Operator and CLI surfaces should be able to inspect each `ToolAction` as a
first-class execution unit.

Minimum observable fields:

- `tool_action_id`, `run_id`, `task_execution_id`
- requested tool/provider identity
- request intent summary and payload reference
- lifecycle status and attempt count
- approval requirement and decision linkage
- failure class and reason when failed/cancelled
- projection outputs (`result_artifact_refs`, receipt refs, state/event refs)
- key timestamps (`requested_at`, `started_at`, `ended_at`)

## Observability Rule

If an operator cannot answer why a tool action ran, was blocked, or produced a
side effect, the execution record is incomplete.

## Relationship To Existing Specs

This spec operationalizes and does not replace:

- `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
  - discovery, descriptor doctrine, risk metadata, projection kinds
- `MORPHOS_V0_RUNTIME_CONTRACTS.md`
  - canonical `ToolAction`, `Directive`, and `ApprovalDecision` contracts
- `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
  - phase and control-point model, including `tool_gate`
- `EXECUTION_RECEIPT_SCHEMA_SPEC.md`
  - evidence artifact shape and invariants

## Ownership

### `morphOS` owns

- execution-engine doctrine
- lifecycle and boundary semantics
- projection and observability expectations

### `skyforce-symphony` owns

- orchestration of `ToolAction` requests within run/task control flow
- directive and approval routing around `tool_gate`

### `skyforce-harness` owns

- concrete execution engine implementation
- provider adapters and invocation runtime
- result normalization and projection plumbing

### `skyforce-core` owns

- shared `ToolAction` and related contract hardening
- schema and CLI visibility helpers for engine outputs

### `skyforce-command-centre` owns

- operator-facing rendering of tool action status, approvals, and evidence

## First Implementation Slice

The first slice should prove one end-to-end governed `ToolAction` transaction
without broad provider coverage.

Recommended slice:

1. Support `ToolAction` lifecycle transitions for one low/medium-risk tool
   family used in normal coding flow.
2. Resolve tool metadata from registry and enforce invocation schema checks.
3. Implement approval-aware pause/resume at `pending_approval` with decision
   application.
4. Execute via one adapter path and capture normalized result envelope.
5. Project outcome into durable `result_artifact_refs` and a compatible
   execution receipt artifact.
6. Expose tool action observability fields in CLI/operator surfaces.

Success criteria:

- one action can be planned, gated, approved/rejected, executed, projected, and
  audited end-to-end
- retries do not produce duplicate side effects for the tested path
- blocked and failed states are distinguishable and operator-visible

## Bottom Line

The correct `morphOS` tool execution layer is:

- contract-bound
- approval-aware
- adapter-driven
- projection-explicit
- retry-safe
- operator-auditable

It should turn `ToolAction` from a shared object definition into a reliable
execution reality while preserving policy and approval authority boundaries.
