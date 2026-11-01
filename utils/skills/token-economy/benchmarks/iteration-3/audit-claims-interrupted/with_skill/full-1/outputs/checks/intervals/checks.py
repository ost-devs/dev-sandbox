import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, main
from kit.intervals import *

def rint(r, lo=-20, hi=20):
    a = r.randint(lo, hi); b = r.randint(lo, hi)
    return (a, b)
def valid(r):
    a = r.randint(-20, 20); return (a, a + r.randint(1, 15))
def vlist(r):
    return [valid(r) for _ in range(r.randint(1, 8))]
def eq(cid, expr_val, expected, label):
    if expr_val != expected:
        return f"{label} = {expr_val!r}, expected {expected!r}"

def ex(cid, f, expected, label):
    try:
        v = f()
    except Exception as e:
        return f"{label} raised {type(e).__name__}: {e}"
    return eq(cid, v, expected, label)

@claim("I01")
def i01(): return ex("I01", lambda: overlaps((0, 5), (5, 10)), False, "overlaps((0,5),(5,10))")
@claim("I02")
def i02():
    r = rng("I02")
    pairs = [((3, 1), (0, 5)), ((0, 0), (0, 0)), ((0, 5), (5, 10))] + [(rint(r), rint(r)) for _ in range(5000)]
    for a, b in pairs:
        if overlaps(a, b) != overlaps(b, a):
            return f"overlaps({a},{b})={overlaps(a,b)} but overlaps({b},{a})={overlaps(b,a)}"
@claim("I03")
def i03(): return ex("I03", lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)], "merge")
@claim("I04")
def i04(): return ex("I04", lambda: merge([(1, 2), (2, 3)]), [(1, 3)], "merge([(1,2),(2,3)])")
@claim("I05")
def i05():
    r = rng("I05")
    for xs in [[(0, 1)]] + [vlist(r) for _ in range(5000)]:
        try: m = merge(xs)
        except Exception as e: return f"merge({xs}) raised {e!r}"
        if m != sorted(m) or any(overlaps(m[i], m[i+1]) for i in range(len(m)-1)):
            return f"merge({xs}) = {m}"
@claim("I06")
def i06():
    r = rng("I06")
    for xs in [[(0, 1)]] + [vlist(r) for _ in range(5000)]:
        m = merge(xs)
        if merge(m) != m: return f"merge({xs})={m}, merge again={merge(m)}"
@claim("I07")
def i07(): return ex("I07", lambda: contains((0, 5), 5), False, "contains((0,5),5)")
@claim("I08")
def i08():
    r = rng("I08")
    for a in [(0, 1)] + [valid(r) for _ in range(3000)]:
        if contains(a, a[0]) is not True: return f"contains({a},{a[0]})={contains(a,a[0])}"
@claim("I09")
def i09(): return ex("I09", lambda: intersect((0, 5), (3, 8)), (3, 5), "intersect")
@claim("I10")
def i10(): return ex("I10", lambda: intersect((0, 2), (5, 6)), None, "intersect")
@claim("I11")
def i11(): return ex("I11", lambda: intersect((0, 5), (5, 8)), None, "intersect")
@claim("I12")
def i12(): return ex("I12", lambda: total_covered([(0, 5), (3, 8)]), 8, "total_covered")
@claim("I13")
def i13():
    r = rng("I13")
    for xs in [[(0, 1)]] + [vlist(r) for _ in range(5000)]:
        t = total_covered(xs); s = sum(length(i) for i in xs)
        if t > s: return f"total_covered({xs})={t} > {s}"
@claim("I14")
def i14():
    r = rng("I14")
    for _ in range(5000):
        a, b = valid(r), valid(r)
        if overlaps(a, b):
            i = intersect(a, b)
            if length(i) > min(length(a), length(b)): return f"a={a} b={b} intersect={i}"
@claim("I15")
def i15(): return ex("I15", lambda: merge([]), [], "merge([])")
@claim("I16")
def i16():
    r = rng("I16")
    for a in [(0, 1)] + [valid(r) for _ in range(3000)]:
        if overlaps(a, a) is not True: return f"overlaps({a},{a})={overlaps(a,a)}"
@claim("I17")
def i17(): return ex("I17", lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)], "merge")
@claim("I18")
def i18():
    r = rng("I18")
    cases = [((0, 5), 5), ((0, 5), 0)] + [(rint(r), r.randint(-25, 25)) for _ in range(5000)]
    for a, x in cases:
        if contains(a, x) and not overlaps(a, (x, x + 1)):
            return f"contains({a},{x})=True but overlaps({a},({x},{x+1}))=False"
@claim("I19")
def i19(): return ex("I19", lambda: length((3, 1)), 0, "length((3,1))")

if __name__ == "__main__":
    main()
