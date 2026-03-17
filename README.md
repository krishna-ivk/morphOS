# morphOS

`morphOS` is the specification and operating-model repository for the long-term agentic system.

It defines how the platform should think, coordinate, protect itself, and evolve.

It is not the primary runtime.

That role belongs to the Skyforce repos:

- `skyforce-symphony`: orchestration runtime
- `skyforce-harness`: execution and adapter runtime
- `skyforce-command-centre`: operator control plane
- `skyforce-core`: shared contracts, CLI, and validation surface

## Start Here

If you are reading this as a human operator, builder, or collaborator, use this order:

1. [Human guide](docs/HUMAN_GUIDE.md)
2. [Skyforce runtime overview](docs/SKYFORCE_RUNTIME_OVERVIEW.md)
3. [Buildability plan](docs/morphos_buildability_plan.md)
4. [morphOS vs Skyforce evaluation](docs/morphos_vs_skyforce_evaluation.md)
5. [morphOS v0 core stack](docs/MORPHOS_V0_CORE_STACK.md)
6. [morphOS v0 runtime contracts](docs/MORPHOS_V0_RUNTIME_CONTRACTS.md)
7. [Symphony and Durable authority boundary](docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
8. [Durable execution handoff contracts](docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
9. [morphOS v0 upstream adoption map](docs/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
10. [morphOS v0 upstream feature backlog](docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
11. [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
12. [Context architecture](docs/CONTEXT_ARCHITECTURE.md)
13. [Context Hub evaluation](docs/CONTEXT_HUB_EVALUATION.md)
14. [Roadmap](docs/ROADMAP.md)

## What morphOS Owns

`morphOS` should own:

- the operating model
- workflow language
- policy language
- agent archetypes
- runtime topology definitions
- safe evolution direction

It should not own:

- the main orchestration runtime
- the main event bus runtime
- node execution
- the operator UI

## Current Relationship To Skyforce

The current platform model is:

- `morphOS` defines the organism
- Skyforce runs the organism

That boundary matters. It keeps architecture and runtime from drifting into two overlapping systems.

## What Is Already Real In Skyforce

The Skyforce runtime already implements several `morphOS`-aligned pieces:

- workflow template loading from `morphOS/workflows`
- template selection inside Symphony
- lightweight workflow progress tracking
- runtime-action classification for current steps
- execution envelopes and receipts carrying workflow metadata
- CLI and dashboard visibility for that progress

## Key Docs

- [Agentic OS architecture](docs/agentic_os_architecture.md)
- [Cell spec](docs/cell_spec.md)
- [Schemas](docs/schemas.md)
- [Event bus spec](docs/event_bus_spec.md)
- [Policy engine spec](docs/policy_engine_spec.md)
- [Runtime topology spec](docs/runtime_topology_spec.md)
- [Interaction layer spec](docs/interaction_layer_spec.md)
- [morphOS v0 core stack](docs/MORPHOS_V0_CORE_STACK.md)
- [morphOS v0 runtime contracts](docs/MORPHOS_V0_RUNTIME_CONTRACTS.md)
- [Symphony and Durable authority boundary](docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
- [Durable execution handoff contracts](docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
- [morphOS v0 upstream adoption map](docs/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
- [morphOS v0 upstream feature backlog](docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
- [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
- [Context architecture](docs/CONTEXT_ARCHITECTURE.md)
- [Context Hub evaluation](docs/CONTEXT_HUB_EVALUATION.md)

## Current Release

Current specification release line:

- `0.1.0`

This is a specification baseline, not a production runtime release.
