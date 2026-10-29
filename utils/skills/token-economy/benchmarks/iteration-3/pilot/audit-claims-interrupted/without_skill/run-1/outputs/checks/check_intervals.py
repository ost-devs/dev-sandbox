#!/usr/bin/env python3
import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.intervals import *

SEED = 20240611
N = 3000
RNG_RANGE = range(-3, 5)

def ivs(strict=True):
    """all integer intervals in -3..4 (ordered by size of repr for determinism), strict => start<end"""
    return [(s, e) for s in RNG_RANGE for e in RNG_RANGE if (s < e or not strict)]

def rand_iv(r, strict=True):
    while True:
        s, e = r.randint(-50, 50), r.randint(-50, 50)
        if not strict or s < e:
            return (s, e)

def rand_lists(r, n=N):
    for _ in range(n):
        yield [rand_iv(r) for _ in range(r.randint(1, 7))]

def small_lists():
    base = ivs()
    for k in (1, 2, 3):
        for xs in itertools.product(base[:: (1 if k < 3 else 3)], repeat=k):
            yield list(xs)

def exact(thunk, expected):
    try:
        got = thunk()
    except Exception as ex:
        return False, "raised %s(%s), expected %r" % (type(ex).__name__, ex, expected)
    if got == expected and type(got) == type(expected):
        return True, None
    return False, "got %r, expected %r" % (got, expected)

def pick_min(cands):
    """cands: list of (size_key, description); smallest by key then repr"""
    return min(cands, key=lambda c: (c[0], c[1]))[1]

def forall_pairs(pred, strict=False, label=""):
    cands = []
    r = random.Random(SEED)
    pairs = [(a, b) for a in ivs(strict) for b in ivs(strict)]
    pairs += [(rand_iv(r, strict), rand_iv(r, strict)) for _ in range(N)]
    for a, b in pairs:
        try:
            ok, msg = pred(a, b)
        except Exception as ex:
            ok, msg = False, "raised %s(%s)" % (type(ex).__name__, ex)
        if not ok:
            cands.append((sum(abs(v) for v in a + b), "a=%r b=%r: %s" % (a, b, msg)))
    return cands

def forall_lists(pred):
    cands = []
    r = random.Random(SEED)
    for xs in itertools.chain(small_lists(), rand_lists(r)):
        try:
            ok, msg = pred(xs)
        except Exception as ex:
            ok, msg = False, "raised %s(%s)" % (type(ex).__name__, ex)
        if not ok:
            cands.append(((len(xs), sum(abs(v) for i in xs for v in i)), "xs=%r: %s" % (xs, msg)))
    return cands

def verdict(cands):
    if not cands:
        return True, None
    return False, pick_min(cands)

def I01(): return exact(lambda: overlaps((0, 5), (5, 10)), False)
def I02():
    return verdict(forall_pairs(lambda a, b: (overlaps(a, b) == overlaps(b, a), "overlaps(a,b)=%r overlaps(b,a)=%r" % (overlaps(a, b), overlaps(b, a))), strict=False))
def I03(): return exact(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
def I04(): return exact(lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
def I05():
    def p(xs):
        m = merge(xs)
        ok = all(m[i][0] < m[i + 1][0] for i in range(len(m) - 1)) and \
             all(not overlaps(m[i], m[j]) for i in range(len(m)) for j in range(i + 1, len(m)))
        return ok, "merge=%r" % (m,)
    return verdict(forall_lists(p))
def I06():
    def p(xs):
        m = merge(xs); mm = merge(m)
        return mm == m, "merge=%r merge(merge)=%r" % (m, mm)
    return verdict(forall_lists(p))
def I07(): return exact(lambda: contains((0, 5), 5), False)
def I08():
    c = []
    r = random.Random(SEED)
    for a in ivs() + [rand_iv(r) for _ in range(N)]:
        if contains(a, a[0]) is not True:
            c.append((sum(map(abs, a)), "a=%r contains(a,a[0])=%r, expected True" % (a, contains(a, a[0]))))
    return verdict(c)
def I09(): return exact(lambda: intersect((0, 5), (3, 8)), (3, 5))
def I10(): return exact(lambda: intersect((0, 2), (5, 6)), None)
def I11(): return exact(lambda: intersect((0, 5), (5, 8)), None)
def I12(): return exact(lambda: total_covered([(0, 5), (3, 8)]), 8)
def I13():
    def p(xs):
        t = total_covered(xs); s = sum(length(i) for i in xs)
        return t <= s, "total_covered=%r sum_lengths=%r" % (t, s)
    return verdict(forall_lists(p))
def I14():
    def p(a, b):
        if not overlaps(a, b):
            return True, None
        l = length(intersect(a, b)); m = min(length(a), length(b))
        return l <= m, "length(intersect)=%r min(length)=%r" % (l, m)
    return verdict(forall_pairs(p, strict=True))
def I15(): return exact(lambda: merge([]), [])
def I16():
    c = []
    r = random.Random(SEED)
    for a in ivs() + [rand_iv(r) for _ in range(N)]:
        if overlaps(a, a) is not True:
            c.append((sum(map(abs, a)), "a=%r overlaps(a,a)=%r, expected True" % (a, overlaps(a, a))))
    return verdict(c)
def I17(): return exact(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
def I18():
    c = []
    r = random.Random(SEED)
    items = [(a, x) for a in ivs(False) for x in range(-4, 6)]
    items += [(rand_iv(r, False), r.randint(-50, 50)) for _ in range(N)]
    for a, x in items:
        if contains(a, x) and not overlaps(a, (x, x + 1)):
            c.append((sum(map(abs, a)) + abs(x), "a=%r x=%r: contains=True but overlaps(a,(x,x+1))=%r" % (a, x, overlaps(a, (x, x + 1)))))
    return verdict(c)
def I19(): return exact(lambda: length((3, 1)), 0)

CHECKS = {"I%02d" % i: globals()["I%02d" % i] for i in range(1, 20)}

if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))
