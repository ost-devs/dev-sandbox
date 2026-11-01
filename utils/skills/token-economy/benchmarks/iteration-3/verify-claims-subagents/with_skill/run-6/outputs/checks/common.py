"""Shared helper for checks. Usage in a check script (run from repo root):
    python3 checks/<module>/check_<ID>.py
Script starts with:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from common import rng, verdict
rng(seed) -> random.Random(seed); record the seed in the script as SEED constant.
verdict(id, ok, counterexample=None) prints one line `<id> TRUE` or `<id> FALSE counterexample: ...`, exits 0.
"""
import random

def rng(seed):
    return random.Random(seed)

def verdict(cid, ok, counterexample=None):
    if ok:
        print(f"{cid} TRUE")
    else:
        print(f"{cid} FALSE counterexample: {counterexample!r}")
