#!/usr/bin/env bash
# Iteration 3, smaller batch: audit-claims-interrupted (4+4 full, 4+4 interrupted) and
# verify-claims-subagents (6+6). The interruption limit is half the mean units of the
# full audit runs, computed after them. Re-running resumes: finished runs are skipped.
set -euo pipefail
H=$(cd "$(dirname "$0")" && pwd)
IT=$H/../iteration-3
WORK=${WORK_ROOT:?set WORK_ROOT to a scratch folder}
cd "$IT"
python3 - <<'PY'
import json
jobs = [{"case": "audit-claims-interrupted", "config": c, "run": f"full-{i}"} for i in range(1, 5) for c in ("with_skill", "without_skill")]
jobs += [{"case": "verify-claims-subagents", "config": c, "run": f"run-{i}"} for i in range(1, 7) for c in ("with_skill", "without_skill")]
json.dump(jobs, open("jobs-1.json", "w"), indent=1)
PY
python3 -I "$H/batch.py" . jobs-1.json --parallel 4 --work-root "$WORK" | tee -a batch.log
python3 - <<'PY'
import json, statistics, pathlib
u = [json.loads(p.read_text())["usage"]["units"] for p in pathlib.Path("audit-claims-interrupted").glob("*/full-*/run.json")]
assert len(u) == 8, f"expected 8 full audit runs, got {len(u)}"
limit = round(0.5 * statistics.mean(u))
pathlib.Path("interrupt-limit.json").write_text(json.dumps({"full_units": u, "limit_units": limit}) + "\n")
jobs = [{"case": "audit-claims-interrupted", "config": c, "run": f"interrupted-{i}", "interrupt_units": limit} for i in range(1, 5) for c in ("with_skill", "without_skill")]
json.dump(jobs, open("jobs-2.json", "w"), indent=1)
print("limit units:", limit)
PY
python3 -I "$H/batch.py" . jobs-2.json --parallel 4 --work-root "$WORK" | tee -a batch.log
python3 -I "$H/compare.py" . --json compare.json > /dev/null
python3 -I "$H/summary.py" . | tee summary.txt
echo DONE
