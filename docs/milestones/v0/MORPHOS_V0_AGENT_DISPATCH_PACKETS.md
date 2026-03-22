# morphOS v0 Agent Dispatch Packets

This document turns the multi-agent implementation plan into ready-to-assign packets.

Use [MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md](MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md) for workstream rules, exclusivity, and wave order.
Use this file when you want to launch multiple agents without repeating system context.

## How To Use This File

- assign one packet per active agent
- attach only the listed lineage and file scope
- do not add unrelated repo history
- require the output artifact listed in the packet
- require the handoff packet format at closeout

## Dependency Matrix

| Capability | Primary owner | Depends on | Unblocks | Must not overlap with |
|---|---|---|---|---|
| Execution-mode contract | Agent A | board lineage, governance docs | orchestration mode behavior, UI mode visibility | UI wording finalization, orchestration state wiring |
| Authority contracts | Agent A | human-role lineage, policy docs | approval routing, audit surfaces, escalation flows | operator role implementation in parallel |
| Event taxonomy contract | Agent A | event lineage, current runtime events | CLI/UI alignment, receipts, observability | any repo-specific event renaming |
| Summary artifact contract | Agent A | summary lineage | CLI summary output, dashboard pyramid views, promotion packet | dashboard summary final wiring |
| Promotion contract | Agent A | validation lineage, approval lineage | promotion readiness, PR packet generation | runtime promotion behavior |
| Program runner | Agent C | frozen contracts from Agent A | delivery spine completion, receipts, validation handoff | orchestration transition redesign |
| Approval orchestration | Agent B | authority contract, summary names | approval gates, audit trail, UI approval views | harness runner internals |
| Persistent durability | Agent B | checkpoint contract, filesystem layout | resume/cancel reliability, promotion safety | separate checkpoint schema edits |
| Policy hook call sites | Agent B | policy contract, event names | governed workflow transitions, admin routing | parallel policy-schema changes |
| Delivery terminology UI rollout | Agent D | frozen terminology, stable events | operator clarity, summary legibility | upstream event or summary renaming |
| Promotion path | Agent E | stable validation outputs, stable approval states, promotion contract | source-repo closeout | contract redesign, runner redesign |

## Required Handoff Packet

Every agent must close with this exact shape:

- `scope_completed`
- `files_changed`
- `contracts_relied_on`
- `events_changed`
- `artifacts_emitted`
- `open_blockers`
- `next_owner`

## Agent A Packet

### Mission

Freeze the shared shapes so downstream runtime and UI work can proceed without re-reading all design docs.

### Owns

- `morphOS/docs/`
- `skyforce-core/packages/contracts/`

### Must produce

- execution-mode contract
- workspace-admin and super-admin contracts
- canonical event taxonomy mapping
- summary artifact contract
- promotion packet contract

### Inputs

