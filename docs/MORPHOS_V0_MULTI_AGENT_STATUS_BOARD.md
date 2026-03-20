# morphOS v0 Multi-Agent Status Board

This document is the operating board for running multiple implementation agents across waves.

Use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/Software Factory/morphOS/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for priority.
Use [MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md](/Users/shivakrishnayadav/Documents/Software Factory/morphOS/docs/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md) for dependency and exclusivity rules.
Use this file to track live ownership, handoffs, and blockers.

## How To Operate This Board

- one row per active or planned agent assignment
- one owner per exclusive surface at a time
- update status as soon as ownership changes
- do not start a blocked packet early just because a repo is idle
- attach the handoff artifact path before closing a row

## Status Values

- `planned`
- `ready`
- `active`
- `blocked`
- `handoff_ready`
- `complete`

## Ownership Surfaces

Only one active owner is allowed per surface:

- `morphOS/docs/`
- `skyforce-core/packages/contracts/`
- `skyforce-symphony/elixir/lib/symphony_elixir/`
- `skyforce-harness/scripts/`
- `skyforce-harness/src/`
- `sky-force-command-centre-live/lib/`
- `skyforce-core/scripts/`

## Master Board

| Wave | Agent | Work packet | Owned surfaces | Depends on | Status | Handoff artifact | Notes |
|---|---|---|---|---|---|---|---|
| 1 | A | Contract and spec freeze | `morphOS/docs/`, `skyforce-core/packages/contracts/` | none | `complete` | `docs/contract_freeze_notes.md` | Wave 1 freeze published |
| 1 | B | Orchestration backbone | `skyforce-symphony/elixir/lib/symphony_elixir/` | Agent A freeze | `complete` | `docs/orchestration_state_handoff.md` | initial runtime state alignment landed |
| 1 | C | Program runner and receipts | `skyforce-harness/scripts/`, `skyforce-harness/src/` | Agent A freeze, Agent B runner expectations | `handoff_ready` | `docs/runner_receipt_examples.md` | receipt and evidence alignment landed |
| 1 | D | UI and CLI inventory only | `sky-force-command-centre-live/lib/`, `skyforce-core/scripts/` | Agent A terminology freeze | `handoff_ready` | `docs/operator_surface_wording_map.md` | inventory completed; UI rollout waits for Wave 2 |
| 1 | E | Promotion path | `skyforce-core/scripts/`, `skyforce-symphony/elixir/lib/symphony_elixir/` | Agent B stable completion, Agent C stable validation | `blocked` | `promotion_packet_examples.md` | not a wave 1 starter |
| 2 | A | Narrow contract extensions | `morphOS/docs/`, `skyforce-core/packages/contracts/` | Wave 1 findings | `planned` | `contract_delta_notes.md` | only if needed |
| 2 | B | Governance hooks and authority routing | `skyforce-symphony/elixir/lib/symphony_elixir/` | Wave 1 stable states | `planned` | `governance_state_handoff.md` | policy and routing |
| 2 | D | Full operator surface rollout | `sky-force-command-centre-live/lib/`, `skyforce-core/scripts/` | Wave 1 state and names | `planned` | `operator_release_notes.md` | real UI wiring starts here |
| 3 | E | Promotion and deterministic closeout | `skyforce-core/scripts/`, `skyforce-symphony/elixir/lib/symphony_elixir/` | Wave 1 validation lineage, Wave 2 governance signals | `planned` | `promotion_packet_examples.md` | closes loop |

## Current Gate Checklist

### Gate G1: Contract Freeze

Must be true before Wave 1 runtime work begins:

- execution-mode fields are frozen
- authority fields are frozen
- canonical event names are frozen
- summary artifact names are frozen
- promotion packet minimum fields are frozen

### Gate G2: Runtime Backbone Stable

Must be true before Wave 2 governance work begins:

- `program` step outputs are stable
- approval pause and resume states are stable
- checkpoint persistence is stable
- receipt and artifact shapes are stable

### Gate G3: Governance Stable

Must be true before Wave 3 promotion finalization:

- policy hook states are stable
- authority routing states are stable
- dashboard and CLI reflect stable summary and event names

## Handoff Log Template

Copy this block when one agent hands off to another:

```text
Date:
From agent:
To agent:
Work packet:
Scope completed:
Files changed:
Contracts relied on:
Events changed:
Artifacts emitted:
Open blockers:
Next owner:
```

## Blocker Rules

Escalate to contract ownership immediately if:

- two agents need different names for the same field
- event names differ across repos for the same transition
- a new artifact is required by multiple downstream agents
- UI wording depends on unstable runtime states

Escalate to orchestration ownership immediately if:

- runner outputs cannot map to workflow transitions
- approval routing needs a new state transition

## Token Discipline

When updating this board, log only:

- ownership change
- status change
- blocker creation or resolution
- handoff artifact path

Do not paste long reasoning into the board.

This file should stay compact enough for every agent to consume quickly.
