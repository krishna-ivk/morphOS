# morphOS v1.0 Release Target

Canonical priority note: use [../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md](../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for current build order. This document defines what that work must add up to if the goal is a real `v1.0` release.

## Purpose

`morphOS v1.0` is the first release where the platform can be described as a governed software-factory operating model with a believable implementation path across the active Skyforce repos.

This is not the target for autonomous evolution or deep memory systems.
It is the target for:

- one stable contract layer
- one believable end-to-end runtime spine
- one governed approval and promotion loop
- one operator-facing control surface that can explain what the system is doing

## Release Position

Treat the current `v0` program as the proving track for `v1.0`.

That means:

- `v0` documents define the build sequence
- `v1.0` defines the release bar
- no major roadmap item should be called complete unless it moves the stack materially closer to the `v1.0` exit criteria below

## v1.0 Product Statement

`morphOS v1.0` is reached when:

1. `morphOS` is the clear specification authority for contracts, workflow semantics, governance semantics, and operator-facing meaning.
2. `skyforce-symphony` can execute the primary workflow spine with explicit step state, durable recovery, and approval-aware progression.
3. `skyforce-harness` can consume and emit trusted execution artifacts with stable contracts and repeatable tests.
4. `skyforce-core` provides the shared contract layer without concept drift from `morphOS`.
5. `skyforce-command-centre-live` provides a protected operator surface that reflects real execution, approval, validation, and promotion state.

## Repo-local requirement ownership

`morphOS` keeps the cross-repo release bar. Detailed repo-specific `v1.0` implementation requirements live in the owning repos:

- `skyforce-symphony`: [../../../../skyforce-symphony/docs/MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-symphony/docs/MORPHOS_V1_REQUIREMENTS.md)
- `skyforce-harness`: [../../../../skyforce-harness/docs/MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-harness/docs/MORPHOS_V1_REQUIREMENTS.md)
- `skyforce-core`: [../../../../skyforce-core/docs/MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-core/docs/MORPHOS_V1_REQUIREMENTS.md)
- `skyforce-command-centre-live`: [../../../../skyforce-command-centre-live/MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-command-centre-live/MORPHOS_V1_REQUIREMENTS.md)
- `morphos-agent-room`: [../../../../morphos-agent-room/docs/MORPHOS_V1_REQUIREMENTS.md](../../../../morphos-agent-room/docs/MORPHOS_V1_REQUIREMENTS.md)

## Required v1.0 Capabilities

### 1. Stable Contract Authority

Required:

- shared contracts in implementation repos match the current `morphOS` canonical forms
- event, receipt, approval, summary, and workflow payloads no longer drift casually across repos
- contract changes follow an explicit planning/update path

Primary repos:

- `morphOS`
- `skyforce-core`

### 2. Proven Delivery Spine

Required:

- one real end-to-end path:
  - `ticket -> workflow -> workspace -> code -> validation -> approval -> promotion`
- the path is executable without hidden manual glue between repos
- pause, resume, fail, retry, and approval transitions are explicit runtime states

Primary repos:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-core`
- `skyforce-command-centre-live`

### 3. Governed Human Authority

Required:

- workspace-scoped admin authority is explicit
- super-admin or higher-trust override authority is explicit
- approval packets, approval decisions, and approval audit state are preserved in stable artifacts
- the operator surface shows who must decide, what is blocked, and why

Primary repos:

- `morphOS`
- `skyforce-core`
- `skyforce-command-centre-live`
- `skyforce-symphony`

### 4. Real Observability And Summary Cohesion

Required:

- one-line, short, full, and evidence-level summary views are aligned
- workflow state, validation state, approval state, and promotion state can be explained from one operator surface
- event and receipt language is consistent enough to support debugging and audits

Primary repos:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre-live`
- `skyforce-core`

### 5. Promotion With Safety

Required:

- validated workspace output can be proposed or promoted back into source repos through a governed path
- readiness, evidence, and approval posture are explicit
- promotion is not merely a simulated control-plane action

Primary repos:

- `skyforce-core`
- `skyforce-symphony`
- `skyforce-command-centre-live`

## What v1.0 Does Not Require

These are explicitly post-`v1.0` unless they become hard blockers:

- autonomous self-modification
- automatic policy rewriting
- broad organizational portfolio systems
- full digital-twin coverage
- rich long-term memory ecosystems
- deep multi-surface parity across every external system

## Current Gating Risks

Based on the current implementation-repo review, the main `v1.0` blockers are:

1. `skyforce-symphony` is the strongest runtime host, but it still needs more explicit step execution and stronger durable recovery semantics.
2. `skyforce-core` has valuable contracts, but its current CLI and app shape are too transitional to treat as the final platform architecture.
3. `skyforce-harness` still needs a typed core and stronger contract-trust/testing posture.
4. `skyforce-command-centre-live` is a cleaner operator shell than older control-plane prototypes, but it still depends on deeper backend authority and execution truth.

See also:

- [../v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md](../v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md)

## Release Exit Criteria

`morphOS v1.0` is ready only when all of the following are true:

1. The implementation board’s `P0` items are materially complete, not merely specified.
2. The `P1` items required for event, policy, summary, terminology, and promotion coherence are materially implemented in the owning repos.
3. The implementation-repo review no longer classifies Harness or Command Centre Live as prototype-grade for their required `v1.0` roles.
4. The primary repo set can pass their intended validation suites in a reproducible environment.
5. The docs can describe the platform in present tense without repeatedly caveating the core workflow spine as aspirational.

## Planning Rule

When choosing work after this point:

- prefer work that closes a release blocker over work that adds a new concept
- prefer convergence across repos over expanding doctrine
- prefer executable control-path improvements over observational-only features
