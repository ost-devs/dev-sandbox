import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def check():
    r = rng('M1')
    cases = [(0,0,0),(5,1,3),(-5,-3,-1),(2,2,2),(1,1,3),(3,1,3),(1e308,-1e308,1e308)]
    cases += [(r.randint(-100,100), *sorted([r.randint(-100,100), r.randint(-100,100)])) for _ in range(1000)]
    cases += [(r.uniform(-1e3,1e3), *sorted([r.uniform(-1e3,1e3), r.uniform(-1e3,1e3)])) for _ in range(1000)]
    for x, lo, hi in cases:
        v = clamp(x, lo, hi)
        if not (lo <= v <= hi):
            return f"clamp({x},{lo},{hi}) -> {v}"
run('M1', 'clamp within [lo,hi]', check)
