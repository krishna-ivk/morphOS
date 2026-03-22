# morphOS v0 Runtime Contracts

This document defines the minimum runtime contracts required for `morphOS v0`.

It exists to answer a practical question:

If the `morphOS v0` core stack is built from:

- `openai/symphony`
- `wavezync/durable`
- `andrewyng/context-hub`
- `ComposioHQ/agent-orchestrator`
- `openai/skills`

then what are the shared objects those systems must agree on?

Without these contracts, each subsystem will invent slightly different meanings for:

- runs
- tasks
- directives
- context
- memory
- skills
- tool actions
- checkpoints
- approvals

That is where integration drift starts.

## Executive Summary

The minimum shared runtime contracts for `morphOS v0` are:

1. `WorkflowRun`
2. `TaskExecution`
3. `Directive`
4. `ContextRef`
5. `MemoryRecord`
6. `SkillRef`
7. `ToolAction`
8. `ExecutionCheckpoint`
9. `ApprovalDecision`

These contracts should be treated as non-negotiable interoperability boundaries between:

- orchestration
- durable execution
- memory/context
- tool execution
- skills
- operator surfaces

## Contract Design Rules

Before defining the objects, the rules should be explicit.

### Rule 1

Every contract must have:

- stable identity
- lifecycle state
- timestamps
- issue/run correlation when relevant

### Rule 2

Every contract must support provenance.

That means the system should be able to answer:

- where did this object come from
- what produced it
- what it influenced

### Rule 3

Every contract must support approval and policy boundaries where applicable.

### Rule 4

Every contract must be usable in:

- live runtime state
- receipts/artifacts
- observability surfaces
- operator UI

### Rule 5

No subsystem should silently redefine the meaning of a shared contract.

## 1. WorkflowRun

### Purpose

`WorkflowRun` is the canonical object for a running or completed workflow instance.

It is the highest-level execution contract.

### Owned By

Primary owner:

- `Symphony`

Durability owner:

- `Durable`

Observed by:

- Command Centre
- CLI
- validation/publish surfaces

### Minimum Fields

- `run_id`
- `workflow_template_id`
- `issue_identifier`
- `status`
- `started_at`
- `updated_at`
- `ended_at`
- `current_task_execution_id`
- `connectivity_mode`
- `context_refs`
- `active_directive_ids`
- `execution_checkpoint_id`

### Allowed Status Values

- `queued`
- `running`
- `paused`
- `blocked`
- `completed`
- `failed`
- `cancelled`

### Key Responsibility

`WorkflowRun` answers:

- what workflow is this
- what issue does it belong to
- what state is it in now
- what is it blocked on

## 2. TaskExecution

### Purpose

`TaskExecution` is the unit of actual work inside a workflow.

It represents one step, one delegated branch, or one concrete execution slot.

### Owned By

Primary owner:

- `Symphony`

Durability owner:

- `Durable`

### Minimum Fields

- `task_execution_id`
- `run_id`
- `step_id`
- `step_type`
- `assigned_agent_id`
- `status`
- `attempt`
- `started_at`
- `updated_at`
- `ended_at`
- `input_context_refs`
- `output_artifact_refs`
- `failure_reason`

### Allowed Status Values

- `pending`
- `running`
- `waiting_for_input`
- `waiting_for_approval`
- `completed`
- `failed`
- `skipped`
- `cancelled`

### Key Responsibility

`TaskExecution` answers:

- what work unit is being executed
- by whom
- with what inputs
- with what outputs

## 3. Directive

### Purpose

`Directive` is the control-layer instruction or intervention object.

This is how the runtime represents:

- approval gates
- operator-required interventions
- pause/resume instructions
- policy-driven control events

### Owned By

Primary owner:

- `Symphony`

Observed by:

- Command Centre
- CLI

Potentially constrained by:

- policy engine

### Minimum Fields

- `directive_id`
- `run_id`
- `issue_identifier`
- `kind`
- `summary`
- `status`
- `created_at`
- `updated_at`
- `requested_by`
- `target_scope`
- `payload`

### Allowed Kinds

- `approval`
- `pause`
- `resume`
- `replan`
- `operator_attention`
- `policy_block`

### Allowed Status Values

- `pending`
- `active`
- `completed`
- `cancelled`
- `rejected`

### Key Responsibility

`Directive` answers:

- what intervention or control instruction exists
- who or what must respond to it
- whether it is still blocking work

## 4. ContextRef

### Purpose

`ContextRef` is the shared reference object for context used by the runtime.

This is not the entire context payload.
It is the pointer and metadata contract.

### Owned By

Produced by:

- `Context Hub`
- Symphony
- execution/runtime layers

Consumed by:

- all agents
- CLI
- operator UI

### Minimum Fields

- `context_id`
- `kind`
- `layer`
- `access_label`
- `title`
- `summary`
- `source_uri`
- `updated_at`

### Required Layer Values

- `reference`
- `operational`
- `memory`

### Key Responsibility

`ContextRef` answers:

- what context object exists
- what type it is
- what trust boundary applies
- where it comes from

## 5. MemoryRecord

### Purpose

`MemoryRecord` is the durable knowledge object.

This is not ephemeral execution state.
It is retained learning or reusable knowledge.

### Owned By

Primary owner:

- memory/context subsystem

Potentially curated by:

- human operators
- learning or synthesis agents

### Minimum Fields

