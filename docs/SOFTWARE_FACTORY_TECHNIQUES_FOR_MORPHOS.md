# Software Factory Techniques For morphOS

Canonical priority note: this file explains the operating methods; use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the actual build sequence.

This document translates the StrongDM Software Factory techniques into
`morphOS` doctrine.

It treats them as practical operating methods for a system that must:

- grow from natural-language intent
- validate behavior without depending on source inspection
- preserve context and memory across runs
- support both interactive and fully specified execution
- scale across multiple agents, repos, and integrations

Read this alongside:

- `docs/milestones/v0/MORPHOS_V0_CORE_STACK.md`
- `docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md`
- `docs/architecture/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md`
- `docs/architecture/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md`

## Core Position

The StrongDM techniques fit `morphOS` because they emphasize the same things
we need:

- behavior over source inspection
- reproducibility over intuition
- filesystem-backed memory over hidden context
- explicit execution modes over vague autonomy
- reusable patterns over repeated invention

For `morphOS`, these should be named system methods, not loose inspiration.

## Digital Twin Universe

### StrongDM meaning

Build behavioral clones of important third-party systems and validate against
those clones instead of live dependencies.

### morphOS interpretation

`morphOS` should prefer behavioral twins for integrations that are:

- risky to mutate
- expensive to test live
- rate-limited
- hard to reproduce deterministically

Examples in the Skyforce direction include:

- Linear
- Slack
- GitHub
- Google Workspace
- identity and approval systems

### Runtime implication

DTU should become the default strategy for high-volume integration validation.

That means:

- integration tests should prefer twins before live services
- dangerous failure modes should be injectable
- replays should be deterministic
- validation should compare observed behavior, not code structure

## Gene Transfusion

### StrongDM meaning

Transfer a working implementation pattern from one codebase into another by
using a strong exemplar and validating behavioral equivalence.

### morphOS interpretation

This is a direct fit for Skyforce multi-repo work.

The reusable asset is not only the code. The reusable asset is the behavioral
pattern and the shape of the solution.

That means:

- we should explicitly reuse strong exemplars across repos
- we should preserve patterns even when local implementation details differ
- we should validate the result behaviorally

### Runtime implication

Gene Transfusion should be a standard method for:

- CLI to UI feature parity
- React to LiveView migration work
- shared contract adoption across repos
- runtime pattern transfer between prototype and production surfaces

## The Filesystem

### StrongDM meaning

Use the filesystem as durable, inspectable working memory for agents.

### morphOS interpretation

This is already one of the strongest natural fits for `morphOS`.

The filesystem should be treated as a first-class memory substrate for:

- receipts
- validation artifacts
- summaries
- scratch state
- indexes
- local context bundles
- replayable execution traces

### Runtime implication

Filesystem-backed state should be:

- inspectable by humans
- reorganizable by agents
- recoverable after interruption
- composable across multiple agents

This aligns directly with the `morphOS` separation between:

- reference context
- operational context
- persistent memory

## Shift Work

### StrongDM meaning

Separate interactive work from non-interactive execution.

### morphOS interpretation

`morphOS` should treat this as a first-class workflow distinction.

There are at least two execution modes:

- interactive mode
  - intent is still evolving
  - operator review and correction matter
- non-interactive mode
  - intent is already complete enough to execute end to end

### Runtime implication

Workflows should declare or infer whether they are:

- exploratory
- approval-gated
- fully specified

This affects:

- how often humans are interrupted
- whether autonomous runs are allowed
- how validation is interpreted
- whether the runtime should continue without feedback

## Semport

### StrongDM meaning

Port trusted upstream behavior into a local language, framework, or runtime
while preserving intent.

### morphOS interpretation

This is highly relevant to the `morphOS v0` stack because we are explicitly
building around upstream systems like:

- `openai/symphony`
- `wavezync/durable`
- `andrewyng/context-hub`
- `ComposioHQ/agent-orchestrator`
- `openai/skills`

We should inherit upstream design thinking where useful and port or adapt it
where our local stack requires deeper integration.

### Runtime implication

Semport should become the sanctioned way to:

- port upstream runtime ideas into local contracts
- preserve behavioral intent while changing implementation language
- keep alignment with upstream designs without taking direct dependency on
  every implementation detail

## Pyramid Summaries

### StrongDM meaning

Use reversible summaries at multiple zoom levels so agents can compress and
later re-expand context.

### morphOS interpretation

This should become a default context-compression method for `morphOS`.

We already need this across:

- CLI summaries
- operator dashboards
- issue inspection
- memory retrieval
- multi-agent handoffs

### Runtime implication

The runtime should support multiple summary layers for the same artifact or
state object, for example:

- one-line readiness signal
- short issue summary
- expanded issue brief
- full artifact trail

## Mapping To morphOS v0

These techniques map cleanly to the current `morphOS v0` stack:

- `openai/symphony`
  - benefits most from Shift Work and Pyramid Summaries
- `wavezync/durable`
  - benefits most from Digital Twin Universe and Shift Work
- `andrewyng/context-hub`
  - benefits most from The Filesystem and Pyramid Summaries
- `ComposioHQ/agent-orchestrator`
  - benefits most from Digital Twin Universe and Gene Transfusion
- `openai/skills`
  - benefits most from Gene Transfusion and Semport

## Recommended Adoption Order

1. The Filesystem
2. Shift Work
3. Pyramid Summaries
4. Digital Twin Universe
5. Gene Transfusion
6. Semport

Reasoning:

- filesystem-backed memory is foundational
- execution mode separation affects runtime policy early
- context compression becomes necessary quickly
- digital twins matter once integrations become important
- pattern transfer and semantic porting get stronger after contracts stabilize

## Non-Negotiable Design Rules

1. Validate behavior first.
2. Prefer inspectable filesystem state over hidden memory.
3. Distinguish exploratory execution from fully specified execution.
4. Treat summaries as reversible compression, not lossy reporting.
5. Reuse proven behavioral patterns before inventing new ones.
6. Port intent, not syntax.

## Practical Next Steps

The first concrete moves for Skyforce should be:

1. formalize filesystem-backed memory and context storage conventions
2. add explicit workflow mode semantics for interactive vs non-interactive runs
3. standardize summary layers across CLI, dashboards, and issue views
4. define the first integration twins for high-risk external systems
5. create an exemplar-transfer workflow for cross-repo feature work
6. document which upstream systems are being semported and where

## Bottom Line

The StrongDM techniques fit `morphOS` because they describe how to build a
behavior-first software organism.

For `morphOS`, the combined posture matters most:

- store state durably
- validate behavior externally
- separate exploratory work from complete execution
- compress context without losing the ability to expand it
- transfer proven patterns instead of repeatedly starting from zero

That posture is a strong match for Skyforce.
