#!/bin/bash
# Re-runs every module check from the repo root; rewrites checks/<module>/results.json
cd "$(dirname "$0")/.." || exit 1
for m in text dates intervals lists money numbers paths records; do python3 checks/$m/check_$m.py >/dev/null || exit 1; done
