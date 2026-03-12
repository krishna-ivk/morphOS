# morphOS Buildability Plan

This document translates the current `morphOS` specification set into an implementation plan.

It answers three questions:

1. What can we build now with high confidence?
2. What needs clarification before we build it?
3. What should not be built yet because the current spec is too abstract or too risky?

This plan assumes the current repo landscape:

- `morphOS` is the specification and operating-model repo
- `skyforce-core` is the shared contracts and CLI repo
- `skyforce-symphony` is the orchestration runtime
- `skyforce-harness` is the execution/runtime adapter layer
- `skyforce-command-centre` is the operator UI

## Executive Summary

### Build now

The strongest immediately buildable areas from `morphOS` are:

- shared event taxonomy
- workflow template loader contract
- policy rule model
- agent archetype to runtime registration mapping
- connectivity mode model
- topology classification model

These are specification-heavy but concrete enough to implement.

### Needs clarity

The areas that need sharper decisions first are:

- memory architecture
- learning loop behavior
- human role model
- exact workflow graph semantics
- policy evaluation engine behavior under conflicts

These are promising, but not yet tight enough for clean implementation.

### Do not build yet

The areas we should explicitly avoid building right now are:

- unconstrained self-evolution
- autonomous self-modifying code loops
- a second orchestrator runtime inside `morphOS`
- a separate event bus runtime inside `morphOS`
- a duplicate schema system outside `skyforce-core`

## What We Can Build Now

## 1. Event Taxonomy and Event Envelope

### Why it is buildable now

The event bus spec is concrete enough already:

- named event families exist
- delivery expectations are described
- publishing/subscription rules are defined
- persistence intent is clear

### What to build

In `skyforce-core`:

- `EventEnvelope`
- `EventType`
- `EventSource`
- `EventDeliveryMode`
- `DeferredEvent`
- `DeadLetterEvent`

In `skyforce-symphony`:

- event emission aligned to `workflow.*`, `agent.*`, `task.*`, `policy.*`

In `skyforce-harness`:

- event emission aligned to execution pickup, adapter execution, result write, heartbeat, and failure

In `skyforce-command-centre`:

- event stream panels
- event filters by issue, agent, node, protocol

### Confidence

High.

### Dependencies

- shared contracts only

## 2. Workflow Template Loader

### Why it is buildable now

`morphOS/workflows/*.yaml` already expresses the intent for:

- feature flow
- release flow
- repo evaluation

The runtime semantics are not fully complete, but template loading is still very buildable.

### What to build

In `skyforce-core`:

- `WorkflowTemplate`
- `WorkflowStep`
- `WorkflowBranch`
- `WorkflowTrigger`
- `WorkflowConstraint`

In `skyforce-symphony`:

- load workflow templates from a configurable path
- validate templates against contracts
- expose loaded templates in observability state

### Initial scope

Only support:

- sequential steps
- parallel fan-out
- conditional branch
- approval step
- retry metadata

### Confidence

High for loading and validation.
Medium for execution semantics beyond the initial subset.

## 3. Policy Rule Model

### Why it is buildable now

The policy spec is already structured around:

- rules
- triggers
- conditions
- actions on fail
- precedence

That is enough to define a real policy contract now.

### What to build

In `skyforce-core`:

- `PolicyRule`
- `PolicyTrigger`
- `PolicyCondition`
- `PolicyDecision`
- `PolicyAction`
- `PolicyViolation`

In `skyforce-symphony`:

- step-level policy evaluation hooks

In `skyforce-harness`:

- execution guard hooks for file/network/tool/process actions

In `skyforce-command-centre`:

- policy decision and violation visibility

### Initial scope

Only enforce:

- destructive action gating
- network write gating
- test-required gate
- deploy gate
- token/time budget gate

### Confidence

High for the contract and enforcement hooks.
Medium for a complete evaluator.

## 4. Agent Archetype Mapping

