"""Shared helper for checks. Usage in checks/<module>/<ID>.py:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from _common import rng, verdict
    r = rng()                      # random.Random(SEED), SEED=20261029 fixed
    verdict('T1', True)            # or verdict('T1', False, counterexample='slugify("-")=...')
Run from repo root: python3 checks/<module>/<ID>.py  (prints one JSON line, exit 0 if true, 1 if false)."""
import json, os, random, sys
SEED = 20261029
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path: sys.path.insert(0, ROOT)
def rng(): return random.Random(SEED)
def verdict(id, ok, counterexample=None):
    print(json.dumps({"id": id, "verdict": "verdadeira" if ok else "falsa",
                      "counterexample": None if ok else counterexample, "seed": SEED}, ensure_ascii=False))
    sys.exit(0 if ok else 1)
