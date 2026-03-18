# Documentation Guide

Use this folder as the main entry point for SkyForce specifications.

## Sections

- `agents/` — role definitions for specialized agent cells
- `vision/` — product vision and problem framing inputs
- `human_roles/` — human collaborators, responsibilities, and escalation paths
- root `docs/*.md` — system-level architecture, schemas, runtime, and policy specs

## Start Here

- `agentic_os_architecture.md` — overall operating system design
- `cell_spec.md` — shared template for all agent definitions
- `schemas.md` — data contracts and shared structures
- `interaction_layer_spec.md` — how humans and agents communicate
- `policy_engine_spec.md` — safety and approval model

## Authoring Conventions

- put new agent role docs in `docs/agents/`
- put new vision inputs in `docs/vision/`
- keep cross-cutting system specs at `docs/`
- keep workspace-wide operating rules in the root `AGENTS.md`
