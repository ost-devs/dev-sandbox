"""Shared helper for claim checks. Each check script defines functions and calls run(globals()).
Seed fixed at SEED; each claim gets its own random.Random(SEED + hash-free offset).
A check function named check_<ID>(rng) returns (True, None) if the claim holds,
or (False, "counterexample text") if falsified. Output: one JSON line per claim."""
import json, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SEED = 20261101

def rng_for(cid):
    return random.Random(f"{SEED}-{cid}")

def run(ns):
    out = []
    for name in sorted(k for k in ns if k.startswith("check_")):
        cid = name[len("check_"):]
        try:
            ok, ce = ns[name](rng_for(cid))
        except Exception as e:  # an exception on a valid input is a counterexample
            ok, ce = False, f"raised {type(e).__name__}: {e}"
        out.append({"id": cid, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce, "seed": SEED})
    for o in out:
        print(json.dumps(o, ensure_ascii=False))
