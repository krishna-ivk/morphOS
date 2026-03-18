#!/bin/bash
set -euo pipefail

REPO="${1:-.}"
OUT_DIR="${2:-artifacts/current}"

python3 scripts/repo_scan.py "$REPO" "$OUT_DIR"
