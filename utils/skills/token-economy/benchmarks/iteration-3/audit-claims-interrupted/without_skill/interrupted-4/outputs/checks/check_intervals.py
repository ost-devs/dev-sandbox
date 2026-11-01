import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.intervals import *

SEED = 20261101
N = 20000


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def rint(rng, strict=True, lo=-10, hi=10):
    a = rng.randint(lo, hi)
    b = rng.randint(lo, hi)
    if strict:
        if a == b:
            b = a + 1
        if a > b:
            a, b = b, a
    return (a, b)


def rlist(rng):
    return [rint(rng) for _ in range(rng.randint(1, 8))]


def I01(): return eq(lambda: overlaps((0, 5), (5, 10)), False)


def I02():
    rng = random.Random(SEED)
    fixed = [((0, 5), (5, 10)), ((3, 1), (0, 5)), ((0, 0), (0, 0)), ((1.5, 2.5), (2, 3))]
    cases = fixed + [(rint(rng, False), rint(rng, False)) for _ in range(N)]
    for a, b in cases:
        try:
            x, y = overlaps(a, b), overlaps(b, a)
        except Exception as e:
            return False, f'a={a!r}, b={b!r}: raised {e!r}'
        if x != y:
            return False, f'a={a!r}, b={b!r}: overlaps(a,b)={x!r}, overlaps(b,a)={y!r}'
    return True, None


def I03(): return eq(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
def I04(): return eq(lambda: merge([(1, 2), (2, 3)]), [(1, 3)])


def I05():
    rng = random.Random(SEED)
    cases = [[(1, 2), (2, 3)], [(0, 1)], [(0, 10), (2, 3)]] + [rlist(rng) for _ in range(N)]
    for xs in cases:
        try:
            m = merge(xs)
        except Exception as e:
            return False, f'xs={xs!r}: raised {e!r}'
        for i in range(len(m) - 1):
            if not m[i][0] <= m[i + 1][0] or overlaps(m[i], m[i + 1]):
                return False, f'xs={xs!r}: merge={m!r}'
    return True, None


def I06():
    rng = random.Random(SEED)
    cases = [[(1, 2), (2, 3)], [(0, 1)]] + [rlist(rng) for _ in range(N)]
    for xs in cases:
        try:
            m = merge(xs)
            m2 = merge(m)
        except Exception as e:
            return False, f'xs={xs!r}: raised {e!r}'
        if m2 != m:
            return False, f'xs={xs!r}: merge={m!r}, merge(merge)={m2!r}'
    return True, None


def I07(): return eq(lambda: contains((0, 5), 5), False)


def I08():
    rng = random.Random(SEED)
    for a in [(0, 5), (-3, -2)] + [rint(rng) for _ in range(N)]:
        if contains(a, a[0]) is not True:
            return False, f'a={a!r}: contains(a, a[0])={contains(a, a[0])!r}'
    return True, None


def I09(): return eq(lambda: intersect((0, 5), (3, 8)), (3, 5))
def I10(): return eq(lambda: intersect((0, 2), (5, 6)), None)
def I11(): return eq(lambda: intersect((0, 5), (5, 8)), None)
def I12(): return eq(lambda: total_covered([(0, 5), (3, 8)]), 8)


def I13():
    rng = random.Random(SEED)
    for xs in [[(0, 5), (3, 8)], [(0, 1)]] + [rlist(rng) for _ in range(N)]:
        try:
            t = total_covered(xs)
        except Exception as e:
            return False, f'xs={xs!r}: raised {e!r}'
        s = sum(length(i) for i in xs)
        if not t <= s:
            return False, f'xs={xs!r}: total_covered={t!r} > sum={s!r}'
    return True, None


def I14():
    rng = random.Random(SEED)
    for a, b in [((0, 5), (3, 8))] + [(rint(rng), rint(rng)) for _ in range(N)]:
        if not overlaps(a, b):
            continue
        try:
            r = intersect(a, b)
            l = length(r)
        except Exception as e:
            return False, f'a={a!r}, b={b!r}: raised {e!r}'
        if not l <= min(length(a), length(b)):
            return False, f'a={a!r}, b={b!r}: intersect={r!r}'
    return True, None


def I15(): return eq(lambda: merge([]), [])


def I16():
    rng = random.Random(SEED)
    for a in [(0, 5)] + [rint(rng) for _ in range(N)]:
        if overlaps(a, a) is not True:
            return False, f'a={a!r}: overlaps(a, a)={overlaps(a, a)!r}'
    return True, None


def I17(): return eq(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])


def I18():
    rng = random.Random(SEED)
    fixed = [((0, 5), 5), ((0, 5), 0), ((0, 5), 2)]
    cases = fixed + [(rint(rng), rng.randint(-12, 12)) for _ in range(N)]
    for a, x in cases:
        if contains(a, x) and not overlaps(a, (x, x + 1)):
            return False, f'a={a!r}, x={x!r}: contains=True, overlaps(a, (x, x+1))={overlaps(a, (x, x + 1))!r}'
    return True, None


def I19(): return eq(lambda: length((3, 1)), 0)


CHECKS = {f'I{i:02d}': globals()[f'I{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        try:
            ok, ce = CHECKS[i]()
        except Exception as e:
            ok, ce = False, f'check raised {e!r}'
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa', 'counterexample': ce,
                          'command': f'python3 checks/check_intervals.py {i}'}, ensure_ascii=False))
