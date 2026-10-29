"""Shared harness for claim checks. Deterministic: every random input comes from a recorded seed.

Usage in a check module (checks/check_<module>.py):

    from harness import claim, example, forall, run
    import random

    @claim('T3')
    def _():
        # fixed-example claim: return (holds: bool, detail: str)
        return example(slugify('Café Noir'), 'cafe-noir')

    @claim('T1')
    def _():
        # universal claim: generator(rng) -> input tuple, prop(*input) -> bool
        return forall(lambda r: (rand_text(r),), lambda s: not s.startswith('-'), seed=1, n=5000)

    if __name__ == '__main__':
        run()

Output: one line per claim, tab-separated: ID, TRUE|FALSE, detail (counterexample when FALSE).
Exit code is 0 regardless of verdicts (a FALSE verdict is a result, not an error).
"""
import random
import string
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # make `calc` importable

_CLAIMS = []

def claim(cid):
    def deco(fn):
        _CLAIMS.append((cid, fn))
        return fn
    return deco

def _call(f, args):
    try:
        return ('ok', f(*args))
    except Exception as e:
        return ('exc', f'{type(e).__name__}: {e}')

def example(actual_thunk, expected):
    """Compare a zero-arg thunk's result (or raised exception) with the expected value."""
    kind, val = _call(actual_thunk, ())
    if kind == 'exc':
        return False, f'raised {val}; expected {expected!r}'
    # Python `==` semantics, as the claims are written (e.g. 3.0 == 3 holds); `is True` claims: pass expected=True
    if (val is expected) if isinstance(expected, bool) else (val == expected):
        return True, f'got {val!r}'
    return False, f'got {val!r}; expected {expected!r}'

def forall(gen, prop, seed, n, cases=()):
    """Check prop on fixed `cases` (tuples) first, then on n inputs from gen(random.Random(seed)).
    prop raising an exception counts as a counterexample. Returns (holds, detail)."""
    def test(args):
        kind, val = _call(prop, args)
        if kind == 'exc':
            return f'input={args!r} -> raised {val}'
        if not val:
            return f'input={args!r}'
        return None
    for args in cases:
        bad = test(args)
        if bad:
            return False, f'fixed case {bad}'
    rng = random.Random(seed)
    for i in range(n):
        args = gen(rng)
        bad = test(args)
        if bad:
            return False, f'seed={seed} i={i} {bad}'
    return True, f'{len(cases)} fixed + {n} random cases (seed={seed}) passed'

# --- common generators -------------------------------------------------------
ALPHABET = string.ascii_letters + string.digits + ' -_\t\n.,!?' + 'áéíóúçãõñüÇÉ' + ' '

def rand_text(r, maxlen=20, alphabet=ALPHABET):
    return ''.join(r.choice(alphabet) for _ in range(r.randint(0, maxlen)))

def rand_int(r, lo=-1000, hi=1000):
    return r.randint(lo, hi)

def rand_list(r, maxlen=15, elem=lambda r: r.randint(-5, 5)):
    return [elem(r) for _ in range(r.randint(0, maxlen))]

def run():
    for cid, fn in _CLAIMS:
        try:
            holds, detail = fn()
        except Exception as e:
            holds, detail = False, f'check itself raised {type(e).__name__}: {e}'
        print(f"{cid}\t{'TRUE' if holds else 'FALSE'}\t{detail}")
