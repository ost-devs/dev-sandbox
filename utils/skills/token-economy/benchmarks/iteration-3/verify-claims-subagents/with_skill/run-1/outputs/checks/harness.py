"""Shared helper for claim checks. Usage from checks/<module>/check_<ID>.py:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))  # repo root -> calc
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))        # checks -> harness
    from harness import run, rng
    def check():
        ...            # return None if claim holds, else a counterexample (repr-able string)
    run('T1', 'claim text', check)

rng(tag) -> random.Random seeded deterministically (SEED=20261101 + tag), so reruns are identical.
run prints one JSON line {id, verdict: verdadeira|falsa, counterexample, seed}; exit 0.
Exceptions raised by check() count as falsa, counterexample = the exception + input if you catch it yourself.
"""
import json, random, traceback
SEED = 20261101

def rng(tag=''):
    return random.Random(f"{SEED}:{tag}")

def run(cid, claim, fn):
    try:
        ce = fn()
    except Exception as e:
        ce = f"exception {type(e).__name__}: {e}"
    print(json.dumps({"id": cid, "verdict": "verdadeira" if ce is None else "falsa",
                      "counterexample": None if ce is None else str(ce), "seed": SEED},
                     ensure_ascii=False))