- `docs/milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- `docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md`
- `docs/human_cell_spec.md`
- `docs/policy_engine_spec.md`
- `docs/event_bus_spec.md`
- `docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md`
- `docs/morphos-software-factory-mvp.md`

### File scope

- `morphOS/docs/`
- `skyforce-core/packages/contracts/src/`

### Must not touch

- `skyforce-symphony` orchestration logic
- `skyforce-harness` runner logic
- final dashboard copy

### Done when

- downstream agents can implement without inventing field names
- shared types are stable enough for one implementation wave
- migration notes identify every renamed or newly required field

### Output artifact

- `contract_freeze_notes.md`

### Recommended prompt

```text
Own the contract and spec freeze for morphOS v0. Work only in morphOS docs and skyforce-core contracts. Finalize execution-mode, authority, event, summary, and promotion contracts. Do not implement runtime logic or UI wording. Return a compact handoff packet plus contract_freeze_notes.md.
```

## Agent B Packet

### Mission

Implement the orchestration-side runtime semantics for program, approval, durability, and policy transitions.

### Owns

- `skyforce-symphony`

### Must produce

- stable step transitions for `program` and `approval`
- persisted checkpoint lifecycle
- policy hook call sites
- execution-mode-aware orchestration behavior

### Inputs

- Agent A contract freeze notes
- `docs/architecture/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`
- `docs/architecture/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`
- `docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md`

### File scope

- `skyforce-symphony/elixir/lib/symphony_elixir/`
- `skyforce-symphony/elixir/test/`

### Must not touch

- harness runner internals
- CLI/dashboard presentation copy
- shared contract definitions unless sent back to Agent A

### Done when

- approval pauses and resumes against stable state
- checkpoint data survives outside in-memory execution
- orchestration emits stable events and state names promised to other agents

### Output artifact

- `orchestration_state_handoff.md`

### Recommended prompt

```text
Own the Symphony orchestration layer for morphOS v0. Implement step transitions, approval pause/resume, checkpoint persistence wiring, policy hook call sites, and execution-mode behavior using frozen contracts. Do not redesign harness internals or UI text. Return a compact handoff packet plus orchestration_state_handoff.md.
```

## Agent C Packet

### Mission

Make `program` steps execute natively and emit stable receipts, artifacts, and validation handoff data.

### Owns

- `skyforce-harness`

### Must produce

- native `program` runner path
- execution receipts aligned to frozen contracts
- artifact emission aligned to filesystem layout
- validation handoff outputs consumed by promotion and summaries

### Inputs

- Agent A contract freeze notes
- Agent B orchestration state handoff for expected runner inputs and outputs
- `docs/morphos-software-factory-mvp.md`
- `docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md`

### File scope

- `skyforce-harness/scripts/`
- `skyforce-harness/src/`
- `skyforce-harness/tests/`

### Must not touch

- Symphony workflow progression semantics
- shared contracts without Agent A handoff

### Done when

- a `program` step can run under runtime control
- receipts and artifacts are stable enough for CLI, UI, and promotion use
- validation outputs do not require downstream guessing

### Output artifact

- `runner_receipt_examples.md`

### Recommended prompt

```text
Own the Harness execution layer for morphOS v0. Implement native program execution, stable receipts, artifact emission, and validation handoff outputs using the frozen contracts and Symphony expectations. Do not redesign orchestration transitions. Return a compact handoff packet plus runner_receipt_examples.md.
```

## Agent D Packet

### Mission

Make the operator-facing surfaces consistent, delivery-first, and summary-pyramid aware.

### Owns

- `sky-force-command-centre-live`
- user-facing CLI surfaces in `skyforce-core`

### Must produce

- delivery terminology rollout
- summary pyramid views
- durable and blocked state views
- workspace-admin and super-admin operator distinctions

### Inputs

- Agent A terminology and summary contract freeze
- Agent B stable workflow states
- `docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md`
- `docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md`

### File scope

- `sky-force-command-centre-live/lib/`
- `sky-force-command-centre-live/assets/`
- `skyforce-core/scripts/`

### Must not touch

- runtime orchestration logic
- contract semantics

### Done when

- CLI and dashboard use the same delivery words for the same run states
- summary pyramid layers are clearly surfaced
- authority role differences are obvious to operators

### Output artifact

- `operator_surface_wording_map.md`

### Recommended prompt

```text
Own the operator surfaces for morphOS v0. Update the dashboard and CLI to use delivery-first terminology, render the summary pyramid clearly, expose durable and blocked states, and show workspace-admin versus super-admin flows. Do not modify runtime logic or contracts. Return a compact handoff packet plus operator_surface_wording_map.md.
```

## Agent E Packet

### Mission

Close the loop back to source repos with safe promotion, deterministic closeout, and reviewable proposal packets.

### Owns

- promotion logic in `skyforce-core`
- promotion orchestration in `skyforce-symphony`

### Must produce

- promotion readiness checks
- PR or proposal packet generation
- deterministic closeout behavior for missing summaries or approval artifacts
- rollback or abort path for invalid promotion

### Inputs

- Agent A promotion contract
- Agent B stable completion and approval states
- Agent C stable validation outputs and receipts
- `docs/morphos-software-factory-mvp.md`
- `docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md`

### File scope

- `skyforce-core/scripts/`
- `skyforce-core/packages/`
- `skyforce-symphony/elixir/lib/symphony_elixir/`

### Must not touch

- shared contract shape after freeze
- core program-runner behavior

### Done when

- promotion uses explicit readiness gates
- review packets include validation, approvals, and summary artifacts
- failure states are inspectable and reversible

### Output artifact

- `promotion_packet_examples.md`

### Recommended prompt

```text
Own the promotion and closeout path for morphOS v0. Implement readiness checks, proposal or PR packet generation, deterministic closeout for mandatory artifacts, and safe abort or rollback behavior using stable contracts and validation outputs. Do not redesign runner or contract shapes. Return a compact handoff packet plus promotion_packet_examples.md.
```

## Suggested Launch Order

### Batch 1

- launch Agent A
- optionally launch Agent D for terminology inventory only

### Batch 2

- launch Agent B after Agent A freeze
- launch Agent C after Agent A freeze and Agent B input contract is clear

### Batch 3

- launch Agent D full implementation after Agent A and Agent B freeze state names
- launch Agent E after Agent B and Agent C produce stable approval and validation outputs

## Minimal Token Packet Per Agent

When dispatching, give only:

- mission
- owned repo and file scope
- exact inputs from this doc
- forbidden surfaces
- output artifact name
- handoff packet format

That is enough context for most work without resending the entire board.
