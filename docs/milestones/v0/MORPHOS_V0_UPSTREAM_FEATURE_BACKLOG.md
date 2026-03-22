# morphOS v0 Upstream Feature Backlog

Canonical priority note: this file explains upstream slices; use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the final prioritized build order.

This document turns the upstream adoption map into an actionable implementation
backlog.

It answers:

- which features should be taken from each upstream system first
- where each feature should land in Skyforce
- whether the feature should be adopted directly, wrapped, or semported
- what the immediate implementation status is

Read this alongside:

- `docs/milestones/v0/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md`
- `docs/milestones/v0/MORPHOS_V0_CORE_STACK.md`
- `docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md`

## Status Labels

- `implemented`
  - already landed in at least one local runtime surface
- `in_progress`
  - architecture and some implementation exist, but the feature is not yet
    complete end to end
- `planned`
  - accepted into the v0 scope, but not yet actively integrated
- `deferred`
  - useful, but intentionally later than v0

## 1. openai/symphony

### Feature slices

1. Workflow coordination and running-entry projection
- local target:
  - `skyforce-symphony`
- adoption mode:
  - wrapped
- status:
  - `implemented`

2. Directive and approval projection
- local target:
  - `skyforce-symphony`
  - `skyforce-core`
  - operator surfaces
- adoption mode:
  - wrapped plus semported contracts
- status:
  - `implemented`

3. WorkflowRun runtime projection
- local target:
  - `skyforce-symphony`
  - `skyforce-core`
- adoption mode:
  - semported contracts over wrapped runtime output
- status:
  - `implemented`

4. Multi-agent delegation semantics
- local target:
  - `skyforce-symphony`
  - future agent-manager layer
- adoption mode:
  - wrapped
- status:
  - `in_progress`

## 2. wavezync/durable

### Feature slices

1. Durable execution request boundary
- local target:
  - `skyforce-symphony`
  - `skyforce-core`
- adoption mode:
  - wrapped plus semported contracts
- status:
  - `implemented`

2. Durable execution status projection
- local target:
  - `skyforce-symphony`
  - `skyforce-core`
  - `skyforce-command-centre`
- adoption mode:
  - wrapped
- status:
  - `implemented`

3. Checkpoint model
- local target:
  - future durable runtime
  - `skyforce-core`
- adoption mode:
  - wrapped plus semported contracts
- status:
  - `in_progress`

4. Resume and cancel lifecycle
- local target:
  - `skyforce-symphony`
  - future operator actions
- adoption mode:
  - wrapped
- status:
  - `in_progress`

5. Real durable backend beyond memory adapter
- local target:
  - future durable runtime/service
- adoption mode:
  - wrapped
- status:
  - `planned`

## 3. andrewyng/context-hub

### Feature slices

1. Reference-context retrieval
- local target:
  - future context-core subsystem
- adoption mode:
  - wrapped
- status:
  - `planned`

2. Persistent annotation model
- local target:
  - future context-core subsystem
  - operator tooling
- adoption mode:
  - wrapped plus semported contracts
- status:
  - `planned`

3. Reference/operational/persistent memory split
- local target:
  - `morphOS`
  - `skyforce-core`
- adoption mode:
  - semported
- status:
  - `implemented` for architecture, `planned` for runtime integration

4. Access labels and context trust boundaries
- local target:
  - `skyforce-core`
  - future context-core subsystem
- adoption mode:
  - semported
- status:
  - `in_progress`

## 4. ComposioHQ/agent-orchestrator

### Feature slices

1. Tool provider and tool action model
- local target:
  - `skyforce-core`
  - `skyforce-symphony`
- adoption mode:
  - semported over wrapped runtime use
- status:
  - `implemented` for contracts and observability

2. Tool execution engine
- local target:
  - future tool-engine subsystem
- adoption mode:
  - wrapped
- status:
  - `planned`

3. Approval-aware tool invocation
- local target:
  - Symphony runtime
  - future tool-engine subsystem
- adoption mode:
  - wrapped
- status:
  - `planned`

4. External result artifact projection
- local target:
  - `skyforce-core`
  - operator surfaces
- adoption mode:
  - semported
- status:
  - `in_progress`

## 5. openai/skills

### Feature slices

1. Skill reference contract
- local target:
  - `skyforce-core`
  - `morphOS`
- adoption mode:
  - semported
- status:
  - `implemented`

2. Skill packaging and registration rules
- local target:
  - future skill/plugin subsystem
- adoption mode:
  - semported
- status:
  - `planned`

3. Archetype-to-skill attachment
- local target:
  - `morphOS`
  - future agent-manager layer
- adoption mode:
  - semported
- status:
  - `planned`

4. Skill trust and versioning
- local target:
  - future skill/plugin subsystem
- adoption mode:
  - semported
- status:
  - `deferred`

## Recommended Immediate Next Slices

These are the strongest next implementation steps from the backlog:

1. Durable checkpoint and resume/cancel flow
- reason:
  - it completes the current Symphony/Durable bridge

2. LiveView durable-status visibility
- reason:
  - React and CLI already expose some of this posture

3. Context Hub integration plan for reference context
- reason:
  - context is the next major stack boundary after orchestration and durability

4. Tool-engine contract refinement around `ToolAction`
- reason:
  - the contract now exists; execution semantics need to catch up

5. Skill packaging rules
- reason:
  - needed before skills become a real reusable subsystem

## Bottom Line

The upstream repos are now part of the `morphOS v0` build plan in two ways:

- architectural adoption map
- implementation backlog

That means the answer to "what are we taking from each upstream repo?" is no
longer implicit. It is now explicit, prioritized, and tied to local targets.
