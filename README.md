# morphOS

`morphOS` is the specification and operating-model repository for a self-improving, agentic operating system.

It defines how the system should think, coordinate, protect itself, learn, and evolve.

It is not the primary runtime implementation.

That role belongs to the Skyforce execution stack:

- `skyforce-symphony`: orchestration runtime
- `skyforce-harness`: execution and adapter runtime
- `skyforce-command-centre`: operator control plane
- `skyforce-core`: shared contracts, CLI, and validation surface

The clean model is:

- `morphOS` defines the organism
- Skyforce runs the organism

## What morphOS Is

`morphOS` is the system-definition layer for an agentic OS built around a biological metaphor.

Core idea:

- every agent is a cell
- schemas are DNA
- the event bus is the nervous system
- policy is the immune system
- orchestration is the brain
- memory is the hippocampus
- tools and programs are muscles
- workflows are the circulatory system

This repository exists to make those ideas concrete enough that the runtime repos can implement them consistently.

## What Skyforce Is

Skyforce is the executable platform that carries out the operating model defined here.

Current practical split:

- `morphOS`
  - specifications
  - archetypes
  - workflow templates
  - policy definitions
  - system topology
  - long-horizon learning and evolution model

- `skyforce-symphony`
  - workflow execution
  - routing
  - execution state
  - observability

- `skyforce-harness`
  - node execution
  - protocol adapters
  - execution envelopes and receipts

- `skyforce-command-centre`
  - approvals
  - operator visibility
  - fleet and execution dashboards

- `skyforce-core`
  - contracts used in code
  - CLI
  - validation and release support

## Why morphOS Should Stay Separate

Keeping `morphOS` separate prevents two major problems:

1. Runtime duplication
   `morphOS` should not grow a second orchestrator or second event bus runtime.

2. Spec drift inside execution repos
   Architecture definitions, policy semantics, topology, and workflow language need a stable home.

This repo should stay the specification authority while Skyforce remains the runtime authority.

## Current Strength of morphOS

This repo is already strong in:

- operating-model clarity
- policy framing
- event bus design
- topology design
- agent archetype framing
- workflow intent
- learning and evolution direction

The runtime implementation is intentionally limited here.

## Current Strength of Skyforce

Skyforce is already strong in:

- actual orchestration behavior
- node-aware routing
- protocol-aware routing
- validation loops
- execution handoff
- receipts and observability
- operator tooling and CLI surface

That means the practical path is not to replace Skyforce with `morphOS`.
The path is to let `morphOS` shape what Skyforce becomes next.

## Current Status

Current maturity:

- `morphOS`: strong architecture and specification repo
- Skyforce: stronger implementation repo set

Key evaluation documents:

- [morphOS vs Skyforce evaluation](docs/morphos_vs_skyforce_evaluation.md)
- [morphOS buildability plan](docs/morphos_buildability_plan.md)
- [Roadmap](docs/ROADMAP.md)

## Repository Structure

```text
morphOS/
├── agents/                       # Agent archetypes
├── docs/                         # System specifications and planning docs
├── memory/                       # Long-term memory seed artifacts
├── programs/                     # Deterministic helper programs
├── scripts/                      # Utility scripts
├── vision/                       # Product vision and intent
├── workflows/                    # Workflow templates
├── AGENTS.md                     # Agent operating rules
├── CHANGELOG.md                  # Release history
└── package.json                  # Versioned release/package manifest
```

## Core Specifications

- [Agentic OS architecture](docs/agentic_os_architecture.md)
- [Cell specification](docs/cell_spec.md)
- [Schemas](docs/schemas.md)
- [Event bus specification](docs/event_bus_spec.md)
- [Policy engine specification](docs/policy_engine_spec.md)
- [Runtime topology specification](docs/runtime_topology_spec.md)
- [Human cell specification](docs/human_cell_spec.md)
- [Interaction layer specification](docs/interaction_layer_spec.md)

## What Can Be Built Right Now

The strongest buildable areas from the current specs are:

- event taxonomy and event envelope contracts
- workflow template loading and validation
- policy rule contracts
- connectivity mode model
- topology classification model
- agent archetype to runtime registration mapping

These should be implemented in the Skyforce runtime repos, not directly here.

See:

- [Buildability plan](docs/morphos_buildability_plan.md)

## What Needs More Clarity

These areas need further decisions before safe implementation:

- memory architecture
- learning loop behavior
- full workflow graph semantics
- human role runtime
- full policy conflict resolution

## What Should Not Be Built Yet

Not yet safe:

- autonomous self-modifying code loops
- a second orchestrator runtime inside `morphOS`
- a second event bus runtime inside `morphOS`
- a premature full memory platform

## Release Packaging

This repository now includes a package manifest and changelog so it can be versioned as a specification package.

Current release line:

- `0.1.0`

This release is best understood as:

- architecture baseline
- integration planning baseline
- not a production runtime release

## Working Model

Use `morphOS` when you need to answer:

- what is the operating model?
- how should agents communicate?
- what policies should exist?
- how should the system scale from laptop to cloud?
- how should the system learn safely?

Use Skyforce when you need to answer:

- what is actually running?
- how is a task routed?
- what node picked up execution?
- what validations passed or failed?
- what should the operator see and approve?

## Design Principles

1. Every agent is a bounded cell.
2. No direct agent-to-agent calls.
3. Default deny for risky actions.
4. Offline-capable, online-amplified.
5. Learning must remain observable and governable.
6. Self-evolution starts as proposal-driven, not unconstrained.

## Near-Term Direction

Near-term work should focus on:

1. aligning contracts with `skyforce-core`
2. making Symphony load and expose `morphOS` workflow templates
3. translating agent archetypes into runtime registrations
4. implementing policy contracts and connectivity modes
5. making the event model consistent across the stack

## Version

Current version: `0.1.0`
