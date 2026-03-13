# morphOS Buildability Plan

This document translates the current `morphOS` specification set into a practical Skyforce implementation plan.

It answers four questions:

1. What is already built from the `morphOS` direction?
2. What can we build next with high confidence?
3. What still needs clarity before implementation?
4. What should explicitly not be built yet?

This plan assumes the current repo split:

- `morphOS`: specification, archetypes, workflow language, policy language
- `skyforce-core`: shared contracts, CLI, validation tooling
- `skyforce-symphony`: orchestration runtime
- `skyforce-harness`: execution adapters and receipts
- `skyforce-command-centre`: human control plane

## Executive Summary

### Already built

The following `morphOS`-aligned capabilities now exist in the Skyforce runtime:

- workflow template loading from `morphOS/workflows`
- template selection per issue
- lightweight workflow progress state in Symphony
- runtime action classification for the current workflow step
- execution envelopes carrying workflow template metadata
- CLI and dashboard visibility for template and step progress
- initial shared contracts for events, policy, cells, workflows, and connectivity

### Build next

The strongest next build targets are:

- explicit execution of `program` steps
- explicit execution of `approval` steps
- event taxonomy alignment across repos
- policy evaluation hooks at workflow boundaries
- agent archetype import into Symphony Agent Hub

### Needs clarity

The biggest unresolved areas are:

- memory architecture
- learning loop behavior
- human authority model
- rich workflow graph semantics
- conflict resolution in policy evaluation

### Do not build yet

Do not build these yet:

- autonomous self-modifying code loops
- a second orchestrator inside `morphOS`
- a second event bus runtime inside `morphOS`
- a full memory platform before contracts and policy settle

## What Is Already Built

## 1. Workflow Template Loading

### Status

Built.

### Where it lives

- `morphOS/workflows/*.yaml`
- `skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_store.ex`
- `skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_planner.ex`

### What works now

- Symphony loads workflow templates from the `morphOS` repo
- Symphony selects a template per issue
- supported v1 step types are tracked explicitly
- template metadata is exposed in Symphony observability

### Current limit

Templates are selected and tracked, but not yet executed as full graph programs.

## 2. Workflow Progress And Runtime Action Mapping

### Status

Built as a lightweight runtime layer.

### Where it lives

- `skyforce-symphony/elixir/lib/symphony_elixir/orchestrator.ex`
- `skyforce-symphony/elixir/lib/symphony_elixir/execution_envelope.ex`
- `skyforce-core/scripts/sky.mjs`
- `skyforce-command-centre/frontend/src/App.jsx`

### What works now

- dispatch creates initial workflow progress
- Codex continuation turns advance the current step index
- Symphony exposes `workflow_progress` in live running state
- the current step is classified into a runtime action:
  - `agent_turn`
  - `program_runner`
  - `parallel_agent_fanout`
  - `conditional_agent_gate`
  - `approval_gate`
- CLI and dashboard show template, step progress, and runtime action

### Current limit

This is runtime-aligned planning, not full step execution.

## 3. Shared Contracts

### Status

Partially built.

### Where it lives

- `skyforce-core/packages/contracts/src/index.ts`

### What works now

The contracts package includes `morphOS`-aligned foundations for:

- event envelopes
- agent cells
- workflow templates and step types
- policy rules and decisions
- connectivity modes and capability flags
- context and artifact references

### Current limit

Not every `morphOS` concept is mapped yet, and some contracts are still broad rather than fully enforced.

## 4. Execution Envelope Bridge

### Status

Built.

### Where it lives

- `skyforce-symphony/elixir/lib/symphony_elixir/execution_envelope.ex`
- `skyforce-harness/scripts/consume-execution-envelope.mjs`
- `skyforce-harness/scripts/inspect-execution-envelope.mjs`

### What works now

- selected workflow template metadata is embedded into execution envelopes
- workflow progress and runtime action metadata are preserved
- Harness inspection and receipt flows can carry those fields

### Current limit

Harness receives the plan metadata, but does not yet execute `program` and `approval` steps directly from it.

## 5. Human Visibility

### Status

Built.

### Where it lives

- `skyforce-core/scripts/sky.mjs`
- `skyforce-command-centre/main.py`
- `skyforce-command-centre/frontend/src/App.jsx`

### What works now

- `sky workflows`
- `sky inspect`
- `sky summary`
- `sky tail`
- Command Centre Fleet Health execution cards

Humans can already see:

- selected template
- current step
- runtime action for the current step
- execution stage
- validation status
- summary sync state

### Current limit

The operator can see the intended runtime action, but cannot yet trigger all step types as first-class workflow actions.

## What We Can Build Next With High Confidence

## 1. Program Step Execution

### Why it is buildable now

The current templates already define deterministic `program` steps, and the runtime action classification is in place.

