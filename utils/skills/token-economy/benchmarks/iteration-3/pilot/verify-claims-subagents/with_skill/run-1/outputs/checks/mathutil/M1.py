import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

r = rng()
cases = [(0,0,0),(-5,-5,-5),(5,5,5),(-1,-3,-1),(0,-2,2),(10,-2,2),(-10,-2,2),(1.5,1,2)]
cases += [(r.randint(-100,100),) + tuple(sorted((r.randint(-100,100), r.randint(-100,100)))) for _ in range(5000)]
cases += [(r.uniform(-1e3,1e3),) + tuple(sorted((r.uniform(-1e3,1e3), r.uniform(-1e3,1e3)))) for _ in range(5000)]
for x, lo, hi in cases:
    try: c = clamp(x, lo, hi)
    except Exception as e: verdict('M1', False, f'clamp({x},{lo},{hi}) raised {e!r}')
    if not (lo <= c <= hi): verdict('M1', False, f'clamp({x},{lo},{hi})={c}')
verdict('M1', True)
