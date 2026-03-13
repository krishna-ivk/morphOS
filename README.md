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

1. [Human guide](/home/vashista/skyforce/morphOS/docs/HUMAN_GUIDE.md)
2. [Skyforce runtime overview](/home/vashista/skyforce/morphOS/docs/SKYFORCE_RUNTIME_OVERVIEW.md)
3. [Buildability plan](/home/vashista/skyforce/morphOS/docs/morphos_buildability_plan.md)
4. [morphOS vs Skyforce evaluation](/home/vashista/skyforce/morphOS/docs/morphos_vs_skyforce_evaluation.md)
5. [Roadmap](/home/vashista/skyforce/morphOS/docs/ROADMAP.md)

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

- [Agentic OS architecture](/home/vashista/skyforce/morphOS/docs/agentic_os_architecture.md)
- [Cell spec](/home/vashista/skyforce/morphOS/docs/cell_spec.md)
- [Schemas](/home/vashista/skyforce/morphOS/docs/schemas.md)
- [Event bus spec](/home/vashista/skyforce/morphOS/docs/event_bus_spec.md)
- [Policy engine spec](/home/vashista/skyforce/morphOS/docs/policy_engine_spec.md)
- [Runtime topology spec](/home/vashista/skyforce/morphOS/docs/runtime_topology_spec.md)
- [Interaction layer spec](/home/vashista/skyforce/morphOS/docs/interaction_layer_spec.md)

## Current Release

Current specification release line:

- `0.1.0`

This is a specification baseline, not a production runtime release.
