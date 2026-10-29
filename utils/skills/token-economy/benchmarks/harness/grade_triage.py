"""Grades a triage-issues run.

    python3 -I grade_triage.py <run-dir> <truth.json>
"""
import csv
import json
import sys
from pathlib import Path

ALIASES = {"bug": "bug", "feature": "feature", "duvida": "question", "dúvida": "question", "question": "question"}


def main():
    run_dir, truth = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    f = run_dir / "outputs" / "triage.csv"
    got = {}
    if f.exists():
        for row in csv.DictReader(f.read_text(encoding="utf-8-sig").splitlines()):
            row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
            try:
                n = str(int(row.get("number", "").lstrip("#")))
            except ValueError:
                continue
            dup = row.get("duplicada_de", "").lstrip("#")
            got[n] = {"type": ALIASES.get(row.get("tipo", "").lower()), "dup_of": int(dup) if dup.isdigit() else None}
    type_ok = sum(1 for n, t in truth.items() if got.get(n, {}).get("type") == t["type"])
    true_dups = {n: t["dup_of"] for n, t in truth.items() if t["dup_of"]}
    found = sum(1 for n, o in true_dups.items() if got.get(n, {}).get("dup_of") == o)
    false_dups = sorted(n for n, g in got.items() if g["dup_of"] and n not in true_dups)
    wrong_types = sorted(n for n, t in truth.items() if got.get(n, {}).get("type") != t["type"])
    exp = [
        {"text": "triage.csv gives the type of truth.json for at least 78 of the 80 issues", "passed": type_ok >= 78,
         "evidence": f"{type_ok}/80; wrong: {wrong_types}"},
        {"text": "triage.csv marks all 12 duplicates of truth.json with the right original", "passed": found == len(true_dups),
         "evidence": f"{found}/{len(true_dups)}"},
        {"text": "triage.csv marks no issue as a duplicate that truth.json does not", "passed": not false_dups,
         "evidence": f"false duplicates: {false_dups}"},
    ]
    passed = sum(e["passed"] for e in exp)
    (run_dir / "grading.json").write_text(json.dumps({"expectations": exp, "summary": {
        "passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": round(passed / len(exp), 4)}}, indent=1) + "\n")
    detail = {"rows": len(got), "types_right": type_ok, "dups_found": found, "false_dups": false_dups, "wrong_types": wrong_types}
    (run_dir / "auto_grade.json").write_text(json.dumps(detail, indent=1) + "\n")
    print(json.dumps(detail))


if __name__ == "__main__":
    main()
