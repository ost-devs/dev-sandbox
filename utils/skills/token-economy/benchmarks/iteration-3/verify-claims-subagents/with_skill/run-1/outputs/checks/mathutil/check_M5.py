import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def ref(n):
    return n >= 2 and all(n % d for d in range(2, n))
def check():
    bad = [n for n in range(0, 1001) if is_prime(n) != ref(n)]
    if bad:
        n = bad[0]
        return f"is_prime({n}) -> {is_prime(n)}, expected {ref(n)} (first of {len(bad)} wrong: {bad[:6]})"
run('M5', 'is_prime correct 0..1000', check)
