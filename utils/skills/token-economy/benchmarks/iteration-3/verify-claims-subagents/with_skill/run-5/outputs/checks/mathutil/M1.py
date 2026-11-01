import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.mathutil import clamp

def test():
    r = rng()
    cases = [(x, lo, hi) for lo in range(-5, 6) for hi in range(lo, 6) for x in range(-10, 11)]
    cases += [(r.uniform(-1e6, 1e6), r.uniform(-1e3, 0), r.uniform(0, 1e3)) for _ in range(20000)]
    cases += [(float('inf'), 0, 1), (float('-inf'), 0, 1), (float('nan'), 0, 1)]
    for x, lo, hi in cases:
        y = clamp(x, lo, hi)
        if not (lo <= y <= hi):
            return f"clamp({x!r}, {lo!r}, {hi!r}) = {y!r} outside [{lo}, {hi}]"
    return None

main("M1", test)
