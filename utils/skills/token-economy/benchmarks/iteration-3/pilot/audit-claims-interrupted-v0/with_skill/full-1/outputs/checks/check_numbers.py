from common import *
from kit.numbers import *

def ints(cid, lo=-100, hi=100, n=N):
    r = rng(cid)
    return [r.randint(lo, hi) for _ in range(n)]

def is_prime_ref(n):
    return n >= 2 and all(n % i for i in range(2, n))

@claim('N01')
def _():
    r = rng('N01')
    ins = []
    for _ in range(N):
        lo = r.randint(-50, 50); hi = lo + r.randint(0, 50); ins.append((r.randint(-100, 100), lo, hi))
    return forall(ins, lambda x, lo, hi: lo <= clamp(x, lo, hi) <= hi)
@claim('N02')
def _(): return eq(lambda: clamp(5, 10, 0), 0)
@claim('N03')
def _(): return eq(lambda: mean([]), 0)
@claim('N04')
def _(): return eq(lambda: mean([1, 2]), 1.5)
@claim('N05')
def _(): return eq(lambda: median([3, 1, 2]), 2)
@claim('N06')
def _(): return eq(lambda: median([]), None)
@claim('N07')
def _():
    r = rng('N07')
    ins = [([r.randint(-9, 9) for _ in range(r.randint(1, 8))],) for _ in range(N)]
    return forall(ins, lambda xs: median(xs) == median(sorted(xs)))
@claim('N08')
def _(): return eq(lambda: round_half(2.5), 3)
@claim('N09')
def _(): return eq(lambda: round_half(3.5), 4)
@claim('N10')
def _(): return eq(lambda: percent(1, 3), 33.3)
@claim('N11')
def _(): return forall([0, 1, -1, 2.5, 100, 10**9], lambda x: percent(x, 0) == 0.0)
@claim('N12')
def _(): return forall(range(0, 1001), lambda n: is_prime(n) == is_prime_ref(n))
@claim('N13')
def _(): return eq(lambda: is_prime(97), True)
@claim('N14')
def _(): return eq(lambda: is_prime(2), True)
@claim('N15')
def _(): return forall(((a, b) for a in range(-50, 51) for b in range(-50, 51)), lambda a, b: gcd(a, b) == gcd(b, a))
@claim('N16')
def _(): return eq(lambda: gcd(12, 18), 6)
@claim('N17')
def _(): return forall(range(-1000, 1001), lambda a: gcd(a, 0) == a)
@claim('N18')
def _(): return eq(lambda: digits_sum(1234), 10)
@claim('N19')
def _(): return forall(list(range(-1000, 1001)) + ints('N19', -10**9, 10**9, 2000), lambda n: isinstance(digits_sum(n), int) and digits_sum(n) >= 0)

if __name__ == '__main__': main('numbers')
