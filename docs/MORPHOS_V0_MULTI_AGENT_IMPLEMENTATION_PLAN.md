# morphOS v0 Multi-Agent Implementation Plan

This document translates the canonical board into a parallel execution plan for multiple agents working across `morphOS` and the Skyforce repos.

Use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/Software Factory/morphOS/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for final priority order.
Use this document when you need to answer different questions:

- which workstreams can run in parallel
- which items block other items
- which repo owns each slice
- what lineage each implementation slice comes from
- where agents must not overlap
- how to minimize duplicated context and token burn

## Planning Rule

Plan by dependency, not by repo.

The right execution order for v0 is:

1. close the software-factory loop
2. make the loop survivable
3. make the loop governable
4. make the loop legible for humans
5. close promotion back into source repos

## Canonical Workstreams

### WS1. Delivery Spine Runtime

Board lineage:

- end-to-end delivery spine
- full `program` and `approval` step execution

Primary repos:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-core`
- `sky-force-command-centre-live`

Goal:

- make `ticket -> workflow -> workspace -> code -> validation -> approval -> promotion` work as one real runtime path

Exit criteria:

- workflow steps execute as real runtime actions
- `program` steps produce receipts and artifacts
- `approval` steps block, surface, and resume correctly
- validation results feed the same run state

### WS2. Durable Survivability

Board lineage:

- durable checkpoint, resume, and cancel lifecycle
- filesystem-first run state and memory layout

Primary repos:

- `skyforce-symphony`
- `skyforce-core`
- `morphOS`

Goal:

- make long-running work restartable, inspectable, and recoverable

Exit criteria:

- checkpoints persist beyond process memory
- resume and cancel work against stored state
- run state is inspectable on disk with stable paths and artifacts

### WS3. Governance And Control

Board lineage:

- explicit `interactive` vs `factory` execution mode
- workspace-scoped admin model
- super-admin global authority model
- policy hooks at workflow boundaries

Primary repos:

- `morphOS`
- `skyforce-core`
- `skyforce-symphony`
- `sky-force-command-centre-live`

Goal:

- give the runtime explicit authority, approval routing, and execution constraints

Exit criteria:

- every run declares or derives an execution mode
- risky actions route to the correct human authority
- policy checks run at workflow boundaries
- audit artifacts show who approved what and why

### WS4. Shared Language And Visibility

Board lineage:

- summary pyramid across CLI, dashboard, and artifacts
- universal delivery terminology in operator surfaces
- event taxonomy alignment across repos

Primary repos:

- `morphOS`
- `skyforce-core`
- `skyforce-symphony`
- `sky-force-command-centre-live`
- `skyforce-harness`

Goal:

- make every surface describe the same run using the same words and evidence layers

Exit criteria:

- one-line, short, full, and evidence views are emitted consistently
- events use one canonical taxonomy
- operator surfaces prefer delivery language over protocol language

### WS5. Promotion Back To Source

Board lineage:

- safe promotion of workspace results back into source repos

Primary repos:

- `skyforce-core`
- `skyforce-symphony`
- `sky-force-command-centre-live`
- `morphOS`

Goal:

- convert validated workspace results into safe source-repo proposals

Exit criteria:

- promotion readiness is explicit
- promotion emits reviewable artifacts
- PR or equivalent proposal flow uses validation and approval thresholds

## Dependency Order

### Layer 0: Contract And Spec Prerequisites

These items should land before broad runtime fan-out:

- filesystem run layout contract
- durable checkpoint contract finalization
- execution mode contract
- workspace-admin and super-admin contracts
- event taxonomy contract
- summary artifact contract
- promotion contract

Most of this belongs first in:

- `morphOS/docs/`
- `skyforce-core/packages/contracts/`

### Layer 1: Runtime Backbone

These items unlock the main loop:

- native `program` step execution in `skyforce-harness`
- native `approval` step pause and resume in `skyforce-symphony`
- persistent checkpoint storage in `skyforce-symphony`
- receipt and artifact projection in `skyforce-core`

### Layer 2: Governance Hooks

These should land once the backbone exists:

- policy checks on step entry and exit
- execution-mode-aware workflow behavior
- workspace-admin approval routing
- super-admin escalation path

### Layer 3: Human Surfaces

These should move once contracts and runtime events stabilize:

- universal delivery terminology in UI and CLI
- summary pyramid rendering
- durable-state and blocked-work views
- approval and audit views by authority role

### Layer 4: Promotion

Promotion should come last in MVP order because it depends on the earlier layers being trustworthy:

- promotion readiness calculation
- change packet or PR packet generation
- approval-aware promotion action
- rollback or abort path for invalid promotion

## Parallelization Model

Use five agents at most for the primary v0 push.

More than five agents increases coordination cost faster than delivery speed.

### Agent A: Contracts And Specs

Primary scope:

- `morphOS/docs/`
- `skyforce-core/packages/contracts/`

Owns:

- execution-mode schema
- authority model contracts
- event taxonomy contract
- summary artifact contract
- promotion contract

May not change:

- runtime execution logic
- UI presentation text except contract-driven labels

Output artifacts:

- contract diffs
- schema notes
- migration notes for downstream agents

### Agent B: Runtime Orchestration

Primary scope:

- `skyforce-symphony`

Owns:

- workflow progression semantics
- approval pause and resume behavior
- durable checkpoint orchestration
- policy hook call sites
- execution-mode behavior at orchestration time

May not change:

- `skyforce-harness` execution internals
- final UI wording

Output artifacts:

- state machine notes
- event emission notes
- run-state examples

### Agent C: Runtime Execution

Primary scope:

- `skyforce-harness`

Owns:

- native `program` runner
- execution receipts
- artifact emission
- sandbox boundary adapters

May not change:

- orchestration step ordering
- global contracts unless Agent A approves a handoff

Output artifacts:

- runner receipts
- command execution traces
- validation handoff notes

### Agent D: Operator Surface

Primary scope:

- `sky-force-command-centre-live`
- user-facing parts of `skyforce-core` CLI

Owns:

- summary pyramid presentation
- delivery terminology rollout
- durable-state visibility
- admin-role views and approval routing surfaces

May not change:

- contract semantics without Agent A handoff
- runtime logic without Agent B handoff

Output artifacts:

- UI wording map
- operator flows
- screenshot or state examples

### Agent E: Promotion And Closeout

Primary scope:

- promotion path in `skyforce-core`
- promotion orchestration in `skyforce-symphony`

Owns:

- promotion readiness checks
- PR packet or proposal packet generation
- deterministic closeout middleware
- source-repo safety checks

May not change:

- upstream runtime step semantics beyond promotion boundaries

Output artifacts:

- promotion packet examples
- closeout checklist
- failure and rollback notes

## Exclusivity Rules

These rules are mandatory if multiple agents are active at once.

### 1. One agent per ownership surface

At any moment, only one agent may own mutation rights for each of these surfaces:

- `morphOS/docs/` contracts and planning docs
- `skyforce-core/packages/contracts/`
- `skyforce-symphony/elixir/lib/symphony_elixir/`
- `skyforce-harness/scripts/` and runtime adapters
- `sky-force-command-centre-live/lib/` and frontend UI flow files

### 2. Contract-first exclusivity

If a change touches a shared schema, event name, artifact shape, or policy decision format:

- Agent A goes first
- all other agents consume the agreed shape
- no parallel contract edits are allowed after runtime implementation starts

### 3. Orchestrator vs runner exclusivity

To avoid token waste and duplicated reasoning:

- Agent B owns step semantics and run-state transitions
- Agent C owns command execution and execution receipts
- Agent B must not redesign runner internals
- Agent C must not redesign orchestration transitions

### 4. UI follows contract and runtime

Agent D should not begin final UI copy and state rendering until:

- Agent A freezes terminology and summary names
- Agent B freezes key workflow states

Exploratory mocks are allowed, but not final state wiring.

### 5. Promotion waits for validation lineage

Agent E may design the promotion packet early, but must not finalize promotion logic until:

- Agent C emits stable validation outputs
- Agent B emits stable approval and completion states

### 6. No duplicate repo exploration

Each agent should receive a narrow file list and should not rescan the entire repo.

Required handoff format:

- changed files
- depended-on contracts
- emitted artifacts
- unresolved blockers
- exact next owner

## Lineage Map

Use lineage to avoid re-deriving intent.

### Delivery spine lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/morphos-software-factory-mvp.md`
- runtime owner: `skyforce-symphony`
- execution owner: `skyforce-harness`
- aggregation owner: `skyforce-core`
- human surface owner: `sky-force-command-centre-live`

