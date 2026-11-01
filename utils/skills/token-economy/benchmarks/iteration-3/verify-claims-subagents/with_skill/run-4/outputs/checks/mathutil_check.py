import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run, SEED
from calc.mathutil import clamp, mean, round_half, gcd, is_prime, percent


def check_M1(rng):
    cases = [(0, 0, 0), (-5, 0, 0), (5, 0, 0), (1, 1, 2), (2, 1, 2), (1.5, 1, 2)]
    for _ in range(5000):
        lo = rng.randint(-100, 100)
        hi = lo + rng.randint(0, 100)
        cases.append((rng.randint(-300, 300), lo, hi))
        cases.append((rng.uniform(-300, 300), lo, hi))
    for x, lo, hi in cases:
        r = clamp(x, lo, hi)
        if not (lo <= r <= hi):
            return False, repr((x, lo, hi, r))
    return True, None


def check_M2(rng):
    return (mean([]) == 0, None) if True else None


def check_M3(rng):
    r = round_half(2.5)
    return (r == 3, None if r == 3 else f"round_half(2.5) == {r!r}")


def check_M4(rng):
    vals = list(range(-30, 31)) + [rng.randint(-10**6, 10**6) for _ in range(2000)]
    for a in vals[:61]:
        for b in vals[:61]:
            if gcd(a, b) != gcd(b, a):
                return False, repr((a, b))
    for _ in range(3000):
        a, b = rng.choice(vals), rng.choice(vals)
        if gcd(a, b) != gcd(b, a):
            return False, repr((a, b))
    return True, None


def _ref_prime(n):
    return n >= 2 and all(n % d for d in range(2, n))


def check_M5(rng):
    for n in range(0, 1001):
        if is_prime(n) != _ref_prime(n):
            return False, f"is_prime({n}) == {is_prime(n)}, expected {_ref_prime(n)}"
    return True, None


def check_M6(rng):
    r = percent(1, 3)
    return (r == 33.3, None if r == 33.3 else f"percent(1, 3) == {r!r}")


run(globals())
