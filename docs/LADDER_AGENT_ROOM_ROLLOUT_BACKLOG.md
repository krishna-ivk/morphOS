# Ladder Agent Room Rollout Backlog

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order. This backlog is a task-oriented companion to [LADDER_AGENT_ROOM_INTEGRATION.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_INTEGRATION.md) and [LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md).

## Purpose

This document translates the Ladder integration design into a practical rollout
backlog for `morphOS-agent-room`.

It is intended to help with:

- implementation sequencing
- issue creation
- review scoping
- progress tracking

## Delivery Lanes

The work naturally falls into five lanes:

- domain model
- UI projection
- task bridge
- validation and promotion
- export integration

## Backlog

| ID | Slice | Lane | Description | Target Repo Area | Depends On | Priority |
|---|---|---|---|---|---|---|
| LAR-001 | Ladder core tables | domain model | Add migrations for `ladder_sources`, `ladder_ideas`, `ladder_hypotheses`, and `ladder_idea_sources` | `apps/murmur_demo/priv/repo/migrations/` | none | P0 |
| LAR-002 | Ladder schemas | domain model | Add Ecto schemas for Source, Idea, and Hypothesis | `apps/murmur_demo/lib/murmur/ladder/` | LAR-001 | P0 |
| LAR-003 | Ladder context | domain model | Add `Murmur.Ladder` CRUD and transition functions | `apps/murmur_demo/lib/murmur/ladder.ex` | LAR-002 | P0 |
| LAR-004 | Read model | UI projection | Add `Murmur.Ladder.Projection` to build the workspace Ladder view model | `apps/murmur_demo/lib/murmur/ladder/projection.ex` | LAR-003 | P0 |
| LAR-005 | WorkspaceLive mount | UI projection | Load Ladder projection in `WorkspaceLive.mount/3` and subscribe to Ladder topic | `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex` | LAR-004 | P0 |
| LAR-006 | Ladder renderer | UI projection | Add `ladder_graph` renderer component for the data panel | `apps/murmur_demo/lib/murmur_web/components/artifacts/` | LAR-004 | P0 |
| LAR-007 | Ladder LiveView events | UI projection | Add create/select/update events for sources, ideas, and hypotheses | `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex` | LAR-005, LAR-006 | P0 |
| LAR-008 | Domain tests | domain model | Add unit tests for changesets and transition rules | `apps/murmur_demo/test/murmur/` | LAR-003 | P0 |
| LAR-009 | LiveView tests | UI projection | Add UI tests for Ladder rendering and live refresh | `apps/murmur_demo/test/murmur_web/live/` | LAR-007 | P0 |
| LAR-010 | Experiment table | task bridge | Add migration and schema for experiments | `apps/murmur_demo/priv/repo/migrations/`, `apps/murmur_demo/lib/murmur/ladder/` | LAR-003 | P1 |
| LAR-011 | Experiment transitions | task bridge | Add experiment start/abort/complete rules | `apps/murmur_demo/lib/murmur/ladder.ex` | LAR-010 | P1 |
| LAR-012 | Experiment-task links | task bridge | Add relation table or metadata bridge to shared tasks | `apps/murmur_demo/lib/murmur/ladder/`, `apps/jido_tasks/` | LAR-010 | P1 |
| LAR-013 | Start experiment flow | task bridge | Add agent/human flow to create tasks from a ready hypothesis | `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex` | LAR-011, LAR-012 | P1 |
| LAR-014 | Result tables | validation and promotion | Add migrations and schemas for results and evidence refs | `apps/murmur_demo/priv/repo/migrations/`, `apps/murmur_demo/lib/murmur/ladder/` | LAR-011 | P1 |
| LAR-015 | Result validation rules | validation and promotion | Add evidence-backed result validation rules | `apps/murmur_demo/lib/murmur/ladder.ex` | LAR-014 | P1 |
| LAR-016 | Algorithm tables | validation and promotion | Add migration and schema for algorithms and result links | `apps/murmur_demo/priv/repo/migrations/`, `apps/murmur_demo/lib/murmur/ladder/` | LAR-015 | P1 |
| LAR-017 | Promotion flow | validation and promotion | Add candidate-to-approved algorithm promotion path | `apps/murmur_demo/lib/murmur/ladder.ex`, `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex` | LAR-016 | P1 |
| LAR-018 | Ladder summaries | export integration | Add Ladder-specific summary text generation | `apps/murmur_demo/lib/murmur/factory_exports.ex` | LAR-015, LAR-017 | P2 |
| LAR-019 | Ladder export files | export integration | Emit `result_register.json`, `algorithm_register.json`, `ladder_context_index.json`, `experiment_plan.json` | `apps/murmur_demo/lib/murmur/factory_exports.ex` | LAR-018 | P2 |
| LAR-020 | Export tests | export integration | Add tests for Ladder-aware export manifests and payloads | `apps/murmur_demo/test/murmur/` | LAR-019 | P2 |
| LAR-021 | Connector parity | export integration | Update Python connector validation if still operationally relevant | `connectors/morphos_factory/` | LAR-019 | P3 |

## Suggested Issue Groups

### Group 1: First PR

- LAR-001
- LAR-002
- LAR-003
- LAR-004
- LAR-005
- LAR-006
- LAR-007
- LAR-008
- LAR-009

Outcome:

- workspace-scoped sources, ideas, and hypotheses with a rendered Ladder panel

### Group 2: Experiment Bridge

- LAR-010
- LAR-011
- LAR-012
- LAR-013

Outcome:

- hypotheses can create experiments and link them to shared tasks

### Group 3: Results And Algorithms

- LAR-014
- LAR-015
- LAR-016
- LAR-017

Outcome:

- evidence-backed validation and algorithm promotion

### Group 4: Export Integration

- LAR-018
- LAR-019
- LAR-020
- LAR-021

Outcome:

- factory-facing Ladder artifacts and optional connector parity

## Acceptance Checkpoints

### Checkpoint A

Pass when:

- sources, ideas, and hypotheses persist
- the Ladder panel renders correctly
- hypotheses enforce readiness rules

### Checkpoint B

Pass when:

- experiments can be created from ready hypotheses
- experiment objects link to shared tasks
- task progress is visible from Ladder context

### Checkpoint C

Pass when:

- results require evidence for validation
- algorithms require validated support or explicit override
- Ladder findings are visible in the room

### Checkpoint D

Pass when:

- exports include the intended Ladder subset
- non-validated work stays out of work-order generation
- export manifests remain backward-compatible

## Recommended Ownership

Suggested ownership by role:

- domain model: backend/product engineer
- UI projection: LiveView engineer
- task bridge: backend engineer familiar with `jido_tasks`
- validation/promotion rules: backend engineer plus product/operator review
- export integration: backend engineer familiar with `FactoryExports`

## Notes

- Keep each PR small and behaviorally coherent.
- Preserve current room behavior when Ladder data is absent.
- Treat export integration as additive, not mandatory, in early slices.
- Resist moving Ladder into a reusable umbrella app before one complete room-to-export cycle succeeds.
