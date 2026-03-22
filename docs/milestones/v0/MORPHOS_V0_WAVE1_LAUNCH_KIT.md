# morphOS v0 Wave 1 Launch Kit

This document is the fastest way to start the first parallel implementation wave.

Use [MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md](MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md) for system coordination rules.
Use [MORPHOS_V0_AGENT_DISPATCH_PACKETS.md](MORPHOS_V0_AGENT_DISPATCH_PACKETS.md) for the full packet definitions.

This file is intentionally narrower.
It only covers the first launch batch and the minimum prompts needed to begin work.

## Wave 1 Goal

Freeze the shared shapes and begin the runtime backbone without wasting tokens on repeated rediscovery.

Wave 1 should produce:

- frozen contracts for execution mode, authority, events, summaries, and promotion
- a Symphony implementation path ready for those contracts
- a Harness implementation path ready for those contracts
- a terminology inventory for later UI rollout

## Launch Order

### Step 1

Launch Agent A alone first.

Agent A is the contract freeze owner.
No downstream runtime implementation should finalize before Agent A publishes its freeze notes.

### Step 2

Once Agent A publishes `contract_freeze_notes.md`, launch these in parallel:

- Agent B
- Agent C
- Agent D in inventory-only mode

### Step 3

Do not launch Agent E yet.

Agent E depends on:

- stable validation outputs from Agent C
- stable approval and completion states from Agent B

## Hard Gates

Do not pass these gates out of order:

1. Agent A freezes shared contracts
2. Agent B and Agent C confirm their state and receipt shapes against the freeze
3. Agent D uses the frozen terminology and summary names
4. Agent E starts only after approval and validation lineage stabilize

## Wave 1 Ownership Map

| Agent | Repo focus | Status in wave 1 | Blocking relationship |
|---|---|---|---|
| Agent A | `morphOS`, `skyforce-core` contracts | mandatory first | blocks B, C, D final wiring, E |
| Agent B | `skyforce-symphony` | starts after A freeze | depends on A, informs C and D |
| Agent C | `skyforce-harness` | starts after A freeze | depends on A and B expectations |
| Agent D | `sky-force-command-centre-live`, CLI inventory only | can start after A freeze | depends on A terminology freeze |
| Agent E | promotion path | do not start in wave 1 | depends on B and C outputs |

## Copy-Paste Prompt: Agent A

```text
You are Agent A for morphOS v0.

Mission:
Freeze the shared contract and spec shapes so downstream runtime and UI work can proceed without re-reading the entire system.

Own only:
- morphOS docs
- skyforce-core contracts

Required outputs:
- execution-mode contract
- workspace-admin and super-admin contracts
- canonical event taxonomy mapping
- summary artifact contract
- promotion packet contract
- contract_freeze_notes.md

Inputs:
- morphOS/docs/milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md
- morphOS/docs/milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md
- morphOS/docs/human_cell_spec.md
- morphOS/docs/policy_engine_spec.md
- morphOS/docs/event_bus_spec.md
- morphOS/docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md
- morphOS/docs/morphos-software-factory-mvp.md

Forbidden surfaces:
- skyforce-symphony runtime logic
- skyforce-harness runner logic
- final dashboard or CLI wording work

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Copy-Paste Prompt: Agent B

Launch only after Agent A publishes `contract_freeze_notes.md`.

```text
You are Agent B for morphOS v0.

Mission:
Implement the Symphony orchestration-side runtime semantics for program, approval, durability, policy transitions, and execution-mode behavior using frozen contracts.

Own only:
- skyforce-symphony orchestration and tests

Required outputs:
- stable step transitions for program and approval
- persisted checkpoint lifecycle wiring
- policy hook call sites
- execution-mode-aware orchestration behavior
- orchestration_state_handoff.md

Inputs:
- Agent A contract_freeze_notes.md
- morphOS/docs/architecture/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md
- morphOS/docs/architecture/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md
- morphOS/docs/milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md

Forbidden surfaces:
- skyforce-harness runner internals
- final CLI or dashboard wording
- shared contracts unless escalated back to Agent A

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Copy-Paste Prompt: Agent C

Launch only after Agent A publishes `contract_freeze_notes.md` and Agent B confirms expected runner inputs and outputs.

```text
You are Agent C for morphOS v0.

Mission:
Implement native program-step execution in Harness and emit stable receipts, artifacts, and validation handoff outputs using the frozen contracts.

Own only:
- skyforce-harness execution layer and tests

Required outputs:
- native program runner path
- stable execution receipts
- artifact emission aligned to filesystem layout
- validation handoff outputs
- runner_receipt_examples.md

Inputs:
- Agent A contract_freeze_notes.md
- Agent B orchestration_state_handoff.md
- morphOS/docs/morphos-software-factory-mvp.md
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md
- morphOS/docs/milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md

Forbidden surfaces:
- Symphony workflow progression semantics
- shared contracts without Agent A approval

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Copy-Paste Prompt: Agent D

Wave 1 Agent D is inventory-only.
Do not wire final UI state in this batch.

```text
You are Agent D for morphOS v0.

Mission:
Prepare an operator-surface inventory for delivery terminology and summary-pyramid rollout using the frozen contract language. In this wave, inventory only; do not finalize UI wiring.

Own only:
- sky-force-command-centre-live inventory
- user-facing skyforce-core CLI inventory

Required outputs:
- current wording inventory
- mismatch list against delivery terminology
- summary-pyramid surface map
- operator_surface_wording_map.md

Inputs:
- Agent A contract_freeze_notes.md
- morphOS/docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md
- morphOS/docs/milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md

Forbidden surfaces:
- runtime logic
- contract changes
- final UI state wiring

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Wave 1 Success Checklist

- Agent A publishes one accepted freeze note
- Agent B can point to stable orchestration states
- Agent C can point to stable receipt and artifact outputs
- Agent D can point to a finite wording and summary rollout list
- no two agents edit the same ownership surface in parallel

## Stop Conditions

Pause the wave if any of these happen:

- Agent B or C needs to rename a shared field
- Agent D discovers terminology depends on unstable event names
- Agent C cannot map runner outputs to the frozen summary or promotion contracts
- more than one agent begins editing shared contracts

If a stop condition happens, return ownership to Agent A, update the freeze, then relaunch downstream work.
