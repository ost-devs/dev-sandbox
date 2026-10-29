import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

bad=None
cases=[[],[1],[1,2],[1,2,3],[None,'a',[1]]]
for _ in range(300):
    cases.append([r.randint(-5,5) for _ in range(r.randint(0,30))])
for xs in cases:
    try:
        o=rotate(xs,len(xs))
        if o!=xs: bad=f"rotate({xs},{len(xs)})={o}"; break
    except Exception as e:
        bad=f"rotate({xs},{len(xs)}) raised {e!r}"; break
verdict('C6', bad is None, bad)
