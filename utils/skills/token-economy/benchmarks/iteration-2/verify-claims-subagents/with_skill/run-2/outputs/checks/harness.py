"""Shared helpers for claim checks. Each check script calls verdict() exactly once."""
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SEED = 20261029


def rng(seed=SEED):
    """Seeded RNG: same seed -> same generated inputs on every run."""
    return random.Random(seed)


def verdict(claim_id, holds, counterexample=None, method=""):
    """Print one JSON line: {"id", "verdict": true|false, "counterexample", "method"}."""
    out = {"id": claim_id, "verdict": bool(holds),
           "counterexample": None if holds else counterexample, "method": method}
    print(json.dumps(out, ensure_ascii=False, default=repr))
    return out


def search(claim_id, cases, prop, method):
    """Return a false verdict on the first case where prop(case) is False (or raises), else true."""
    n = 0
    for case in cases:
        n += 1
        try:
            ok = prop(case)
        except Exception as e:  # an exception counts as a violation
            return verdict(claim_id, False, f"{case!r} -> raised {type(e).__name__}: {e}", method)
        if not ok:
            return verdict(claim_id, False, repr(case), method)
    return verdict(claim_id, True, None, f"{method}; {n} cases, none violated")
