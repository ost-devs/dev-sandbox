from lib import strings, ints, int_lists, first_fail, eq
from kit.lists import *


def chunk_cases(tag):
    for xs in int_lists(tag, n=500):
        for k in range(1, 10):
            yield (xs, k)
    for k in range(1, 5):
        yield ([], k)


def topn_cases(tag):
    for xs in int_lists(tag, n=500):
        for k in range(0, 12):
            yield (xs, k)
    for k in range(0, 3):
        yield ([], k)


def rot_cases(tag, neg=False, nonempty=False):
    for xs in int_lists(tag, n=500, min_len=1 if nonempty else 0):
        for k in range(-10 if neg else 0, 20):
            yield (xs, k)
    if not nonempty:
        yield ([], 0)
        yield ([], 3)


def first_occ(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def two_lists(tag):
    a = list(int_lists(tag + 'a', n=400))
    b = list(int_lists(tag + 'b', n=400))
    yield from zip(a, b)
    yield ([], [])
    yield ([], [1])
    yield ([1], [])


CHECKS = {
    'L01': lambda: eq(lambda: chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]], 'chunk(range(7),3)'),
    'L02': lambda: first_fail(chunk_cases('l2'), lambda p: flatten(chunk(*p)) == p[0]),
    'L03': lambda: first_fail([[], [1], [1, 2, 3]], lambda xs: _raises(lambda: chunk(xs, 0), ValueError)),
    'L04': lambda: eq(lambda: dedupe([3, 1, 3, 2, 1]), [3, 1, 2], 'dedupe'),
    'L05': lambda: first_fail(int_lists('l5', n=2000), lambda xs: dedupe(xs) == first_occ(xs)),
    'L06': lambda: first_fail(int_lists('l6', n=2000), lambda xs: len(dedupe(xs)) == len(set(xs))),
    'L07': lambda: eq(lambda: flatten([[1, [2]], [3]]), [1, 2, 3], 'flatten([[1,[2]],[3]])'),
    'L08': lambda: eq(lambda: top_n([5, 1, 4], 2), [5, 4], 'top_n([5,1,4],2)'),
    'L09': lambda: first_fail(topn_cases('l9'), lambda p: len(top_n(*p)) == min(p[1], len(p[0]))),
    'L10': lambda: eq(lambda: top_n([3, 2, 1], -1), [], 'top_n([3,2,1],-1)'),
    'L11': lambda: eq(lambda: rotate([1, 2, 3], 1), [2, 3, 1], 'rotate([1,2,3],1)'),
    'L12': lambda: first_fail(rot_cases('l12', nonempty=True), lambda p: rotate(*p) == rotate(p[0], p[1] % len(p[0]))),
    'L13': lambda: first_fail(rot_cases('l13', neg=True), lambda p: len(rotate(*p)) == len(p[0])),
    'L14': lambda: eq(lambda: interleave([1, 2, 3], [9]), [1, 9, 2, 3], 'interleave([1,2,3],[9])'),
    'L15': lambda: first_fail(two_lists('l15'), lambda p: len(interleave(*p)) == 2 * min(len(p[0]), len(p[1]))),
    'L16': lambda: eq(lambda: frequencies('abca'), {'a': 2, 'b': 1, 'c': 1}, "frequencies('abca')"),
    'L17': lambda: first_fail(int_lists('l17', n=2000), lambda xs: sum(frequencies(xs).values()) == len(xs)),
    'L18': lambda: eq(lambda: pairwise([1, 2, 3]), [(1, 2), (2, 3)], 'pairwise([1,2,3])'),
    'L19': lambda: first_fail(list(int_lists('l19', n=2000)) + [[]], lambda xs: len(pairwise(xs)) == len(xs) - 1),
}


def _raises(f, exc):
    try:
        f()
    except exc:
        return True
    return False
