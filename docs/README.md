# Documentation Guide

Use this folder as the main entry point for SkyForce specifications.

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) when you need the authoritative cross-repo build order.

## Sections

- `agents/` — role definitions for specialized agent cells
- `vision/` — product vision and problem framing inputs
- `human_roles/` — human collaborators, responsibilities, and escalation paths
- root `docs/*.md` — system-level architecture, schemas, runtime, and policy specs

## Start Here

- `agentic_os_architecture.md` — overall operating system design
- `MORPHOS_V0_IMPLEMENTATION_BOARD.md` — canonical prioritized build board
- `MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md` — cross-repo parallel execution plan with dependencies, lineage, and exclusivity rules
- `MORPHOS_V0_AGENT_DISPATCH_PACKETS.md` — ready-to-assign packets and dependency matrix for parallel agent execution
- `MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md` — live ownership, gate, and handoff board for running parallel agents
- `contract_freeze_notes.md` — Wave 1 Agent A freeze artifact for execution mode, authority, events, summaries, and promotion
- `orchestration_state_handoff.md` — Wave 1 Agent B handoff artifact for Symphony runtime payload and approval-state alignment
- `runner_receipt_examples.md` — Wave 1 Agent C handoff artifact for Harness receipt and evidence alignment
- `operator_surface_wording_map.md` — Wave 1 Agent D inventory artifact for command-centre and CLI terminology rollout
- `MORPHOS_V0_WAVE1_LAUNCH_KIT.md` — exact first-wave launch order and copy-paste prompts for agent startup
- `MORPHOS_V0_WAVE2_LAUNCH_KIT.md` — governance and operator rollout launch kit for the second wave
- `MORPHOS_V0_WAVE3_LAUNCH_KIT.md` — promotion and deterministic closeout launch kit for the third wave
- `cell_spec.md` — shared template for all agent definitions
- `schemas.md` — data contracts and shared structures
- `interaction_layer_spec.md` — how humans and agents communicate
- `policy_engine_spec.md` — safety and approval model

## Authoring Conventions

- put new agent role docs in `docs/agents/`
- put new vision inputs in `docs/vision/`
- keep cross-cutting system specs at `docs/`
- keep workspace-wide operating rules in the root `AGENTS.md`
