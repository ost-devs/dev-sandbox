import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.intervals import overlaps, length, contains, merge, intersect, total_covered

CMD = "python3 -I checks/intervals.py"
rng = random.Random(12345)
G = range(-3, 6)
ALL = [(a, b) for a in G for b in G]          # includes empty and inverted
PROPER = [(a, b) for a, b in ALL if a < b]
lists = [[rng.choice(PROPER) for _ in range(rng.randint(1, 5))] for _ in range(400)]
lists += [[(1, 3)], [(1, 2), (2, 3)], [(0, 10), (2, 3)], [(2, 3), (0, 10)], [(0, 1), (0, 1)]]
lists += [[a, b] for a in PROPER[:30] for b in PROPER[:30]]

def first_fail(cases, pred):
    for c in cases:
        try:
            r = pred(c)
            if r is not True:
                return r if isinstance(r, str) else repr(c)
        except Exception as e:
            return "%r raised %r" % (c, e)
    return ""

def eq(expr_fn, expected):
    def run():
        try:
            r = expr_fn()
        except Exception as e:
            return "raised %r" % (e,)
        return "" if r == expected else "got %r, expected %r" % (r, expected)
    return run

def overlap_free_sorted(xs):
    m = merge(xs)
    if [i[0] for i in m] != sorted(i[0] for i in m): return "unsorted: %r -> %r" % (xs, m)
    for p, q in itertools.combinations(m, 2):
        if overlaps(p, q): return "overlap: %r -> %r" % (xs, m)
    return True

def rep(f):
    def w(c):
        r = f(c)
        return r
    return w

res = {}
res["I01"] = eq(lambda: overlaps((0, 5), (5, 10)), False)()
res["I02"] = first_fail(itertools.product(ALL, ALL), lambda p: overlaps(*p) == overlaps(p[1], p[0]) or "overlaps(%r,%r)=%r vs %r" % (p[0], p[1], overlaps(*p), overlaps(p[1], p[0])))
res["I03"] = eq(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])()
res["I04"] = eq(lambda: merge([(1, 2), (2, 3)]), [(1, 3)])()
res["I05"] = first_fail(lists, overlap_free_sorted)
res["I06"] = first_fail(lists, lambda xs: merge(merge(xs)) == merge(xs) or "%r: %r vs %r" % (xs, merge(merge(xs)), merge(xs)))
res["I07"] = eq(lambda: contains((0, 5), 5), False)()
res["I08"] = first_fail(PROPER, lambda a: contains(a, a[0]) is True or "contains(%r,%r)=%r" % (a, a[0], contains(a, a[0])))
res["I09"] = eq(lambda: intersect((0, 5), (3, 8)), (3, 5))()
res["I10"] = eq(lambda: intersect((0, 2), (5, 6)), None)()
res["I11"] = eq(lambda: intersect((0, 5), (5, 8)), None)()
res["I12"] = eq(lambda: total_covered([(0, 5), (3, 8)]), 8)()
res["I13"] = first_fail(lists, lambda xs: total_covered(xs) <= sum(length(i) for i in xs) or "%r: %r > %r" % (xs, total_covered(xs), sum(length(i) for i in xs)))
def i14(p):
    a, b = p
    if not overlaps(a, b): return True
    r = intersect(a, b)
    return length(r) <= min(length(a), length(b)) or "intersect(%r,%r)=%r" % (a, b, r)
res["I14"] = first_fail(itertools.product(PROPER, PROPER), i14)
res["I15"] = eq(lambda: merge([]), [])()
res["I16"] = first_fail(PROPER, lambda a: overlaps(a, a) is True or "overlaps(%r,%r)=False" % (a, a))
res["I17"] = eq(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])()
def i18(p):
    a, x = p
    if contains(a, x) and not overlaps(a, (x, x + 1)):
        return "contains(%r,%r)=True but overlaps(%r,%r)=False" % (a, x, a, (x, x + 1))
    return True
res["I18"] = first_fail(itertools.product(ALL, range(-4, 8)), i18)
res["I19"] = eq(lambda: length((3, 1)), 0)()

for k in sorted(res):
    v = res[k]
    print("%s\t%s\t%s\t%s" % (k, "falsa" if v else "verdadeira", v, CMD))
