# Ladder Agent Room Implementation Brief

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order. This brief is the short execution companion to [LADDER_AGENT_ROOM_INTEGRATION.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_INTEGRATION.md).

## Goal

Integrate `Ladder` into `morphOS-agent-room` as a workspace-scoped discovery
and validation subsystem that:

- turns room discussion into structured objects
- links experiments to the shared task board
- promotes validated findings into exportable factory artifacts
- does not introduce a second orchestration runtime

## `v1` Scope

In scope:

- sources
- ideas
- hypotheses
- Ladder projection in the room UI
- relational persistence in `murmur_demo`

Out of scope for the first PR:

- experiments
- results
- algorithms
- export extensions
- cross-workspace reuse

## First PR Target

Implement the smallest useful slice in `../morphos-agent-room`:

- `apps/murmur_demo/lib/murmur/ladder.ex`
- `apps/murmur_demo/lib/murmur/ladder/source.ex`
- `apps/murmur_demo/lib/murmur/ladder/idea.ex`
- `apps/murmur_demo/lib/murmur/ladder/hypothesis.ex`
- `apps/murmur_demo/lib/murmur/ladder/projection.ex`
- `apps/murmur_demo/lib/murmur_web/components/artifacts/ladder_graph.ex`
- `apps/murmur_demo/priv/repo/migrations/*_create_ladder_core_tables.exs`
- `apps/murmur_demo/test/murmur/ladder_test.exs`
- `apps/murmur_demo/test/murmur_web/live/workspace_live_ladder_test.exs`

## Core Decisions

- canonical state lives in relational tables, not artifact-only storage
- `murmur_demo` is the `v1` home of the Ladder domain
- the UI renders a Ladder projection rather than deriving state from chat
- experiments later integrate with `jido_tasks`
- export later extends `Murmur.FactoryExports`

## Minimal Data Model

Tables for the first PR:

- `ladder_sources`
- `ladder_ideas`
- `ladder_hypotheses`
- `ladder_idea_sources`

Minimum statuses:

- ideas: `proposed`, `shortlisted`, `rejected`
- hypotheses: `draft`, `ready`, `archived`

Minimum rule:

- a hypothesis cannot become `ready` without both `success_metric` and
  `failure_metric`

## UI Shape

Add one Ladder panel to the workspace data area with:

- `Inbox`
  - sources
- `Incubator`
  - ideas
- `Claims`
  - hypotheses

First PR interactions:

- create source
- propose idea
- create hypothesis
- mark hypothesis ready
- select an object for detail view

## Acceptance Criteria

The first PR is complete when:

- a workspace can persist sources, ideas, and hypotheses
- Ladder objects survive refresh and restart
- the Ladder panel renders current state from a backend projection
- hypotheses enforce readiness metrics
- LiveView updates reflect Ladder changes without transcript parsing
- tests cover context transitions and basic UI rendering

## Suggested Sequence

1. Add migrations and Ecto schemas.
2. Add `Murmur.Ladder` context API.
3. Add projection builder.
4. Add Ladder assign/subscription flow in `WorkspaceLive`.
5. Add renderer component.
6. Add tests.

## Immediate Follow-Up PRs

Second PR:

- experiments
- task linking through `jido_tasks`

Third PR:

- results
- validation rules
- algorithm promotion

Fourth PR:

- export extension in `Murmur.FactoryExports`
- Ladder-aware artifact files

## Risks To Watch

- UI starts owning state mutations
- artifact projection becomes mistaken for canonical persistence
- first PR grows to include experiments or export logic
- Ladder status model drifts from task/external export eligibility rules

## Build Posture

Use a conservative rollout:

- small relational core first
- UI projection second
- operational task bridge third
- export integration last

That ordering gives `morphOS-agent-room` a usable Ladder foundation without
destabilizing its current room, task, or export behavior.
