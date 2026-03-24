# Starred Repo Status And Next Steps

This document turns the starred-repo backlog into a practical status map for the
current Skyforce codebase.

It is not a reading list.
It is a repo-by-repo reality check:

- what each starred repo is useful for
- what Skyforce has already implemented
- what is still missing
- which Skyforce repo should own the next move

## Status Scale

- `implemented` - the borrowed idea is materially real in code today
- `strong_partial` - the idea clearly shapes the runtime, but important slices are still missing
- `partial` - some pattern or surface is present, but the adoption is still narrow
- `spec_only` - the idea mainly exists in doctrine or planning, not runtime behavior yet

## Selected Starred Repos

### `openai/symphony`

Why it matters:

- primary upstream for orchestration posture
- strongest fit for the Elixir-first runtime spine
- shapes workflow execution, run lifecycle, and orchestration boundaries

Skyforce status:

- `strong_partial`

Already real:

- real Symphony work-order to execution-envelope path
- work-order CLI in `skyforce-symphony`
- Symphony-backed emitter used by the P0 spine
- workflow-oriented runtime shaping across Symphony, Harness, and Command Centre

Still missing:

- fuller shared event registry across repos
- deeper production orchestration semantics beyond the current proving path
- more complete durable and promotion handoff integration

Next concrete move:

- turn the current event taxonomy into a shared runtime registry used by Symphony, Harness, and Command Centre

Owning repos:

- `skyforce-symphony`
- `skyforce-core`
- `morphOS`

### `wavezync/durable`

Why it matters:

- survivability layer under orchestration
- durable refresh, resume, cancel, and checkpoint posture
- clean separation between workflow lifecycle and kernel survivability

Skyforce status:

- `strong_partial`

Already real:

- durable refresh, resume, and cancel surfaces in Command Centre
- operator-facing durable control actions
- durable state shaping in the issue operator console

Still missing:

- stronger checkpoint truth model
- clearer durable state layout and storage model
- sharper retry ownership split between workflow and durable kernel

Next concrete move:

- extract durable state and receipts into a dedicated store or service layer instead of treating them as adjacent control-plane actions

Owning repos:

- `skyforce-command-centre`
- `skyforce-symphony`
- `skyforce-core`

### `DannyMac180/ace-platform`

Why it matters:

- strongest inspiration for playbook evolution and outcome capture
- useful model for turning execution history into better future guidance
- good reference for MCP-facing execution ergonomics

Skyforce status:

- `partial`

Already real:

- outcome-oriented operator receipts and audit history
- stronger control-plane visibility into runs, approvals, and promotion posture
- explicit adoption analysis in `GENE_TRANSFUSION_FROM_ACE_PLATFORM.md`

Still missing:

- playbook discovery loop
- outcome recording specifically tied to reusable workflow guidance
- learning loop that upgrades future execution from prior run evidence

Next concrete move:

- add playbook-outcome capture per workflow run and feed it into workflow/template improvement

Owning repos:

- `skyforce-command-centre`
- `skyforce-core`
- `morphOS`

### `agentjido/jido`

Why it matters:

- best additional Elixir reference for agent, action, and signal semantics
- useful for cleaning up runtime vocabulary around directives and transitions

Skyforce status:

- `partial`

Already real:

- doctrine-level agent, action, and signal framing in `morphOS`
- operator-facing policy and event classification now shaping runtime behavior

Still missing:

- deeper concrete runtime model for agent supervision and signal handling
- clearer code-level action/signal boundary in Symphony and Core

Next concrete move:

- turn the current doctrine into shared runtime types or contracts for actions, signals, and directives

Owning repos:

- `skyforce-symphony`
- `skyforce-core`
- `morphOS`

### `sentientwave/automata`

Why it matters:

- graph and swarm execution reference
- useful for workflow graph vocabulary and branch/join semantics

Skyforce status:

- `spec_only`

Already real:

- high-level workflow and phase control doctrine

Still missing:

- concrete graph execution model
- first-class fanout, fanin, and branch-join behavior

Next concrete move:

- keep this as a later graph-runtime influence after the current factory spine is more stable

Owning repos:

- `morphOS`
- `skyforce-symphony`

### `zblanco/runic`

Why it matters:

- secondary Elixir reference for graph-oriented and swarm-like coordination

Skyforce status:

