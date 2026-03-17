# Symphony and Durable Authority Boundary

This document defines the authority boundary between:

- `openai/symphony`
- `wavezync/durable`

for `morphOS v0`.

This is the critical boundary that must be made explicit before introducing a real `ExecutionCheckpoint` contract into the runtime.

Without this boundary, the system will drift into one of two failure modes:

1. Symphony quietly becomes both orchestrator and durable kernel
2. Durable quietly becomes a second workflow engine

Both outcomes are architecturally wrong.

## Executive Summary

The correct split is:

- `Symphony` owns **workflow meaning**
- `Durable` owns **durable execution state**

Said another way:

- Symphony decides what should happen next
- Durable decides what is still alive, resumable, persisted, retrying, or recoverable

This means:

- Symphony owns planning, delegation, and workflow transitions
- Durable owns checkpoints, retries, resumption, and execution persistence

`ExecutionCheckpoint` must be a Durable-owned contract.
It should not be inferred from Symphony observability alone.

## Core Principle

Orchestration and durability are separate powers.

### Symphony Power

Symphony has authority over:

- workflow graph interpretation
- step ordering
- branch transitions
- delegation decisions
- approval routing
- task selection
- issue-to-workflow mapping

### Durable Power

Durable has authority over:

- persisted execution records
- retry scheduling
- resumability
- checkpoint lifecycle
- timeout recovery
- crash recovery
- long-running task state

### Why This Matters

A workflow system can know what should happen next without knowing how to persist it.

A durable engine can know how to persist and resume work without understanding the meaning of the workflow graph.

That separation is healthy.

## Clear Ownership Table

### Symphony Owns

- `WorkflowRun` semantic status
- `TaskExecution` semantic meaning
- workflow template interpretation
- directive generation
- approval gate semantics
- selection of target agent, node, or step
- orchestration events such as:
  - `workflow.step.started`
  - `workflow.step.completed`
  - `workflow.step.failed`

### Durable Owns

- `ExecutionCheckpoint`
- retry timers
- retry attempt bookkeeping
- resumable execution snapshots
- in-flight task persistence
- interrupted-task recovery
- execution expiration and invalidation

### Shared But Not Equal

Some objects are shared but with different responsibilities.

#### `WorkflowRun`

- Symphony owns semantic state
- Durable owns persistence and recoverability metadata

#### `TaskExecution`

- Symphony owns step identity and intended behavior
- Durable owns runtime persistence, attempts, and resumption data

#### `Directive`

- Symphony owns creation and semantic meaning
- Durable may persist or replay related blocked-state execution, but does not decide the directive’s meaning

## What Symphony Must Never Own

Symphony must not become the source of truth for:

- checkpoint creation
- retry scheduling policy execution
- persisted recovery snapshots
- resumable execution snapshots
- timeout ownership
- crash recovery bookkeeping

Symphony may ask for these things.
It must not silently absorb them.

## What Durable Must Never Own

Durable must not become the source of truth for:

- workflow graph semantics
- agent selection logic
- step-type semantics
- approval-gate meaning
- policy reasoning
- memory/context interpretation

Durable may execute and persist.
It must not reinterpret workflow meaning.

## Operational Flow

The healthy runtime flow should be:

1. Symphony selects a workflow and current step
2. Symphony emits a `TaskExecution` request into the durable layer
3. Durable starts the actual durable execution record
4. Durable persists attempts and checkpoints as needed
5. Durable reports execution state back to Symphony
6. Symphony decides semantic next-step transitions
7. Durable either:
   - completes
   - retries
   - pauses
   - resumes
   - invalidates checkpoints

That means the layers cooperate, but they do not collapse into each other.

## Retry Responsibility

Retry meaning and retry execution must be separated.

### Symphony Decides

- whether a failed step is retryable in workflow terms
- whether to retry the same step, branch, or agent
- whether to escalate instead of retry

### Durable Decides

- where the retry timer lives
- how retry attempts are persisted
- what checkpoint is reused
- whether the execution record is resumable

## Checkpoint Responsibility

Checkpoint semantics should be:

