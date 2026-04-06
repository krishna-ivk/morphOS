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
- `cell_spec.md` — shared template for all agent definitions
- `schemas.md` — data contracts and shared structures
- `interaction_layer_spec.md` — how humans and agents communicate
- `policy_engine_spec.md` — safety and approval model
- `GITHUB_2_0_FROM_STARRED_REPOS.md` — starred-repo inspiration mapped into a software-factory GitHub direction
- `MORPHOS_GAP_ANALYSIS_FROM_GITHUB_STARS.md` — concrete gaps between current morphOS plans and star-driven inspiration
- `LADDER_AGENT_ROOM_INTEGRATION.md` — how Ladder can fit the morphOS agent-room and feed the software factory
- `LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md` — concise execution brief for the first Ladder integration slices
- `LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md` — task-oriented rollout backlog for implementing Ladder in the agent-room
- `LADDER_AGENT_ROOM_FAQ.md` — plain-language FAQ for the Ladder agent-room integration decisions
- `ADR_LADDER_AGENT_ROOM_V1.md` — architecture decision record for the `v1` Ladder integration approach
- `LADDER_AGENT_ROOM_REVIEW_CHECKLIST.md` — review checklist for approving the Ladder agent-room design and rollout
- `LADDER_AGENT_ROOM_DOCSET.md` — entry point for the full Ladder agent-room documentation set

## Authoring Conventions

- put new agent role docs in `docs/agents/`
- put new vision inputs in `docs/vision/`
- keep cross-cutting system specs at `docs/`
- keep workspace-wide operating rules in the root `AGENTS.md`