### Durable lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`
- design: `docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`
- contract owner: `skyforce-core`
- runtime owner: `skyforce-symphony`

### Filesystem and memory lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/morphos-software-factory-mvp.md`
- design: `docs/CONTEXT_ARCHITECTURE.md`
- contract owner: `skyforce-core`
- runtime owner: `skyforce-symphony`

### Governance lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/human_cell_spec.md`
- design: `docs/policy_engine_spec.md`
- contract owner: `skyforce-core`
- runtime owner: `skyforce-symphony`
- surface owner: `sky-force-command-centre-live`

### Language and observability lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md`
- design: `docs/event_bus_spec.md`
- design: `docs/morphos-software-factory-mvp.md`
- contract owner: `skyforce-core`
- surface owner: `sky-force-command-centre-live`

### Promotion lineage

- board: `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- design: `docs/morphos-software-factory-mvp.md`
- contract owner: `skyforce-core`
- runtime owner: `skyforce-symphony`
- surface owner: `sky-force-command-centre-live`

## Execution Waves

### Wave 1: Freeze shared shapes

Parallel allowed:

- Agent A on contracts and missing morphOS spec detail
- Agent D on terminology inventory only

Do not parallelize yet:

- runtime implementation against unstable contracts

Deliverables:

- execution-mode contract
- authority contract
- durable checkpoint and artifact contract adjustments
- canonical event names
- canonical summary artifact names
- promotion packet schema

### Wave 2: Build the runtime backbone

Parallel allowed:

- Agent B on Symphony orchestration
- Agent C on Harness execution

Dependencies:

- Wave 1 contracts must be frozen

Deliverables:

- runnable `program` path
- resumable `approval` path
- persisted checkpoint lifecycle
- stable receipts and artifacts

### Wave 3: Add governance

Parallel allowed:

- Agent B on policy hook call sites
- Agent A on any narrow contract extensions
- Agent D on authority-aware operator views

Dependencies:

- Wave 2 state model must be stable

Deliverables:

- policy checks at workflow boundaries
- execution mode behavior
- workspace-admin routing
- super-admin escalation

### Wave 4: Unify surfaces

Parallel allowed:

- Agent D on dashboard and CLI presentation
- Agent A on final terminology cleanup in specs

Dependencies:

- Wave 3 state, events, and summaries must be stable

Deliverables:

- summary pyramid visible across surfaces
- universal delivery terminology rollout
- durable, blocked, and approval state views

### Wave 5: Close promotion loop

Parallel allowed:

- Agent E on promotion path
- Agent D on promotion UI

Dependencies:

- validation, approval, and summary outputs must be stable

Deliverables:

- promotion readiness calculation
- PR or proposal packet generation
- approval-aware promotion action
- promotion audit artifacts

## Token Optimization Rules

The plan should reduce duplicate context loading.

### Context budget rules

- give each agent one workstream, not the whole board
- give each agent a narrow lineage packet with only the relevant docs and files
- never ask more than one agent to interpret the same contract doc at the same time
- freeze terminology before UI work to avoid repeated rewrite passes
- require handoff artifacts instead of asking the next agent to rediscover state

### Recommended handoff packet

Every agent should leave a compact packet with:

- scope completed
- files changed
- contracts relied on
- events added or changed
- artifacts emitted
- open blockers
- exact consumer agent

### Recommended prompt discipline

Each agent prompt should include only:

- the current workstream goal
- the owned repo and files
- the exact dependency inputs
- the exact forbidden surfaces
- the required output artifact

Do not include the full system backstory once lineage is already attached.

## Suggested First Parallel Batch

Start here for the highest leverage:

1. Agent A: freeze execution-mode, event, summary, and authority contracts
2. Agent B: prepare Symphony step transition and durable persistence changes against frozen contracts
3. Agent C: implement native `program` execution and receipt emission in Harness
4. Agent D: prepare terminology and summary-surface inventory only
5. Agent E: draft promotion packet schema and closeout rules only

This batch optimizes for future parallelism because it removes the highest-cost ambiguities first.

## Definition Of Done For The Multi-Agent Push

The v0 push is complete when:

- a ticket starts one durable run
- the run selects and executes a workflow
- `program` steps produce real artifacts and receipts
- `approval` steps block and resume with explicit authority routing
- validation, summaries, and evidence attach to the same run state
- CLI and dashboard show the same run using the same terminology
- promotion emits a safe reviewable proposal back to the source repo

## What Not To Parallelize

Do not split these across multiple active agents:

- event taxonomy design
- authority model design
- summary artifact naming
- promotion packet schema
- any migration that renames shared run-state fields

Each of those should have one temporary owner and one accepted shape before downstream work begins.
