#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MISE_BIN="${MISE_BIN:-$HOME/.local/bin/mise}"
MODE="${1:-quick}"

if [[ "$MODE" != "quick" && "$MODE" != "full" ]]; then
  echo "Usage: $0 [quick|full]" >&2
  exit 2
fi

failures=0
checks_run=0
declare -a failed_checks=()

section() {
  echo
  echo "== $1 =="
}

run_check() {
  local name="$1"
  local dir="$2"
  local cmd="$3"

  checks_run=$((checks_run + 1))
  echo
  echo "[check] $name"
  echo "  dir: $dir"
  echo "  cmd: $cmd"

  if (
    cd "$dir"
    bash -lc "$cmd"
  ); then
    echo "[pass] $name"
  else
    echo "[fail] $name"
    failures=$((failures + 1))
    failed_checks+=("$name")
  fi
}

require_path() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    echo "Required path missing: $path" >&2
    exit 1
  fi
}

require_path "$ROOT_DIR/morphOS"
require_path "$ROOT_DIR/skyforce-core"
require_path "$ROOT_DIR/skyforce-symphony"
require_path "$ROOT_DIR/skyforce-harness"
require_path "$ROOT_DIR/skyforce-api-gateway"
require_path "$ROOT_DIR/skyforce-command-centre"
require_path "$ROOT_DIR/skyforce-command-centre-live"

section "Workspace Verification"
echo "Root: $ROOT_DIR"
echo "Mode: $MODE"

section "morphOS"
run_check \
  "morphOS pytest" \
  "$ROOT_DIR/morphOS" \
  "python3 -m venv .venv && . .venv/bin/activate && python -m pip install -q -e . && python -m pytest -q tests"

if [[ "$MODE" == "full" ]]; then
  run_check \
    "morphOS validation runner" \
    "$ROOT_DIR/morphOS" \
    "python3 scripts/run_tests.py workspace-verify"
fi

section "skyforce-core"
run_check \
  "skyforce-core contracts" \
  "$ROOT_DIR/skyforce-core" \
  "npm run test:contracts"
run_check \
  "skyforce-core cli smoke" \
  "$ROOT_DIR/skyforce-core" \
  "npm run sky:smoke"

if [[ "$MODE" == "full" ]]; then
  run_check \
    "skyforce-core build" \
    "$ROOT_DIR/skyforce-core" \
    "npm run build"
fi

section "skyforce-symphony"
run_check \
  "skyforce-symphony test" \
  "$ROOT_DIR/skyforce-symphony/elixir" \
  "\"$MISE_BIN\" exec -- mix test"

if [[ "$MODE" == "full" ]]; then
  run_check \
    "skyforce-symphony lint" \
    "$ROOT_DIR/skyforce-symphony/elixir" \
    "\"$MISE_BIN\" exec -- mix lint"
fi

section "skyforce-harness"
run_check \
  "skyforce-harness smoke" \
  "$ROOT_DIR/skyforce-harness" \
  "npm run smoke"
run_check \
  "skyforce-harness p0 smoke" \
  "$ROOT_DIR/skyforce-harness" \
  "npm run smoke:p0"

section "skyforce-api-gateway"
run_check \
  "skyforce-api-gateway compile" \
  "$ROOT_DIR/skyforce-api-gateway" \
  "make compile"
run_check \
  "skyforce-api-gateway test" \
  "$ROOT_DIR/skyforce-api-gateway" \
  "make test"
run_check \
  "skyforce-api-gateway smoke" \
  "$ROOT_DIR/skyforce-api-gateway" \
  "make smoke"

section "skyforce-command-centre"
run_check \
  "skyforce-command-centre api smoke" \
  "$ROOT_DIR/skyforce-command-centre" \
  "npm run test:compat-smoke"
run_check \
  "skyforce-command-centre api test" \
  "$ROOT_DIR/skyforce-command-centre" \
  "npm run test:compat-api"

if [[ "$MODE" == "full" ]]; then
  run_check \
    "skyforce-command-centre frontend build" \
    "$ROOT_DIR/skyforce-command-centre" \
    "npm run frontend:build"
fi

section "skyforce-command-centre-live"
run_check \
  "skyforce-command-centre-live test" \
  "$ROOT_DIR/skyforce-command-centre-live" \
  "\"$MISE_BIN\" exec -- mix test"

if [[ "$MODE" == "full" ]]; then
  run_check \
    "skyforce-command-centre-live format check" \
    "$ROOT_DIR/skyforce-command-centre-live" \
    "\"$MISE_BIN\" exec -- mix format --check-formatted"
fi

section "Optional Integration"
if [[ -d "$ROOT_DIR/skyforce-hermes" ]]; then
  run_check \
    "skyforce-hermes integration smoke" \
    "$ROOT_DIR/skyforce-hermes" \
    "python3 integration_smoke_test.py"
fi

section "Summary"
echo "Checks run: $checks_run"
echo "Failures : $failures"

if [[ "$failures" -gt 0 ]]; then
  echo
  echo "Failed checks:"
  printf ' - %s\n' "${failed_checks[@]}"
  exit 1
fi

echo "Workspace verification passed."
