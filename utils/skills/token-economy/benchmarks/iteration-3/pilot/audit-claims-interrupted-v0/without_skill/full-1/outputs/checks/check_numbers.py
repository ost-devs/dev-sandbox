from harness import *
from kit.numbers import *


def _ref_prime(n):
    return n >= 2 and all(n % d for d in range(2, n))


@claim('N01')
def _(): return forall([(x, lo, hi) for lo in range(-6, 7) for hi in range(lo, 7) for x in range(-12, 13)],
                       lambda x, lo, hi: lo <= clamp(x, lo, hi) <= hi)
@claim('N02')
def _(): return eq('clamp(5, 10, 0)', lambda: clamp(5, 10, 0), 0)
@claim('N03')
def _(): return eq('mean([])', lambda: mean([]), 0)
@claim('N04')
def _(): return eq('mean([1, 2])', lambda: mean([1, 2]), 1.5)
@claim('N05')
def _(): return eq('median([3, 1, 2])', lambda: median([3, 1, 2]), 2)
@claim('N06')
def _(): return eq('median([])', lambda: median([]), None)
@claim('N07')
def _():
    r = rng('N07')
    return forall([[r.randint(-20, 20) for _ in range(r.randint(1, 9))] for _ in range(5000)],
                  lambda xs: median(xs) == median(sorted(xs)))
@claim('N08')
def _(): return eq('round_half(2.5)', lambda: round_half(2.5), 3)
@claim('N09')
def _(): return eq('round_half(3.5)', lambda: round_half(3.5), 4)
@claim('N10')
def _(): return eq('percent(1, 3)', lambda: percent(1, 3), 33.3)
@claim('N11')
def _(): return forall([0, 1, -1, 2.5, 100, 0.0], lambda x: percent(x, 0) == 0.0)
@claim('N12')
def _():
    for n in range(0, 1001):
        if is_prime(n) != _ref_prime(n):
            return f'is_prime({n}) = {is_prime(n)}; correto = {_ref_prime(n)}'
@claim('N13')
def _(): return eq('is_prime(97)', lambda: is_prime(97), True)
@claim('N14')
def _(): return eq('is_prime(2)', lambda: is_prime(2), True)
@claim('N15')
def _(): return forall([(a, b) for a in range(-50, 51) for b in range(-50, 51)],
                       lambda a, b: gcd(a, b) == gcd(b, a) or f'gcd({a},{b})={gcd(a, b)}, gcd({b},{a})={gcd(b, a)}')
@claim('N16')
def _(): return eq('gcd(12, 18)', lambda: gcd(12, 18), 6)
@claim('N17')
def _():
    r = rng('N17')
    return forall(list(range(-1000, 1001)) + [r.randint(-10**12, 10**12) for _ in range(2000)],
                  lambda a: gcd(a, 0) == a)
@claim('N18')
def _(): return eq('digits_sum(1234)', lambda: digits_sum(1234), 10)
@claim('N19')
def _(): return forall(list(range(-20, 1001)),
                       lambda n: (lambda v: isinstance(v, int) and v >= 0)(digits_sum(n)))

if __name__ == '__main__':
    sys.exit(main())