### Why it is buildable now

The current agent files are structured enough to become archetypes:

- vision
- coding
- debugging
- architecture
- learning

Skyforce already has Agent Hub and runtime registrations.

### What to build

In `morphOS`:

- normalize each agent spec into a machine-readable archetype manifest

In `skyforce-core`:

- `AgentCell`
- `AgentArchetype`
- `AgentToolPolicy`
- `AgentSubscription`

In `skyforce-symphony`:

- import archetypes into Agent Hub registrations

### Confidence

High.

### Constraint

Treat the current markdown files as human-readable source, not direct runtime config forever.

## 5. Connectivity Mode Model

### Why it is buildable now

The runtime architecture clearly defines:

- offline
- connected
- restricted connected

This maps well to your real hybrid environment.

### What to build

In `skyforce-core`:

- `ConnectivityMode`
- `CapabilityFlags`

In `skyforce-symphony`:

- runtime connectivity state
- queue/defer rules for blocked actions

In `skyforce-harness`:

- node connectivity reporting
- protocol availability reporting

In `skyforce-command-centre`:

- connectivity mode visibility
- deferred action counts

### Confidence

High.

## 6. Runtime Topology Classification

### Why it is buildable now

The topology spec is concrete and closely matches your actual environment:

- laptop
- Mac Mini / home server
- cloud
- hybrid

Skyforce already has node records and routing heuristics.

### What to build

In `skyforce-core`:

- topology enums and node-class contracts

In `skyforce-symphony`:

- routing rules based on topology class

In `skyforce-harness`:

- per-node descriptor fields

In `skyforce-command-centre`:

- topology view

### Confidence

High.

## What Needs Clarity Before We Build It

## 1. Workflow Execution Semantics

### Why it needs clarity

The docs clearly want richer graph behavior, but they do not yet lock:

- step I/O schema
- branch merge rules
- retry ownership
- compensation logic
- event checkpoints between every node

### Questions to answer

- Are workflow steps declarative only, or can they embed execution logic?
- How are workflow outputs typed and passed forward?
- What is the canonical approval step behavior?
- How do we pause and resume graph nodes?

### What to do first

Define a strict v1 workflow subset and reject everything else.

### Current buildability

Medium.

## 2. Memory Architecture

### Why it needs clarity

The memory layer is directionally strong, but not implementation-ready.

Open areas:

- storage model
- retrieval model
- memory TTL and retention
- indexing
- privacy boundary
- write authority

### Questions to answer

- Is memory local-first, cloud-first, or hybrid?
- What is authoritative: file memory, database memory, or graph memory?
- Which agents may write semantic memory?
- What is the approval policy for stored lessons?

### Current buildability

Medium-low.

## 3. Learning Loop

### Why it needs clarity

The learning agent idea is compelling, but the path from observation to platform change is not yet tight.

Open areas:

- what counts as a learned pattern
- who approves a learned pattern
- how learning becomes a proposal
- whether learning affects prompts, policies, workflows, or code

### Questions to answer

- Is learning read-only at first?
- Does learning create issues, docs, or code patches?
- Can learning ever update policy automatically?

### Current buildability

Medium for artifact generation.
Low for automatic system adaptation.

## 4. Human Cell Model

### Why it needs clarity

The concept of human roles is interesting, but there is not yet enough operational detail to implement it cleanly.

Open areas:

- permission mapping
- role assignment model
- escalation flow
- approval rights
- human-to-agent interaction protocol

### What we need first

- explicit role schema
- authority model
- action matrix

### Current buildability

Low-medium.

## 5. Policy Conflict Resolution Beyond the Basics

### Why it needs clarity

The spec gives precedence rules, but real policy evaluation needs stronger definitions for:

- multi-rule matching on one action
- partial approval
- deferred vs blocked behavior
- human override semantics
- per-node vs global policy

### Current buildability

