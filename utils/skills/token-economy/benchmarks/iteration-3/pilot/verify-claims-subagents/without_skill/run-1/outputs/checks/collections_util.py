import os, sys, random, copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
rng = random.Random(SEED)
FUZZ = 2000

def rand_list(maxlen=12, hi=5):
    return [rng.randint(-hi, hi) for _ in range(rng.randint(0, maxlen))]

def run(f):
    try:
        return f(), None
    except Exception as e:
        return None, e

def fmt(r):
    v, e = r
    return f"excecao {type(e).__name__}: {e}" if e else repr(v)

def verdict(cid, cases, prop):
    """cases: list of (label, input args); prop(args)->(ok, actual_str). Minimal = first by repr length."""
    bad = []
    for args in cases:
        ok, actual = prop(args)
        if not ok:
            bad.append((len(repr(args)), repr(args), actual))
    if bad:
        _, a, act = min(bad)
        print(f"{cid}: FALSA | contraexemplo: {a} -> {act}")
    else:
        print(f"{cid}: VERDADEIRA ({len(cases)} casos testados, sem contraexemplo, seed={SEED})")

# C1
def p1(a):
    xs, n = a; orig = copy.deepcopy(xs)
    r = run(lambda: chunk(xs, n))
    if r[1]: return False, fmt(r)
    cat = [y for c in r[0] for y in c]
    return (cat == orig and xs == orig), fmt(r)
cases = [([], 1), ([], 3), ([1], 1), ([1], 5), ([1, 2, 3], 1), ([1, 2, 3], 2), ([1, 2, 3], 3), ([1, 2, 3], 10), ([1, 1, 1], 2)]
cases += [(rand_list(), rng.randint(1, 15)) for _ in range(FUZZ)]
verdict("C1", cases, p1)

# C2
def p2(xs):
    orig = list(xs)
    exp = []
    for x in orig:
        if x not in exp: exp.append(x)
    r = run(lambda: dedupe(xs))
    return (r[1] is None and r[0] == exp and xs == orig), fmt(r)
cases = [[], [1], [1, 1], [2, 1, 2, 1], [3, 1, 3, 2, 1], [1, 1.0, True], [0, False, 0.0], ["a", "b", "a"]]
cases += [rand_list() for _ in range(FUZZ)]
verdict("C2", cases, p2)

# C3
def p3(a):
    r = run(lambda: flatten(a))
    return r == ([1, 2, 3], None), fmt(r)
verdict("C3", [[[1, [2]], [3]]], p3)

# C4
def p4(a):
    xs, n = a; orig = list(xs)
    r = run(lambda: top_n(xs, n))
    return (r[1] is None and len(r[0]) == min(n, len(xs)) and xs == orig), fmt(r)
cases = [([], 0), ([], 1), ([], -1), ([1], 0), ([1], 2), ([1, 2, 3], 0), ([1, 2, 3], 5), ([1, 2, 3], -1), ([1, 2, 3], -5), ([1, 1], 1)]
cases += [(rand_list(), rng.randint(-15, 15)) for _ in range(FUZZ)]
verdict("C4", cases, p4)

# C5
def p5(a):
    x, y = a; cx, cy = dict(x), dict(y)
    r = run(lambda: merge_dicts(x, y))
    if r[1]: return False, fmt(r)
    ok = all(r[0][k] == x[k] for k in x if k in y) and x == cx and y == cy
    return ok, fmt(r)
cases = [({}, {}), ({"k": 1}, {"k": 2}), ({"k": 1}, {}), ({}, {"k": 2}), ({"a": 1}, {"b": 2})]
for _ in range(FUZZ):
    cases.append(({rng.randint(0, 5): rng.randint(0, 9) for _ in range(rng.randint(0, 5))},
                  {rng.randint(0, 5): rng.randint(0, 9) for _ in range(rng.randint(0, 5))}))
verdict("C5", cases, p5)

# C6
def p6(xs):
    orig = list(xs)
    r = run(lambda: rotate(xs, len(xs)))
    return (r[1] is None and r[0] == orig and xs == orig), fmt(r)
cases = [[], [1], [1, 2], [1, 1], [1, 2, 3]] + [rand_list(20) for _ in range(FUZZ)]
verdict("C6", cases, p6)
sys.exit(0)
