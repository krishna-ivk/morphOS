# Software Factory Control Flow Spec

This document defines the control flow for `morphOS` as a software factory.

It is the fifth follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `fabro-sh/fabro`
- StrongDM software-factory techniques
- the morphOS agent model
- the git-native work ledger
- the tool registry and action discovery model

The goal is to define a control flow that is:

- legible to humans
- executable by the runtime
- resilient under interruption
- explicit about gates and intervention
- aligned with software delivery language

without turning the system into either a black-box agent swarm or a bureaucratic
approval maze.

## Why This Spec Exists

The current morphOS docs already define:

- workflows
- agent actions
- durable boundaries
- filesystem state
- tool surfaces

What is still missing is the factory-shaped control flow that ties those pieces
together into one delivery loop.

Without that flow:

- orchestration stays too step-centric
- human interventions feel ad hoc
- promotion posture appears late
- approvals are treated as isolated events instead of flow control
- the operator surface lacks a clean mental model

This spec exists to solve that.

## Executive Summary

The correct software-factory control flow is:

1. intake
2. planning
3. assignment
4. execution
5. validation
6. review
7. promotion
8. closeout

At every phase, the runtime should know:

- who owns the next move
- what evidence exists
- what gate is active
- what the current delivery posture is

The key rule is:

- agents perform work
- Symphony advances factory flow
- Durable preserves execution truth
- operators intervene at explicit control points

## Factory Control States

The factory should expose these canonical high-level states:

1. `intake`
2. `planning`
3. `ready_to_run`
4. `running`
5. `awaiting_validation`
6. `awaiting_review`
7. `ready_for_promotion`
8. `promoted`
9. `closed`
10. `blocked`
11. `aborted`

### Notes

- these are flow-level delivery states, not low-level task states
- low-level runtime states may be more detailed
- operator surfaces should default to these simpler control states first

## The Factory Loop

## 1. Intake

Purpose:

- accept a ticket, seed, or work request

Required outputs:

- normalized run identity
- workflow template choice or pending selection
- execution mode
- workspace scope

Gate question:

- is the work sufficiently defined to enter planning?

## 2. Planning

Purpose:

- translate intent into a valid execution plan

Required outputs:

- plan record
- task and action breakdown
- initial context refs
- expected outputs

Gate question:

- is the plan acceptable to proceed?

### Human intervention options

- revise scope
- request replan
- approve plan

## 3. Assignment

Purpose:

- bind semantic actions to available agents and tool surfaces

Required outputs:

- assignment records
- action-to-tool posture
- policy snapshot

Gate question:

- do we have the right agents, tools, permissions, and connectivity posture to
  start?

## 4. Execution

Purpose:

- perform assigned work and emit evidence

Required outputs:

- signals
- receipts
- artifact refs
- checkpoints

Gate question:

- is the work proceeding, blocked, or failed?

### Control options

- continue
- retry
- reroute
- pause
- escalate

## 5. Validation

Purpose:

- determine whether the outputs satisfy expected behavior

Required outputs:

- validation record
- check results
- evidence refs
- promotion posture update

Gate question:

- does the work satisfy the quality threshold?

### Control options

- accept validation
- request rework
- allow retry
- block promotion

## 6. Review

Purpose:

- route human or policy review where needed

Required outputs:

- review request or approval packet
- authority routing context
- review decision record

Gate question:

- is this work approved to proceed toward promotion or release?

### Control options

- approve
- reject
- request rework
- escalate to super-admin

## 7. Promotion

Purpose:

- convert validated workspace outputs into safe source-repo proposals or
  equivalent promoted state

Required outputs:

- promotion record
- proposed branch or packet
- linked summaries and evidence

Gate question:

- is the work ready to move from workspace state into source-of-truth review
  or delivery?

## 8. Closeout

Purpose:

- finalize the run with durable evidence and final posture

Required outputs:

- summary artifacts
- evidence artifact
- final ledger posture
- final status projection

Gate question:

- is the run fully auditable and complete?

## Control Points

Control points are where humans or policy may alter the path intentionally.

The first required control points should be:

