# morphOS Repository Full Review

Date: 2026-04-02  
Reviewer: Codex agent

## Executive Summary

The repository is coherent as a **spec-first + local runtime prototype** project, with clear direction in `README.md`, strong documentation indexing in `docs/README.md`, and runnable Python runtime surfaces under `skyforce/`. The biggest risks are in **runtime-test drift** and **test environment reproducibility**.

Current headline status:

- Documentation and specification footprint: **strong**.
- Runtime scaffolding and modularity: **good**.
- Automated test health in a clean environment: **degraded** (21 failing tests under `PYTHONPATH=.`).
- Packaging/test ergonomics: **needs stabilization** (`pytest` fails collection unless import path is set).

## Scope and Inputs Reviewed

- Top-level product/system framing: `README.md`, `docs/README.md`.
- Runtime implementation: `skyforce/cli.py`, `skyforce/runtime/orchestrator.py`, `skyforce/runtime/models.py`, `skyforce/runtime/policy_engine.py`.
- Workflow specs: `workflows/feature_pipeline.yaml`, `workflows/bug_fix_pipeline.yaml`, `workflows/release_pipeline.yaml`.
- Packaging and test config: `pyproject.toml`.
- Tooling scripts: `scripts/run_tests.py`, `scripts/repo_scan.py`.
- Test suites and outcomes: `tests/` via pytest runs.

## Strengths

1. **Clear architecture boundary and intent**
   - The repository clearly describes itself as the specification/operating-model layer, not the primary production runtime.
   - The docs establish a practical reading order and canonical priorities.

2. **Reasonable modular runtime decomposition**
   - The runtime is split into orchestration, policy, event bus, context, and models modules.
   - CLI formatting logic is separated into dedicated functions, which improves maintainability.

3. **Workflow-driven execution model with policy and contract hooks**
   - Workflows define steps, contracts, and signals declaratively.
   - Orchestrator integrates contracts/signals and pause/approval behavior, which is aligned with the factory-spine direction.

4. **Existing test coverage breadth is good**
   - There are targeted suites for policy, runtime behavior, CLI, event bus, and context hub.
   - Failures appear concentrated in integration/behavior drift rather than complete absence of testing.

## Findings (Issues / Risks)

### 1) Test invocation and packaging ergonomics are brittle

- Running `pytest -q` directly fails test collection with `ModuleNotFoundError: No module named 'skyforce'`.
- This indicates test discovery/import path assumptions are not encoded robustly for a fresh checkout.

**Impact:** Slows contributor onboarding and CI portability.

### 2) Runtime behavior is currently out of sync with test expectations

- Under `PYTHONPATH=. pytest -q`, 21 tests fail.
- Most failing tests expect `release_pipeline` and `feature_pipeline` runs to pause or complete in specific states, but runtime produces `failed` runs.
- Downstream failures then appear in approval listing, paused-run filters, retrieval evidence, and batch-approval APIs.

**Impact:** Core orchestration confidence is reduced; approval/deployment control-flow likely regressed.

### 3) Async event bus tests are blocked by missing async pytest support

- Async tests in `tests/test_event_bus.py` fail with guidance to install an async plugin.
- `pyproject.toml` does not currently include async test plugin dependency or pytest marker registration.

**Impact:** Event-bus contract may be unverified in standard test environments.

### 4) Spec/runtime realism gap remains high

- The docs and milestone specs are extensive and well organized.
- Runtime implementation is present but narrower and currently unstable against its own tests.

**Impact:** Risk of “spec confidence” exceeding runtime confidence, especially for approval/deploy paths.

## Priority Recommendations

### P0 (Immediate)

1. **Restore deterministic runtime test baseline**
   - Start with release-pipeline failures (approval/deferred behavior), then feature-pipeline status/evidence regressions.
   - Ensure `run_summary` always emits the retrieval evidence shape expected by tests.

2. **Fix test environment reproducibility**
   - Make default local command (`pytest -q`) work in a clean checkout without manual `PYTHONPATH`.
   - Add/declare async pytest plugin so event bus tests execute rather than hard-fail.

3. **Decide and lock supported Python runtime for tests**
   - Repository declares `>=3.11`; local environment here is 3.10.19.
   - Add explicit CI matrix and a documented “golden” local setup path.

### P1 (Near Term)

4. **Harden workflow/program coupling checks**
   - Validate at startup that each workflow program command resolves to an existing script and required artifacts are writable.

5. **Add minimal health command**
   - A single command that validates importability, workflow references, policy loading, and critical directories before running full workflows.

### P2 (After stabilization)

6. **Trim or tier doctrine-facing docs for operator execution paths**
   - Keep the broad doctrine corpus, but provide tighter “runtime implementer” and “operator runbook” slices to reduce cognitive load.

## Suggested 7-Day Stabilization Plan

- Day 1-2: Reproduce and fix release-pipeline pause/approval regressions.
- Day 2-3: Repair feature-pipeline completion + retrieval evidence shape.
- Day 3: Add async pytest support and marker config; verify event bus tests.
- Day 4: Resolve default import-path issue for plain `pytest`.
- Day 5: Add quick healthcheck command and docs.
- Day 6-7: Run full suite in clean environment + capture baseline test report artifact.

## Commands Executed for This Review

- `rg --files -g 'AGENTS.md'`
- `rg --files`
- `sed -n '1,220p' README.md`
- `sed -n '1,220p' pyproject.toml`
- `sed -n '1,260p' docs/README.md`
- `sed -n '1,260p' skyforce/cli.py`
- `sed -n '1,260p' scripts/run_tests.py`
- `sed -n '1,260p' scripts/repo_scan.py`
- `sed -n '1,260p' skyforce/runtime/orchestrator.py`
- `sed -n '1,260p' skyforce/runtime/models.py`
- `sed -n '1,260p' skyforce/runtime/policy_engine.py`
- `sed -n '1,240p' workflows/release_pipeline.yaml`
- `sed -n '1,220p' workflows/feature_pipeline.yaml`
- `sed -n '1,220p' workflows/bug_fix_pipeline.yaml`
- `pytest -q`
- `PYTHONPATH=. pytest -q`

## Final Assessment

This repository has a strong architecture/documentation backbone and a meaningful local runtime skeleton. The immediate focus should be to close the execution gap in orchestration behavior and make test execution frictionless. Once those are stabilized, the current modular structure is a good foundation for scaling implementation against the spec corpus.
