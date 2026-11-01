"""Compares with_skill and without_skill per case, by the rule in iteration-3/RUN.md.

    python3 -I compare.py <iteration-dir> [--json out.json]

Cost metric: usage units (usage.py), proportional to cost on one model. A run killed by
the simulated usage limit counts both phases. Ratio = mean(with) / mean(without), with a
seeded bootstrap 95% interval and an exact permutation p-value (two-sided, difference of
means).
"""
import argparse
import itertools
import json
import random
import statistics as st
from pathlib import Path

BANDS = [(0.5, "abismo"), (0.75, "grande diferença"), (0.9, "diferença pequena"), (1.0, "quase páreo")]


def runs(cfg_dir):
    out = []
    for r in sorted(p for p in cfg_dir.glob("*/run.json") if ".failed" not in p.parent.name):
        d = json.loads(r.read_text())
        g = json.loads((r.parent / "grading.json").read_text()) if (r.parent / "grading.json").exists() else None
        a = json.loads((r.parent / "auto_grade.json").read_text()) if (r.parent / "auto_grade.json").exists() else {}
        units = d["usage"]["units"]
        before_kill = d["phases"][0]["usage_after"]["units"] if len(d["phases"]) > 1 else None
        out.append({"run": r.parent.name, "units": units, "units_at_kill": before_kill,
                    "interrupted": len(d["phases"]) > 1,
                    "seconds": sum(p["seconds"] for p in d["phases"]),
                    "usd": sum(p["reported_cost_usd"] or 0 for p in d["phases"]) if all(p["reported_cost_usd"] for p in d["phases"]) else None,
                    "pass_rate": g["summary"]["pass_rate"] if g else None,
                    "skill_used": "token-economy" in (d.get("skill_calls") or []), "subagents": d.get("subagents"), "grade": a})
    return out


def boot_ratio(a, b, n=10000, seed=1):
    r = random.Random(seed)
    vals = sorted(st.mean(r.choices(a, k=len(a))) / st.mean(r.choices(b, k=len(b))) for _ in range(n))
    return vals[int(0.025 * n)], vals[int(0.975 * n)]


def perm_p(a, b):
    obs = abs(st.mean(a) - st.mean(b))
    pool, k, hits, tot = a + b, len(a), 0, 0
    for idx in itertools.combinations(range(len(pool)), k):
        s = set(idx)
        x = [pool[i] for i in idx]
        y = [pool[i] for i in range(len(pool)) if i not in s]
        tot += 1
        hits += abs(st.mean(x) - st.mean(y)) >= obs - 1e-9
    return hits / tot


def band(ratio, lo, hi):
    if lo <= 1 <= hi:
        return "páreo" if 0.9 <= lo and hi <= 1.1 else "inconclusivo (intervalo cruza 1)"
    x = ratio if ratio < 1 else 1 / ratio
    name = next(n for t, n in BANDS if x < t) if x < 1 else "quase páreo"
    return name + (" a favor da skill" if ratio < 1 else " contra a skill (custa mais)")


def compare(w, wo, key):
    a, b = [x[key] for x in w if x[key] is not None], [x[key] for x in wo if x[key] is not None]
    if len(a) < 2 or len(b) < 2:
        return None
    ratio = st.mean(a) / st.mean(b)
    lo, hi = boot_ratio(a, b)
    return {"with_mean": round(st.mean(a)), "without_mean": round(st.mean(b)),
            "with_sd": round(st.stdev(a)), "without_sd": round(st.stdev(b)),
            "ratio": round(ratio, 3), "ci95": [round(lo, 3), round(hi, 3)], "p": round(perm_p(a, b), 4),
            "verdict": band(ratio, lo, hi), "n": [len(a), len(b)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("it_dir", type=Path)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    result = {}
    for case_dir in sorted(p for p in a.it_dir.iterdir() if (p / "with_skill").is_dir()):
        w, wo = runs(case_dir / "with_skill"), runs(case_dir / "without_skill")
        groups = {"all": (w, wo)}
        if any(x["interrupted"] for x in w + wo):
            groups = {"full": ([x for x in w if not x["interrupted"]], [x for x in wo if not x["interrupted"]]),
                      "interrupted": ([x for x in w if x["interrupted"]], [x for x in wo if x["interrupted"]])}
        res = {}
        for gname, (gw, gwo) in groups.items():
            res[gname] = {
                "units": compare(gw, gwo, "units"), "usd": compare(gw, gwo, "usd"), "seconds": compare(gw, gwo, "seconds"),
                "pass_rate": {"with": [x["pass_rate"] for x in gw], "without": [x["pass_rate"] for x in gwo]},
                "skill_used": [x["skill_used"] for x in gw], "subagents": {"with": [x["subagents"] for x in gw], "without": [x["subagents"] for x in gwo]},
                "units_raw": {"with": [x["units"] for x in gw], "without": [x["units"] for x in gwo]},
            }
        if "interrupted" in groups:
            for cfg, xs in (("with", w), ("without", wo)):
                full = [x["units"] for x in xs if not x["interrupted"]]
                inter = [x for x in xs if x["interrupted"]]
                if full and inter:
                    base = st.mean(full)
                    res.setdefault("resume_overhead", {})[cfg] = {
                        "full_mean": round(base),
                        "interrupted_mean": round(st.mean(x["units"] for x in inter)),
                        "overhead_units": round(st.mean(x["units"] for x in inter) - base),
                        "overhead_pct_of_full": round(100 * (st.mean(x["units"] for x in inter) - base) / base, 1),
                        "units_at_kill": [x["units_at_kill"] for x in inter]}
        result[case_dir.name] = res
    text = json.dumps(result, indent=1, ensure_ascii=False)
    if a.json:
        a.json.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
