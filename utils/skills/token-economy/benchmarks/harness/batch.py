"""Runs and grades a list of jobs, a few at a time.

    python3 -I batch.py <iteration-dir> <jobs.json> [--parallel 4]

jobs.json: [{"case": "parser-diff", "config": "with_skill", "run": "run-1",
             "interrupt_units": null}, ...]. Results go to
<iteration-dir>/<case>/<config>/<run>/; a job whose run.json exists is skipped,
so an interrupted batch resumes where it stopped.
"""
import argparse
import json
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent.parent
GRADERS = {
    "verify-claims-subagents": ["grade_claims.py", "truth"],
    "audit-claims-interrupted": ["grade_claims.py", "truth"],
    "parser-diff": ["grade_parser_diff.py"],
    "triage-issues": ["grade_triage.py", "truth"],
}


STOP = threading.Event()


def failed(out):
    """A phase that ended in error (a real usage limit, a crash), not killed by our watcher."""
    d = json.loads((out / "run.json").read_text())
    return any(p["killed"] is not True and (p["subtype"] != "success" or p.get("is_error")) for p in d["phases"])


def job(it_dir, work_root, j):
    if STOP.is_set():
        return f"not started (batch stopped): {j}"
    case_dir = SKILL_ROOT / "evals" / j["case"]
    out = it_dir / j["case"] / j["config"] / j["run"]
    if (out / "run.json").exists():
        return f"skip {out}"
    cmd = [sys.executable, "-I", str(HERE / "run_case.py"), str(case_dir), j["config"], str(out),
           "--skill", str(it_dir / "skill-snapshot" / "SKILL.md"), "--work-root", str(work_root)]
    if j.get("interrupt_units"):
        cmd += ["--interrupt-units", str(j["interrupt_units"])]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (out / "runner.log").write_text(r.stdout + r.stderr)
    if not (out / "run.json").exists() or failed(out):
        STOP.set()
        out.rename(out.with_name(out.name + f".failed-{int(time.time())}"))
        return f"FAILED, batch stopped: {out} (see runner.log and result-*.json there)"
    g = GRADERS[j["case"]]
    gcmd = [sys.executable, "-I", str(HERE / g[0]), str(out)] + ([str(case_dir / "truth.json")] if len(g) > 1 else [])
    gr = subprocess.run(gcmd, capture_output=True, text=True)
    return f"{j['case']} {j['config']} {j['run']}: {gr.stdout.strip()[:200]} {gr.stderr.strip()[-300:]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("it_dir", type=Path)
    ap.add_argument("jobs", type=Path)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--work-root", type=Path, required=True)
    a = ap.parse_args()
    jobs = json.loads(a.jobs.read_text())
    a.work_root.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.parallel) as ex:
        for line in ex.map(lambda j: job(a.it_dir.resolve(), a.work_root.resolve(), j), jobs):
            print(line, flush=True)


if __name__ == "__main__":
    main()
