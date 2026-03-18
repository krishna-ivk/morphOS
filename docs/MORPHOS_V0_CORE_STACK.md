# morphOS v0 Core Stack

Canonical priority note: this file defines the mandatory stack; use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the prioritized implementation order.

This document defines the non-negotiable runtime stack for `morphOS v0`.

If `morphOS` is the specification for the organism, this stack is the minimum set of runtime organs that make the organism viable.

These components should be treated as foundational, not optional experiments.

## Executive Summary

`morphOS v0` is built around five mandatory subsystems:

1. `openai/symphony`
2. `wavezync/durable`
3. `andrewyng/context-hub`
4. `ComposioHQ/agent-orchestrator`
5. `openai/skills`

These become the core runtime layers for:

- orchestration
- durable execution
- memory/context
- tool execution
- modular capabilities

The role of `morphOS` is not to replace these systems.

Its role is to define:

- the semantics
- the trust model
- the workflow language
- the memory model
- the policy model
- the agent/archetype model

The role of Skyforce is to integrate and operate this stack.

## The Five Non-Negotiables

### 1. Orchestration Core

Component:

- `openai/symphony`

Primary role:

- multi-agent coordination
- task breakdown
- delegation
- workflow graph execution

This becomes:

- `Agent Manager`
- `Workflow Engine`

What it should own:

- selecting what happens next
- assigning work to agents
- controlling workflow transitions
- handling approvals and escalation routing

What it should not own:

- durable persistence semantics
- long-term memory
- raw external tool integration logic
- plugin/skill registry semantics

### 2. Execution + State Engine

Component:

- `wavezync/durable`

Primary role:

- long-running execution
- retries
- persistence
- resumability
- recovery

This becomes:

- `Kernel Scheduler`
- `State Engine`

What it should own:

- durable workflow/job execution
- checkpointing
- retry policy execution
- task persistence
- recovery after interruption or restart

What it should not own:

- workflow semantics
- memory retrieval strategy
- agent skill definitions
- operator UI decisions

### 3. Memory Core

Component:

- `andrewyng/context-hub`

Primary role:

- context retrieval
- memory-like grounding
- task history and retrieval support
- embeddings-backed recall

This becomes:

- `Memory Core`

This is the most important subsystem boundary to get right.

What it should own first in `v0`:

- reference context
- retrieval of curated documents
- reusable context lookup
- session-to-session carryover through annotations or indexed knowledge

What it should not be stretched into immediately:

- the full operational context store
- the full event lineage store
- the entire policy-aware memory system

Important note:

`context-hub` should be treated as the foundation of memory/context architecture, but not automatically as the entire memory architecture.

The broader `morphOS` memory model still needs layers:

- reference context
- operational context
- persistent memory

### 4. Tool Execution Layer

Component:

- `ComposioHQ/agent-orchestrator`

Primary role:

- connecting agents to external APIs and tools
- executing real-world actions
- bridging agent intent to system actions

This becomes:

- `Tool Engine`

What it should own:

- tool/API connectivity
- external system execution
- action invocation surfaces
- permissioned integrations

What it should not own:

- workflow orchestration semantics
- long-term memory semantics
- durable retry state by itself
- skill taxonomy

### 5. Skill System

Component:

- `openai/skills`

Primary role:

- modular reusable capabilities
- composable behavior units
- capability packaging

This becomes:

- `Skill System`
- `Plugin System`

What it should own:

- reusable skill definitions
- capability packaging
- behavior composition
- skill reuse across agents and workflows

What it should not own:

- orchestration logic
- durable execution state
- memory storage
- external tool policy on its own

## System Mapping

The clean `morphOS v0` runtime map should be:

- `Symphony`
  - decides who should do what next
- `Durable`
  - decides what is still running, persisted, retrying, or resumable
- `Context Hub`
  - decides what memory or context can be retrieved
- `Composio`
  - decides how external actions are performed
- `Skills`
  - decides what modular capabilities are available to an agent

If these boundaries blur, the system will accumulate duplicated logic and weak contracts.

## morphOS vs Skyforce Ownership

### morphOS Should Own

- workflow semantics
- agent archetypes
- policy and trust semantics
- context architecture
- memory model
- approval model
- topology intent
- safety and evolution rules

### Skyforce Should Own

- integration of the five runtime systems
- shared contracts and APIs
- execution surfaces
- operator tooling
- observability
- validation and publishing
- deployment/runtime packaging

### Practical Rule

- `morphOS` defines what the organism is
- Skyforce runs the organism

