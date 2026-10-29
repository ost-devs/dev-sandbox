"""Shared harness for claim checks. Usage in checks/<module>/check_<module>.py:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from harness import claim, run, rng, rand_str, rand_ints, SEED
    from kit import text

    @claim('T01')
    def t01():
        return text.slugify('Café Noir') == 'cafe-noir'   # True => verdadeira

    A check returns True (claim holds) or returns/raises a counterexample:
      return (False, "slugify('-')=... ")      # falsa + counterexample string
    For property claims: loop N=2000 cases from rng('T02') (seed = SEED + claim id, deterministic),
    return (False, repr(first_failing_input_and_output)) on first failure, else True.
    An exception raised by the code under test on a valid input counts as falsa (counterexample = input + exception).
    Every file ends with:  if __name__ == '__main__': run(__file__)

CLI:  python3 -I checks/<mod>/check_<mod>.py [ID ...]   -> prints one JSON line per claim and
      writes checks/<mod>/results.json when run with no ID. Exit code 0 always.
"""
import json, os, random, sys, zlib, traceback

SEED = 20261029
_REG = []

def claim(cid):
    def deco(f):
        _REG.append((cid, f)); return f
    return deco

def rng(cid):
    return random.Random(SEED * 1000 + zlib.crc32(cid.encode()) % 1000003)

_ALPHA = "abcXYZ019 -_.,:\t\néçãØøßİΣ中!/\\"
def rand_str(r, maxlen=12, alphabet=_ALPHA):
    return ''.join(r.choice(alphabet) for _ in range(r.randint(0, maxlen)))

def rand_ints(r, maxlen=8, lo=-20, hi=20):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]

def run(path):
    ids = sys.argv[1:]
    out = []
    for cid, f in _REG:
        if ids and cid not in ids: continue
        try:
            res = f()
            if res is True: v, ce = 'verdadeira', ''
            elif isinstance(res, tuple): v, ce = 'falsa', str(res[1])
            else: v, ce = 'falsa', str(res)
        except Exception as e:
            v, ce = 'falsa', 'exceção: ' + repr(e)
        out.append({'id': cid, 'veredito': v, 'contraexemplo': ce})
        print(json.dumps(out[-1], ensure_ascii=False))
    if not ids:
        with open(os.path.join(os.path.dirname(os.path.abspath(path)), 'results.json'), 'w') as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
