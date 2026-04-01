# Documentation Guide

Use this folder as the main entry point for SkyForce specifications.

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) when you need the authoritative cross-repo build order.

## Sections

- `agents/` — role definitions for specialized agent cells
- `vision/` — product vision and problem framing inputs
- `human_roles/` — human collaborators, responsibilities, and escalation paths
- root `docs/*.md` — system-level architecture, schemas, runtime, and policy specs

## Start Here

- `agentic_os_architecture.md` — overall operating system design
- `MORPHOS_V0_IMPLEMENTATION_BOARD.md` — canonical prioritized build board
- `cell_spec.md` — shared template for all agent definitions
- `schemas.md` — data contracts and shared structures
- `interaction_layer_spec.md` — how humans and agents communicate
- `policy_engine_spec.md` — safety and approval model

## Research Inputs

These docs are synthesis inputs that help sharpen the canonical backlog and
implementation board. They should not be read as top-level architecture
commitments by themselves.

- `GITHUB_2_0_FROM_STARRED_REPOS.md` — starred-repo product synthesis
- `MORPHOS_GAP_ANALYSIS_FROM_GITHUB_STARS.md` — starred-repo gap synthesis against the current morphOS plan

## Authoring Conventions

- put new agent role docs in `docs/agents/`
- put new vision inputs in `docs/vision/`
- keep cross-cutting system specs at `docs/`
- keep workspace-wide operating rules in the root `AGENTS.md`
