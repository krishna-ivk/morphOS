# morphOS Local Runtime & Spec Review (2026-04-02)

Canonical priority note: keep [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) as the build-order source of truth. This review is a code-and-spec alignment pass for the local `morphOS` repository snapshot.

## Scope and Method

Reviewed areas:

- runtime code under `skyforce/` and `skyforce/runtime/`
- workflow and policy packets under `workflows/` and `policies/`
- operator/spec documentation with emphasis on `README.md`, `docs/README.md`, and P0/P1 milestone specs
- test harness and execution scripts under `tests/`, `scripts/`, and `programs/`

Validation commands run during this review:

- `pytest -q`
- `PYTHONPATH=. pytest -q`
- `bash programs/run_tests.sh review-run artifacts/review-check`

## Executive Summary

Overall posture: **transitional, partially coherent, and test-red by default**.

Strengths:

1. The repository has a clear operating-model narrative and extensive doctrine/spec decomposition.
2. Runtime seams for orchestration, policy decisions, event persistence, and context retrieval are present and test-addressed.
3. CLI surface is broad and meaningfully structured around operator flows (status, approvals, paused runs, promotion previews).

Main concerns:

1. Baseline test posture is red in a fresh environment due to packaging/import assumptions and async-test dependency gaps.
2. Integration-style runtime tests are fragile because they execute against shared repository state (not isolated fixtures), especially existing `artifacts/runs` history.
3. “YAML” workflow/policy files are actually JSON payloads; currently functional, but misleading and easy to break by future YAML-native edits.
4. `programs/run_tests.sh` currently ignores `tests/test_runtime.py` and `tests/test_context_hub.py`, which can hide regressions in orchestration-critical paths.

## Spec-to-Implementation Alignment

### What aligns well

- `P1_IMPLEMENTATION_STATUS.md` explicitly distinguishes `implemented` vs `partially_implemented` and avoids over-claiming full delivery.
- Runtime behavior includes practical P1-shaped slices: approvals, promotion preview/apply, run summaries, and event/policy metadata.

### Where implementation diverges from “expected practical truth”

1. **Test reliability does not yet support “implemented” confidence** for parts of the runtime path because local verification is not green without extra environment assumptions.
2. **Approval and paused-run workflows are highly state-sensitive** and fail under non-isolated run-history conditions, reducing confidence in deterministic operator outcomes.
3. **Context/retrieval evidence expectations are inconsistent** in some tests (`summary["evidence"]["retrieval"]` expectations do not match produced payload structure in failing paths).

## Findings (Prioritized)

### Critical

1. **Default test command fails at import-time without `PYTHONPATH=.`**
   - `pytest -q` fails with `ModuleNotFoundError: No module named 'skyforce'`.
   - This is a bad default developer/operator experience and undermines CI reproducibility.

2. **Async event-bus tests require plugin that is not declared in project dependencies**
   - `pytest.mark.asyncio` tests fail with “async def functions are not natively supported”.
   - Indicates missing `pytest-asyncio` (or equivalent) in dev/test dependency setup.

### High

3. **Runtime tests are coupled to shared repo state instead of isolated temp repo fixtures**
   - `tests/conftest.py` fixture points directly to repository root.
   - Assertions involving paused runs and ordering are polluted by pre-existing `artifacts/runs/*` history.

4. **Test runner intentionally skips major runtime suites**
   - `scripts/run_tests.py` ignores `tests/test_runtime.py` and `tests/test_context_hub.py`.
   - This creates false confidence for release-like flows because critical orchestrator paths are excluded.

5. **Python version contract mismatch with execution environment risk**
   - Project requires Python `>=3.11`, while this review environment used Python 3.10.19.
   - While not the only failure source, this mismatch increases hidden incompatibility risk.

### Medium

6. **File-extension semantics are misleading (`*.yaml` files contain JSON)**
   - Policy and workflow loaders currently parse those files with `json.loads`.
   - Future contributors may author true YAML and break runtime parsing unexpectedly.

7. **Spec corpus scale is strong but operationally heavy**
   - Documentation breadth is impressive, but discoverability and “what is currently enforceable in code” remain hard to track unless users already know `P1_IMPLEMENTATION_STATUS.md`.

## Recommended Next Actions

### 1) Restore a trustworthy red/green baseline first

- Add a documented test bootstrap path (editable install or guaranteed `PYTHONPATH` setup).
- Add test extras/dependencies for async tests and register async markers.
- Promote a single canonical command that must pass locally before merge.

### 2) Make runtime tests deterministic

- Switch core orchestration tests to temporary repo fixtures (copy minimal test data only).
- Ensure tests cleanly isolate `artifacts/runs` and do not depend on pre-existing local history.

### 3) Close test-surface blind spots

- Stop ignoring `test_runtime.py` and `test_context_hub.py` in default validation scripts, or split into explicit lanes (`quick`, `runtime`, `full`) with policy on which lanes gate promotion.

### 4) Normalize data-format intent

- Either rename workflow/policy files to `.json` or support true YAML parsing consistently.
- Document accepted format in the contributor guide to avoid drift.

### 5) Tighten spec-to-runtime status reporting

- Add a compact “implemented behavior must-have checks” table linked to real test commands and expected pass criteria.

## Validation Evidence Snapshot

- `pytest -q`: fails during collection (`skyforce` import not resolved by default).
- `PYTHONPATH=. pytest -q`: executes suite but remains red with runtime and async-related failures.
- `bash programs/run_tests.sh review-run artifacts/review-check`: produces `test_results.json` with 40 executed tests, 5 failed (all event-bus async-plugin related), and excludes runtime/context-hub suites by design.

## Final Assessment

This repo is **architecturally promising but operationally not yet stable as a fully trusted factory baseline**. The immediate leverage point is not more doctrine expansion; it is restoring a deterministic, comprehensive, and default-green test path that matches the operator-critical runtime seams.
