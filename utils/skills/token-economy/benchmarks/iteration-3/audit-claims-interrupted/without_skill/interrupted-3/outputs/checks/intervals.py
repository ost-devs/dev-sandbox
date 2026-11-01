import os, sys, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.intervals import overlaps, length, contains, merge, intersect, total_covered

SEED = 20240607
N = 5000


def rint(r, lo=-10, hi=10):
    a = r.randint(lo, hi)
    b = r.randint(lo, hi)
    while a >= b:
        a = r.randint(lo, hi)
        b = r.randint(lo, hi)
    return (a, b)


def rany(r):
    return (r.randint(-10, 10), r.randint(-10, 10))


def rlist(r):
    return [rint(r) for _ in range(r.randint(1, 8))]


def pt(name, got, exp):
    if got == exp:
        return None
    return "%s -> %r (esperado %r)" % (name, got, exp)


def safe(f, desc):
    try:
        return f()
    except Exception as e:
        return ("EXC", desc, "%s: %s" % (type(e).__name__, e))


def pointwise(desc, call, exp):
    try:
        got = call()
    except Exception as e:
        return "%s -> exceção %s: %s" % (desc, type(e).__name__, e)
    return pt(desc, got, exp)


def universal(gen, pred, fmt, edge=()):
    r = random.Random(SEED)
    cases = list(edge) + [gen(r) for _ in range(N)]
    best = None
    for c in cases:
        try:
            ok, out = pred(c)
        except Exception as e:
            ok, out = False, "exceção %s: %s" % (type(e).__name__, e)
        if not ok:
            s = "%s -> %s" % (fmt(c), out)
            if best is None or len(repr(c)) < best[0]:
                best = (len(repr(c)), s)
    return best[1] if best else None


def c_I02():
    return universal(lambda r: (rany(r), rany(r)),
        lambda c: (overlaps(*c) == overlaps(c[1], c[0]), (overlaps(*c), overlaps(c[1], c[0]))),
        lambda c: "overlaps(a,b),overlaps(b,a) com a,b=%r" % (c,),
        edge=[((0, 0), (0, 0)), ((0, 5), (5, 10)), ((3, 1), (0, 5))])


def merged_ok(m):
    return all(m[i][0] <= m[i][1] for i in range(len(m))) and all(
        m[i][0] <= m[i + 1][0] and not overlaps(m[i], m[i + 1]) for i in range(len(m) - 1))


def c_I05():
    return universal(rlist, lambda xs: (lambda m: (merged_ok(m), m))(merge(xs)),
        lambda xs: "merge(%r)" % (xs,), edge=[[(0, 1)], [(1, 2), (2, 3)], [(1, 3), (2, 6)]])


def c_I06():
    return universal(rlist, lambda xs: (lambda m: (merge(m) == m, merge(m)))(merge(xs)),
        lambda xs: "merge(merge(%r))" % (xs,), edge=[[(0, 1)], [(1, 2), (2, 3)]])


def c_I08():
    return universal(rint, lambda a: (contains(a, a[0]) is True, contains(a, a[0])),
        lambda a: "contains(%r, %r)" % (a, a[0]), edge=[(0, 1)])


def c_I13():
    return universal(rlist,
        lambda xs: (total_covered(xs) <= sum(length(i) for i in xs), (total_covered(xs), sum(length(i) for i in xs))),
        lambda xs: "total_covered(%r)" % (xs,), edge=[[(0, 1)], [(0, 5), (3, 8)]])


def c_I14():
    def gen(r):
        while True:
            a, b = rint(r), rint(r)
            if overlaps(a, b):
                return (a, b)
    def pred(c):
        a, b = c
        i = intersect(a, b)
        return (length(i) <= min(length(a), length(b)), i)
    return universal(gen, pred, lambda c: "intersect%r" % (c,), edge=[((0, 5), (3, 8)), ((0, 5), (0, 5))])


def c_I16():
    return universal(rint, lambda a: (overlaps(a, a) is True, overlaps(a, a)),
        lambda a: "overlaps(%r, %r)" % (a, a), edge=[(0, 1)])


def c_I18():
    def pred(c):
        a, x = c
        if contains(a, x):
            o = overlaps(a, (x, x + 1))
            return (o is True, o)
        return (True, None)
    def gen(r):
        return (rint(r), r.randint(-12, 12))
    return universal(gen, pred, lambda c: "contains(%r,%r) implica overlaps(%r,%r)" % (c[0], c[1], c[0], (c[1], c[1] + 1)),
        edge=[((0, 5), 5), ((0, 5), 0), ((0, 5), 4)])


CLAIMS = {
 "I01": lambda: pointwise("overlaps((0,5),(5,10))", lambda: overlaps((0, 5), (5, 10)), False),
 "I02": c_I02,
 "I03": lambda: pointwise("merge([(1,3),(2,6),(8,10)])", lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)]),
 "I04": lambda: pointwise("merge([(1,2),(2,3)])", lambda: merge([(1, 2), (2, 3)]), [(1, 3)]),
 "I05": c_I05,
 "I06": c_I06,
 "I07": lambda: pointwise("contains((0,5),5)", lambda: contains((0, 5), 5), False),
 "I08": c_I08,
 "I09": lambda: pointwise("intersect((0,5),(3,8))", lambda: intersect((0, 5), (3, 8)), (3, 5)),
 "I10": lambda: pointwise("intersect((0,2),(5,6))", lambda: intersect((0, 2), (5, 6)), None),
 "I11": lambda: pointwise("intersect((0,5),(5,8))", lambda: intersect((0, 5), (5, 8)), None),
 "I12": lambda: pointwise("total_covered([(0,5),(3,8)])", lambda: total_covered([(0, 5), (3, 8)]), 8),
 "I13": c_I13,
 "I14": c_I14,
 "I15": lambda: pointwise("merge([])", lambda: merge([]), []),
 "I16": c_I16,
 "I17": lambda: pointwise("merge([(5,7),(1,2)])", lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)]),
 "I18": c_I18,
 "I19": lambda: pointwise("length((3,1))", lambda: length((3, 1)), 0),
}


def main():
    ids = sys.argv[1:] or sorted(CLAIMS)
    for i in ids:
        ce = CLAIMS[i]()
        print(json.dumps({"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce}, ensure_ascii=False))


if __name__ == "__main__":
    main()
