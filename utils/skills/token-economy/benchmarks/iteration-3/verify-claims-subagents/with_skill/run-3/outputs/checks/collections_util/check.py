import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common import rng, report
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

def rlists(r, k=200):
    for _ in range(k):
        yield [r.randint(-3, 3) for _ in range(r.randint(0, 8))]

def search(cid, cases, prop):
    """cases: iterable of args tuples; returns smallest counterexample (by repr length)."""
    bad = []
    for args in cases:
        try:
            ok = prop(*args)
            res = None
        except Exception as e:
            ok = False; res = f"raises {type(e).__name__}: {e}"
        if not ok:
            if res is None:
                res = 'violated'
            bad.append((len(repr(args)), repr(args), res))
    if bad:
        _, a, res = min(bad)
        report(cid, False, f"args={a} {res}")
    else:
        report(cid, True)

edge = [[], [1], [1, 1], [1, 2, 3], [2, 1, 2, 1], [3, 3, 3]]

r = rng('C1')
search('C1', [(xs, n) for xs in edge + list(rlists(r)) for n in (1, 2, 3, 5, 100)],
       lambda xs, n: [y for c in chunk(xs, n) for y in c] == xs)

r = rng('C2')
def first_occ(xs):
    out = []
    for x in xs:
        if x not in out: out.append(x)
    return out
search('C2', [(xs,) for xs in edge + list(rlists(r))], lambda xs: dedupe(xs) == first_occ(xs))

search('C3', [(None,)], lambda _: flatten([[1, [2]], [3]]) == [1, 2, 3])

r = rng('C4')
search('C4', [(xs, n) for xs in edge + list(rlists(r)) for n in (-5, -1, 0, 1, 2, 3, 10)],
       lambda xs, n: len(top_n(xs, n)) == min(n, len(xs)))

r = rng('C5')
ds = [{}, {'k': 1}, {'k': 2}, {'a': 1, 'b': 2}]
for _ in range(50):
    ds.append({r.choice('abc'): r.randint(0, 5) for _ in range(r.randint(0, 3))})
search('C5', [(a, b) for a in ds for b in ds if set(a) & set(b)],
       lambda a, b: all(merge_dicts(a, b)[k] == a[k] for k in set(a) & set(b)))

r = rng('C6')
search('C6', [(xs,) for xs in edge + list(rlists(r))], lambda xs: rotate(xs, len(xs)) == xs)
