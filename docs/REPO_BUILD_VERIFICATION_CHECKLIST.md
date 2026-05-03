# morphOS Repo Build Verification Checklist

## Purpose

This checklist defines how to verify the `morphOS` repo itself.

Unlike the runtime repos, `morphOS` is primarily a specification and contract repo.
Its verification gate focuses on:

- documentation integrity
- workflow-template integrity
- local Python package health
- test execution for the local MVP runtime helpers that still live here

## Repo Role

`morphOS` should own:

- doctrine
- workflow language
- policy language
- agent archetypes
- runtime contract direction

`morphOS` should not become:

- the primary orchestration runtime
- the primary execution runtime
- a second operator control plane

## Required Local Prerequisites

- Python 3.11+
- `pip`
- optional virtual environment support via `python3 -m venv`

## Build Verification

### 1. Python environment

- [ ] create a virtual environment if needed
- [ ] install the local package and test dependencies

Suggested commands:

```bash
cd /home/vashista/skyforce/morphOS
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip pytest
python -m pip install -e .
```

### 2. Package import health

- [ ] the local `skyforce` package imports
- [ ] the local runtime modules import

Suggested commands:

```bash
cd /home/vashista/skyforce/morphOS
. .venv/bin/activate
python -c "import skyforce; import skyforce.runtime"
```

### 3. Workflow and docs integrity

- [ ] `workflows/` contains the expected YAML templates
- [ ] milestone and status docs are present
- [ ] the main README still points to the canonical milestone and runtime-contract docs

Suggested commands:

```bash
cd /home/vashista/skyforce/morphOS
find workflows -maxdepth 2 -type f | sort
find docs/milestones -maxdepth 3 -type f | sort | sed -n '1,120p'
```

## Test Verification

### 1. Direct pytest run

- [ ] the repo test suite runs under `pytest`

Suggested command:

```bash
cd /home/vashista/skyforce/morphOS
. .venv/bin/activate
python -m pytest -q tests
```

### 2. Validation-oriented test runner

- [ ] the repository test runner script executes and writes validation artifacts

Suggested command:

```bash
cd /home/vashista/skyforce/morphOS
. .venv/bin/activate
python scripts/run_tests.py local-run
```

Expected artifact outputs:

- `artifacts/current/test_results.json`
- `artifacts/current/validation_report.json`
- `artifacts/current/test_results.txt`

## Repo-Specific Verification Checklist

- [ ] `README.md` still describes `morphOS` as doctrine and operating-model ownership
- [ ] `docs/morphos_buildability_plan.md` still matches the current repo split
- [ ] `docs/milestones/P1/P1_IMPLEMENTATION_STATUS.md` reflects runtime truth rather than pure aspiration
- [ ] `docs/milestones/P1/P1_V1_BUILD_AND_TEST_CHECKLIST.md` remains aligned with current platform expectations
- [ ] Python package import health is intact
- [ ] repo-local tests pass
- [ ] workflow files remain parseable and intentionally small enough for the current runtime subset

## Pass Condition

Treat `morphOS` as repo-healthy when all of the following are true:

- docs remain internally coherent
- the local Python package installs and imports
- tests pass
- validation artifacts can still be produced
- workflow and milestone docs still match the actual Skyforce runtime boundary
