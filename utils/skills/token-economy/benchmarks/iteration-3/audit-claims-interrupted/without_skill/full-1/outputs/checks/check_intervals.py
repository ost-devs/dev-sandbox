import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import Results, rng
from kit.intervals import *

R = Results("intervals")
N = range(-3, 5)
ALL = [(s, e) for s in N for e in N]            # inclui degenerados/invertidos
VALID = [(s, e) for s, e in ALL if s < e]

def lists():
    """listas não vazias exaustivas (até 3 intervalos) + aleatórias, start<end."""
    for n in (1, 2, 3):
        pool = [(s, e) for s in range(0, 4) for e in range(0, 5) if s < e]
        import itertools
        for xs in itertools.product(pool, repeat=n):
            yield list(xs)
    r = rng()
    for _ in range(2000):
        xs = []
        for _ in range(r.randint(1, 8)):
            s = r.randint(-20, 20); xs.append((s, s + r.randint(1, 10)))
        yield xs
    yield [(0.5, 1.5), (1.5, 2.5)]

def eq(cid, fn, expected):
    def f():
        got = fn()
        return got == expected, (got if got != expected else None)
    R.check(cid, f)

def forall(cid, items, pred):
    def f():
        for x in items:
            if not pred(x):
                return False, x
        return True, None
    R.check(cid, f)

R.check("I01", lambda: (overlaps((0, 5), (5, 10)) is False, overlaps((0, 5), (5, 10))))
forall("I02", [(a, b) for a in ALL for b in ALL], lambda p: overlaps(*p) == overlaps(p[1], p[0]))
eq("I03", lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
eq("I04", lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
def p5(xs):
    m = merge(xs)
    return all(m[i][0] <= m[i+1][0] and not overlaps(m[i], m[i+1]) for i in range(len(m)-1))
forall("I05", lists(), p5)
forall("I06", lists(), lambda xs: merge(merge(xs)) == merge(xs))
R.check("I07", lambda: (contains((0, 5), 5) is False, contains((0, 5), 5)))
forall("I08", VALID, lambda a: contains(a, a[0]) is True)
eq("I09", lambda: intersect((0, 5), (3, 8)), (3, 5))
R.check("I10", lambda: (intersect((0, 2), (5, 6)) is None, intersect((0, 2), (5, 6))))
R.check("I11", lambda: (intersect((0, 5), (5, 8)) is None, intersect((0, 5), (5, 8))))
eq("I12", lambda: total_covered([(0, 5), (3, 8)]), 8)
forall("I13", lists(), lambda xs: total_covered(xs) <= sum(length(i) for i in xs))
forall("I14", [(a, b) for a in VALID for b in VALID if overlaps(a, b)],
       lambda p: length(intersect(*p)) <= min(length(p[0]), length(p[1])))
eq("I15", lambda: merge([]), [])
forall("I16", VALID, lambda a: overlaps(a, a) is True)
eq("I17", lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
forall("I18", [(a, x) for a in sorted(ALL, key=lambda t: (t[0] == t[1], t)) for x in range(-4, 6) if contains(a, x)],
       lambda p: overlaps(p[0], (p[1], p[1] + 1)))
eq("I19", lambda: length((3, 1)), 0)
R.finish()
