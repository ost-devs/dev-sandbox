import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.intervals import overlaps, length, contains, merge, intersect, total_covered

SEED = 12345
N = 3000


def rnd_iv(r, strict=True):
    while True:
        a, b = r.randint(-20, 20), r.randint(-20, 20)
        if not strict or a < b:
            return (a, b)


def rnd_list(r):
    return [rnd_iv(r) for _ in range(r.randint(1, 6))]


def eq(expr_fn, expected):
    try:
        got = expr_fn()
    except Exception as e:
        got = "%s: %s" % (type(e).__name__, e)
    return got == expected, got


def fixed(label, fn, expected):
    ok, got = eq(fn, expected)
    return (True, None) if ok else (False, "%s -> %r, esperado %r" % (label, got, expected))


def check_I01(): return fixed("overlaps((0, 5), (5, 10))", lambda: overlaps((0, 5), (5, 10)), False)
def check_I03(): return fixed("merge([(1, 3), (2, 6), (8, 10)])", lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
def check_I04(): return fixed("merge([(1, 2), (2, 3)])", lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
def check_I07(): return fixed("contains((0, 5), 5)", lambda: contains((0, 5), 5), False)
def check_I09(): return fixed("intersect((0, 5), (3, 8))", lambda: intersect((0, 5), (3, 8)), (3, 5))
def check_I10(): return fixed("intersect((0, 2), (5, 6))", lambda: intersect((0, 2), (5, 6)), None)
def check_I11(): return fixed("intersect((0, 5), (5, 8))", lambda: intersect((0, 5), (5, 8)), None)
def check_I12(): return fixed("total_covered([(0, 5), (3, 8)])", lambda: total_covered([(0, 5), (3, 8)]), 8)
def check_I15(): return fixed("merge([])", lambda: merge([]), [])
def check_I17(): return fixed("merge([(5, 7), (1, 2)])", lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
def check_I19(): return fixed("length((3, 1))", lambda: length((3, 1)), 0)


def check_I02():
    r = random.Random(SEED)
    for _ in range(N):
        a, b = rnd_iv(r, False), rnd_iv(r, False)
        if overlaps(a, b) != overlaps(b, a):
            return False, "a=%r b=%r" % (a, b)
    return True, None


def check_I05():
    r = random.Random(SEED)
    for _ in range(N):
        xs = rnd_list(r)
        m = merge(xs)
        for i in range(len(m) - 1):
            if not (m[i][0] <= m[i + 1][0]) or overlaps(m[i], m[i + 1]):
                return False, "xs=%r merge=%r" % (xs, m)
    return True, None


def check_I06():
    r = random.Random(SEED)
    for _ in range(N):
        xs = rnd_list(r)
        if merge(merge(xs)) != merge(xs):
            return False, "xs=%r" % (xs,)
    return True, None


def check_I08():
    r = random.Random(SEED)
    for _ in range(N):
        a = rnd_iv(r)
        if contains(a, a[0]) is not True:
            return False, "a=%r" % (a,)
    return True, None


def check_I13():
    r = random.Random(SEED)
    for _ in range(N):
        xs = rnd_list(r)
        if total_covered(xs) > sum(length(i) for i in xs):
            return False, "xs=%r" % (xs,)
    return True, None


def check_I14():
    r = random.Random(SEED)
    for _ in range(N):
        a, b = rnd_iv(r), rnd_iv(r)
        if overlaps(a, b):
            i = intersect(a, b)
            if length(i) > min(length(a), length(b)):
                return False, "a=%r b=%r" % (a, b)
    return True, None


def check_I16():
    r = random.Random(SEED)
    for _ in range(N):
        a = rnd_iv(r)
        if overlaps(a, a) is not True:
            return False, "a=%r" % (a,)
    return True, None


def check_I18():
    r = random.Random(SEED)
    cases = [((0, 5), 5)] + [(rnd_iv(r), r.randint(-22, 22)) for _ in range(N)]
    for a, x in cases:
        if contains(a, x) and not overlaps(a, (x, x + 1)):
            return False, "a=%r x=%r" % (a, x)
    return True, None


def main():
    ids = sys.argv[1:] or ["I%02d" % i for i in range(1, 20)]
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce,
                          "command": "python3 -I checks/intervals.py " + i}, ensure_ascii=False))


main()