Medium for a small engine.
Low for a full policy platform without sharper rules.

## What We Should Not Build Yet

## 1. Autonomous Self-Modifying System Loops

### Why not

This is the highest-risk interpretation of "self-evolve."

Problems:

- too easy to bypass validation
- too easy to create feedback loops
- too easy to create architecture drift
- impossible to trust early

### What to do instead

Only build proposal-driven evolution first:

- observe
- propose
- validate
- require approval
- then execute

## 2. A Separate Orchestrator Runtime in morphOS

### Why not

Skyforce already has Symphony.

If `morphOS` also grows a real orchestrator runtime now, we create:

- dual workflow engines
- dual execution models
- dual observability

That is wasted motion and long-term confusion.

### What to do instead

Keep orchestration runtime implementation in `skyforce-symphony`.

## 3. A Separate Event Bus Runtime in morphOS

### Why not

The event bus belongs to the running system, not to the spec repo.

### What to do instead

`morphOS` should define the event model.
Skyforce should implement it.

## 4. A Full Memory Platform Before Contracts and Policy Are Stable

### Why not

Memory becomes a dumping ground if built too early.

Problems:

- unclear schemas
- unclear write permissions
- unclear retention
- unclear search model

### What to do instead

First stabilize:

- events
- policy
- workflow state
- execution artifacts

Then build the memory layer on top of those.

## 5. Full Human-Role Runtime Without an Authority Model

### Why not

Human roles affect:

- approvals
- escalation
- safety
- accountability

Without a clear authority model, the implementation will be arbitrary.

## Recommended Build Order

## Stage 1: Immediate

Build now:

1. event contracts
2. workflow template contracts and loader
3. policy contracts
4. connectivity mode contracts
5. topology contracts
6. agent archetype mapping

## Stage 2: Near-Term

Build after stage 1 lands:

1. Symphony workflow template execution subset
2. policy enforcement hooks
3. event stream alignment
4. command-centre policy and event visibility
5. CLI support for `morphOS` repo search and status

## Stage 3: Mid-Term

Build after execution and policy settle:

1. memory write model
2. learning artifact model
3. deferred action replay model
4. topology-aware scheduling refinement

## Stage 4: Later

Only build after trust and validation are strong:

1. proposal-driven self-evolution loop
2. learning-to-policy suggestions
3. learning-to-workflow suggestions
4. human role runtime

## Repo-by-Repo Build Map

## Build in morphOS

- specification authority
- agent archetypes
- workflow templates
- policy reference files
- topology model
- integration plans

## Build in skyforce-core

- contracts for events, policy, topology, connectivity, workflow templates, agent cells
- CLI visibility into morphOS assets

## Build in skyforce-symphony

- workflow template loader and executor
- policy hooks
- event publication
- connectivity-aware orchestration
- archetype-backed Agent Hub registration

## Build in skyforce-harness

- event emission for execution lifecycle
- execution guard rails
- connectivity reporting
- protocol/tool policy enforcement

## Build in skyforce-command-centre

- event visibility
- policy visibility
- topology/connectivity panels
- archetype and workflow template visibility

## Final Recommendation

### Can be built now

- yes: events
- yes: workflow loader
- yes: policy contracts
- yes: topology model
- yes: connectivity model
- yes: agent archetype mapping

### Needs clarity

- memory
- learning
- workflow graph semantics beyond v1
- human roles
- full policy conflict semantics

### Cannot be built safely yet

- autonomous self-modification
- a second runtime orchestrator in `morphOS`
- a second event bus runtime in `morphOS`
- a full memory platform before core contracts stabilize

## Bottom Line

The current `morphOS` specs are good enough to drive the next real platform layer.

What they are not yet good enough for is unconstrained autonomy.

So the immediate move is:

- build the contracts
- build the loader
- build the policy hooks
- build the event alignment

Then use Skyforce runtime and validation to carry the rest safely.
