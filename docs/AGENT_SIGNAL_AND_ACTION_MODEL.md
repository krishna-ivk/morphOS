# Agent Signal And Action Model

This document defines how agents should behave as runtime participants in
`morphOS v0`.

It is the first follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `openai/symphony`
- `wavezync/durable`
- `agentjido/jido`

The goal is not to copy any one upstream framework.
The goal is to give Skyforce a clean, Elixir-friendly semantic model for:

- what an agent is
- what an action is
- what a signal is
- how directives relate to agents
- where state transitions stop and side effects begin

## Why This Spec Exists

The current morphOS docs define:

- cells
- workflows
- directives
- durable execution boundaries

What is still under-specified is the runtime behavior of an agent between those
layers.

Without that missing middle layer, systems drift into confusing overlaps:

- agents become mini-orchestrators
- tools become pseudo-agents
- directives become ad hoc messages
- events and signals get used interchangeably
- side effects happen before policy and durability boundaries are clear

This spec exists to prevent that.

## Executive Summary

The clean model is:

- `Agent`
  - a named runtime participant with capabilities, bounded tools, and a
    lifecycle
- `Action`
  - a unit of intended work an agent knows how to perform
- `Signal`
  - a typed state-bearing message that agents and runtime components emit or
    consume
- `Directive`
  - a control-layer instruction created by orchestration or policy, not by
    arbitrary peer agents

The key rule is:

- agents decide within their bounded role
- Symphony decides workflow meaning
- Durable decides persistence and resumability
- tools perform external or deterministic side effects

## Core Objects

## 1. Agent

### Meaning

An `Agent` is a long-lived runtime identity with:

- a role
- a capability boundary
- a bounded tool surface
- a lifecycle
- a signal interface

An agent is not just a prompt.
It is a runtime participant.

### What an Agent Owns

- role-local reasoning
- transforming inputs into outputs
- proposing state changes through outputs and signals
- deciding how to perform its assigned action within policy and tool limits

### What an Agent Must Not Own

- workflow graph transitions
- durable checkpoint truth
- global policy interpretation
- direct mutation of unrelated runs
- unrestricted peer-to-peer coordination

## 2. Action

### Meaning

An `Action` is the unit of work an agent is asked to perform.

Examples:

- interpret a product vision
- decompose a feature into tasks
- implement a scoped code change
- review an execution plan
- diagnose a failed validation result

An action is not the same thing as a tool invocation.
An action may use zero or more tools.

### Design Rule

Actions should be semantically meaningful and stable across implementations.

Prefer:

- `plan_feature`
- `implement_task`
- `review_patch`
- `diagnose_failure`

Avoid:

- `call_bash`
- `run_python`
- `do_step_7`

## 3. Signal

### Meaning

A `Signal` is a typed message that communicates a meaningful state fact across
runtime boundaries.

Signals are lighter-weight than full artifact payloads and more semantic than
raw log lines.

Examples:

- `agent.started`
- `agent.progress`
- `agent.blocked`
- `agent.output_ready`
- `agent.failed`
- `action.requested`
- `action.completed`

### Design Rule

Signals describe runtime truth.
They should not smuggle arbitrary, untyped prose in place of structured state.

## 4. Directive

### Meaning

A `Directive` is a control-layer instruction produced by orchestration, policy,
or operator action.

Examples:

- pause
- resume
- approval required
- replan
- operator attention required

### Design Rule

Directives are not peer messages between ordinary agents.
They belong to the control plane.

## Control Split

## Symphony Owns

- workflow meaning
- task selection
- action assignment
- directive generation
- branch and join semantics
- escalation routing

## Durable Owns

- persistence of in-flight execution
- retry attempts
- checkpoint lifecycle
- resumability truth
- expiry and invalidation

## Agents Own

- role-local execution of assigned actions
- production of outputs and signals
- bounded tool usage within policy

## Tools Own

- deterministic execution of external or local operations
- explicit side effects
- machine-readable results when possible

## Required Lifecycle

Every runtime agent should follow this semantic lifecycle:

1. `registered`
2. `available`
3. `assigned`
4. `running`
5. `blocked`
6. `completed`
7. `failed`
8. `cooldown`
9. `offline`

### Notes

- `registered` means known to the runtime
- `available` means eligible for assignment
- `assigned` means Symphony has bound the agent to an action
- `running` means the agent is actively performing that action
- `blocked` means progress cannot continue without an external condition
- `completed` and `failed` are terminal per action, not necessarily per agent
- `cooldown` allows bounded rest or backoff
- `offline` means the runtime should not route work there

