import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import intervals as V


def iv(r):  # any interval, possibly inverted/empty
    return (gen_int(r, -6, 6), gen_int(r, -6, 6))

def pv(r):  # proper interval start < end
    a = gen_int(r, -6, 6)
    return (a, a + r.randint(1, 6))

def pl(r):  # non-empty list of proper intervals
    return [pv(r) for _ in range(r.randint(1, 6))]

def ln(i): return i[1] - i[0]

@claim("I01")
def i01(): return eq(V.overlaps((0, 5), (5, 10)), False)
@claim("I02")
def i02(): return forall(lambda r: (iv(r), iv(r)), lambda a, b: V.overlaps(a, b) == V.overlaps(b, a))
@claim("I03")
def i03(): return eq(V.merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@claim("I04")
def i04(): return eq(V.merge([(1, 2), (2, 3)]), [(1, 3)])
@claim("I05")
def i05():
    def p(xs):
        m = V.merge(xs)
        return all(m[k][0] < m[k + 1][0] and not V.overlaps(m[k], m[k + 1]) for k in range(len(m) - 1))
    return forall(lambda r: (pl(r),), p)
@claim("I06")
def i06(): return forall(lambda r: (pl(r),), lambda xs: V.merge(V.merge(xs)) == V.merge(xs))
@claim("I07")
def i07(): return eq(V.contains((0, 5), 5), False)
@claim("I08")
def i08(): return forall(lambda r: (pv(r),), lambda a: V.contains(a, a[0]) is True)
@claim("I09")
def i09(): return eq(V.intersect((0, 5), (3, 8)), (3, 5))
@claim("I10")
def i10(): return eq(V.intersect((0, 2), (5, 6)), None)
@claim("I11")
def i11(): return eq(V.intersect((0, 5), (5, 8)), None)
@claim("I12")
def i12(): return eq(V.total_covered([(0, 5), (3, 8)]), 8)
@claim("I13")
def i13(): return forall(lambda r: (pl(r),), lambda xs: V.total_covered(xs) <= sum(ln(i) for i in xs))
@claim("I14")
def i14():
    def p(a, b):
        if not V.overlaps(a, b): return True
        return ln(V.intersect(a, b)) <= min(ln(a), ln(b))
    return forall(lambda r: (pv(r), pv(r)), p)
@claim("I15")
def i15(): return eq(V.merge([]), [])
@claim("I16")
def i16(): return forall(lambda r: (pv(r),), lambda a: V.overlaps(a, a) is True)
@claim("I17")
def i17(): return eq(V.merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@claim("I18")
def i18(): return forall(lambda r: (pv(r), gen_int(r, -8, 14)), lambda a, x: (not V.contains(a, x)) or V.overlaps(a, (x, x + 1)))
@claim("I19")
def i19(): return eq(V.length((3, 1)), 0)

if __name__ == "__main__":
    main("intervals")
