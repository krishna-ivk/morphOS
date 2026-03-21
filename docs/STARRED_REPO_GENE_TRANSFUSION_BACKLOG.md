# Starred Repo Gene Transfusion Backlog

This document turns the public starred repositories on the `krishna-ivk` GitHub
profile into a practical morphOS specification backlog.

It is not a generic reading list.
It is an execution-ordered adoption map.

## Design Rule

Follow this preference order unless a lower-ranked repo contributes a uniquely
important idea:

1. Elixir and Erlang references first
2. Rust references second
3. Other languages only when the idea is materially stronger than the local
   implementation options

This keeps Skyforce aligned with its runtime bias:

- `skyforce-symphony` as the orchestration center
- OTP-style process and supervision semantics where possible
- Rust for high-performance, tool-facing, and CLI-adjacent subsystems

## Scope

This backlog is derived from the public starred repositories visible on the
`krishna-ivk` profile as of March 21, 2026.

Primary source:

- <https://github.com/krishna-ivk?tab=stars>

## Execution Order

## Phase 1: Lock The Elixir Runtime Spine

These repos should shape the next round of runtime-facing morphOS specs before
additional context, tools, or workflow packaging work.

### 1. `openai/symphony`

Why first:

- it is already a core upstream for Skyforce
- it matches the Elixir-first platform direction
- it defines the orchestration center

Spec topics to continue:

- `WorkflowRun` semantics
- isolated implementation-run lifecycle
- directive creation and projection
- approval pause and resume semantics
- orchestration event families

Likely output docs:

- refinement of `MORPHOS_V0_RUNTIME_CONTRACTS.md`
- refinement of `SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`

Implementation target:

- `skyforce-symphony`
- `skyforce-core`

### 2. `wavezync/durable`

Why second:

- it completes the survivability layer under Symphony
- it is also Elixir-native
- it is already named as a mandatory stack component

Spec topics to continue:

- durable checkpoint truth
- durable execution request boundary
- durable status projection
- resume and cancel lifecycle
- retry ownership split between workflow and kernel

Likely output docs:

- refinement of `DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`
- a future durable-state layout spec

Implementation target:

- `skyforce-symphony`
- `skyforce-core`
- future durable runtime surface

### 3. `agentjido/jido`

Why third:

- strongest additional Elixir reference for agent semantics
- useful for cleaning up agent, action, and signal boundaries
- close fit with Symphony runtime concerns

Spec topics to continue:

- `Agent`
- `Action`
- `Signal`
- `Directive`
- side-effect boundary vs state transition boundary
- supervision and recovery semantics for agent processes

Likely output docs:

- new `AGENT_SIGNAL_AND_ACTION_MODEL.md`
- refinement of `cell_spec.md`

Implementation target:

- `morphOS`
- `skyforce-symphony`
- `skyforce-core`

### 4. `sentientwave/automata` and `zblanco/runic`

Why fourth:

- they are good secondary Elixir references for graph and swarm behavior
- lower priority than Symphony and Durable because they are less central

Spec topics to continue:

- DAG semantics
- fanout and fanin behavior
- branch join semantics
- swarm coordination vocabulary

Likely output docs:

- refinement of workflow graph semantics
- refinement of `agentic_os_architecture.md`

Implementation target:

- `morphOS`
- `skyforce-symphony`

## Phase 2: Make Work Durable And Inspectable

These repos help define how work should persist on disk and in git-backed state.

### 5. `jallum/beadwork`

Why here:

- not Elixir, but the idea quality is too strong to ignore
- strongest reference for git-native durable work ledgers
- directly fits filesystem-first morphOS doctrine

Spec topics to continue:

- git-native work ledger
- file-backed plans, progress, and decisions
- agent-visible but human-auditable work history
- branch-isolated run memory

Likely output docs:

- new `GIT_NATIVE_WORK_LEDGER_SPEC.md`
- refinement of filesystem-first run-state layout docs

Implementation target:

- `morphOS`
- `skyforce-core`
- `skyforce-symphony`

### 6. `volcengine/OpenViking`

Why here:

- strongest context and memory reference in the starred set
- directly useful for morphOS context and memory topology
- fits filesystem-oriented reasoning even though it is not Elixir or Rust

Spec topics to continue:

- context/resource/skill hierarchy
- hierarchical context delivery
- memory topology on disk
- separation of reference context, operational context, and persistent memory

Likely output docs:

- new `FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md`
- refinement of `CONTEXT_ARCHITECTURE.md`
- refinement of `CONTEXT_HUB_INTEGRATION_PLAN.md`

Implementation target:

- `morphOS`
- `skyforce-core`
- future context subsystem

## Phase 3: Define Safe Tool Surfaces

Rust references become especially valuable once the orchestration and
survivability model is stable.

### 7. `googleworkspace/cli`

Why first in the Rust wave:

- strong example of dynamic, structured, agent-friendly tool exposure
- relevant to external action surfaces
- good fit for a `ToolAction`-driven model

Spec topics to continue:

- dynamic tool discovery
- structured CLI action contracts
- command surface generation from upstream schemas
- agent-friendly machine-readable output conventions

Likely output docs:

- new `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
- refinement of `ToolAction`-related contracts

Implementation target:

- `skyforce-core`
- future tool engine
- command-centre integrations

### 8. `fabro-sh/fabro`

Why second in the Rust wave:

- direct software-factory relevance
- useful for control-flow, intervention, and graph execution ideas

Spec topics to continue:

- graph-defined work execution
- intervention points
- operator checkpoints
- reviewable production-line style work surfaces

Likely output docs:

- new `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`

Implementation target:

- `morphOS`
- `skyforce-symphony`
- `skyforce-command-centre`

### 9. `rtk-ai/rtk`

Why third in the Rust wave:

- helpful for token-efficiency and command mediation ideas
- lower priority than tool discovery and factory control

Spec topics to continue:

- token-conscious mediation layer
- command proxy semantics
- cost-aware execution shaping

Likely output docs:

- future `TOKEN_AND_COMMAND_MEDIATION_SPEC.md`

Implementation target:

- `skyforce-core`
- CLI and command runners

## Phase 4: Package Reusable Workflows

### 10. `nikilster/clawflows`

Why here:

- strong source for reusable workflow packs
- useful after core runtime semantics are stable

Spec topics to continue:

- workflow pack format
- workflow registry model
- pack validation and compatibility rules
- import/export between workflow libraries and local runtime templates

Likely output docs:

- new `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`

Implementation target:

- `morphOS`
- `skyforce-symphony`

## Phase 5: Strengthen Governance And Operator Surfaces

### 11. `paperclipai/paperclip`

Why here:

- useful for operator control plane thinking
- later than runtime and durability because governance depends on stable run
  semantics

Spec topics to continue:

- workspace-admin surfaces
- super-admin surfaces
- policy and override visibility
- audit-oriented operator navigation

Likely output docs:

- refinement of admin and operator governance specs

Implementation target:

- `morphOS`
- `skyforce-command-centre`
- `skyforce-core`

### 12. `johannesjo/parallel-code`, `bradygaster/squad`, `superset-sh/superset`

Why here:

- useful for multi-agent ergonomics
- lower priority than authority and state contracts

Spec topics to continue:

- worktree isolation
- shared-run collaboration rules
- parallel agent execution limits
- merge and conflict discipline

Likely output docs:

- future `PARALLEL_WORKSPACE_EXECUTION_SPEC.md`

Implementation target:

- `skyforce-symphony`
- `skyforce-core`

## Phase 6: Make Retrieval And Validation Smarter

These are valuable, but should sit on top of a stable runtime and context model.

### 13. `ForLoopCodes/contextplus`, `mixedbread-ai/mgrep`, `tirth8205/code-review-graph`

Why here:

- useful for codebase intelligence
- should not outrun the base context architecture

Spec topics to continue:

- code-feature graph retrieval
- semantic code search surfaces
- AST-aware context projection

Likely output docs:

- future `CODE_INTELLIGENCE_RETRIEVAL_SPEC.md`

Implementation target:

- future context subsystem
- `skyforce-core`

### 14. `nizos/tdd-guard`, `pbakaus/agent-reviews`, `vercel-labs/openreview`, `hamelsmu/evals-skills`

Why here:

- important for validation discipline
- should build on stable workflow, artifact, and promotion semantics

Spec topics to continue:

- validation guardrails
- deterministic closeout backstops
- review-loop automation
- eval-driven acceptance surfaces

Likely output docs:

- future `VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md`

Implementation target:

- `skyforce-core`
- `skyforce-symphony`
- `skyforce-command-centre`

## Repos Worth Tracking But Not Prioritizing For Specs

These may be useful later, but they should not drive the next spec wave:

- `clawmonitor`
- `OpenOrca`
- `agent-view`
- `awesome-codex-subagents`
- `agent-skills`
- `pm-skills`
- `deepagents`
- `pydantic-ai`
- `Qwen-Agent`
- `job-ops`

Reason:

- helpful patterns exist, but they are either less aligned with the preferred
  language direction, less foundational, or more implementation-oriented than
  specification-critical right now

## Operating Rule

When a starred repo contributes a good idea, do not copy its implementation
shape blindly.

Use one of these moves explicitly:

- adopt directly
- wrap behind a local boundary
- semport into local contracts
- use as design influence only

That rule should stay consistent with `MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md`.

## Recommended Immediate Next Docs

Create or refine these docs in this order:

1. `AGENT_SIGNAL_AND_ACTION_MODEL.md`
2. `GIT_NATIVE_WORK_LEDGER_SPEC.md`
3. `FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md`
4. `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
5. `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
6. `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`

## Bottom Line

If morphOS continues specification work from starred repos, the correct order
is:

1. Elixir orchestration and durability
2. Elixir agent and graph semantics
3. git-backed durable work state
4. filesystem memory and context hierarchy
5. Rust-based tool and factory surfaces
6. reusable workflow packaging
7. governance and operator control
8. retrieval and validation refinement