## State Transition Rule

Agents may transition their local execution state.
They may not redefine workflow state.

For example:

- an agent may emit `agent.blocked`
- Symphony decides whether the related `TaskExecution` becomes
  `waiting_for_input`, `waiting_for_approval`, or `failed`

## Signal Families

The first useful signal families should be:

### Agent lifecycle

- `agent.registered`
- `agent.assigned`
- `agent.started`
- `agent.heartbeat`
- `agent.blocked`
- `agent.completed`
- `agent.failed`

### Action lifecycle

- `action.requested`
- `action.accepted`
- `action.started`
- `action.progress`
- `action.output_ready`
- `action.completed`
- `action.failed`

### Tool boundary

- `tool.requested`
- `tool.allowed`
- `tool.blocked`
- `tool.completed`
- `tool.failed`

### Policy and control

- `directive.created`
- `directive.applied`
- `policy.blocked`
- `approval.requested`
- `approval.resolved`

## Action Boundary vs Tool Boundary

This distinction is critical.

### Action

An action is semantic work.

Examples:

- implement login API
- review execution plan
- summarize operator findings

### Tool

A tool is an execution mechanism.

Examples:

- run tests
- apply patch
- create branch
- post Linear comment

### Rule

Actions may call tools.
Tools must not silently define the action’s meaning.

If the system loses this distinction, policy and observability become muddy.

## Side-Effect Rule

There are two classes of action outcomes:

### Pure state transition outcomes

Examples:

- task decomposition
- review findings
- plan generation
- confidence update

These should primarily emit:

- artifacts
- structured outputs
- signals

### Side-effecting outcomes

Examples:

- editing files
- creating a PR
- publishing a summary
- calling an external API
- deploying a build

These must cross a tool or durable execution boundary.

Agents should not perform these as hidden implicit behavior.

## Assignment Model

Symphony should assign work to agents using an explicit action request.

Minimum assignment shape:

- `assignment_id`
- `run_id`
- `task_execution_id`
- `agent_id`
- `action_type`
- `input_context_refs`
- `input_artifact_refs`
- `expected_outputs`
- `policy_snapshot_ref`
- `requested_at`

This may later become a first-class shared contract, but the semantic shape
should be frozen now.

## Output Model

An agent should produce three possible outputs:

1. `structured_result`
2. `artifact_refs`
3. `signals`

### `structured_result`

The immediate semantic result of the action.

### `artifact_refs`

Files or receipts that durable surfaces, validation, or operators may inspect.

### `signals`

Short-lived runtime facts that move the orchestration state forward.

## Failure Model

Agent failure should be classified at least into:

- `input_invalid`
- `tool_blocked`
- `policy_blocked`
- `execution_failed`
- `timeout`
- `dependency_unavailable`
- `human_input_required`

### Rule

An agent failure is not automatically a workflow failure.
It is first a signal to Symphony.
Symphony then decides:

- retry
- reroute
- escalate
- block
- fail the task

## Jido-Inspired But Localized Principles

The strongest ideas to preserve from the Elixir agent references are:

- clear action boundaries
- explicit signal emission
- separation of orchestration from execution
- state-machine-friendly process semantics
- supervision-aware recovery

The local adaptation rule is:

- preserve the semantics
- do not blindly copy framework vocabulary where it conflicts with morphOS
  contracts

## Relationship To Existing morphOS Contracts

This spec does not replace:

- `WorkflowRun`
- `TaskExecution`
- `Directive`
- `ExecutionCheckpoint`

It refines the behavior between them.

### Mapping

- `WorkflowRun`
  - macro execution context
- `TaskExecution`
  - workflow-owned unit of work
- `Agent assignment`
  - binding of a task execution to an agent action
- `Signal`
  - runtime fact emitted during that execution
- `Directive`
  - control-plane intervention or requirement

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `GIT_NATIVE_WORK_LEDGER_SPEC.md`
2. `FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md`
3. `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`

## Bottom Line

The correct agent model for morphOS is:

- agents perform bounded semantic actions
- signals communicate runtime truth
- directives come from the control plane
- tools perform explicit side effects
- Symphony owns workflow meaning
- Durable owns persistence and recovery

That separation is what keeps the system legible as it grows.