### Symphony Can Know

- that a step is resumable or not
- that a workflow is currently blocked waiting to resume

### Durable Must Own

- `checkpoint_id`
- snapshot storage
- checkpoint creation timestamp
- resumable-until timestamp
- checkpoint invalidation
- restoration of execution state

Therefore:

- Symphony can expose checkpoint metadata
- Durable must own checkpoint truth

## Approval Responsibility

Approvals are a useful example of the split.

### Symphony Owns

- when an approval gate exists
- which workflow step requires it
- what effect approval has on the workflow graph

### Durable Owns

- persistence of paused or blocked execution state while the approval is pending
- restoration of the paused execution after approval

### Operator Layer Owns

- the actual UI/action path for approve/reject

## Event Responsibility

### Symphony Emits

Semantic orchestration events:

- `workflow.started`
- `workflow.step.started`
- `workflow.step.completed`
- `workflow.step.failed`
- `directive.created`
- `directive.applied`

### Durable Emits

Durability and runtime-state events:

- `execution.checkpoint.created`
- `execution.checkpoint.invalidated`
- `execution.retry.scheduled`
- `execution.retry.started`
- `execution.resumed`
- `execution.expired`

This distinction matters because event consumers should know whether they are reacting to:

- workflow meaning
- kernel state

## Required Data Flow Between Them

The minimum contract handoff should be:

### Symphony -> Durable

- `WorkflowRun` identity
- `TaskExecution` identity and semantic intent
- retry eligibility / policy hints
- timeout hints
- approval-block status

### Durable -> Symphony

- execution status
- retry attempt count
- checkpoint ids
- checkpoint state
- resumability state
- final task execution outcome

## Required Shared Contracts

The `morphOS v0` contracts map to the boundary like this:

- `WorkflowRun`
  - shared
  - semantic authority: Symphony
  - persistence authority: Durable

- `TaskExecution`
  - shared
  - semantic authority: Symphony
  - persistence authority: Durable

- `ExecutionCheckpoint`
  - owned by Durable

- `Directive`
  - owned by Symphony

- `ApprovalDecision`
  - produced by operator/policy layer
  - applied by Symphony
  - may unblock Durable-held execution state

## Bad Smells

If any of these are true, the boundary is drifting.

### Smell 1

Symphony is generating checkpoint ids by itself.

### Smell 2

Durable is deciding which workflow step comes next.

### Smell 3

Symphony retry logic exists without durable persisted attempt state.

### Smell 4

Durable is mutating workflow graph status without Symphony mediation.

### Smell 5

Operator surfaces show checkpoint data that has no durable owner.

## Recommended Implementation Order

To make this real in Skyforce:

1. define the Durable-facing execution request contract
2. define the Durable execution status callback/event contract
3. introduce real `ExecutionCheckpoint` records from the durable side
4. then expose checkpoint metadata in Symphony observability
5. finally flow that checkpoint state into CLI and Command Centre

## What Not To Do Next

Do not:

- fake checkpoints in presenter payloads
- infer retry state purely from orchestration events
- let observability become the source of truth for resumability

That would produce a convincing demo but the wrong architecture.

## Recommended Next Step

After this document, the next architecture or implementation step should be:

1. define a Durable execution request contract
2. define a Durable execution status/checkpoint response contract
3. map those contracts into `skyforce-core`
4. only then add `ExecutionCheckpoint` projections into Symphony

## Related Docs

- [MORPHOS_V0_CORE_STACK.md](/home/vashista/skyforce/morphOS/docs/MORPHOS_V0_CORE_STACK.md)
- [MORPHOS_V0_RUNTIME_CONTRACTS.md](/home/vashista/skyforce/morphOS/docs/MORPHOS_V0_RUNTIME_CONTRACTS.md)
- [runtime_topology_spec.md](/home/vashista/skyforce/morphOS/docs/runtime_topology_spec.md)
- [event_bus_spec.md](/home/vashista/skyforce/morphOS/docs/event_bus_spec.md)
- [policy_engine_spec.md](/home/vashista/skyforce/morphOS/docs/policy_engine_spec.md)
