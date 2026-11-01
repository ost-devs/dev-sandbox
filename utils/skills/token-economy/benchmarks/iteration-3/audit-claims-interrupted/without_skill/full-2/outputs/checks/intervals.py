import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kit.intervals import overlaps, length, contains, merge, intersect, total_covered  # noqa: E402

SEED = 20240607

# Exhaustive domain: all intervals with 0 <= start < end <= 6 (valid), and all pairs 0..5 (any order)
VALID = [(s, e) for s in range(-2, 6) for e in range(s + 1, 7)]
ANY = [(s, e) for s in range(-2, 6) for e in range(-2, 6)]


def rand_lists(rng, n=3000, maxlen=8, lo=-20, hi=20):
    out = []
    for _ in range(n):
        k = rng.randint(1, maxlen)
        xs = []
        for _ in range(k):
            s = rng.randint(lo, hi)
            xs.append((s, s + rng.randint(1, 10)))
        out.append(xs)
    return out


def _call(f, *a):
    try:
        return f(*a)
    except Exception as e:  # noqa: BLE001
        return "EXC %s: %s" % (type(e).__name__, e)


def eq(cid, expr, got, exp):
    if got == exp and type(got) is type(exp):
        return True, None
    return False, "%s -> %r vs. esperado %r" % (expr, got, exp)


def check_I01():
    return eq("I01", "overlaps((0,5),(5,10))", _call(overlaps, (0, 5), (5, 10)), False)


def check_I02():
    for a in ANY:
        for b in ANY:
            x, y = _call(overlaps, a, b), _call(overlaps, b, a)
            if x != y:
                return False, "a=%r b=%r -> overlaps(a,b)=%r vs overlaps(b,a)=%r" % (a, b, x, y)
    return True, None


def check_I03():
    return eq("I03", "merge([(1,3),(2,6),(8,10)])", _call(merge, [(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])


def check_I04():
    return eq("I04", "merge([(1,2),(2,3)])", _call(merge, [(1, 2), (2, 3)]), [(1, 3)])


def check_I05():
    rng = random.Random(SEED)
    cases = rand_lists(rng) + [[(0, 1)], [(1, 2), (2, 3)], [(0, 5), (1, 2)], [(-3, -1), (-2, 0)]]
    for xs in cases:
        r = _call(merge, xs)
        if isinstance(r, str):
            return False, "merge(%r) -> %s" % (xs, r)
        ok = all(r[i][0] <= r[i + 1][0] for i in range(len(r) - 1)) and \
            not any(overlaps(r[i], r[j]) for i in range(len(r)) for j in range(i + 1, len(r)))
        if not ok:
            return False, "merge(%r) -> %r vs. esperado ordenado e sem sobreposicao" % (xs, r)
    return True, None


def check_I06():
    rng = random.Random(SEED)
    for xs in rand_lists(rng) + [[(0, 1)], [(1, 2), (2, 3)]]:
        m = _call(merge, xs)
        mm = _call(merge, m) if not isinstance(m, str) else m
        if m != mm:
            return False, "xs=%r -> merge(merge(xs))=%r vs merge(xs)=%r" % (xs, mm, m)
    return True, None


def check_I07():
    return eq("I07", "contains((0,5),5)", _call(contains, (0, 5), 5), False)


def check_I08():
    for a in VALID:
        r = _call(contains, a, a[0])
        if r is not True:
            return False, "contains(%r,%r) -> %r vs. True" % (a, a[0], r)
    return True, None


def check_I09():
    return eq("I09", "intersect((0,5),(3,8))", _call(intersect, (0, 5), (3, 8)), (3, 5))


def check_I10():
    return eq("I10", "intersect((0,2),(5,6))", _call(intersect, (0, 2), (5, 6)), None)


def check_I11():
    return eq("I11", "intersect((0,5),(5,8))", _call(intersect, (0, 5), (5, 8)), None)


def check_I12():
    return eq("I12", "total_covered([(0,5),(3,8)])", _call(total_covered, [(0, 5), (3, 8)]), 8)


def check_I13():
    rng = random.Random(SEED)
    for xs in rand_lists(rng) + [[(0, 1)], [(0, 5), (0, 5)]]:
        t = _call(total_covered, xs)
        s = sum(length(i) for i in xs)
        if isinstance(t, str) or not t <= s:
            return False, "total_covered(%r) -> %r vs. <= %r" % (xs, t, s)
    return True, None


def check_I14():
    for a in VALID:
        for b in VALID:
            if overlaps(a, b):
                r = _call(intersect, a, b)
                if isinstance(r, str) or r is None:
                    return False, "intersect(%r,%r) -> %r" % (a, b, r)
                if not length(r) <= min(length(a), length(b)):
                    return False, "intersect(%r,%r) -> %r, length %r > min" % (a, b, r, length(r))
    return True, None


def check_I15():
    return eq("I15", "merge([])", _call(merge, []), [])


def check_I16():
    for a in VALID:
        r = _call(overlaps, a, a)
        if r is not True:
            return False, "overlaps(%r,%r) -> %r vs. True" % (a, a, r)
    return True, None


def check_I17():
    return eq("I17", "merge([(5,7),(1,2)])", _call(merge, [(5, 7), (1, 2)]), [(1, 2), (5, 7)])


def check_I18():
    for a in VALID:
        for x in range(-4, 9):
            if contains(a, x) and not overlaps(a, (x, x + 1)):
                return False, "a=%r x=%r -> contains=True, overlaps(a,(x,x+1))=%r vs. True" % (a, x, overlaps(a, (x, x + 1)))
    return True, None


def check_I19():
    return eq("I19", "length((3,1))", _call(length, (3, 1)), 0)


def main():
    ids = ["I%02d" % i for i in range(1, 20)]
    sel = sys.argv[1:] or ids
    for i in sel:
        try:
            ok, msg = globals()["check_" + i]()
        except Exception as e:  # noqa: BLE001
            ok, msg = False, "excecao: %s: %s" % (type(e).__name__, e)
        print("%s\t%s\t%s" % (i, "verdadeira" if ok else "falsa", "" if ok else (msg or "").replace("\n", " ")))


if __name__ == "__main__":
    main()
