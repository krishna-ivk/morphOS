# morphOS Repository Review (Full) — 2026-04-02

## Scope and method

This review covered repository structure, specification posture, runtime implementation slices under `skyforce/`, workflow/policy assets, and executable test posture.

Reviewed inputs:
- root overview and ownership posture (`README.md`)
- documentation index and milestone pointers (`docs/README.md`)
- workflow templates (`workflows/*.yaml`)
- runtime implementation (`skyforce/runtime/*.py`, `skyforce/cli.py`)
- policy and program scripts (`policies/*.yaml`, `programs/*.sh`, `scripts/*.py`)
- automated tests (`tests/*.py`)

## Repository inventory summary

- Repository is documentation-heavy and intentionally spec-first.
- Non-artifact file count (excluding `artifacts/` and cache bytecode): **233**.
- Documentation files dominate the repo (**177 files** under `docs/`).
- Runtime and automation footprint is compact:
  - `skyforce/`: 13 files
  - `scripts/`: 5 files
  - `programs/`: 4 files
  - `workflows/`: 9 files
  - `tests/`: 7 files

## What is working well

1. **Strong architecture intent and ownership boundaries**
   - The repo clearly states it is a specification baseline and not the production runtime while still retaining a local MVP runtime for proving behavior.

2. **Contract-first workflow design**
   - Workflow definitions consistently attach contract expectations (`file_exists`, `json_schema`) and connect step outputs to later gates.

3. **Operational controls present in the runtime shape**
   - The orchestrator includes approval pause behavior, deferred-action handling, run summaries, and artifactized output paths.

4. **Spec depth is unusually high**
   - Coverage spans core mechanics, architecture, governance, doctrine, and phased milestone execution artifacts.

## Key findings (prioritized)

### High priority

1. **Current automated test posture is red (collection + behavior failures), blocking confidence in runtime claims.**
   - Without `PYTHONPATH=.`, test collection fails due to import resolution (`ModuleNotFoundError: skyforce`).
   - With `PYTHONPATH=.`, tests run but produce broad failures (runtime state transitions, approval packet lifecycle, retrieval evidence shape, and async test execution support).

2. **Async test infrastructure is incomplete for the declared test suite.**
   - Async tests are marked (`@pytest.mark.asyncio`), but pytest plugin support is absent in environment/dependencies, producing framework errors for async test functions.

3. **Validation path appears to mask failing suites during workflow execution.**
   - `scripts/run_tests.py` explicitly ignores `tests/test_runtime.py` and `tests/test_context_hub.py`, meaning core runtime behaviors are excluded from workflow validation in `run_tests` steps.
   - This introduces a confidence gap between “pipeline validation passed” and “full runtime behavior verified.”

### Medium priority

4. **Spec/runtime divergence risk is structurally high due to doctrine volume vs implementation surface.**
   - The repo intentionally holds a very large doctrine/spec catalog while the executable runtime remains narrow; this is valid strategically, but requires strict traceability to avoid drift.

5. **Repository hygiene includes generated cache content in top-level inventory (`.pytest_cache`).**
   - Not severe, but it increases noise and can complicate deterministic review outputs if not consistently ignored/cleaned.

6. **Approval and paused-run behavior appears brittle under integration tests.**
   - Multiple failing tests indicate paused/approval lifecycle assumptions are not consistently met (e.g., missing `approval_packet.json`, expected paused states becoming failed states).

### Low priority

7. **“Spec-first” and “local runtime” duality could confuse new contributors without an explicit contributor runbook front-and-center.**
   - The current docs contain the needed material, but a single concise “what to run locally for trusted signal” checklist would reduce onboarding variance.

## Recommended action plan

### 0–7 days (stabilization)

1. **Fix test execution baseline**
   - Ensure import path is deterministic (editable install or pytest config path handling).
   - Add async test dependency (`pytest-asyncio`) and configure pytest marks cleanly.

2. **Unmask validation**
   - Remove hard ignores for runtime/context-hub tests from `scripts/run_tests.py` or split into explicit fast/full profiles with transparent reporting labels.

3. **Repair approval/deferred lifecycle regression(s)**
   - Prioritize failing release pipeline tests around `paused` and approval packet generation, then rerun full suite.

### 1–3 weeks (alignment)

4. **Introduce spec-to-runtime traceability map**
   - Build a lightweight matrix: `spec doc -> code owner -> test coverage -> status`.

5. **Promote “definition of green” to a single canonical command set**
   - Example: lint + full pytest + sample workflow smoke run.

### 1–2 months (scale readiness)

6. **Formalize doctrine drift controls**
   - Add automated checks that require any behavior-affecting spec changes to reference corresponding runtime/test deltas.

## Final assessment

- **Strategic quality**: strong (excellent design articulation and governance depth).
- **Execution confidence (current branch)**: moderate-to-low until test baseline and approval/pause lifecycle failures are corrected.
- **Overall**: this repository is a strong architecture/spec command center, but immediate runtime verification hardening is needed for “full fledged” implementation confidence.
