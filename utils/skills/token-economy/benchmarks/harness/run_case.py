"""Runs one eval case once, with or without the skill, on a fresh copy of its files.

    python3 -I run_case.py <case-dir> <with_skill|without_skill> <out-dir> \
        [--skill SKILL.md] [--model M] [--interrupt-units N] [--resume-prompt TEXT]

- Isolation: --setting-sources project,local, so skills in ~/.claude/skills are not
  loaded; with_skill gets the skill at .claude/skills/token-economy/ in the copy.
- --interrupt-units: simulated usage limit. A watcher sums the usage of the session
  transcripts (main and subagents) and kills the whole run once it passes N
  units, so agents in flight die together, as with a real limit. Then the session
  is resumed with --resume and --resume-prompt.
- Writes <out-dir>/: run.json (phases, usage, exit), result-<phase>.json,
  outputs/ (the working copy at the end), snapshot-interrupt/ (copy at the kill).
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage  # noqa: E402

TOOLS = "Bash Read Write Edit Glob Grep Agent Skill"


def task_prompt(case_dir):
    text = (case_dir / "prompt.md").read_text()
    parts = text.split("---")
    body = parts[2] if len(parts) >= 3 else text
    lines = [l for l in body.strip().splitlines() if not l.startswith("Input files")]
    return "\n".join(lines).strip()


def claude_cmd(prompt, model, sid, resume):
    cmd = ["claude", "-p", prompt, "--model", model, "--setting-sources", "project,local",
           "--output-format", "json", "--permission-mode", "acceptEdits", "--allowedTools", TOOLS]
    cmd += ["--resume", sid] if resume else ["--session-id", sid]
    return cmd


def run_phase(cmd, cwd, out_json, sid, limit_units, timeout_s):
    start = time.time()
    with open(out_json, "w") as out, open(str(out_json) + ".stderr", "w") as err:
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=out, stderr=err, start_new_session=True)
        killed = False
        while proc.poll() is None:
            time.sleep(2)
            if limit_units is not None and usage.session_usage(sid)["units"] >= limit_units:
                os.killpg(proc.pid, signal.SIGKILL)
                killed = True
            elif time.time() - start > timeout_s:
                os.killpg(proc.pid, signal.SIGKILL)
                killed = "timeout"
        proc.wait()
    try:
        result = json.loads(Path(out_json).read_text())
    except Exception:
        result = None
    return {"seconds": round(time.time() - start, 1), "exit": proc.returncode, "killed": killed,
            "reported_cost_usd": (result or {}).get("total_cost_usd"),
            "subtype": (result or {}).get("subtype"), "is_error": (result or {}).get("is_error")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir", type=Path)
    ap.add_argument("config", choices=["with_skill", "without_skill"])
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--skill", type=Path)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--work-root", type=Path, required=True)
    ap.add_argument("--interrupt-units", type=float)
    ap.add_argument("--resume-prompt", default="A sessão parou no meio porque bati no limite de uso. Continua de onde parou e termina a tarefa.")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()

    case_dir = a.case_dir.resolve()
    out_dir = a.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    work = (a.work_root / f"{case_dir.name}-{a.config}-{uuid.uuid4().hex[:8]}").resolve()
    shutil.copytree(case_dir / "files", work, ignore=shutil.ignore_patterns("__pycache__"))
    if a.config == "with_skill":
        dst = work / ".claude" / "skills" / "token-economy"
        dst.mkdir(parents=True)
        shutil.copy(a.skill, dst / "SKILL.md")

    sid = str(uuid.uuid4())
    prompt = task_prompt(case_dir)
    record = {"case": case_dir.name, "config": a.config, "model": a.model, "session_id": sid,
              "work_dir": str(work), "interrupt_units": a.interrupt_units, "phases": []}

    ph = run_phase(claude_cmd(prompt, a.model, sid, False), work, out_dir / "result-1.json",
                   sid, a.interrupt_units, a.timeout)
    ph["usage_after"] = usage.session_usage(sid)
    record["phases"].append(ph)
    if ph["killed"] is True:
        shutil.copytree(work, out_dir / "snapshot-interrupt", ignore=shutil.ignore_patterns(".claude", "__pycache__"))
        ph2 = run_phase(claude_cmd(a.resume_prompt, a.model, sid, True), work, out_dir / "result-2.json",
                        sid, None, a.timeout)
        ph2["usage_after"] = usage.session_usage(sid)
        record["phases"].append(ph2)

    record["usage"] = usage.session_usage(sid)
    record["skill_calls"] = usage.skill_calls(sid)
    record["subagents"] = usage.subagent_count(sid)
    out = out_dir / "outputs"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(work, out, ignore=shutil.ignore_patterns(".claude", "__pycache__"))
    (out_dir / "run.json").write_text(json.dumps(record, indent=1) + "\n")
    print(json.dumps({k: record[k] for k in ("case", "config", "usage", "skill_calls", "subagents")}))


if __name__ == "__main__":
    main()
