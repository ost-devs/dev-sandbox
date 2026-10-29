import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

def ref(n): return n > 1 and all(n % d for d in range(2, n))
bad = [n for n in range(0, 1001) if is_prime(n) != ref(n)]
verdict('M5', not bad, f'is_prime({bad[0]})={is_prime(bad[0])}, expected {ref(bad[0])}; all wrong: {bad[:10]}' if bad else None)
