import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import Checker, rand_int
from kit.lists import *

c = Checker("lists")
def eq(a, b): return None if a == b else f"got {a!r}, expected {b!r}"
def ints(rng, m=12): return [rand_int(rng, -5, 9) for _ in range(rng.randint(0, m))]

c.fixed("L01", lambda: eq(chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]]))
c.prop("L02", lambda r: (ints(r), r.randint(1, 15)), lambda xs, k: flatten(chunk(xs, k)) == xs)
def l03():
    try: chunk([1, 2], 0)
    except ValueError: return None
    except Exception as e: return f"raised {type(e).__name__}"
    return "no exception"
c.fixed("L03", l03)
c.fixed("L04", lambda: eq(dedupe([3,1,3,2,1]), [3,1,2]))
def first_occ(xs):
    seen = []
    for x in xs:
        if x not in seen: seen.append(x)
    return seen
c.prop("L05", lambda r: (ints(r),), lambda xs: dedupe(xs) == first_occ(xs))
c.prop("L06", lambda r: (ints(r),), lambda xs: len(dedupe(xs)) == len(set(xs)))
c.fixed("L07", lambda: eq(flatten([[1,[2]],[3]]), [1,2,3]))
c.fixed("L08", lambda: eq(top_n([5,1,4], 2), [5,4]))
c.prop("L09", lambda r: (ints(r), r.randint(0, 15)), lambda xs, k: len(top_n(xs, k)) == min(k, len(xs)))
c.fixed("L10", lambda: eq(top_n([3,2,1], -1), []))
c.fixed("L11", lambda: eq(rotate([1,2,3], 1), [2,3,1]))
c.prop("L12", lambda r: (ints(r) or [1], r.randint(0, 20)), lambda xs, k: rotate(xs, k) == rotate(xs, k % len(xs)))
c.prop("L13", lambda r: (ints(r), r.randint(-20, 20)), lambda xs, k: len(rotate(xs, k)) == len(xs))
c.fixed("L14", lambda: eq(interleave([1,2,3], [9]), [1,9,2,3]))
c.prop("L15", lambda r: (ints(r), ints(r)), lambda a, b: len(interleave(a, b)) == 2*min(len(a), len(b)))
c.fixed("L16", lambda: eq(frequencies('abca'), {'a':2,'b':1,'c':1}))
c.prop("L17", lambda r: (ints(r),), lambda xs: sum(frequencies(xs).values()) == len(xs))
c.fixed("L18", lambda: eq(pairwise([1,2,3]), [(1,2),(2,3)]))
c.prop("L19", lambda r: (ints(r),), lambda xs: len(pairwise(xs)) == len(xs) - 1)
c.finish()
