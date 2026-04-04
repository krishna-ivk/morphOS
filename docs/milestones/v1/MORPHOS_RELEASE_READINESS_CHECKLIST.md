# morphOS Release Readiness Checklist

Baseline date: 2026-04-02

Canonical priority note: use [../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md](../v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for build order, [MORPHOS_V1_RELEASE_TARGET.md](MORPHOS_V1_RELEASE_TARGET.md) for the formal release bar, and [MORPHOS_SPEC_BASELINE.md](MORPHOS_SPEC_BASELINE.md) for the current baseline posture.

## Purpose

This checklist translates the current `v1.0` release target into a short operational view:

- what must be true before release
- how complete each major area currently looks
- which repos are closest to release shape
- which blockers still dominate the path to production

## Current Overall Read

Current overall readiness estimate:

- **~45% of the way to a believable `v1.0` production release**

Interpretation:

- above doctrine-only
- below beta
- not yet release-candidate quality

This percentage is a judgment call based on the current implementation board, repo review, and `P1` implementation bridge.
It should be used for prioritization, not for marketing claims.

## Release Gates

The platform should not be called production-ready until all of these gates are green.

| Gate | Current state | Estimate |
|---|---|---:|
| Stable contract authority across repos | partial | 55% |
| End-to-end delivery spine | in progress | 40% |
| Native `program` + `approval` step execution | in progress | 35% |
| Durable checkpoint / resume / cancel lifecycle | in progress | 35% |
| Governed human authority model | mostly planned | 25% |
| Observability + summary cohesion | partially strong | 65% |
| Safe promotion back into source repos | partial | 40% |
| Reproducible cross-repo validation in clean environments | partial | 45% |

## Immediate Critical Bar

The next critical proof point is one **single executable release gate** for the P0 spine:

- source of truth command: `npm run release-gate:p0`
- source of truth repo: `skyforce-harness`
- supporting runbook: [../P0/P0_FACTORY_SPINE_IMPLEMENTATION_CHECKLIST.md](../P0/P0_FACTORY_SPINE_IMPLEMENTATION_CHECKLIST.md)
- gate expansion: when `skyforce-core` is present, this command also executes the governed land-safety suite there
- governed land bar:
  - pre-land invariant gate blocks merge without promotion receipt, merge-ready validation, summary readiness, and clean target repo state
  - rollback safety restores branch/repo posture if land fails after checkout
  - post-land verification confirms landed state before merge is treated as final

This gate should remain the short-form answer to “how do we prove the full path twice?” until a stricter clean-environment release gate replaces it.

## Repo-by-Repo Readiness

These are grounded estimates for how close each active repo is to its required `v1.0` role.

| Repo | Role in `v1.0` | Readiness | Owner spec |
|---|---|---:|---|
| `morphOS` | specification authority | 70% | this file set (`morphOS` remains cross-repo release authority) |
| `skyforce-symphony` | orchestration runtime host | 60% | [MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-symphony/docs/MORPHOS_V1_REQUIREMENTS.md) |
| `skyforce-core` | contracts + CLI + validation seam | 50% | [MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-core/docs/MORPHOS_V1_REQUIREMENTS.md) |
| `skyforce-harness` | execution + receipts + validation seam | 40% | [MORPHOS_V1_REQUIREMENTS.md](../../../../skyforce-harness/docs/MORPHOS_V1_REQUIREMENTS.md) |
| `skyforce-command-centre-live` | operator control surface | 50% | [MORPHOS_V1_REQUIREMENTS.md](../../../../sky-force-command-centre-live/MORPHOS_V1_REQUIREMENTS.md) |
| `morphos-agent-room` | room-to-factory intake adjunct | 25% | [MORPHOS_V1_REQUIREMENTS.md](../../../../morphos-agent-room/docs/MORPHOS_V1_REQUIREMENTS.md) |

## Detailed Checklist

### 1. Contract Authority

- [x] `morphOS` remains the canonical spec source
- [x] `skyforce-core` has a meaningful shared contracts layer
- [ ] contract changes are uniformly enforced across all runtime repos
- [ ] event, receipt, approval, summary, and promotion payloads stop drifting repo-by-repo
- [ ] contract evolution follows one explicit governed update path

Current estimate: **55%**

### 2. End-to-End Delivery Spine

- [x] there is a credible planned path from intake through promotion
- [x] major repos already expose parts of that path in code
- [ ] one full `ticket -> workflow -> workspace -> code -> validation -> approval -> promotion` transaction runs without hidden manual glue
- [ ] the same path succeeds more than once without redesigning the stack
- [ ] the main docs can describe the spine in present tense without caveats

Current estimate: **40%**

### 3. Workflow Step Reality

- [x] workflow templates exist
- [x] step intent is visible in runtime state
- [ ] `program` steps execute as first-class runtime behavior
- [ ] `approval` steps pause, wait, and resume as first-class runtime behavior
- [ ] branching / transitions rely on explicit step state rather than projections and heuristics

Current estimate: **35%**

### 4. Durable Runtime

- [x] long-running work has meaningful runtime identity
- [x] Symphony has partial lifecycle and observability support
- [ ] restart-safe step state is durably persisted
- [ ] resume after interruption is proven in practice
- [ ] cancel semantics are consistent and auditable
- [ ] retry behavior is governed, bounded, and evidence-backed

Current estimate: **35%**

### 5. Governance And Human Authority

- [x] approval and policy are modeled clearly in doctrine
- [x] operator-facing surfaces already expose some approval and promotion context
- [ ] workspace-admin authority is fully executable
- [ ] super-admin authority is fully executable
- [ ] approval routing is consistent across the stack
- [ ] authority decisions are preserved as stable audit artifacts everywhere

Current estimate: **25%**

### 6. Operator Surface And Observability

- [x] summary pyramid is effectively implemented
- [x] operator login surface exists
- [x] Command Centre Live shows issue/operator state meaningfully
- [x] CLI and operator surfaces expose real runtime and artifact data
- [ ] terminology is fully normalized across all repos and artifacts
- [ ] operator truth is consistent enough to serve as a final production source of truth

Current estimate: **65%**

### 7. Safe Promotion

- [x] promotion is explicitly modeled as a governed outcome
- [x] promotion preview/apply seams exist in the current stack
- [ ] promotion is proven as a reliable execution path instead of a partial control-plane seam
- [ ] readiness, validation, approval, and summary state all bind cleanly to promotion
- [ ] source-repo reintegration is auditable and repeatable

Current estimate: **40%**

### 8. Validation And Release Confidence

- [x] major repos expose meaningful test/check entrypoints
- [x] there is a real validation doctrine and artifact model
- [ ] all primary repos pass intended validation suites in a reproducible clean environment
- [ ] validation claims are backed by regularly exercised release-path checks
- [ ] release confidence no longer depends on repo-by-repo inspection and caveats

Current estimate: **45%**

## Critical Path To Production

If the goal is to move fastest toward production, the next work should bias toward:

1. proving one full end-to-end factory transaction twice
2. making `program` and `approval` runtime steps real
3. closing durable lifecycle gaps
4. making promotion truly executable and governed
5. finishing the executable human authority model

## What Should Not Delay `v1.0`

The following should stay secondary unless they become direct blockers:

- broad doctrine expansion
- portfolio-level maturity systems
- full digital twin coverage
- deep long-term memory ecosystems
- high-theory governance additions that do not improve the factory spine

## Update Rule

Update this checklist whenever one of the following changes materially:

- `P0` factory-spine completion posture
- `P1` implementation posture
- repo review classification
- overall release-readiness judgment
