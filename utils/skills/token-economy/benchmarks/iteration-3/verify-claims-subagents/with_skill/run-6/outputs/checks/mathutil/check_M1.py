import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 101
r = rng(SEED)
cases = [(0,0,0),(-5,-3,-1),(5,-3,-1),(-1.5,-1.5,2.5),(0.0,-0.0,0.0),(10**30,-1,1)]
for _ in range(20000):
    lo = r.choice([r.randint(-100,100), r.uniform(-100,100)])
    hi = lo + r.choice([0, r.randint(0,50), r.uniform(0,50)])
    cases.append((r.choice([r.randint(-200,200), r.uniform(-200,200)]), lo, hi))
bad = next(((x,lo,hi) for x,lo,hi in cases if not (lo <= clamp(x,lo,hi) <= hi)), None)
verdict("M1", bad is None, bad)
