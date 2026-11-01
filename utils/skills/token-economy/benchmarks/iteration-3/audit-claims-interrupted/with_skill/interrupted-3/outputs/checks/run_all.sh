#!/bin/sh
# Re-runs every check from the repo root; each writes checks/<module>/results.json
cd "$(dirname "$0")/.." || exit 1
for m in dates intervals lists money numbers paths records text; do python3 -I checks/$m/check_$m.py > /dev/null || exit 1; done
python3 -I checks/make_report.py
