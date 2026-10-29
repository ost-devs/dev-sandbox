"""Grades a claims-audit run (verify-claims-subagents, audit-claims-interrupted).

    python3 -I grade_claims.py <run-dir> <truth.json>

Reads <run-dir>/outputs/report.md, compares the verdicts with truth.json, checks that
false rows have a counterexample, runs each distinct reproduce command twice from
outputs/ and compares the two outputs. Writes <run-dir>/grading.json (skill-creator
format) and <run-dir>/auto_grade.json (details).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TRUE_WORDS = ("verdadeira", "true", "verdadeiro")
FALSE_WORDS = ("falsa", "false", "falso")


def parse_report(text, ids):
    rows = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if not cells:
            continue
        m = re.search(r"\b([A-Z]\d{1,2})\b", cells[0])
        if not m or m.group(1) not in ids:
            continue
        rest = [c.lower().strip("*` ") for c in cells[1:]]
        verdict = None
        for c in rest:
            if any(c.startswith(w) for w in FALSE_WORDS):
                verdict = False
                break
            if any(c.startswith(w) for w in TRUE_WORDS):
                verdict = True
                break
        cmd = None
        for c in reversed(cells[1:]):
            mm = re.search(r"`([^`]*python[^`]*)`", c)
            if mm:
                cmd = mm.group(1).replace("\\|", "|")
                break
        cex = cells[2] if len(cells) > 2 else ""
        rows[m.group(1)] = {"verdict": verdict, "cmd": cmd, "counterexample": cex}
    return rows


def run(cmd, cwd):
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return "timeout", ""


def main():
    run_dir, truth = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    out = run_dir / "outputs"
    report = out / "report.md"
    rows = parse_report(report.read_text(), set(truth)) if report.exists() else {}
    wrong = sorted(i for i in truth if i not in rows or rows[i]["verdict"] != truth[i])
    missing = sorted(i for i in truth if i not in rows)
    no_cex = sorted(i for i, r in rows.items() if r["verdict"] is False and
                    (not r["counterexample"] or r["counterexample"] in ("-", "—", "")))
    cmds = sorted({r["cmd"] for r in rows.values() if r["cmd"]})
    unstable, failing = [], []
    for c in cmds:
        a, b = run(c, out), run(c, out)
        if a != b:
            unstable.append(c)
        if a[0] not in (0, 1):
            failing.append(c)
    no_cmd = sorted(i for i, r in rows.items() if not r["cmd"])
    n, nf = len(truth), sum(not v for v in truth.values())
    detail = {"rows": len(rows), "wrong": wrong, "missing": missing, "no_counterexample": no_cex,
              "commands": len(cmds), "unstable": unstable, "failing": failing, "no_command": no_cmd}
    exp = [
        {"text": f"report.md gives the verdict of truth.json for all {n} claims ({nf} false)",
         "passed": not wrong, "evidence": f"{n - len(wrong)}/{n} right; wrong={wrong[:20]}"},
        {"text": "Every claim report.md marks false has a concrete counterexample",
         "passed": bool(rows) and not no_cex, "evidence": f"false rows without counterexample: {no_cex[:20]}"},
        {"text": "Running the reproduce command of every row twice gives the same output both times",
         "passed": bool(cmds) and not unstable and not no_cmd and not failing,
         "evidence": f"{len(cmds)} distinct commands; unstable={len(unstable)} failing={len(failing)} rows without command={len(no_cmd)}"},
    ]
    passed = sum(e["passed"] for e in exp)
    (run_dir / "grading.json").write_text(json.dumps({"expectations": exp, "summary": {
        "passed": passed, "failed": len(exp) - passed, "total": len(exp),
        "pass_rate": round(passed / len(exp), 4)}}, indent=1) + "\n")
    (run_dir / "auto_grade.json").write_text(json.dumps(detail, indent=1) + "\n")
    print(json.dumps({"right": n - len(wrong), "of": n, **{k: (len(v) if isinstance(v, list) else v) for k, v in detail.items()}}))


if __name__ == "__main__":
    main()