- `memory_id`
- `kind`
- `title`
- `summary`
- `confidence`
- `access_label`
- `provenance_refs`
- `related_context_refs`
- `created_at`
- `updated_at`

### Allowed Kinds

- `episodic`
- `semantic`
- `task`
- `policy`
- `communication`

### Key Responsibility

`MemoryRecord` answers:

- what long-term knowledge was retained
- how trustworthy it is
- what artifacts or context justify it

## 6. SkillRef

### Purpose

`SkillRef` is the contract for reusable capability modules.

It allows workflows and agents to refer to skills without embedding their full implementation details.

### Owned By

Primary owner:

- skill system

Referenced by:

- archetypes
- workflow templates
- runtime assignment logic

### Minimum Fields

- `skill_id`
- `name`
- `version`
- `description`
- `provider`
- `input_contract_refs`
- `output_contract_refs`
- `required_tools`
- `required_context_layers`
- `updated_at`

### Key Responsibility

`SkillRef` answers:

- what skill is required
- what version it is
- what it expects and produces

## 7. ToolAction

### Purpose

`ToolAction` is the runtime contract for an external action or tool invocation.

This is the object that bridges workflow intent into real-world systems.

### Owned By

Primary owner:

- tool execution layer

Governed by:

- workflow directives
- policy checks
- approval rules

### Minimum Fields

- `tool_action_id`
- `run_id`
- `task_execution_id`
- `tool_provider`
- `tool_name`
- `status`
- `requested_at`
- `started_at`
- `ended_at`
- `requested_by_agent_id`
- `request_payload_ref`
- `result_artifact_refs`
- `approval_required`

### Allowed Status Values

- `planned`
- `pending_approval`
- `running`
- `completed`
- `failed`
- `cancelled`

### Key Responsibility

`ToolAction` answers:

- what external action is being attempted
- whether it was approved
- what result it produced

## 8. ExecutionCheckpoint

### Purpose

`ExecutionCheckpoint` is the resumability object for durable execution.

It represents the persisted point from which a workflow or task can continue.

### Owned By

Primary owner:

- `Durable`

Observed by:

- Symphony
- operator surfaces

### Minimum Fields

- `checkpoint_id`
- `run_id`
- `task_execution_id`
- `status`
- `snapshot_ref`
- `created_at`
- `resumable_until`
- `reason`

### Allowed Status Values

- `created`
- `resumed`
- `expired`
- `invalidated`

### Key Responsibility

`ExecutionCheckpoint` answers:

- where recovery can resume from
- whether the saved state is still usable

## 9. ApprovalDecision

### Purpose

`ApprovalDecision` is the durable record of a human or policy decision on a directive or tool action.

### Owned By

Produced by:

- operator UI
- policy engine

Applied by:

- Symphony
- durable execution layer

### Minimum Fields

- `approval_decision_id`
- `directive_id`
- `issue_identifier`
- `decision`
- `decided_by`
- `decided_at`
- `reason`
- `resulting_status`

### Allowed Decisions

- `approved`
- `rejected`
- `cancelled`
- `deferred`

### Key Responsibility

`ApprovalDecision` answers:

- what was decided
- who decided it
- when it changed runtime behavior

## Contract Ownership Matrix

The ownership boundary should be:

- `WorkflowRun`
  - Symphony + Durable
- `TaskExecution`
  - Symphony + Durable
- `Directive`
  - Symphony
- `ContextRef`
  - Context subsystem + runtime publishers
- `MemoryRecord`
  - memory subsystem
- `SkillRef`
  - skills subsystem
- `ToolAction`
  - tool execution layer
- `ExecutionCheckpoint`
  - Durable
- `ApprovalDecision`
  - operator/policy layer, then applied by runtime

## Required Cross-Contract Links

To keep lineage usable, these links should exist:

- `WorkflowRun -> TaskExecution`
- `WorkflowRun -> Directive`
- `WorkflowRun -> ContextRef`
- `TaskExecution -> ToolAction`
- `TaskExecution -> ExecutionCheckpoint`
- `Directive -> ApprovalDecision`
- `MemoryRecord -> ContextRef`
- `MemoryRecord -> Artifact provenance`
- `SkillRef -> input/output contracts`

## What Must Be Observable

Every contract should eventually be visible, directly or indirectly, in:

- CLI inspection
- operator UI
- receipts and artifacts
- runtime observability APIs

If a contract cannot be observed, it cannot be debugged.

## What Must Be Persisted

At minimum, persistence should cover:

- `WorkflowRun`
- `TaskExecution`
- `Directive`
- `ExecutionCheckpoint`
- `ApprovalDecision`
- relevant `ToolAction` history

`ContextRef` and `MemoryRecord` persistence may depend on subsystem design, but they must still be durable when used as part of workflow lineage.

## Recommended Next Step

After this document, the next architecture layer should be:

1. define the authority boundary between `Symphony` and `Durable`
2. define the wrapping model for `Context Hub`
3. define skill registration and versioning rules
4. define tool-action approval rules
5. align Skyforce shared contracts to these objects incrementally

## Related Docs

- [MORPHOS_V0_CORE_STACK.md](MORPHOS_V0_CORE_STACK.md)
- [schemas.md](../../architecture/schemas.md)
- [CONTEXT_ARCHITECTURE.md](../../architecture/CONTEXT_ARCHITECTURE.md)
- [morphos_vs_skyforce_evaluation.md](../../morphos_vs_skyforce_evaluation.md)
