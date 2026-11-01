import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.mathutil import gcd

def test():
    r = rng()
    pairs = [(a, b) for a in range(-60, 61) for b in range(-60, 61)]
    pairs += [(r.randint(-10**12, 10**12), r.randint(-10**12, 10**12)) for _ in range(5000)]
    for a, b in pairs:
        if gcd(a, b) != gcd(b, a):
            return f"gcd({a}, {b}) = {gcd(a, b)} != gcd({b}, {a}) = {gcd(b, a)}"
    return None

main("M4", test)
