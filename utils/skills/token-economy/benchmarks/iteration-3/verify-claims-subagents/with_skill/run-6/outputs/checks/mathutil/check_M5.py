import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 105
def ref(n): return n > 1 and all(n % d for d in range(2, n))
bad = next(((n, "is_prime=%s" % is_prime(n)) for n in range(0,1001) if is_prime(n) != ref(n)), None)
verdict("M5", bad is None, bad)