1. `plan_gate`
2. `tool_gate`
3. `validation_gate`
4. `review_gate`
5. `promotion_gate`

### Rule

If the system is blocked, the control point must be named.

Avoid vague blocked states like:

- “waiting”
- “stuck”
- “needs input”

Prefer:

- `blocked_at: validation_gate`
- `blocked_at: review_gate`

## Intervention Model

An intervention is a deliberate control-plane change to a run’s trajectory.

Interventions may be:

- human
- policy-driven
- deterministic runtime backstops

### Allowed intervention types

- `pause`
- `resume`
- `replan`
- `reroute`
- `retry`
- `approve`
- `reject`
- `abort`

### Rule

Interventions should create:

- a directive or decision record
- a ledger entry
- an updated control state

## Delivery Language Mapping

Operator-facing control flow should prefer delivery language.

Recommended user-facing terms:

- `ticket`
- `active work`
- `quality checks`
- `review queue`
- `delivery status`
- `ready for promotion`
- `published update`

Internal structures may still use:

- `WorkflowRun`
- `Directive`
- `ToolAction`
- `ExecutionCheckpoint`

## Control Flow Artifacts

Every factory run should be able to point to:

- intake record
- current plan
- current assignment set
- latest checkpoint
- latest validation record
- latest review decision
- latest promotion posture
- summary and evidence artifacts

### Rule

The factory state should be reconstructable from durable artifacts plus current
runtime projections.

## Branching Rules

The factory loop is not always linear.

Allowed common branches:

- replan after failed review
- retry after failed validation
- reroute after agent failure
- pause for approval
- abort after unrecoverable policy block

### Rule

Branches must re-enter the main loop at an explicit phase.

Example:

- failed validation -> rework -> assignment -> execution -> validation

Avoid:

- hidden retries with no visible phase change

## Minimal State Transition Table

Recommended high-level transitions:

- `intake` -> `planning`
- `planning` -> `ready_to_run`
- `ready_to_run` -> `running`
- `running` -> `awaiting_validation`
- `awaiting_validation` -> `awaiting_review`
- `awaiting_review` -> `ready_for_promotion`
- `ready_for_promotion` -> `promoted`
- `promoted` -> `closed`

Exception transitions:

- any state -> `blocked`
- any state -> `aborted`
- `awaiting_validation` -> `running` via rework
- `awaiting_review` -> `planning` via replan

## Deterministic Backstops

Some control-flow tasks should not rely entirely on the model remembering them.

The first good candidates are:

- summary emission
- evidence file emission
- approval packet emission
- promotion packet generation
- final delivery posture projection

### Rule

Creative work may be agent-led.
Deterministic closeout should have runtime backstops.

## Authority Model

The control flow must align with the workspace-admin and super-admin model.

### Workspace admin should own

- local risky approvals
- review of blocked work in that workspace
- local policy-constrained promotion decisions

### Super admin should own

- cross-workspace exceptions
- global policy overrides
- unusually risky promotion or rollout decisions

## Relationship To Existing Specs

This spec depends on:

- `AGENT_SIGNAL_AND_ACTION_MODEL.md`
- `GIT_NATIVE_WORK_LEDGER_SPEC.md`
- `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
- `UNIVERSAL_DELIVERY_TERMINOLOGY.md`

It complements rather than replaces:

- workflow template specs
- durable execution handoff contracts
- approval and promotion contracts

## Ownership

### `morphOS` owns

- the control-flow doctrine
- phase meanings
- named control points

### `skyforce-symphony` owns

- runtime phase progression
- directive and intervention routing

### `skyforce-core` owns

- shared phase and control-point contracts
- CLI projections

### `skyforce-command-centre` owns

- operator rendering of control states, review queues, and intervention actions

### `skyforce-harness` owns

- execution and validation evidence feeding the flow

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
2. `VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md`
3. `DIGITAL_TWIN_VALIDATION_SPEC.md`

## Bottom Line

The correct morphOS software-factory control flow is:

- phase-based
- gate-aware
- delivery-language-friendly
- intervention-explicit
- evidence-backed

It should feel like a real production workflow with clear ownership and clear
next actions, not like a hidden agent conversation.
