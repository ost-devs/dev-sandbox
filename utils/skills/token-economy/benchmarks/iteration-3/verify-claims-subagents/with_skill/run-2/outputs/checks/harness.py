"""Shared harness. A check file defines functions decorated with @claim('ID').
Each returns None if the claim holds, or a string with a concrete counterexample
(call + actual result) if it is false. Random inputs must use rng() (fixed SEED).
Run: python3 checks/<module>_checks.py  -> prints one line per claim, writes
checks/results/<module>.json, exit 0 always."""
import json, os, random, sys, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SEED = 20261101
_CLAIMS = []


def rng():
    return random.Random(SEED)


def claim(cid):
    def deco(f):
        _CLAIMS.append((cid, f))
        return f
    return deco


def run(module):
    out = []
    for cid, f in _CLAIMS:
        try:
            ce = f()
            v, ce = ('verdadeira', '') if ce is None else ('falsa', ce)
        except Exception as e:
            v, ce = 'falsa', 'raises %s: %s' % (type(e).__name__, e)
        out.append({'id': cid, 'verdict': v, 'counterexample': ce})
        print(cid, v, ce)
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    os.makedirs(d, exist_ok=True)
    json.dump({'seed': SEED, 'results': out}, open(os.path.join(d, module + '.json'), 'w'), ensure_ascii=False, indent=1)
