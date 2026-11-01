import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def check():
    r = rng('M4')
    pairs = [(a,b) for a in range(-30,31) for b in range(-30,31)]
    pairs += [(r.randint(-10**9,10**9), r.randint(-10**9,10**9)) for _ in range(2000)]
    for a, b in pairs:
        if gcd(a,b) != gcd(b,a):
            return f"gcd({a},{b})={gcd(a,b)} != gcd({b},{a})={gcd(b,a)}"
run('M4', 'gcd symmetric', check)
