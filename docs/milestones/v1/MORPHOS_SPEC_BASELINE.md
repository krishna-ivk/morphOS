# morphOS Spec Baseline

Baseline date: 2026-04-02

Canonical priority note: use [../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md](../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for build order and [MORPHOS_V1_RELEASE_TARGET.md](MORPHOS_V1_RELEASE_TARGET.md) for the `v1.0` release bar. This document records the current specification baseline and a grounded judgment about how far the active Skyforce stack is from a production release.

## Purpose

This document exists to answer four practical questions:

1. what `morphOS` should currently claim as baseline truth
2. what should still be treated as proving-track or prototype behavior
3. how far the platform is from a believable production release
4. what must change before the baseline can move upward

## Baseline Classification

Current baseline classification:

- specification line: `0.1.0`
- release posture: `pre-v1 proving track`
- runtime posture: `alpha-quality software-factory spine`
- production posture: `not production-ready`

This is a specification baseline with meaningful implementation progress.
It is not yet a release candidate.

## Evidence Snapshot

This baseline is grounded in the current implementation and planning documents:

- [../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md](../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md)
- [../v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md](../v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md)
- [../P1/P1_IMPLEMENTATION_STATUS.md](../P1/P1_IMPLEMENTATION_STATUS.md)
- [MORPHOS_V1_RELEASE_TARGET.md](MORPHOS_V1_RELEASE_TARGET.md)

### Current execution truth

What is already real enough to count toward the baseline:

- workflow templates load from `morphOS` into `skyforce-symphony`
- Symphony exposes meaningful workflow progress and observability
- Harness can emit and consume execution artifacts and summary layers
- Command Centre Live provides a real operator-facing shell with login and issue views
- `skyforce-core` provides shared contracts plus a workspace-aware CLI
- `morphos-agent-room` now exists as a room-to-factory handoff repo in the active workspace

### Current gap truth

What still prevents a production claim:

- the end-to-end spine is still marked `in_progress`, not complete
- full native `program` and `approval` step execution is still `in_progress`
- durable checkpoint, resume, and cancel lifecycle is still `in_progress`
- workspace-admin and super-admin governance models are still `planned`
- policy hooks, event taxonomy alignment, and terminology convergence are not yet fully implemented across repos
- promotion remains partially implemented rather than proven as a reliable production path

### P1 implementation posture

The current `P1` bridge shows:

- `implemented`
  - summary pyramid
  - operator login surface
- `partially_implemented`
  - event taxonomy
  - policy hooks
  - safe promotion
  - universal terminology

That means the operator and reporting layer is moving faster than the fully governed runtime spine beneath it.

## Production Readiness Judgment

Judgment as of 2026-04-02:

`morphOS` is materially beyond pure doctrine, but still clearly short of a production release.

The most accurate label today is:

- **spec baseline with alpha runtime**

Not:

- beta
- release candidate
- production-ready

### How far from production?

Inference from the current board and repo review:

- roughly **one major proving phase plus one hardening phase away** from a believable `v1.0` production release
- equivalently: the platform looks **closer to the middle of the release path than to the end**

Why this is the right judgment:

1. the core spine exists conceptually and partially in code, so this is not an early-zero state
2. the highest-risk seams are still the exact seams that define a production factory:
   - durable workflow execution
   - approval pause/resume semantics
   - trustworthy promotion
   - stable operator governance
3. multiple critical repos are still classified as transitional or prototype-grade in the repo review

## Repo-by-Repo Baseline Posture

### `skyforce-symphony`

- posture: strongest current runtime host
- baseline truth: credible execution host and observability surface
- still missing for production:
  - explicit durable step execution
  - stronger restart/recovery semantics
  - less heuristic workflow routing

### `skyforce-harness`

- posture: useful artifact and execution seam, still prototype-grade
- baseline truth: good proving surface for receipts, summaries, approval packets, and factory-spine scripts
- still missing for production:
  - typed core
  - stronger contract enforcement
  - deeper idempotency and trust guarantees

### `skyforce-core`

- posture: valuable but transitional
- baseline truth: contract layer plus practical workspace CLI
- still missing for production:
  - cleaner architecture boundaries
  - stronger validation story
  - less monolithic orchestration logic in the CLI

### `skyforce-command-centre-live`

- posture: credible operator shell, not yet the final governance runtime
- baseline truth: real operator-facing surface with login, issue views, and summary/promotion/approval affordances
- still missing for production:
  - stronger backend truth and authority alignment
  - less dependence on transitional control-plane seams

### `morphos-agent-room`

- posture: new room-to-factory intake surface
- baseline truth: useful adjunct repo for collaborative feature-room handoff
- still missing for production:
  - explicit integration into the validated production spine
  - clear release ownership within the `v1.0` bar

## Baseline Release Blockers

The minimum blockers that still stand between the current stack and a production claim are:

1. complete one real `ticket -> workflow -> workspace -> code -> validation -> approval -> promotion` transaction with no hidden manual glue
2. make `program` and `approval` steps first-class runtime behavior, not only projected intent
3. prove durable resume, cancel, and recovery semantics across restart boundaries
4. converge the operator truth model so approval, validation, summary, and promotion state are consistent everywhere
5. run reproducible validation suites across the primary repos in a clean environment

## What Can Raise The Baseline Next

The next baseline upgrade should happen only after these are materially true:

- `P0` factory-spine items are mostly implemented, not mostly planned or proving
- promotion is real enough to stop being described as a partial control-plane seam
- governance roles are executable and auditable
- the repo review can stop calling Harness prototype-grade and Core transitional for their required release roles
- the docs can describe the main spine in present tense without repeated caveats

## Current Safe Claim

As of 2026-04-02, the safe public/internal claim is:

> `morphOS` has an active specification baseline and a credible software-factory proving stack, but it has not yet crossed the bar for a production release.

That is the baseline this repo should defend until the release blockers above are closed.
