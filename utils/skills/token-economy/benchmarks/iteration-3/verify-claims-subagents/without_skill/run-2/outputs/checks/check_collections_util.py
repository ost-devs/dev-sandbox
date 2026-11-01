import os, sys, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

rng = random.Random(12345)
lists = [[], [0], [1, 1], [1, 2, 3], [3, 1, 2], [1, 1.0, True], [None], ['a', 'b', 'a']]
for _ in range(300):
    lists.append([rng.randint(-5, 5) for _ in range(rng.randint(0, 12))])

def first(it):
    for x in it:
        return x
    return None

def run(f):
    try:
        return f()
    except Exception as e:
        return ('EXC', repr(e))

def c1():
    for xs in lists:
        for n in range(1, 15):
            r = run(lambda: chunk(xs, n))
            if isinstance(r, tuple) or [y for c in r for y in c] != xs:
                return (xs, n, r)
def c2():
    for xs in lists:
        exp, seen = [], []
        for x in xs:
            if x not in seen:
                seen.append(x); exp.append(x)
        r = run(lambda: dedupe(xs))
        if r != exp:
            return (xs, r)
def c3():
    r = run(lambda: flatten([[1, [2]], [3]]))
    if r != [1, 2, 3]:
        return ([[1, [2]], [3]], r)
def c4():
    for xs in lists:
        for n in range(-6, 20):
            r = run(lambda: top_n(xs, n))
            if isinstance(r, tuple) or len(r) != min(n, len(xs)):
                return (xs, n, r)
def c5():
    for a, b in [({}, {}), ({'k': 1}, {'k': 2}), ({'k': 1}, {'j': 2})]:
        r = run(lambda: merge_dicts(a, b))
        for k in a:
            if k in b and (isinstance(r, tuple) or r[k] != a[k]):
                return (a, b, r)
def c6():
    for xs in lists:
        r = run(lambda: rotate(xs, len(xs)))
        if r != xs:
            return (xs, r)

for name, f in [('C1', c1), ('C2', c2), ('C3', c3), ('C4', c4), ('C5', c5), ('C6', c6)]:
    ce = f()
    print(f"{name} {'TRUE -' if ce is None else 'FALSE ' + repr(ce)}")
