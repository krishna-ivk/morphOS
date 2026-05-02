#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

MISE_BIN="${MISE_BIN:-$HOME/.local/bin/mise}"
BACKEND_TARGET="${SKYFORCE_BACKEND_TARGET:-gateway}"
VERIFY_MODE="${SKYFORCE_VERIFY_MODE:-quick}"
SKIP_VERIFY="${SKYFORCE_SKIP_VERIFY:-0}"
ENABLE_CONTEXT_HUB="${SKYFORCE_ENABLE_CONTEXT_HUB:-0}"
ENABLE_PI_AGENT="${SKYFORCE_ENABLE_PI_AGENT:-1}"

API_HOST="${SKYFORCE_API_HOST:-127.0.0.1}"
API_PORT="${SKYFORCE_API_PORT:-3000}"
LIVEVIEW_PORT="${SKYFORCE_COMMAND_CENTRE_LIVE_PORT:-4000}"
CORE_PORT="${SKYFORCE_CORE_PORT:-3100}"
CORE_BOTS_PORT="${SKYFORCE_CORE_BOTS_PORT:-3001}"
CONTEXT_HUB_PORT="${SKYFORCE_CONTEXT_HUB_PORT:-3005}"
CONTEXT_HUB_URL="http://127.0.0.1:$CONTEXT_HUB_PORT"
OPENCLAW_PORT="${SKYFORCE_OPENCLAW_PORT:-18789}"
OPENCLAW_DIR="$ROOT_DIR/openclaw"
OPENCLAW_STATE_DIR="${OPENCLAW_STATE_DIR:-$ROOT_DIR/.openclaw}"
OPENCLAW_CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$OPENCLAW_STATE_DIR/openclaw.json}"
OPENCLAW_MODEL="${SKYFORCE_OPENCLAW_MODEL:-openai-codex/gpt-5.4}"
OPENCLAW_ENV_PREFIX="OPENCLAW_CONFIG_PATH=\"$OPENCLAW_CONFIG_PATH\" OPENCLAW_STATE_DIR=\"$OPENCLAW_STATE_DIR\""

case "$BACKEND_TARGET" in
  compat)
    BACKEND_NAME="skyforce-command-centre"
    BACKEND_DIR="$ROOT_DIR/skyforce-command-centre"
    BACKEND_INSTALL_CMD="python3 -m pip install -r requirements.txt"
    BACKEND_TEST_CMD="npm run test:compat-api && npm run test:compat-smoke"
    BACKEND_RUN_CMD="python3 -m uvicorn main:app --host $API_HOST --port $API_PORT"
    BACKEND_URL="http://$API_HOST:$API_PORT"
    ;;
  gateway)
    BACKEND_NAME="skyforce-api-gateway"
    BACKEND_DIR="$ROOT_DIR/skyforce-api-gateway"
    BACKEND_INSTALL_CMD="make venv && make install"
    BACKEND_TEST_CMD="make compile && make test && make smoke"
    BACKEND_RUN_CMD="make run"
    BACKEND_URL="http://127.0.0.1:3000"
    ;;
  *)
    echo "Unsupported SKYFORCE_BACKEND_TARGET: $BACKEND_TARGET" >&2
    echo "Use 'compat' or 'gateway'." >&2
    exit 2
    ;;
esac

run_step() {
  local name="$1"
  local dir="$2"
  local cmd="$3"

  echo
  echo "[$name] $cmd"
  (
    cd "$dir"
    bash -lc "$cmd"
  )
}

launch_service() {
  local name="$1"
  local dir="$2"
  local cmd="$3"

  echo "[$name] Starting in $dir..."
  (
    cd "$dir"
    nohup bash -lc "$cmd" > "$LOG_DIR/$name.log" 2>&1 &
    echo $! > "$LOG_DIR/$name.pid"
    echo "[$name] PID: $(cat "$LOG_DIR/$name.pid")"
    echo "[$name] Logs: $LOG_DIR/$name.log"
  )
}

prepare_openclaw_state() {
  local config_dir
  config_dir="$(dirname "$OPENCLAW_CONFIG_PATH")"

  mkdir -p "$OPENCLAW_STATE_DIR" "$config_dir"
  chmod 700 "$OPENCLAW_STATE_DIR" "$config_dir"

  if [[ -L "$OPENCLAW_STATE_DIR" || -L "$config_dir" ]]; then
    echo "Refusing to use symlinked OpenClaw state/config directories." >&2
    exit 2
  fi
}

configure_openclaw_pi_startup() {
  if [[ ! -d "$OPENCLAW_DIR" ]]; then
    echo "OpenClaw repo not found at $OPENCLAW_DIR" >&2
    exit 2
  fi

  prepare_openclaw_state

  run_step \
    "openclaw-pi-bootstrap" \
    "$OPENCLAW_DIR" \
    "$OPENCLAW_ENV_PREFIX pnpm install --frozen-lockfile && $OPENCLAW_ENV_PREFIX pnpm openclaw config set gateway.mode local && $OPENCLAW_ENV_PREFIX pnpm openclaw config set agents.defaults.model \"$OPENCLAW_MODEL\" && $OPENCLAW_ENV_PREFIX pnpm openclaw config set agents.defaults.workspace \"$ROOT_DIR\" && $OPENCLAW_ENV_PREFIX pnpm openclaw config set agents.defaults.repoRoot \"$ROOT_DIR\" && $OPENCLAW_ENV_PREFIX pnpm openclaw config set hooks.internal.enabled true --strict-json && $OPENCLAW_ENV_PREFIX pnpm openclaw hooks enable boot-md && $OPENCLAW_ENV_PREFIX pnpm openclaw config validate"
}

