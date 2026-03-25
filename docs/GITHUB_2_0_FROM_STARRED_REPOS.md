# GitHub 2.0 From Starred Repos

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative implementation order. This document captures the higher-level product thesis implied by the public GitHub stars retrieved for `krishna-ivk` on March 25, 2026.

Read this alongside:

- `docs/MORPHOS_GAP_ANALYSIS_FROM_GITHUB_STARS.md`
- `docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
- `docs/morphos-software-factory-mvp.md`

The working hypothesis is simple:

GitHub 2.0 should not be only a place where code is stored and reviewed.
It should become the operating surface for specification-backed, test-driven,
agent-assisted software delivery.

The star set supports that direction strongly.

## Observed Pattern Clusters

The retrieved public stars leaned heavily toward:

- agent orchestration and workflow systems
- skills, memory, and reusable context tooling
- local-first and durable runtimes
- test, eval, and model-based validation tools
- review-first coding workflows

Representative repos from the March 25, 2026 snapshot include:

- `BloopAI/vibe-kanban`
- `wavezync/durable`
- `ComposioHQ/agent-orchestrator`
- `greyhaven-ai/autocontext`
- `agentscope-ai/ReMe`
- `openclaw/acpx`
- `informalsystems/quint-connect`
- `nizos/tdd-guard`
- `modem-dev/hunk`
- `fabro-sh/fabro`
- `obra/superpowers`
- `slavingia/skills`

## GitHub 2.0 Thesis

GitHub 2.0 should treat the repository as a living factory, not a passive
filestore.

That implies six product pillars:

1. Specs are first-class

Issues and pull requests should be downstream of executable specs.
Every feature should begin from a structured intent document with acceptance
criteria, policy constraints, and test contracts.

2. Tests gate autonomy

Agents should be able to work in a bounded way, but only against explicit
behavioral contracts. The system should prefer model-based tests, fixture-backed
integration twins, and durable validation receipts over trust-me code changes.

3. Workflows are durable

Long-running coding, review, and release flows should survive interruption,
resume cleanly, and preserve a full artifact trail. `wavezync/durable`,
`agent-orchestrator`, and related projects all point in this direction.

4. Memory and context are native

Stars like `autocontext`, `ReMe`, and multiple skills repositories suggest that
repositories need a built-in context layer: reusable lessons, local memory,
retrieval, and annotated evidence that agents can cite.

5. Review becomes structured, not ad hoc

Repos like `modem-dev/hunk` and `BloopAI/vibe-kanban` point toward a
review-first flow where plans, diffs, tests, approvals, and promotion are
separate but connected stages.

6. Repo boundaries stay real, but patterns transfer

The future product should support gene-transfusion style reuse:
copy a working pattern from one repository into another, then validate behavior
instead of only copying source.

## Product Shape

A practical GitHub 2.0 loop for Skyforce-style development looks like:

`intent -> spec -> task graph -> workspace -> implementation -> validation -> approval -> promotion`

The core platform objects should therefore be:

- intent records
- executable specs
- task graphs
- durable run records
- context bundles
- validation receipts
- promotion proposals

## What To Build Next Here

For this repo, the immediate concrete move is:

- sync starred repos into the local Context Hub
- let retrieval use those repos as inspiration context
- keep the inspiration inspectable as a filesystem artifact
- use that context when defining future software-factory workflows

That is now partially implemented through the GitHub-star snapshot path:

- `artifacts/context_hub/github_starred_repos.json`

## Design Standard

If we keep pushing this direction, a change is “GitHub 2.0 aligned” when it:

- starts from a spec or structured intent
- produces or updates tests before trusting implementation
- leaves durable evidence on disk
- keeps human approval boundaries explicit
- makes reusable patterns easier to transfer across repos
