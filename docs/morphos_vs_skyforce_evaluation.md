# morphOS Existing Spec vs Skyforce Current Build

This document compares the current `morphOS` specification set with what is already built across the Skyforce repositories:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre`
- `skyforce-core`

The goal is to evaluate whether `morphOS` should remain a separate repo, what it is strong at today, and where it currently overlaps or lags behind the executable Skyforce platform.

## Executive View

### Short answer

`morphOS` is stronger as a system design and operating model.

Skyforce is stronger as an executable platform.

That means:

- `morphOS` is currently better at defining the organism
- Skyforce is currently better at running the organism

This is a good situation if we keep the boundary clean.
It becomes a bad situation if both repos try to be the runtime brain.

## What morphOS Is Better At

### 1. Clear unifying metaphor and system language

`morphOS` has a much stronger conceptual frame.
The organism metaphor gives every major subsystem a role:

- cell
- DNA
- nervous system
- immune system
- brain
- memory
- muscles
- circulatory system

### Pros

- easier to reason about as a full operating model
- easier to onboard collaborators into the intended architecture
- gives a natural place for future capabilities like memory, policy, learning, and topology
- much better at defining the "why" and the overall shape of the system

### Cons

- metaphor can hide implementation gaps
- some concepts are still abstract rather than executable
- risk of becoming a design-heavy repo if not tied to runtime contracts

### Evaluation

Skyforce does not currently have an equally strong top-level conceptual model.
`morphOS` wins here.

## 2. Better specification coverage of foundational OS concerns

`morphOS` already has dedicated specs for:

- runtime topology
- event bus
- policy engine
- cell model
- human roles
- interaction layer

### Pros

- covers real operating-system concerns that Skyforce only partly implements today
- defines offline vs online behavior clearly
- defines event-driven architecture explicitly
- defines policy as a first-class layer rather than a late add-on
- gives a path to scale from laptop to cloud to distributed hybrid

### Cons

- most of this is still specification, not running code
- no proven contract yet between these specs and Symphony/Harness runtime code
- topology and policy are richer on paper than in execution today

### Evaluation

`morphOS` is ahead on architecture completeness.
Skyforce is ahead on runtime execution.

## 3. Better framing for self-evolution

The `morphOS` direction is explicitly agentic, adaptive, and learning-oriented.

### Pros

- stronger home for learning loops and system improvement
- better place for capability memory and post-run evolution
- more natural repo for long-horizon planning and meta-agents

### Cons

- "self-evolve" is still mostly aspirational at this stage
- dangerous if interpreted as direct self-modification without gates
- needs strong validation and approval boundaries from Skyforce

### Evaluation

`morphOS` is the right repo for defining self-evolution.
It is not yet the right repo to execute uncontrolled self-evolution.

## What Skyforce Is Better At

### 1. Actual orchestration runtime

Skyforce already has real orchestration behavior in `skyforce-symphony`.

Already built:

- agent-aware routing
- protocol-aware routing
- node-aware routing
- execution target selection
- execution envelopes
- running state exposure
- validation summary publication
- receipt ingestion and observability

### Pros

- it runs now
- it has working tests
- it already emits state the CLI and dashboard can consume
- it already supports the multi-node and multi-agent direction in practical form

### Cons

- the runtime model is ahead of the formal OS model
- some architectural ideas are encoded as implementation behavior rather than imported from a single spec source
- still missing full workflow template execution from `morphOS`

### Evaluation

Skyforce wins decisively on executable orchestration.

## 2. Operator surface and visibility

Skyforce already has:

- `command-centre` UI
- validation and summary readiness
- execution pickup visibility
- node and routing visibility
- `sky` CLI

### Pros

- there is already a real human control plane
- state is inspectable from terminal and dashboard
- the system is not only conceptual; it is observable

### Cons

- some state is still derived from artifacts and fallback loaders instead of one canonical runtime API
- UI still trails the breadth of the underlying architecture

### Evaluation

Skyforce is much more mature as an operator-facing system.
`morphOS` has no equivalent live surface yet.

## 3. Integration with real execution infrastructure

Skyforce already knows about:

- Hermes runtime / cloud agent lane
- Mac Mini
- Windows PC
- Android monitoring nodes
- A2A and MCP adapter boundaries
- execution receipts and envelopes

### Pros

- grounded in the actual device topology you are building
- already split into orchestration, execution, core contracts, and UI
- much closer to a usable personal distributed system

### Cons

- device and protocol architecture is ahead of the top-level unification
- still needs stronger policy and connectivity layers

### Evaluation

Skyforce is much closer to reality and deployment.

## Area-by-Area Comparison

## Orchestration

### morphOS spec

#### Pros

- defines orchestration as a central OS layer
- describes workflow graphs, retries, connectivity branches, and coordination cleanly
- strong long-term architecture language

#### Cons

- no real orchestrator runtime implemented here
- no direct evidence yet of task routing, leases, or execution state behavior

### Skyforce build

#### Pros

- Symphony is already routing and exposing state
- execution envelopes and receipts exist
- tests exist for the orchestration path

#### Cons

- not yet fully driven by `morphOS` workflow templates
- some behavior may drift from the spec unless aligned

### Verdict

Use `morphOS` to define orchestration semantics.
Use `skyforce-symphony` to implement them.

## Event Bus

### morphOS spec

#### Pros

- event taxonomy is explicit and thoughtful
- strong rules: no direct agent-to-agent calls, at-least-once delivery, durable when offline
- very good foundational design

#### Cons

- still a spec
- no evidence of actual durable bus implementation in this repo

### Skyforce build

#### Pros

- real event-like observability already exists in Symphony and the CLI/dashboards
- enough structure exists to adopt a formal event envelope

#### Cons

- not yet a full bus with replay, dead letters, and deferred online-only delivery
- event semantics are less formal than `morphOS` currently describes

### Verdict

`morphOS` wins on event model quality.
Skyforce wins on runtime foothold.

## Policy Engine

### morphOS spec

#### Pros

- one of the strongest specs in the repo
- default-deny, fail-closed, auditable, layered
- clearly defines threats and responses

#### Cons

- not yet a running cross-repo policy evaluator
- no evidence yet of enforcement hooks in this repo

### Skyforce build

#### Pros

- validation, approvals, and routing constraints already exist in partial form
- trust-level and allowed-task concepts are already emerging

#### Cons

- policy is fragmented across validation logic, routing heuristics, approvals, and conventions
- not yet a unified policy engine

### Verdict

`morphOS` is ahead on policy design.
Skyforce is the right place to enforce it.

## Agent Model

### morphOS spec

#### Pros

- strong agent archetypes
- cell-based standardization is a good idea
- roles are clearly scoped

#### Cons

- agent definitions are markdown archetypes, not executable registrations
- no current import path into runtime agent registration

### Skyforce build

#### Pros

- Agent Hub already exists
- protocol-aware routing already exists
- execution targets are already visible and testable

#### Cons

- the runtime agent model is more implementation-specific and less elegantly unified than `morphOS`
- archetype-to-runtime translation is not built yet

### Verdict

`morphOS` should define the archetypes.
Skyforce should register and run them.

## Runtime Topology

### morphOS spec

#### Pros

- excellent topology framing from laptop to cloud to hybrid
- directly relevant to your real environment
- gives a strong deployment map

#### Cons

- still not wired into actual node registry/runtime selection code

### Skyforce build

#### Pros

- actual node registry exists
- actual device classes are already being modeled
- routing already considers node classes and capabilities

#### Cons

- topology is implemented tactically, not yet aligned to one canonical topology spec

### Verdict

`morphOS` is ahead on topology design.
Skyforce is ahead on topology execution.

## Memory and Learning

### morphOS spec

#### Pros

- gives memory and learning a clear architectural home
- capability store already exists
- strong direction for future self-improvement loops

#### Cons

- no strong evidence yet of a full memory runtime or learning pipeline

### Skyforce build

#### Pros

- validation artifacts, receipts, summaries, and workflow artifacts already create raw material for learning

#### Cons

- learning loop is still weak
- no explicit memory architecture as rich as `morphOS` yet

### Verdict

`morphOS` should own the learning model.
Skyforce should feed it real data.

## Biggest Risks If We Keep Both Without Boundaries

### 1. Dual-brain problem

If `morphOS` and `skyforce-symphony` both evolve as orchestrators, the system will split into:

- one conceptual brain
- one runtime brain

This is the highest risk.

### 2. Schema drift

If `morphOS/docs/schemas.md` and `skyforce-core/packages/contracts` evolve independently, contracts will diverge.

### 3. Policy drift

If policy stays in `morphOS` docs while real constraints live ad hoc in Skyforce code, operators will trust the wrong source of truth.

### 4. Duplicate workflow systems

If `morphOS/workflows/*.yaml` and Symphony runtime workflows become separate ecosystems, neither will stay authoritative.

## Biggest Upside If We Keep Both Cleanly

### 1. Strong separation of definition vs execution

This is the ideal model:

- `morphOS` defines the operating system
- Skyforce runs the operating system

### 2. Better long-term scalability

`morphOS` can stay strategic and architectural while Skyforce iterates rapidly on runtime concerns.

### 3. Safer self-evolution

`morphOS` can define how the system learns and evolves, while Skyforce supplies validation, observability, and human approval gates.

## Recommendation

## Keep `morphOS` separate

### Why

- it is stronger as a system-definition repo
- it should govern multiple runtime repos
- it should not absorb execution responsibilities already implemented in Skyforce

## Make `morphOS` the specification authority

It should own:

- agent archetypes
- event taxonomy
- policy language
- workflow semantics
- topology model
- learning/evolution model

## Make Skyforce the runtime authority

It should own:

- orchestration runtime
- execution runtime
- contracts used in code
- operator interfaces
- validation and safe rollout

## Final Verdict

### morphOS existing spec

#### Pros

- better architecture language
- stronger whole-system design
- stronger policy, event, topology, and memory framing
- better home for self-evolution

#### Cons

- mostly non-executable today
- overlaps with Symphony if boundaries are not enforced
- high risk of spec/runtime drift

### Skyforce current build

#### Pros

- real runtime exists now
- real routing, observability, validation, and execution handoff already work
- better fit for immediate platform execution

#### Cons

- less unified as an operating-system model
- policy and event semantics are not yet as coherent as the `morphOS` specs
- still needs to import more of the `morphOS` architecture intentionally

## Bottom Line

`morphOS` is the better blueprint.

Skyforce is the better machine.

The right move is not to choose one over the other.
The right move is to let `morphOS` define the organism and let Skyforce become the organism's executable body.
