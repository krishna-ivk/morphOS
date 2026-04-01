# morphOS Gap Analysis From GitHub Stars

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative build order. This document is a starred-repo synthesis input intended to sharpen that board using patterns observed in the public GitHub stars retrieved for `krishna-ivk` on March 25, 2026.

This document translates the starred-repo signal into `morphOS`-style product
and architecture gaps.

It answers:

- what the starred repos suggest is strategically important
- where the current `morphOS` plan is already strong
- where the current plan is still under-specified
- which contract families should be added next
- which repo should eventually own each capability

Read this alongside:

- `docs/GITHUB_2_0_FROM_STARRED_REPOS.md`
- `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- `docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md`
- `docs/MORPHOS_V0_CORE_STACK.md`
- `docs/CONTEXT_ARCHITECTURE.md`
- `docs/morphos-software-factory-mvp.md`
- `docs/STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md`
- `docs/STARRED_REPO_STATUS_AND_NEXT_STEPS.md`

This document should be treated as synthesis and prioritization input.
It does not replace the existing starred-repo backlog or status map.

## Executive Summary

The public stars retrieved on March 25, 2026 do not fundamentally contradict
the current `morphOS` direction.

They reinforce it.

The major conclusion is:

`morphOS` is already pointed at the right organism, but several high-leverage
subsystems are still described more as intent than as explicit contracts.

The strongest missing or under-specified layers are:

1. a first-class work graph and review surface
2. operationalized context bundles and memory assembly
3. richer validation profiles beyond deterministic checks alone
4. durable run-thread identity across follow-up guidance and delegation
5. governed skills and subagent capability packaging
6. denser operator control-plane objects for blocked work and approvals
7. explicit exemplar transfer contracts for gene-transfusion style reuse
8. execution-tier planning for local-first versus remote-heavy work

The practical implication is not "change the roadmap completely."

The practical implication is:

- finish the current `P0` work
- pull several `planned` items forward into explicit contracts
- add one new contract family that does not yet appear strongly enough in the
  current docs: the `work graph`

## Source Pattern Summary

The stars synced into the local snapshot at:

- `artifacts/context_hub/github_starred_repos.json`

Representative repos that most strongly influenced this analysis include:

- `BloopAI/vibe-kanban`
- `wavezync/durable`
- `ComposioHQ/agent-orchestrator`
- `greyhaven-ai/autocontext`
- `agentscope-ai/ReMe`
- `informalsystems/quint-connect`
- `nizos/tdd-guard`
- `modem-dev/hunk`
- `jallum/beadwork`
- `fabro-sh/fabro`
- `slavingia/skills`
- `openclaw/acpx`
- `tirth8205/code-review-graph`
- `volcengine/OpenViking`
- `matt-k-wong/mlx-flash`
- `brontoguana/krasis`

These repos cluster around six repeated themes:

- workflow and durable execution
- memory, context, and repo-grounding
- review-first development surfaces
- test, eval, and guardrail enforcement
- skills and agent capability packaging
- local-first or efficiency-aware execution

## Current Strengths In morphOS

The current docs are already strong on:

- the software-factory loop
- filesystem-backed run state and inspectability
- durable execution as a first-class requirement
- approval and governance boundaries
- summary pyramids and evidence artifacts
- upstream adoption discipline
- the separation of reference context, operational context, and persistent memory

This matters because the stars do not reveal a broken strategy.

They reveal the next specification layers needed to make the current strategy
denser and more operational.

## Must Specify Next

| Feature Slice | Why it matters | Source influence | Local target | Status | Priority |
|---|---|---|---|---|---|
| Work graph contracts for plan, execution, review, and promotion | The current loop has workflows and tasks, but not yet a durable graph object that humans and agents can jointly navigate | `BloopAI/vibe-kanban`, `jallum/beadwork`, `modem-dev/hunk`, `fabro-sh/fabro` | `morphOS`, `skyforce-core`, future operator surfaces | `planned` | `P1` |
| Context bundle assembly for one run | The architecture exists, but workflows still need a named way to assemble docs, exemplars, annotations, and memory into one execution bundle | `greyhaven-ai/autocontext`, `agentscope-ai/ReMe`, `volcengine/OpenViking`, `tirth8205/code-review-graph` | `morphOS`, future context subsystem, `skyforce-core` | `planned` | `P1` |
| Validation profile contracts | The system needs a richer validation doctrine spanning deterministic tests, model-based checks, evals, and safety probes | `informalsystems/quint-connect`, `nizos/tdd-guard`, `hamelsmu/evals-skills`, `Hellsender01/LLMMap` | `morphOS`, `skyforce-core`, `skyforce-harness` | `planned` | `P1` |
| Durable run-thread identity across follow-ups | Durable runs are not enough if follow-up comments, approvals, and subagent results do not attach to one persistent thread | `wavezync/durable`, `ComposioHQ/agent-orchestrator`, `openclaw/acpx`, `langchain-ai/deepagents` | `skyforce-symphony`, `skyforce-core`, operator surfaces | `planned` | `P1` |
| Skill packaging, attachment, and trust contracts | Skills are clearly important in the ecosystem signal, but the current stack still treats most of them as a future subsystem | `slavingia/skills`, `MiniMax-AI/skills`, `VoltAgent/awesome-codex-subagents` | `morphOS`, `skyforce-core`, future skill subsystem | `planned` | `P1` |
| Operator inbox and blocked-run queue contracts | Human trust depends on dense operator views for blocked work, approvals, and deferred actions | `BloopAI/vibe-kanban`, `fabro-sh/fabro`, `jallum/beadwork` | operator surfaces, `skyforce-core`, `skyforce-symphony` | `planned` | `P1` |

## Next After That

| Feature Slice | Why it matters | Source influence | Local target | Status | Priority |
|---|---|---|---|---|---|
| Exemplar transfer packets for gene-transfusion work | Pattern transfer becomes safer when the reusable unit is an explicit packet, not only an informal exemplar reference | StrongDM `Gene Transfusion`, `jallum/beadwork`, `ComposioHQ/agent-orchestrator` | `morphOS`, `skyforce-core`, `skyforce-symphony` | `planned` | `P2` |
| Code-graph retrieval and review-grounding | Large repos need more than markdown retrieval; code review and planning need structural repo grounding | `tirth8205/code-review-graph`, `volcengine/OpenViking` | future context subsystem, `skyforce-core` | `planned` | `P2` |
| Multi-admin authorship and intervention contracts | Shared human control becomes important once runs are long-lived and high-value | Ramp-style multiplayer control ideas, `BloopAI/vibe-kanban` | operator surfaces, `skyforce-core`, `skyforce-symphony` | `planned` | `P2` |
| Execution-tier planning contracts | The system should eventually choose between local lightweight execution and heavier remote execution more explicitly | `matt-k-wong/mlx-flash`, `brontoguana/krasis`, `unslothai/unsloth` | future execution planner, `skyforce-harness` | `planned` | `P2` |

## Defer

| Feature Slice | Why it is deferred | Source influence | Local target | Status |
|---|---|---|---|---|
| Full autonomous self-improvement loop | The stars include recursive and self-improving systems, but this exceeds the current trust boundary and validation maturity | `greyhaven-ai/autocontext`, `ranausmanai/tinyforge` | none yet | `deferred` |
| Fully generalized context database as the whole memory system | Useful, but `morphOS` still needs to keep reference context, operational context, and persistent memory distinct | `volcengine/OpenViking` | future context subsystem | `deferred` |
| Global optimization around model economics and execution routing | Valuable later, but the current milestone is reliable factory semantics first | local-first inference repos and runtime optimization projects | future execution planner | `deferred` |

## Gap 1: Work Graph And Review Surface

### Role In The Platform

This should become the durable object model connecting:

- intake
- plan
- task graph
- diff set
- validation status
- approval state
- promotion readiness

The current workflow model captures progression.
It does not yet clearly capture the human-and-agent navigable delivery graph.

### Why The Existing Docs Are Not Yet Enough

Current `morphOS` docs already define:

- workflows
- tasks
- summaries
- approvals
- promotion

But the stars suggest one missing connective tissue:

there is no first-class object that says "this is the graph of work and review
for this delivery effort."

Without that:

- planning is harder to re-enter
- review context is spread across artifacts
- follow-up guidance has no natural graph anchor
- operators see state, but not enough relational shape

### What The Star Pattern Suggests

Projects like `BloopAI/vibe-kanban`, `jallum/beadwork`, and `modem-dev/hunk`
suggest a review-first and graph-visible workflow where:

- planning persists
- decisions persist
- review packets are first-class
- diffs and tests are anchored to task nodes

### What Should Be Specified Now

Add contracts for:

- `WorkGraph`
- `WorkNode`
- `ReviewPacket`
- `DecisionLog`
- `PromotionCandidate`

Each should include:

- identity
- parent-child or dependency relations
- authorship
- timestamps
- evidence refs
- validation refs
- approval refs

### Local Target

- `morphOS`
  - semantic shape
- `skyforce-core`
  - shared contract types
- operator surfaces
  - graph visualization and review UI

## Gap 2: Context Bundle Assembly

### Role In The Platform

The context architecture already distinguishes:

- reference context
- operational context
- persistent memory

The missing piece is the assembly surface that combines them for one run.

### Why The Existing Docs Are Not Yet Enough

The current architecture explains the layers well.
It does not yet fully define:

- how a run asks for a bundle
- how bundle provenance is recorded
- how annotations shape later bundles
- how code-graph context joins markdown-style reference context

### What The Star Pattern Suggests

Repos like `greyhaven-ai/autocontext`, `agentscope-ai/ReMe`,
`volcengine/OpenViking`, and `tirth8205/code-review-graph` point toward a more
operational notion of context:

- assembled per task
- persisted per run
- compact enough for reuse
- attributable to a source
- structured enough for selective replay

### What Should Be Specified Now

Add contracts for:

- `ContextBundle`
- `ReferencePack`
- `OperationalPack`
- `MemoryPack`
- `RunMemoryIndex`
- `BundleSelectionReason`

Each should support:

- source attribution
- trust labels
- access labels
- freshness or version labels
- citations into produced artifacts

### Local Target

- `morphOS`
  - context doctrine
- `skyforce-core`
  - shared shapes and access labels
- future context subsystem
  - retrieval, assembly, and annotation

## Gap 3: Validation Profiles

### Role In The Platform

Validation should become a typed profile, not only a loose list of checks.

That profile should describe what kind of proof a workflow needs before it may:

- continue
- pause for approval
- promote
- publish

### Why The Existing Docs Are Not Yet Enough

Current docs strongly emphasize:

- deterministic tests
- schemas
- objective checks
- validation evidence

That is correct, but incomplete for an agentic software factory.

The star pattern suggests that behavior-proof should include:

- deterministic repo checks
- model-based checks
- eval-style checks
- adversarial or safety checks

### What The Star Pattern Suggests

`informalsystems/quint-connect` highlights model-based validation.
`nizos/tdd-guard` highlights enforcement of test-first posture.
`hamelsmu/evals-skills` and `Hellsender01/LLMMap` suggest richer eval and
security validation.

### What Should Be Specified Now

Add contracts for:

- `ValidationProfile`
- `ValidationLayer`
- `BehaviorCheck`
- `EvalCheck`
- `SafetyProbe`
- `PromotionGateResult`

A workflow should be able to say:

- which validation layers are mandatory
- which are advisory
- which failures require a hard block
- which failures require human approval

### Local Target

- `morphOS`
  - validation doctrine
- `skyforce-core`
  - contract shapes
- `skyforce-harness`
  - execution and evidence collection

## Gap 4: Durable Run Thread Identity

### Role In The Platform

Durability should mean more than a resumable step execution.

It should also mean that:

- the same run has a stable identity across follow-up guidance
- approvals attach to that same run thread
- delegated sub-work remains attached to the same delivery thread

### Why The Existing Docs Are Not Yet Enough

The board already includes:

- durable checkpoint, resume, and cancel
- persistent run and thread identity
- follow-up message injection

That is good directionally.

The missing part is a denser contract family describing how those identities and
injections behave.

### What The Star Pattern Suggests

`wavezync/durable`, `ComposioHQ/agent-orchestrator`, `openclaw/acpx`, and
`langchain-ai/deepagents` all reinforce the same idea:

- long-running agent work is normal
- interruption is normal
- subagent delegation is normal
- therefore thread continuity is a core platform primitive

### What Should Be Specified Now

Add contracts for:

- `RunThread`
- `FollowUpInjection`
- `DelegationCheckpoint`
- `SubtaskThreadRef`
- `ToolActionExecutionReceipt`

Each should capture:

- parent run identity
- correlation IDs
- causality
- approval lineage
- artifact lineage

### Local Target

- `skyforce-symphony`
  - runtime projection
- `skyforce-core`
  - shared contracts
- operator surfaces
  - follow-up and run-thread views

## Gap 5: Governed Skills And Subagents

### Role In The Platform

Skills should become the governed unit of reusable capability.

They should not remain merely:

- loose references
- prompt snippets
- informal workflow aids

### Why The Existing Docs Are Not Yet Enough

The current docs correctly identify:

- skill references
- packaging and registration rules
- archetype-to-skill attachment

But they do not yet fully define:

- trust and version semantics
- workspace allowlists
- rollout control
- attachment rules by workflow step type

### What The Star Pattern Suggests

The stars show strong sustained interest in:

- skills repositories
- subagent catalogs
- specialist role packs

That means capability packaging is becoming one of the main transfer units in
agent engineering.

### What Should Be Specified Now

Add contracts for:

- `SkillPackage`
- `SkillAttachment`
- `SkillPolicy`
- `SkillRollout`
- `SkillEvidence`

These should support:

- version labels
- trust levels
- workspace or global scope
- required approvals for risky skills
- expected outputs and artifact contracts

### Local Target

- `morphOS`
  - doctrine for archetypes and attachment
- `skyforce-core`
  - package and policy contracts
- future skill subsystem
  - packaging, resolution, rollout

## Gap 6: Operator Control-Plane Density

### Role In The Platform

The human control plane should not be a thin approval button surface.

It should be the place where a workspace admin or super admin can see:

- blocked work
- risky actions
- pending approvals
- deferred actions
- promotion readiness
- intervention history

### Why The Existing Docs Are Not Yet Enough

The current board already includes:

- workspace-admin model
- super-admin model
- stronger operator views
- multi-admin collaboration

The gap is not awareness.
The gap is contract density.

### What The Star Pattern Suggests

The operator-surface repos in the star set suggest that trustworthy software
factories need clear queues and intervention surfaces, not only status strings.

### What Should Be Specified Now

Add contracts for:

- `OperatorInbox`
- `BlockedRunQueue`
- `ApprovalQueue`
- `InterventionAction`
- `AdminInterventionReceipt`

These should be able to answer:

- what is blocked
- why it is blocked
- who owns the next move
- which approvals are oldest
- what evidence is available before intervention

### Local Target

- operator surfaces
  - UI and queue views
- `skyforce-core`
  - queue and intervention contracts
- `skyforce-symphony`
  - runtime state projection

## Gap 7: Exemplar Transfer As A First-Class Packet

### Role In The Platform

The board already calls out Gene Transfusion.
The missing detail is the transport unit.

If exemplars remain informal, transfer quality will stay inconsistent.

### What Should Be Specified Now

Add contracts for:

- `ExemplarTransferPacket`
- `PatternSourceRef`
- `BehavioralParityCheck`
- `TransferApprovalGate`

Each should describe:

- which exemplar is being reused
- what behavior is expected to match
- what local adaptation is allowed
- how parity is checked

### Local Target

- `morphOS`
  - doctrine
- `skyforce-core`
  - contracts
- `skyforce-symphony`
  - workflow support

## Gap 8: Execution Tiers And Local-First Planning

### Role In The Platform

The star set includes strong interest in:

- efficient local inference
- hybrid execution
- larger-model access on constrained hardware

That does not immediately change `morphOS` semantics.

It does suggest a future planning dimension the current docs barely touch:

the system should eventually reason about execution tier.

### What Should Be Specified Later

Add contracts for:

- `ExecutionTier`
- `ModelBudgetClass`
- `ExecutionPlacementDecision`
- `LocalFirstFallback`

These should help choose between:

- fast local execution
- remote heavier execution
- hybrid staged execution

### Local Target

- future execution planner
- `skyforce-harness`

## Recommended Immediate Next Spec Slices

These are the most valuable star-driven additions that should be specified soon,
without displacing the existing `P0` work.

1. `WorkGraph` family

- because it is the clearest missing object model

2. `ContextBundle` family

- because the architecture is already present and waiting to become operational

3. `ValidationProfile` family

- because test-governed autonomy needs stronger proof surfaces

4. `RunThread` family

- because durable work and follow-up routing need one stable identity model

5. `SkillPackage` family

- because skill reuse is becoming one of the core capability units in the
  broader agent ecosystem

## Recommended Relationship To The Current Board

This document should not replace the existing implementation board, the starred
repo backlog, or the starred repo status map.

It should be used to sharpen them in three ways:

1. Pull several items from vague `planned` language into contract families

2. Add the `work graph` as a named missing layer

3. Clarify that context and validation need denser runtime shapes before the
   software-factory loop will feel truly complete

## Bottom Line

The public star set from March 25, 2026 suggests that the next leap for
`morphOS` is not a new philosophy.

It is a denser specification of:

- graph-shaped work
- assembled context
- layered validation
- durable run threads
- governed skills
- operator queues and interventions

Those are the main places where the current `morphOS` direction appears right,
but not yet specified deeply enough.
