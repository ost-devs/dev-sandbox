import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import Checker, rand_int
from kit.numbers import *

c = Checker("numbers")
def eq(f, exp):
    def g():
        r = f()
        return None if r == exp and type(r) in (type(exp), bool) or r == exp else f"got {r!r}"
    return g
def pair(rng):
    lo = rand_int(rng, -50, 50); return (rand_int(rng, -100, 100), lo, lo + rand_int(rng, 0, 50))
c.prop("N01", pair, lambda x, lo, hi: lo <= clamp(x, lo, hi) <= hi)
c.fixed("N02", eq(lambda: clamp(5, 10, 0), 0))
c.fixed("N03", eq(lambda: mean([]), 0))
c.fixed("N04", eq(lambda: mean([1, 2]), 1.5))
c.fixed("N05", eq(lambda: median([3, 1, 2]), 2))
c.fixed("N06", eq(lambda: median([]), None))
c.prop("N07", lambda r: ([rand_int(r, -20, 20) for _ in range(r.randint(1, 10))],),
       lambda xs: median(xs) == median(sorted(xs)))
c.fixed("N08", eq(lambda: round_half(2.5), 3))
c.fixed("N09", eq(lambda: round_half(3.5), 4))
c.fixed("N10", eq(lambda: percent(1, 3), 33.3))
c.prop("N11", lambda r: (r.choice([0, 1, -3, 2.5, 100, 7]),), lambda x: percent(x, 0) == 0.0)
def ref(n):
    return n >= 2 and all(n % i for i in range(2, n))
def n12():
    bad = [n for n in range(1001) if is_prime(n) != ref(n)]
    return None if not bad else f"wrong for {bad[:10]}"
c.fixed("N12", n12)
c.fixed("N13", eq(lambda: is_prime(97), True))
c.fixed("N14", eq(lambda: is_prime(2), True))
def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            if gcd(a, b) != gcd(b, a): return f"a={a} b={b}: {gcd(a,b)} vs {gcd(b,a)}"
c.fixed("N15", n15)
c.fixed("N16", eq(lambda: gcd(12, 18), 6))
c.prop("N17", lambda r: (rand_int(r, -100, 100),), lambda a: gcd(a, 0) == a)
c.prop("N19", lambda r: (rand_int(r, -1000, 1000),),
       lambda n: isinstance(digits_sum(n), int) and digits_sum(n) >= 0)
c.fixed("N18", eq(lambda: digits_sum(1234), 10))
c.finish()
