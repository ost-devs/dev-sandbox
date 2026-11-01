"""Shared helpers for claim checks. Stdlib only, deterministic.

Usage in checks/<module>/check_<module>.py:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))   # repo root -> kit
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))         # checks -> _lib
    from _lib import Checker, rand_strings, rand_ints
    c = Checker('text')

    @c.claim('T01')
    def _():
        return c.eq(kit.text.slugify('Café Noir'), 'cafe-noir')   # fixed input

    @c.claim('T02')
    def _():
        # property: use seeded generators; return first counterexample
        return c.forall(rand_strings(seed=1002, n=2000), lambda s: not slugify(s).startswith('-'))

    c.main()   # runs all, prints table, writes results.json next to the script

Each claim fn returns a Result via c.eq / c.forall / c.ok(True) / c.fail(counterexample_text).
Exceptions raised by the code under test count as FALSE with the exception as counterexample
(unless the claim says otherwise -- then catch it yourself).
"""
import json, os, random, sys, string, traceback

class Result:
    def __init__(self, ok, cex=None, note=None):
        self.ok, self.cex, self.note = ok, cex, note

# Edge-case pool mixed into every generated string set (unicode, whitespace, empty, symbols).
EDGE_STRINGS = ['', ' ', '  ', '-', '--', ' - ', 'a', 'A', 'ab', '\t', '\n', 'a  b', 'Café Noir',
                'ø', 'ß', 'İ', 'ǆ', 'ﬁ', 'Ação', 'élan', '日本語', '😀', ' ', 'á',
                '___', 'a-b', '-a-', '  a  ', 'x'*50, '0', '007', '1e5', '-1', '.', '..', '/', '//a//b/']

def rand_strings(seed, n=2000, maxlen=12):
    """Deterministic: edge pool first, then n random strings from a mixed alphabet. Seed must be recorded in the check."""
    r = random.Random(seed)
    alpha = string.ascii_letters + string.digits + ' -_.\t\n/' + 'éèçãøßİǆﬁ日😀 '
    out = list(EDGE_STRINGS)
    for _ in range(n):
        out.append(''.join(r.choice(alpha) for _ in range(r.randint(0, maxlen))))
    return out

def rand_ints(seed, n=2000, lo=-50, hi=50):
    r = random.Random(seed)
    return [0, 1, -1, 2, lo, hi] + [r.randint(lo, hi) for _ in range(n)]

def rand_floats(seed, n=2000, lo=-1e6, hi=1e6):
    r = random.Random(seed)
    return [0.0, -0.0, 0.5, 1.5, 2.5, 0.1, 0.2, 0.3, 1e-9, 1e15] + [round(r.uniform(lo, hi), r.randint(0, 6)) for _ in range(n)]

def rand_lists(seed, n=1000, maxlen=8, lo=-5, hi=5):
    r = random.Random(seed)
    out = [[], [0], [1, 1], [1, 2, 3], [3, 2, 1]]
    for _ in range(n):
        out.append([r.randint(lo, hi) for _ in range(r.randint(0, maxlen))])
    return out

class Checker:
    def __init__(self, module):
        self.module, self.claims = module, []
    def claim(self, cid):
        def deco(fn):
            self.claims.append((cid, fn)); return fn
        return deco
    # result builders
    def ok(self, note=None): return Result(True, note=note)
    def fail(self, cex): return Result(False, cex=cex)
    def eq(self, got, want):
        return Result(True) if got == want else Result(False, f'got {got!r}, expected {want!r}')
    def forall(self, inputs, pred):
        """pred(x) -> bool. First failing input (or raised exception) is the counterexample."""
        for x in inputs:
            try:
                if not pred(x): return Result(False, f'input {x!r}')
            except Exception as e:
                return Result(False, f'input {x!r} raised {type(e).__name__}: {e}')
        return Result(True, note=f'{len(inputs)} inputs')
    def main(self):
        here = os.path.dirname(os.path.abspath(sys.argv[0]))
        res = []
        for cid, fn in self.claims:
            try:
                r = fn()
            except Exception as e:
                r = Result(False, f'raised {type(e).__name__}: {e}')
            res.append({'id': cid, 'verdict': 'verdadeira' if r.ok else 'falsa', 'counterexample': r.cex, 'note': r.note})
            print(f"{cid}\t{res[-1]['verdict']}\t{r.cex or ''}")
        with open(os.path.join(here, 'results.json'), 'w') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
