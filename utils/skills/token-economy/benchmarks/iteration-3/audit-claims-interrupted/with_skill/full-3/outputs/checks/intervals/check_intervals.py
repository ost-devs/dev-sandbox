import os, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(D))
from lib import Checker
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(D)), "kit"))
from intervals import *

c = Checker("intervals")
def eq(got, exp): return None if got == exp else f"got {got!r}, expected {exp!r}"
def iv(rng, strict=True):
    a = rng.randint(-10, 20); b = rng.randint(-10, 20)
    if strict:
        if a == b: b += 1
        return (min(a, b), max(a, b))
    return (a, b)
def lst(rng):
    return ([iv(rng) for _ in range(rng.randint(1, 8))],)

c.fixed("I01", lambda: eq(overlaps((0, 5), (5, 10)), False))
c.prop("I02", lambda r: (iv(r, False), iv(r, False)), lambda a, b: overlaps(a, b) == overlaps(b, a))
c.fixed("I03", lambda: eq(merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)]))
c.fixed("I04", lambda: eq(merge([(1, 2), (2, 3)]), [(1, 3)]))
def i05(xs):
    m = merge(xs)
    return all(m[i][0] <= m[i+1][0] and not overlaps(m[i], m[i+1]) for i in range(len(m)-1))
c.prop("I05", lst, i05)
c.prop("I06", lst, lambda xs: merge(merge(xs)) == merge(xs))
c.fixed("I07", lambda: eq(contains((0, 5), 5), False))
c.prop("I08", lambda r: (iv(r),), lambda a: contains(a, a[0]) is True)
c.fixed("I09", lambda: eq(intersect((0, 5), (3, 8)), (3, 5)))
c.fixed("I10", lambda: eq(intersect((0, 2), (5, 6)), None))
c.fixed("I11", lambda: eq(intersect((0, 5), (5, 8)), None))
c.fixed("I12", lambda: eq(total_covered([(0, 5), (3, 8)]), 8))
c.prop("I13", lst, lambda xs: total_covered(xs) <= sum(length(i) for i in xs))
c.prop("I14", lambda r: (iv(r), iv(r)),
       lambda a, b: (not overlaps(a, b)) or length(intersect(a, b)) <= min(length(a), length(b)))
c.fixed("I15", lambda: eq(merge([]), []))
c.prop("I16", lambda r: (iv(r),), lambda a: overlaps(a, a) is True)
c.fixed("I17", lambda: eq(merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)]))
c.prop("I18", lambda r: (iv(r), r.randint(-10, 20)),
       lambda a, x: (not contains(a, x)) or overlaps(a, (x, x + 1)))
c.fixed("I19", lambda: eq(length((3, 1)), 0))
c.finish()