echo "========================================="
echo "Skyforce Product Spine Launcher"
echo "========================================="
echo "Root           : $ROOT_DIR"
echo "Backend target : $BACKEND_TARGET"
echo "Backend URL    : $BACKEND_URL"
echo "Verify mode    : $VERIFY_MODE"
echo "Context hub    : $ENABLE_CONTEXT_HUB"
echo "Pi agent       : $ENABLE_PI_AGENT"
echo "OpenClaw state : $OPENCLAW_STATE_DIR"
echo "OpenClaw config: $OPENCLAW_CONFIG_PATH"
echo "OpenClaw model : $OPENCLAW_MODEL"

if [[ "$SKIP_VERIFY" != "1" ]]; then
  echo
  echo "Preflight verification..."
  run_step \
    "workspace-verify" \
    "$ROOT_DIR" \
    "bash scripts/verify-workspace.sh $VERIFY_MODE"
else
  echo
  echo "Preflight verification skipped because SKYFORCE_SKIP_VERIFY=1"
fi

echo
echo "Build phase..."

run_step \
  "skyforce-core-build" \
  "$ROOT_DIR/skyforce-core" \
  "npm install && npm run build"

run_step \
  "${BACKEND_NAME}-build" \
  "$BACKEND_DIR" \
  "$BACKEND_INSTALL_CMD"

run_step \
  "skyforce-harness-build" \
  "$ROOT_DIR/skyforce-harness" \
  "npm install"

run_step \
  "skyforce-command-centre-live-build" \
  "$ROOT_DIR/skyforce-command-centre-live" \
  "$MISE_BIN exec -- mix setup"

if [[ "$ENABLE_CONTEXT_HUB" == "1" && -d "$ROOT_DIR/skyforce-context-hub" ]]; then
  run_step \
    "skyforce-context-hub-build" \
    "$ROOT_DIR/skyforce-context-hub" \
    "npm install"
fi

if [[ "$ENABLE_PI_AGENT" == "1" ]]; then
  configure_openclaw_pi_startup
fi

echo
echo "Test phase..."

run_step \
  "skyforce-core-smoke" \
  "$ROOT_DIR/skyforce-core" \
  "npm run sky:smoke"

run_step \
  "${BACKEND_NAME}-test" \
  "$BACKEND_DIR" \
  "$BACKEND_TEST_CMD"

run_step \
  "skyforce-harness-smoke" \
  "$ROOT_DIR/skyforce-harness" \
  "npm run smoke"

run_step \
  "skyforce-command-centre-live-test" \
  "$ROOT_DIR/skyforce-command-centre-live" \
  "$MISE_BIN exec -- mix test"

if [[ "$ENABLE_CONTEXT_HUB" == "1" && -d "$ROOT_DIR/skyforce-context-hub" ]]; then
  run_step \
    "skyforce-context-hub-test" \
    "$ROOT_DIR/skyforce-context-hub" \
    "npm test"
fi

echo
echo "Launch phase..."

launch_service \
  "skyforce-core-next" \
  "$ROOT_DIR/skyforce-core" \
  "PORT=$CORE_PORT npm run dev"
sleep 2

launch_service \
  "skyforce-core-bots" \
  "$ROOT_DIR/skyforce-core" \
  "ENVIRONMENT=development npx tsx lib/linear-bots/server.ts"
sleep 2

launch_service \
  "$BACKEND_NAME" \
  "$BACKEND_DIR" \
  "SKYFORCE_CONTEXT_HUB_URL=$CONTEXT_HUB_URL $BACKEND_RUN_CMD"
sleep 2

if [[ "$ENABLE_CONTEXT_HUB" == "1" && -d "$ROOT_DIR/skyforce-context-hub" ]]; then
  launch_service \
    "skyforce-context-hub" \
    "$ROOT_DIR/skyforce-context-hub" \
    "PORT=$CONTEXT_HUB_PORT npm start"
  sleep 2
fi

launch_service \
  "skyforce-command-centre-live" \
  "$ROOT_DIR/skyforce-command-centre-live" \
  "SKYFORCE_COMMAND_CENTRE_API_URL=$BACKEND_URL PORT=$LIVEVIEW_PORT $MISE_BIN exec -- mix phx.server"
sleep 2

if [[ "$ENABLE_PI_AGENT" == "1" ]]; then
  launch_service \
    "openclaw-gateway" \
    "$OPENCLAW_DIR" \
    "$OPENCLAW_ENV_PREFIX pnpm openclaw gateway run --port $OPENCLAW_PORT"
  sleep 2
fi

echo
echo "========================================="
echo "Skyforce product spine launched."
echo
echo "Services:"
echo "- skyforce-core: http://127.0.0.1:$CORE_PORT"
echo "- skyforce-core-bots health: http://127.0.0.1:$CORE_BOTS_PORT/health"
echo "- $BACKEND_NAME: $BACKEND_URL"
echo "- skyforce-command-centre-live: http://127.0.0.1:$LIVEVIEW_PORT"
if [[ "$ENABLE_CONTEXT_HUB" == "1" && -d "$ROOT_DIR/skyforce-context-hub" ]]; then
  echo "- skyforce-context-hub: $CONTEXT_HUB_URL"
fi
if [[ "$ENABLE_PI_AGENT" == "1" ]]; then
  echo "- openclaw-gateway: ws://127.0.0.1:$OPENCLAW_PORT"
fi
echo
echo "Log files:"
ls -la "$LOG_DIR"
echo
echo "Follow logs with:"
echo "tail -f $LOG_DIR/<service-name>.log"
echo
echo "Stop services with:"
echo "pkill -f 'next dev|tsx lib/linear-bots/server.ts|uvicorn main:app|mix phx.server|scripts/run-node.mjs gateway|openclaw.mjs gateway'"
echo "========================================="
