import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker, rand_ints, rand_lists
from kit.numbers import *
c = Checker('numbers')

@c.claim('N01')
def _():
    vals = rand_ints(1001, 300, -60, 60)
    pairs = [(x, lo, hi) for x in vals[:80] for lo in (-50, 0, 7) for hi in (7, 7, 50) if lo <= hi]
    return c.forall(pairs, lambda t: t[1] <= clamp(*t) <= t[2])

@c.claim('N02')
def _(): return c.eq(clamp(5, 10, 0), 0)

@c.claim('N03')
def _(): return c.eq(mean([]), 0)

@c.claim('N04')
def _(): return c.eq(mean([1, 2]), 1.5)

@c.claim('N05')
def _(): return c.eq(median([3, 1, 2]), 2)

@c.claim('N06')
def _(): return c.eq(median([]), None)

@c.claim('N07')
def _():
    return c.forall([l for l in rand_lists(1007, 1000) if l], lambda l: median(l) == median(sorted(l)))

@c.claim('N08')
def _(): return c.eq(round_half(2.5), 3)

@c.claim('N09')
def _(): return c.eq(round_half(3.5), 4)

@c.claim('N10')
def _(): return c.eq(percent(1, 3), 33.3)

@c.claim('N11')
def _():
    return c.forall([0, 1, -1, 0.5, 100, 1e9, 0.0], lambda x: percent(x, 0) == 0.0)

def ref_prime(n):
    return n >= 2 and all(n % i for i in range(2, n))

@c.claim('N12')
def _():
    return c.forall(list(range(0, 1001)), lambda n: is_prime(n) == ref_prime(n))

@c.claim('N13')
def _(): return c.eq(is_prime(97), True)

@c.claim('N14')
def _(): return c.eq(is_prime(2), True)

@c.claim('N15')
def _():
    r = range(-50, 51)
    return c.forall([(a, b) for a in r for b in r], lambda t: gcd(*t) == gcd(t[1], t[0]))

@c.claim('N16')
def _(): return c.eq(gcd(12, 18), 6)

@c.claim('N17')
def _():
    return c.forall(list(range(-60, 61)) + [10**20, -10**20], lambda a: gcd(a, 0) == a)

@c.claim('N18')
def _(): return c.eq(digits_sum(1234), 10)

@c.claim('N19')
def _():
    ins = [0, 1, -1, 9, -5, 10, 1234, -1234, 10**30, -10**30] + rand_ints(1019, 300, -10**6, 10**6)
    return c.forall(ins, lambda n: type(digits_sum(n)) is int and digits_sum(n) >= 0)

c.main()
