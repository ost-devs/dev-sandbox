import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
rng = random.Random(SEED)

def rand_list(maxlen=8, lo=-3, hi=3):
    return [rng.randint(lo, hi) for _ in range(rng.randint(0, maxlen))]

ADV = [[], [0], [1], [1, 1], [1, 2, 3], [3, 1, 2], [2, 2, 1, 1], [1, 2, 3, 4, 5], [None], ['a', 'b', 'a']]
LISTS = ADV + [rand_list() for _ in range(300)]
INTS = [-5, -2, -1, 0, 1, 2, 3, 5, 10]

def first_fail(cases, pred):
    best = None
    for c in cases:
        try:
            ok = pred(*c)
            err = None
        except Exception as e:
            ok, err = False, f"{type(e).__name__}: {e}"
        if not ok:
            key = (sum(len(repr(x)) for x in c), repr(c))
            if best is None or key < best[0]:
                best = (key, c, err)
    return best

def report(id_, cases, pred, call):
    f = first_fail(cases, pred)
    if f is None:
        print(f"{id_} TRUE no counterexample in {len(cases)} cases (seed={SEED})")
    else:
        c, err = f[1], f[2]
        try:
            res = repr(call(*c))
        except Exception as e:
            res = f"raises {type(e).__name__}: {e}"
        print(f"{id_} FALSE counterexample args={c!r} -> {res}")

def c1(xs, n):
    return [y for ch in chunk(xs, n) for y in ch] == xs
report("C1", [(xs, n) for xs in LISTS for n in INTS if n >= 1], c1, chunk)

def c2(xs):
    exp, seen = [], set()
    for x in xs:
        if x not in seen:
            seen.add(x); exp.append(x)
    return dedupe(xs) == exp
report("C2", [(xs,) for xs in LISTS], c2, dedupe)

report("C3", [([[1, [2]], [3]],)], lambda x: flatten(x) == [1, 2, 3], flatten)

def c4(xs, n):
    return len(top_n(xs, n)) == min(n, len(xs))
report("C4", [(xs, n) for xs in LISTS if all(isinstance(x, int) for x in xs) for n in INTS], c4, top_n)

dicts = [{}, {'k': 1}, {'k': 2}, {'a': 1, 'b': 2}, {'b': 3, 'c': 4}]
dicts += [{rng.choice('abc'): rng.randint(0, 9) for _ in range(rng.randint(0, 4))} for _ in range(100)]
def c5(a, b):
    r = merge_dicts(a, b)
    return all(r[k] == a[k] for k in a if k in b)
report("C5", [(a, b) for a in dicts for b in dicts], c5, merge_dicts)

report("C6", [(xs,) for xs in LISTS], lambda xs: rotate(xs, len(xs)) == xs, lambda xs: rotate(xs, len(xs)))
