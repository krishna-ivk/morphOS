# morphOS Full Repository + Specs Review (2026-04-02)

## Scope

This review covers:

- repository structure and runtime code (`skyforce/`, `scripts/`, `programs/`, `tests/`, `workflows/`)
- specification surface (`docs/`, especially architecture and milestone status docs)
- implementation-to-spec consistency checks
- testability and release readiness signals

## Executive Summary

morphOS is currently a **spec-first repository with an MVP runtime seam**. The architecture intent is clear and well documented, and the workflow/policy model is coherent. The main near-term gap is not architectural direction; it is **execution reliability and environment determinism**:

1. runtime/test behavior currently diverges from expectations in key release paths
2. local test execution is fragile without explicit environment setup
3. async event-bus tests are defined but the test environment is missing the async pytest plugin

Overall status for immediate shipping confidence: **yellow** (good model clarity, unstable runtime path).

## Repository Contents Review

### 1) Documentation and architecture quality

Strengths:

- The root README clearly positions morphOS as the spec/operating-model layer and distinguishes it from runtime repos. This prevents ownership drift. 
- The docs index and milestone documents provide broad and deep coverage (architecture, workflow behavior, policy hooks, contracts, rollout guidance).
- `P1_IMPLEMENTATION_STATUS.md` already includes a practical status rubric (`specified`, `partially_implemented`, `implemented`) and avoids over-claiming completion.

Risk:

- The repository has very high documentation volume. Without stricter “canonical source” pointers per feature area, contributors can still choose outdated/parallel docs.

### 2) Runtime and orchestration surface

Strengths:

- `Orchestrator` provides a single entry for workflow execution, resume, approvals, and operational reporting.
- Execution produces structured artifacts and includes policy checks before step execution.
- Workflow definitions are simple and readable (`workflows/*.yaml` using JSON content), lowering the onboarding cost.

Risk:

- Runtime behavior around release-pipeline pause/defer/approval appears unstable under current tests, indicating either logic regressions or stale test assumptions.

### 3) Policy surface

Strengths:

- Policy rules are centralized under `policies/` and loaded as enabled rule bundles.
- Explicit policy decisions are represented as structured objects (`allowed`, `action`, `rule_id`, `reason`), which is good for auditability.

Risk:

- Policy files use `.yaml` extension but contain JSON payloads. This is technically valid only as JSON, and it may confuse tools/contributors expecting YAML semantics.

### 4) Test and validation posture

Strengths:

- Test suite is substantial and covers CLI, policy, runtime, context hub, task splitting, and event bus.
- `scripts/run_tests.py` emits machine-readable artifacts and validation reports, which aligns with factory-style evidence generation.

Critical risks observed during review:

- Running `pytest -q` directly fails module import unless `PYTHONPATH` is set or the package is installed.
- Running with `PYTHONPATH=. pytest -q` executes, but multiple failures appear in runtime and async event bus areas.
- Async tests are marked with `pytest.mark.asyncio`, but plugin support is absent in the current environment (tests are discovered but not executed properly as async).

## Spec-to-Implementation Consistency Check

### What is consistent

- The repo intent (“spec baseline, not production runtime”) matches the README framing and the P1 status caveats.
- Approval/defer concepts are present both in workflow specs and runtime methods.

### What is inconsistent / at risk

1. **Release workflow expected state transitions vs observed test outcomes**
   - Release pipeline includes approval/deploy gates and connectivity requirements, but tests indicate runs often end in `failed` instead of expected `paused` states in several scenarios.

2. **Validation signal contract expectations**
   - Some tests expect retrieval evidence and approval artifacts that are missing in produced run outputs.

3. **Environment contract drift**
   - `pyproject.toml` requires Python `>=3.11`, while this environment executes Python `3.10.19`; this can hide or create compatibility issues.

## Prioritized Findings

### P0 (must address first)

1. **Stabilize release pipeline control-flow behavior**
   - Reconcile orchestrator logic with tests around defer/approval transitions and approval packet creation.
   - Add narrow regression tests for each transition boundary (offline -> online_read -> approval -> deploy_enabled).

2. **Make test execution deterministic for contributors and CI**
   - Ensure one documented command works from a clean checkout.
   - Either package-install before tests or enforce `PYTHONPATH` within wrapper scripts and CI commands.

3. **Add async test dependency and config**
   - Add `pytest-asyncio` and pytest config for asyncio mode; remove current plugin gap so async tests are genuinely executed.

### P1 (important, next)

4. **Clarify policy file format expectations**
   - Rename `.yaml` files to `.json` or switch parser to a YAML parser and allow true YAML.

5. **Reduce spec sprawl for operators/builders**
   - Add a “canonical map” doc that explicitly states the authoritative doc per capability and marks superseded docs.

### P2 (quality hardening)

6. **Add smoke checks for artifact completeness per workflow**
   - Verify expected artifact set (summary, evidence, approvals where relevant) after each run in CI.

7. **Publish compatibility matrix**
   - Document supported Python version(s), required local tooling, and expected command sequence.

## Suggested 7-Day Hardening Plan

- **Day 1-2**: fix environment determinism (Python version alignment, test entrypoint, async plugin).
- **Day 2-4**: fix release-pipeline state machine regressions and missing approval artifacts.
- **Day 4-5**: enforce artifact completeness tests + add focused regression suite.
- **Day 6-7**: docs consolidation (canonical map + policy format cleanup).

## Final Assessment

The repository is architecturally strong and unusually well-specified for this stage. The limiting factor is operational reliability in the runtime/test seam. If the P0 set is addressed, morphOS can move from “spec-heavy with fragile execution” to a dependable implementation baseline suitable for faster upstream adoption.
