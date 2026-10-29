"""One line per run: python3 -I summary.py <iteration-dir>"""
import json
import sys
from pathlib import Path

for rj in sorted(p for p in Path(sys.argv[1]).glob("*/*/*/run.json") if ".failed" not in p.parent.name):
    d = json.loads(rj.read_text())
    g = json.loads((rj.parent / "grading.json").read_text())
    usd = [p["reported_cost_usd"] for p in d["phases"]]
    print("%-58s units=%7d usd=%-22s s=%-12s sub=%-2s skill=%-5s pass=%.2f %s" % (
        str(rj.parent.relative_to(sys.argv[1])), d["usage"]["units"], usd, [p["seconds"] for p in d["phases"]],
        d["subagents"], bool(d["skill_calls"]), g["summary"]["pass_rate"], [p["subtype"] for p in d["phases"]]))
