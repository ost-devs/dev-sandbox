from lib import ints, int_lists, first_fail, eq
from kit.numbers import *


def _pairs(tag, lo=-50, hi=50):
    for a in range(lo, hi + 1):
        for b in range(lo, hi + 1):
            yield (a, b)


def n01():
    import itertools
    cases = ((x, lo, hi) for x in ints('n1x', lo=-100, hi=100)
             for lo, hi in [(-5, 5), (0, 0), (-3, 10), (7, 7), (-20, -10)])
    return first_fail(cases, lambda c: c[1] <= clamp(*c) <= c[2])


def n07():
    return first_fail((l for l in int_lists('n7', min_len=1)), lambda l: median(l) == median(sorted(l)))


def n11():
    return first_fail([(x,) for x in [0, 1, -1, 5, 2.5, 100]],
                      lambda c: percent(c[0], 0) == 0.0 and isinstance(percent(c[0], 0), float))


def n12():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, n))
    return first_fail(range(0, 1001), lambda n: is_prime(n) == ref(n))


def n19():
    return first_fail(list(ints('n19', lo=-1000, hi=1000)) + [10**20, -10**20],
                      lambda n: isinstance(digits_sum(n), int) and digits_sum(n) >= 0)


CHECKS = {
    'N01': n01,
    'N02': lambda: eq(lambda: clamp(5, 10, 0), 0, 'clamp(5,10,0)'),
    'N03': lambda: eq(lambda: mean([]), 0, 'mean([])'),
    'N04': lambda: eq(lambda: mean([1, 2]), 1.5, 'mean([1,2])'),
    'N05': lambda: eq(lambda: median([3, 1, 2]), 2, 'median([3,1,2])'),
    'N06': lambda: eq(lambda: median([]), None, 'median([])'),
    'N07': n07,
    'N08': lambda: eq(lambda: round_half(2.5), 3, 'round_half(2.5)'),
    'N09': lambda: eq(lambda: round_half(3.5), 4, 'round_half(3.5)'),
    'N10': lambda: eq(lambda: percent(1, 3), 33.3, 'percent(1,3)'),
    'N11': n11,
    'N12': n12,
    'N13': lambda: eq(lambda: is_prime(97), True, 'is_prime(97)'),
    'N14': lambda: eq(lambda: is_prime(2), True, 'is_prime(2)'),
    'N15': lambda: first_fail(_pairs('n15'), lambda p: gcd(*p) == gcd(p[1], p[0])),
    'N16': lambda: eq(lambda: gcd(12, 18), 6, 'gcd(12,18)'),
    'N17': lambda: first_fail(ints('n17', lo=-1000, hi=1000), lambda a: gcd(a, 0) == a),
    'N18': lambda: eq(lambda: digits_sum(1234), 10, 'digits_sum(1234)'),
    'N19': n19,
}