- `spec_only`

Already real:

- only indirect doctrinal influence

Still missing:

- concrete runtime adoption

Next concrete move:

- defer until after the shared event registry and durable model are stronger

Owning repos:

- `morphOS`
- `skyforce-symphony`

### `jallum/beadwork`

Why it matters:

- strongest reference for git-native durable work ledgers
- good fit for filesystem-first and audit-heavy execution

Skyforce status:

- `partial`

Already real:

- file-backed audit history
- file-backed operator action receipts
- file-backed approval and run artifacts
- strong operator-visible artifact chain

Still missing:

- true git-native work ledger
- branch-aware durable work memory
- more explicit ledger semantics around plans, decisions, and checkpoints

Next concrete move:

- introduce a small durable work-ledger layer that groups run, approval, promotion, and action history into one governed structure

Owning repos:

- `skyforce-command-centre`
- `skyforce-core`
- `morphOS`

### `volcengine/OpenViking`

Why it matters:

- strongest context and memory topology reference in the backlog
- useful for separating reference context, operational context, and persistent memory

Skyforce status:

- `partial`

Already real:

- `morphOS` context architecture and context-hub doctrine
- repaired `morphOS` runtime modules for context retrieval and context hub integration

Still missing:

- fuller production memory topology
- stronger hierarchy for reusable context delivery across repos

Next concrete move:

- stabilize context and memory into a dedicated shared subsystem instead of leaving it split between doctrine and local runtime helpers

Owning repos:

- `morphOS`
- `skyforce-core`

### `googleworkspace/cli`

Why it matters:

- good reference for structured tool exposure and dynamic action discovery
- useful for future tool-registry and adapter evolution

Skyforce status:

- `partial`

Already real:

- Harness adapter/runtime surfaces
- structured execution and artifact generation
- doctrine for tool registry and action discovery

Still missing:

- stronger dynamic tool discovery
- schema-driven tool surface generation
- unified tool registry across runtime repos

Next concrete move:

- turn the tool-registry doctrine into a minimal shared registry contract used by Harness and Core

Owning repos:

- `skyforce-harness`
- `skyforce-core`
- `morphOS`

### `fabro-sh/fabro`

Why it matters:

- useful factory-style reference for checkpointed software delivery and intervention-aware execution

Skyforce status:

- `partial`

Already real:

- approval packets
- execution receipts
- promotion preview and apply control-plane slices
- operator-facing run bundle and intervention surfaces

Still missing:

- more explicit workflow-graph execution semantics
- stronger intervention and state-machine modeling

Next concrete move:

- tighten the promotion and intervention model into a clearer run-state machine shared by Command Centre and Symphony

Owning repos:

- `skyforce-command-centre`
- `skyforce-symphony`
- `morphOS`

## Current P1 Feature Truth

This is the practical status after the recent `P1` implementation wave.

- `P1_SUMMARY_PYRAMID` - `implemented`
- `P1_OPERATOR_LOGIN_SURFACE` - `implemented`
- `P1_POLICY_HOOKS` - `partially_implemented`
- `P1_EVENT_TAXONOMY` - `partially_implemented`
- `P1_SAFE_PROMOTION` - `partially_implemented`
- `P1_UNIVERSAL_TERMINOLOGY` - `partially_implemented`

## Recommended Build Order Now

1. Merge `skyforce-command-centre-live` branch `codex/liveview-bootstrap` into `main`.
2. Update `P1_IMPLEMENTATION_STATUS.md` so the spec layer matches the current runtime truth.
3. Move promotion from control-plane simulation toward a real execution seam in `skyforce-core`.
4. Replace or harden the file-backed JSON control-plane stores with locking or a durable store layer.
5. Add a shared event registry so taxonomy stops being only a Command Centre concern.
6. Add playbook outcome capture so ACE-style learning becomes runtime reality instead of only doctrine.

## Strategic Recommendation

The starred repos should keep guiding Skyforce, but only through the lens of
current product pressure.

Right now the highest-value borrowings are:

- Symphony-style orchestration discipline
- Durable-style survivability
- ACE-style outcome capture
- Beadwork-style durable work history
- Google Workspace CLI-style tool surfacing

The lower-value move right now would be adopting more swarm or graph doctrine
before the current factory spine, promotion seam, and durable control plane are
fully hardened.
