import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.intervals import *

def iv(r, strict=True, lo=-10, hi=10):
    a = r.randint(lo, hi); b = r.randint(lo, hi)
    if r.random() < 0.05: a, b = a * 1000, b * 1000
    if strict:
        if a == b: b = a + 1
        if a > b: a, b = b, a
    return (a, b)

def ivs(r, strict=True, minlen=1):
    return [iv(r, strict) for _ in range(r.randint(minlen, 8))]

def eq(actual, expected):
    if actual != expected: raise Counter(f"actual={actual!r} expected={expected!r}")

@claim("I01")
def i01(): eq(overlaps((0, 5), (5, 10)), False)
@claim("I02")
def i02(): forall("I02", lambda r: (iv(r, False), iv(r, False)), lambda a, b: overlaps(a, b) == overlaps(b, a))
@claim("I03")
def i03(): eq(merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@claim("I04")
def i04(): eq(merge([(1, 2), (2, 3)]), [(1, 3)])
@claim("I05")
def i05():
    def p(xs):
        m = merge(xs)
        return all(m[i][0] <= m[i+1][0] for i in range(len(m)-1)) and not any(overlaps(m[i], m[j]) for i in range(len(m)) for j in range(i+1, len(m)))
    forall("I05", lambda r: (ivs(r),), p)
@claim("I06")
def i06(): forall("I06", lambda r: (ivs(r),), lambda xs: merge(merge(xs)) == merge(xs))
@claim("I07")
def i07(): eq(contains((0, 5), 5), False)
@claim("I08")
def i08(): forall("I08", lambda r: (iv(r),), lambda a: contains(a, a[0]) is True)
@claim("I09")
def i09(): eq(intersect((0, 5), (3, 8)), (3, 5))
@claim("I10")
def i10(): eq(intersect((0, 2), (5, 6)), None)
@claim("I11")
def i11(): eq(intersect((0, 5), (5, 8)), None)
@claim("I12")
def i12(): eq(total_covered([(0, 5), (3, 8)]), 8)
@claim("I13")
def i13(): forall("I13", lambda r: (ivs(r),), lambda xs: total_covered(xs) <= sum(length(i) for i in xs))
@claim("I14")
def i14():
    def p(a, b):
        if not overlaps(a, b): return True
        return length(intersect(a, b)) <= min(length(a), length(b))
    forall("I14", lambda r: (iv(r), iv(r)), p)
@claim("I15")
def i15(): eq(merge([]), [])
@claim("I16")
def i16(): forall("I16", lambda r: (iv(r),), lambda a: overlaps(a, a) is True)
@claim("I17")
def i17(): eq(merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@claim("I18")
def i18(): forall("I18", lambda r: (iv(r), r.randint(-12, 12)), lambda a, x: (not contains(a, x)) or overlaps(a, (x, x + 1)))
@claim("I19")
def i19(): eq(length((3, 1)), 0)

if __name__=='__main__': main('intervals')
