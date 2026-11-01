import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 104
r = rng(SEED)
pairs = [(a,b) for a in range(-60,61) for b in range(-60,61)]
pairs += [(r.randint(-10**9,10**9), r.randint(-10**9,10**9)) for _ in range(20000)]
bad = next(((a,b,gcd(a,b),gcd(b,a)) for a,b in pairs if gcd(a,b) != gcd(b,a)), None)
verdict("M4", bad is None, bad)
