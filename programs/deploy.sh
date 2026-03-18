#!/bin/bash
set -euo pipefail

RUN_ID="${1:-local-run}"
OUT_DIR="${2:-artifacts/current}"

python3 scripts/deploy.py "$RUN_ID" "$OUT_DIR"