### What to build

In `skyforce-symphony`:

- a `program_runner` execution path
- bounded command execution metadata
- step completion events

In `skyforce-harness`:

- program execution receipt schema
- command allowlist or policy gate integration

### Confidence

High.

## 2. Approval Step Execution

### Why it is buildable now

Approval is already a natural fit for `command-centre`, and the workflow model now identifies approval gates explicitly.

### What to build

In `skyforce-symphony`:

- approval step pause state
- approval wait/resume behavior

In `skyforce-command-centre`:

- approval step card and action
- resume signal back into Symphony

### Confidence

High.

## 3. Event Taxonomy Alignment

### Why it is buildable now

The event model is already strong in `morphOS`, and Symphony already emits rich observability events.

### What to build

In `skyforce-core`:

- canonical event type families

In `skyforce-symphony` and `skyforce-harness`:

- event naming and payload alignment

In `skyforce-command-centre`:

- event stream sections grouped by event family

### Confidence

High.

## 4. Agent Archetype Import

### Why it is buildable now

`morphOS/agents/*.md` already describe the intended agent roles, and Symphony already has Agent Hub.

### What to build

- a machine-readable archetype manifest derived from agent docs
- import into Symphony Agent Hub
- mapping to capabilities, allowed task kinds, and trust policies

### Confidence

Medium-high.

## 5. Policy Hooking

### Why it is buildable now

The contract side is far enough along to begin guarded enforcement.

### What to build

- workflow boundary checks in Symphony
- execution-side checks in Harness
- policy decision visibility in Command Centre

### Confidence

Medium-high for v1 enforcement hooks.

## What Needs Clarity Before We Build It

## 1. Full Workflow Graph Semantics

### Why it needs clarity

We still do not have one tight answer for:

- step input and output typing
- branch merge behavior
- compensation logic
- retry ownership per step
- resumability semantics across all step kinds

### Current buildability

Medium for a strict subset.
Low for a full graph runtime.

## 2. Memory Architecture

### Why it needs clarity

The memory direction is compelling, but the implementation boundary is still open.

Open questions:

- file vs database vs graph storage
- retention and TTL
- who may write memory
- privacy boundaries
- retrieval strategy

### Current buildability

Medium-low.

## 3. Learning Loop

### Why it needs clarity

We still need a precise model for:

- what counts as learning
- who approves learned changes
- whether learning creates docs, issues, prompts, policies, or code

### Current buildability

Medium for proposal artifacts.
Low for autonomous adaptation.

## 4. Human Authority Model

### Why it needs clarity

The role taxonomy exists, but authority boundaries do not yet.

Open questions:

- who can approve what
- what can be overridden
- what must escalate
- which actions are operator-only

### Current buildability

Low-medium.

## 5. Policy Conflict Resolution

### Why it needs clarity

We still need stronger definitions for:

- multi-rule matches
- partial approvals
- per-node overrides
- deferred vs blocked outcomes
- human override rules

### Current buildability

Medium for a narrow engine.
Low for a full policy platform.

## What We Should Not Build Yet

## 1. Autonomous Self-Modifying Code Loops

These would bypass trust and validation too early.

Build proposal-driven evolution first:

- observe
- propose
- validate
- require approval
- execute

## 2. A Second Orchestrator Inside morphOS

Symphony is already the orchestration runtime.

`morphOS` should stay the specification authority, not become a duplicate runtime.

## 3. A Separate Event Bus Runtime Inside morphOS

`morphOS` should define the event model.
Skyforce should implement it.

## 4. A Full Memory Platform Before Policy And Contracts Settle

Without stable contracts, memory becomes a dumping ground and governance risk.

## 5. Full Human-Role Runtime Without A Clear Authority Matrix

Approval and escalation logic should not be guessed into existence.

## Recommended Build Order

1. Finish explicit execution for `program` steps.
2. Add explicit pause/resume handling for `approval` steps.
3. Align event taxonomy across repos.
4. Add first policy evaluation hooks.
5. Import agent archetypes into Symphony Agent Hub.
6. Define the authority model for human roles.
7. Design memory and learning on top of the stabilized runtime.

## Decision Summary

### Build now

- deterministic workflow step execution
- approval handling
- event taxonomy alignment
- policy hook integration
- agent archetype import

### Needs clarity

- memory
- learning
- full graph semantics
- human authority
- advanced policy conflicts

### Do not build yet

- self-modifying code loops
- duplicate orchestrator runtime
- duplicate event bus runtime
- premature memory platform

## Human Reading Order

For someone new to the platform, read in this order:

1. `README.md`
2. `docs/SKYFORCE_RUNTIME_OVERVIEW.md`
3. `docs/morphos_vs_skyforce_evaluation.md`
4. this buildability plan
5. `docs/ROADMAP.md`
