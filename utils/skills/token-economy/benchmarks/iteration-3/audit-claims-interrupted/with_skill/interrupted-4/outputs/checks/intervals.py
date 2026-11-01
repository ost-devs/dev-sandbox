from lib import ints, first_fail, eq, rng, N
from kit.intervals import *


def ivs(tag, n=N, proper=True):
    """Intervals (a, b) of ints; proper => a < b, else any order."""
    r = rng(tag)
    for a in range(-3, 4):
        for b in range(-3, 4):
            if not proper or a < b:
                yield (a, b)
    for _ in range(n):
        a, b = r.randint(-20, 20), r.randint(-20, 20)
        if proper and a >= b:
            continue
        yield (a, b)


def pairs(tag, proper=True):
    r = rng(tag)
    base = list(ivs(tag + 'x', 80, proper))
    for a in base:
        for b in base:
            yield (a, b)


def lists(tag, n=N):
    r = rng(tag)
    for _ in range(n):
        yield [(a, a + r.randint(1, 8)) for a in (r.randint(-20, 20) for _ in range(r.randint(1, 8)))]
    for L in ([(0, 1)], [(0, 5), (5, 10)], [(1, 2), (2, 3), (3, 4)], [(0, 10), (2, 3)]):
        yield L


def sorted_disjoint(m):
    return all(m[i][0] < m[i][1] for i in range(len(m))) and \
        all(m[i][0] < m[i + 1][0] and not overlaps(m[i], m[i + 1]) for i in range(len(m) - 1))


CHECKS = {
    'I01': lambda: eq(lambda: overlaps((0, 5), (5, 10)), False, 'overlaps((0,5),(5,10))'),
    'I02': lambda: first_fail(pairs('i2', proper=False), lambda p: overlaps(*p) == overlaps(p[1], p[0])),
    'I03': lambda: eq(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)], 'merge I03'),
    'I04': lambda: eq(lambda: merge([(1, 2), (2, 3)]), [(1, 3)], 'merge I04'),
    'I05': lambda: first_fail(lists('i5'), lambda L: sorted_disjoint(merge(L))),
    'I06': lambda: first_fail(lists('i6'), lambda L: merge(merge(L)) == merge(L)),
    'I07': lambda: eq(lambda: contains((0, 5), 5), False, 'contains((0,5),5)'),
    'I08': lambda: first_fail(ivs('i8'), lambda a: contains(a, a[0]) is True),
    'I09': lambda: eq(lambda: intersect((0, 5), (3, 8)), (3, 5), 'intersect I09'),
    'I10': lambda: eq(lambda: intersect((0, 2), (5, 6)), None, 'intersect I10'),
    'I11': lambda: eq(lambda: intersect((0, 5), (5, 8)), None, 'intersect I11'),
    'I12': lambda: eq(lambda: total_covered([(0, 5), (3, 8)]), 8, 'total_covered I12'),
    'I13': lambda: first_fail(lists('i13'), lambda L: total_covered(L) <= sum(length(i) for i in L)),
    'I14': lambda: first_fail(((a, b) for a, b in pairs('i14') if overlaps(a, b)),
                              lambda p: length(intersect(*p)) <= min(length(p[0]), length(p[1]))),
    'I15': lambda: eq(lambda: merge([]), [], 'merge([])'),
    'I16': lambda: first_fail(ivs('i16'), lambda a: overlaps(a, a) is True),
    'I17': lambda: eq(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)], 'merge I17'),
    'I18': lambda: first_fail(((a, x) for a in ivs('i18', proper=False) for x in range(-22, 23)),
                              lambda p: (not contains(*p)) or overlaps(p[0], (p[1], p[1] + 1))),
    'I19': lambda: eq(lambda: length((3, 1)), 0, 'length((3,1))'),
}