That boundary should remain strict.

## Repo Ownership Map

### [morphOS](..)

Should own:

- semantics
- policies
- archetypes
- workflow language
- memory architecture
- role definitions

### [skyforce-symphony](../../skyforce-symphony)

Should own:

- Symphony integration
- workflow execution bridge
- orchestration-state publishing
- directive routing
- workflow observability

### [skyforce-core](../../skyforce-core)

Should own:

- shared contracts
- CLI
- validation and publish contract layer
- cross-runtime schemas

### [skyforce-command-centre](../../skyforce-command-centre)
### [skyforce-command-centre-live](../../skyforce-command-centre-live)

Should own:

- operator surfaces only
- approval/publish/validation UX
- visibility into runtime state

Should not become:

- the orchestration brain
- the durable kernel
- the memory core

### Likely New Runtime Surfaces

For `v0`, two more runtime surfaces are likely needed:

- `skyforce-durable`
  - wraps or hosts the durable execution backbone
- `skyforce-context-core`
  - wraps the context/memory subsystem and exposes context contracts

These do not need to be new repos immediately, but the architectural ownership should be explicit.

## Integration Order

This is the recommended order for building the stack coherently.

### 1. Memory / Context Foundation

Start with:

- `Context Hub`
- context architecture
- memory boundaries

Why:

- context and memory shape the quality of orchestration, skills, and action safety

### 2. Orchestration + Durable Execution

Bring together:

- `Symphony`
- `Durable`

Why:

- orchestration without durability is fragile
- durability without orchestration semantics is blind

### 3. Skills

Add:

- reusable skills
- composable capability units

Why:

- once workflow and memory boundaries exist, skills become reusable instead of ad hoc prompt fragments

### 4. Tool Execution

Add:

- `Composio`
- external tool and API access

Why:

- tool execution should be introduced after workflow, policy, and memory boundaries are stable enough to govern it

### 5. Operator + Governance Layer

Finalize:

- approvals
- observability
- validation
- dashboards
- cutover and runtime governance

## Non-Negotiable Runtime Contracts

At minimum, the stack needs explicit shared contracts for:

- `WorkflowRun`
- `TaskExecution`
- `Directive`
- `ContextRef`
- `MemoryRecord`
- `SkillRef`
- `ToolAction`
- `ExecutionCheckpoint`
- `ApprovalDecision`

These contracts are the glue between the five systems.

Without them, integration will drift into adapter-specific hidden assumptions.

## The Most Important Open Questions

Even with the core stack fixed, several architecture decisions still need to be answered clearly.

### 1. Symphony vs Durable Authority

We need a strict answer to:

- what Symphony decides
- what Durable decides
- where retries and resumptions actually live

### 2. Context Hub Scope

We need a strict answer to:

- what is reference context
- what is operational context
- what is persistent memory
- what `context-hub` owns directly versus what Skyforce wraps around it

### 3. Skill Versioning

We need a strict answer to:

- how skills are versioned
- how archetypes depend on skills
- how skills are registered and approved

### 4. Tool Governance

We need a strict answer to:

- whether tool actions flow through directives
- how approvals can block external actions
- where policy checks happen before Composio execution

### 5. Approval Scope

We need a strict answer to:

- what approvals can block
- workflow transitions
- tool actions
- memory writes
- self-modification

## Design Rules For v0

These rules should guide implementation.

### Rule 1

Do not build a second orchestration engine beside Symphony.

### Rule 2

Do not let Durable quietly redefine workflow semantics.

### Rule 3

Do not let Context Hub become a vague catch-all for every form of state.

### Rule 4

Do not let Composio bypass policy, approval, or workflow control paths.

### Rule 5

Do not let Skills become ungoverned prompt fragments without versioning and ownership.

## Recommended Next Step

After this document, the next architecture work should be:

1. define the `morphOS v0` contract layer explicitly
2. define the `Symphony + Durable` authority boundary
3. define the `Context Hub` wrapping model for Skyforce
4. define the skill registration/versioning model
5. define the tool-action approval boundary

## Related Docs

- [README.md](../README.md)
- [HUMAN_GUIDE.md](HUMAN_GUIDE.md)
- [CONTEXT_ARCHITECTURE.md](CONTEXT_ARCHITECTURE.md)
- [CONTEXT_HUB_EVALUATION.md](CONTEXT_HUB_EVALUATION.md)
- [morphos_vs_skyforce_evaluation.md](morphos_vs_skyforce_evaluation.md)
