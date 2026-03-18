# morphOS v0 Upstream Adoption Map

This document defines what `morphOS v0` intends to adopt from the mandatory
upstream systems in the stack.

It answers a practical question:

- what are we taking from each upstream repo?
- what are we wrapping locally?
- what are we only treating as design inspiration?
- where in Skyforce should each capability land?

This should be read alongside:

- `docs/MORPHOS_V0_CORE_STACK.md`
- `docs/MORPHOS_V0_RUNTIME_CONTRACTS.md`
- `docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`
- `docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`
- `docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md`

## Core Rule

The mandatory stack should not be treated as a pile of dependencies.

Each upstream repo must fall into one of these categories:

- adopted directly
- wrapped behind a local boundary
- semported into local contracts or runtime surfaces
- used only as design influence

If this distinction is not explicit, the platform will drift into overlapping
authority and duplicated semantics.

## Adoption Categories

### Direct adoption

Use the upstream system as an active runtime dependency with minimal local
reinterpretation.

### Wrapped adoption

Use the upstream system behind a Skyforce-owned adapter or boundary so the
platform preserves local control over contracts and authority.

### Semported adoption

Preserve the upstream design intent while translating it into local contracts,
runtime code, or operator surfaces.

### Design influence only

Use the upstream system to shape architecture, but do not treat it as an active
runtime dependency.

## 1. openai/symphony

### Role in morphOS v0

Primary orchestration brain.

### What we want from it

- workflow coordination
- delegation patterns
- agent routing
- task breakdown
- runtime observability surfaces
- directive lifecycle patterns

### Adoption mode

Wrapped adoption plus selective semporting.

### What should be used directly

- orchestration runtime behavior
- workflow execution coordination
- running-entry state publication

### What should be wrapped locally

- workflow payload projection
- directive projection
- approval lifecycle projection
- durable-boundary projection

### What should be semported

- shared runtime contracts where local type ownership matters
- observability shapes consumed by CLI and dashboards
- local workflow semantics where `morphOS` must stay authoritative

### What should not be outsourced

- overall platform semantics
- policy language
- memory model
- operator trust model

### Local target

- `skyforce-symphony`

### Priority

Highest. Already underway.

## 2. wavezync/durable

### Role in morphOS v0

Reliable execution kernel and state engine.

### What we want from it

- durable execution lifecycle
- retries
- resumability
- persistent status
- checkpointing
- cancellation and resume controls

### Adoption mode

Wrapped adoption.

### What should be used directly

- durable execution semantics
- durable status and checkpoint concepts
- retry and resume lifecycle

### What should be wrapped locally

- request submission boundary
- status projection
- checkpoint projection
- Symphony handoff and authority boundary

### What should be semported

- shared contracts for `DurableExecutionRequest`
- `DurableExecutionStatus`
- `ExecutionCheckpointRecord`

### What should not be outsourced

- workflow meaning
- step selection
- approval semantics
- orchestration authority

### Local target

- `skyforce-symphony` durable adapter boundary
- future dedicated durable runtime repo or service

### Priority

Highest. Already partially implemented.

## 3. andrewyng/context-hub

### Role in morphOS v0

Reference-context and memory substrate.

### What we want from it

- curated documentation retrieval
- persistent annotations
- reusable reference context
- session-to-session knowledge continuity
- retrieval patterns for external knowledge

### Adoption mode

Wrapped adoption plus semporting.

### What should be used directly

- reference-context retrieval ideas
- persistent annotation model
- curated-doc access patterns

### What should be wrapped locally

- any context-hub integration into Skyforce runtime
- access control boundaries
- context classification

### What should be semported

- local contracts for:
  - reference context
  - operational context
  - persistent memory
- memory access labels and trust boundaries

### What should not be conflated with Context Hub

- full operational context
- workflow execution state
- all persistent memory
- approval context
- distributed node synchronization

### Local target

- future context-core subsystem
- `skyforce-core` shared context contracts

### Priority

Very high, but behind the current orchestration and durable boundary work.

## 4. ComposioHQ/agent-orchestrator

### Role in morphOS v0

Tool execution layer.

### What we want from it

- API and tool connectivity patterns
- external action execution
- tool permission boundaries
- connector-style integration patterns

### Adoption mode

Wrapped adoption plus design influence.

### What should be used directly

- tool integration concepts where local ownership does not need to be deep

### What should be wrapped locally

- tool invocation contracts
- approval gates for risky actions
- result artifact projection
- operator observability

### What should be semported

- local `ToolAction` contract shapes
- external-tool result recording
- policy-aware action execution flows

### What should not be outsourced

- approval policy
- workflow authority
- audit and provenance rules

### Local target

- future tool-engine subsystem
- `skyforce-core` shared contracts
- Symphony runtime action projection

### Priority

Medium. Important, but should follow contract stabilization.

## 5. openai/skills

### Role in morphOS v0

Reusable skill and plugin capability layer.

### What we want from it

- modular capability packaging
- composable behavior units
- reusable skill definitions
- portable capability bundles for agents

### Adoption mode

Semported adoption plus design influence.

### What should be used directly

- capability packaging ideas
- reusable-skill organization patterns

### What should be wrapped locally

- skill registration
- skill trust and versioning
- archetype-to-skill attachment

### What should be semported

- local `SkillRef` contracts
- capability taxonomy
- plugin ownership rules

### What should not be outsourced

- agent archetype semantics
- policy constraints on skills
- deployment/version authority

### Local target

- future skill/plugin subsystem
- `morphOS` archetype and capability definitions
- `skyforce-core` shared skill references

### Priority

Medium. Follows core runtime and memory boundaries.

## Cross-Repo Feature Import Map

This is the short version of what we want to import from each upstream system.

### Symphony

Import:

- orchestration patterns
- delegation and workflow routing
- runtime running-entry observability

Do not import blindly:

- platform semantics
- memory policy
- operator trust boundaries

### Durable

Import:

- durable request model
- durable status model
- checkpoints
- retry/resume lifecycle

Do not import blindly:

- workflow authority
- approval meaning

### Context Hub

Import:

- reference retrieval
- annotation persistence
- curated context access

Do not import blindly:

- full runtime state
- all long-term memory semantics

### Composio

Import:

- connector and tool-execution patterns
- action integration model

Do not import blindly:

- platform policy
- audit and provenance semantics

### Skills

Import:

- modular capability packaging
- reusable behavior structure

Do not import blindly:

- archetype semantics
- local deployment/version ownership

## Recommended Integration Order

1. Symphony
2. Durable
3. Context Hub
4. Skills
5. Composio

Reasoning:

- orchestration and durable authority must stabilize first
- context architecture should be layered onto a clear runtime boundary
- skills become more useful once contracts and memory surfaces exist
- tool execution should come after policy, approval, and provenance rules are
  clear

## Required Local Ownership

No matter how much we adopt from upstream repos, these remain local
responsibilities:

- `morphOS` semantics
- policy language
- trust and approval boundaries
- context classification
- operator observability
- auditability
- artifact and receipt conventions

## Bottom Line

The mandatory stack is the foundation of `morphOS v0`, but the platform should
not dissolve into upstream repos.

The rule is simple:

- adopt upstream runtime strengths
- wrap them behind local boundaries
- semport what must become local contract
- keep system meaning and trust ownership inside `morphOS` and Skyforce
