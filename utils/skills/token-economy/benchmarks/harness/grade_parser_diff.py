"""Grades a parser-diff run.

    python3 -I grade_parser_diff.py <run-dir>

Kinds of difference are read from how old.parse walks each input (a tracer with the
same state machine), so the grade does not depend on how the run names them.
"""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KINDS = ["trailing_empty", "escape", "spaces", "glued"]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def events(line):
    """What old.parse meets on this line."""
    ev, cur, quoted, unq, i = set(), [], False, [], 0

    def close():
        if unq and (unq[0].isspace() or unq[-1].isspace()):
            ev.add("spaces")

    while i < len(line):
        c = line[i]
        if quoted:
            if c == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    ev.add("escape")
                    i += 1
                else:
                    quoted = False
                    if i + 1 < len(line) and line[i + 1] != ',':
                        ev.add("glued")
        elif c == '"':
            quoted = True
        elif c == ',':
            close()
            unq = []
            if i == len(line) - 1:
                ev.add("trailing_empty")
        else:
            unq.append(c)
        i += 1
    close()
    return ev


def reproduce_cmd(report):
    blocks = re.findall(r"```[a-z]*\n(.*?)```", report, re.S)
    for b in blocks:
        for l in b.splitlines():
            if "python" in l and not l.strip().startswith("#"):
                return l.strip()
    m = re.search(r"`([^`\n]*python[^`\n]*)`", report)
    return m.group(1) if m else None


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def main():
    run_dir = Path(sys.argv[1])
    out = run_dir / "outputs"
    sys.dont_write_bytecode = True
    old, new = load(out / "csvline" / "old.py"), load(out / "csvline" / "new.py")
    rows, bad_lines = [], 0
    f = out / "diffs.jsonl"
    for l in (f.read_text().splitlines() if f.exists() else []):
        try:
            rows.append(json.loads(l))
        except ValueError:
            bad_lines += 1
    found, not_real = set(), []
    for r in rows:
        s = r.get("input")
        if not isinstance(s, str):
            not_real.append(r)
            continue
        o, n = old.parse(s), new.parse(s)
        if o == n or r.get("old") != o or r.get("new") != n:
            not_real.append(s)
        if o != n:
            found |= events(s)
    report = (out / "diff-report.md").read_text() if (out / "diff-report.md").exists() else ""
    cmd = reproduce_cmd(report)
    hashes = []
    if cmd:
        for _ in range(2):
            tmp = Path(tempfile.mkdtemp())
            shutil.copytree(out, tmp / "w")
            (tmp / "w" / "diffs.jsonl").unlink(missing_ok=True)
            try:
                subprocess.run(["bash", "-c", cmd], cwd=tmp / "w", capture_output=True, timeout=300)
            except subprocess.TimeoutExpired:
                pass
            hashes.append(digest(tmp / "w" / "diffs.jsonl"))
            shutil.rmtree(tmp)
    stable = bool(cmd) and hashes[0] is not None and hashes[0] == hashes[1]
    same_as_submitted = stable and hashes[0] == digest(f)
    missing = [k for k in KINDS if k not in found]
    exp = [
        {"text": "diffs.jsonl has at least one input for each of the 4 kinds of difference", "passed": not missing,
         "evidence": f"found={sorted(found)} missing={missing}"},
        {"text": "Every line of diffs.jsonl is a real difference with the recorded outputs", "passed": bool(rows) and not not_real and not bad_lines,
         "evidence": f"{len(rows)} lines; not real or wrong output: {len(not_real)}; unparsable: {bad_lines}"},
        {"text": "Running the reproduce command twice regenerates the same diffs.jsonl", "passed": stable,
         "evidence": f"cmd={cmd!r}; same twice={stable}; same as submitted={same_as_submitted}"},
    ]
    passed = sum(e["passed"] for e in exp)
    (run_dir / "grading.json").write_text(json.dumps({"expectations": exp, "summary": {
        "passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": round(passed / len(exp), 4)}}, indent=1) + "\n")
    detail = {"diff_lines": len(rows), "kinds_found": sorted(found), "missing": missing, "not_real": len(not_real),
              "cmd": cmd, "stable": stable, "same_as_submitted": same_as_submitted}
    (run_dir / "auto_grade.json").write_text(json.dumps(detail, indent=1) + "\n")
    print(json.dumps(detail))


if __name__ == "__main__":
    main()
