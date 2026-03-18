#!/bin/bash
set -euo pipefail

REPO="${1:-.}"
OUT_DIR="${2:-artifacts/current}"

python3 scripts/dependency_scan.py "$REPO" "$OUT_DIR"
