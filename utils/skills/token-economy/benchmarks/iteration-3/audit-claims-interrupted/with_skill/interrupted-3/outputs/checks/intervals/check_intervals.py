import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker
from kit.intervals import *
c = Checker('intervals')

def gen_ivs(seed, n=1500, lo=-10, hi=10, strict=True):
    r = random.Random(seed)
    out = [(0, 1), (-1, 0), (0, 5), (-5, 5)]
    if not strict:
        out += [(3, 1), (0, 0), (5, 0)]
    for _ in range(n):
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if strict:
            if a == b: b = a + 1
            a, b = min(a, b), max(a, b)
        out.append((a, b))
    return out

def gen_lists(seed, n=800):
    r = random.Random(seed)
    ivs = gen_ivs(seed + 1, 200)
    out = [[(0, 1)], [(1, 2), (2, 3)], [(0, 5), (1, 2)], [(0, 1), (0, 1)]]
    for _ in range(n):
        out.append([r.choice(ivs) for _ in range(r.randint(1, 8))])
    return out

def pairs(seed, strict=True):
    ivs = gen_ivs(seed, 60, strict=strict)
    return [(a, b) for a in ivs for b in ivs]

@c.claim('I01')
def _(): return c.eq(overlaps((0, 5), (5, 10)), False)
@c.claim('I02')
def _(): return c.forall(pairs(2, False), lambda p: overlaps(*p) == overlaps(p[1], p[0]))
@c.claim('I03')
def _(): return c.eq(merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@c.claim('I04')
def _(): return c.eq(merge([(1, 2), (2, 3)]), [(1, 3)])
@c.claim('I05')
def _():
    def p(xs):
        m = merge(xs)
        return all(m[i][0] <= m[i+1][0] and not overlaps(m[i], m[i+1]) for i in range(len(m)-1))
    return c.forall(gen_lists(5), p)
@c.claim('I06')
def _(): return c.forall(gen_lists(6), lambda xs: merge(merge(xs)) == merge(xs))
@c.claim('I07')
def _(): return c.eq(contains((0, 5), 5), False)
@c.claim('I08')
def _(): return c.forall(gen_ivs(8), lambda a: contains(a, a[0]) is True)
@c.claim('I09')
def _(): return c.eq(intersect((0, 5), (3, 8)), (3, 5))
@c.claim('I10')
def _(): return c.eq(intersect((0, 2), (5, 6)), None)
@c.claim('I11')
def _(): return c.eq(intersect((0, 5), (5, 8)), None)
@c.claim('I12')
def _(): return c.eq(total_covered([(0, 5), (3, 8)]), 8)
@c.claim('I13')
def _(): return c.forall(gen_lists(13), lambda xs: total_covered(xs) <= sum(length(i) for i in xs))
@c.claim('I14')
def _():
    return c.forall([p for p in pairs(14) if overlaps(*p)],
                    lambda p: length(intersect(*p)) <= min(length(p[0]), length(p[1])))
@c.claim('I15')
def _(): return c.eq(merge([]), [])
@c.claim('I16')
def _(): return c.forall(gen_ivs(16), lambda a: overlaps(a, a) is True)
@c.claim('I17')
def _(): return c.eq(merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@c.claim('I18')
def _():
    r = random.Random(18)
    cases = [((0, 5), 5), ((0, 1), 1)] + [(a, x) for a in gen_ivs(18, 500) for x in (r.randint(-12, 12), a[0], a[1])]
    return c.forall(cases, lambda t: (not contains(*t)) or overlaps(t[0], (t[1], t[1] + 1)))
@c.claim('I19')
def _(): return c.eq(length((3, 1)), 0)
c.main()
