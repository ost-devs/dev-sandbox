import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import Results, rng
from kit.numbers import *
R = Results("numbers")

def n01():
    r = rng()
    cases = [(x, lo, hi) for lo in range(-6, 7) for hi in range(lo, 7) for x in range(-9, 10)]
    cases += [(r.randint(-10**9, 10**9), *sorted((r.randint(-10**9, 10**9), r.randint(-10**9, 10**9)))) for _ in range(2000)]
    for x, lo, hi in cases:
        if not (lo <= clamp(x, lo, hi) <= hi):
            return False, (x, lo, hi, clamp(x, lo, hi))
    return True, None
def eq(f, want):
    def g():
        v = f()
        return (v == want and type(v) is type(want) or v == want), (None if v == want else f"got {v!r}")
    return g
def n07():
    r = rng()
    for _ in range(3000):
        xs = [r.randint(-20, 20) for _ in range(r.randint(1, 9))]
        if median(xs) != median(sorted(xs)):
            return False, xs
    return True, None
def n12():
    for n in range(0, 1001):
        ref = n >= 2 and all(n % d for d in range(2, n))
        if is_prime(n) != ref:
            return False, (n, is_prime(n))
    return True, None
def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            if gcd(a, b) != gcd(b, a):
                return False, (a, b, gcd(a, b), gcd(b, a))
    return True, None
def n17():
    for a in range(-1000, 1001):
        if gcd(a, 0) != a:
            return False, (a, gcd(a, 0))
    return True, None
def n19():
    for n in list(range(-1000, 1001)) + [10**30, -10**30]:
        v = digits_sum(n)
        if not (isinstance(v, int) and v >= 0):
            return False, (n, v)
    return True, None
def n11():
    for x in [0, 1, -1, 5, 0.5, 10**9]:
        if percent(x, 0) != 0.0:
            return False, x
    return True, None

R.check("N01", n01)
R.check("N02", eq(lambda: clamp(5, 10, 0), 0))
R.check("N03", eq(lambda: mean([]), 0))
R.check("N04", eq(lambda: mean([1, 2]), 1.5))
R.check("N05", eq(lambda: median([3, 1, 2]), 2))
R.check("N06", lambda: (median([]) is None, "median([])"))
R.check("N07", n07)
R.check("N08", eq(lambda: round_half(2.5), 3))
R.check("N09", eq(lambda: round_half(3.5), 4))
R.check("N10", eq(lambda: percent(1, 3), 33.3))
R.check("N11", n11)
R.check("N12", n12)
R.check("N13", lambda: (is_prime(97) is True, 97))
R.check("N14", lambda: (is_prime(2) is True, 2))
R.check("N15", n15)
R.check("N16", eq(lambda: gcd(12, 18), 6))
R.check("N17", n17)
R.check("N18", eq(lambda: digits_sum(1234), 10))
R.check("N19", n19)
R.finish()
