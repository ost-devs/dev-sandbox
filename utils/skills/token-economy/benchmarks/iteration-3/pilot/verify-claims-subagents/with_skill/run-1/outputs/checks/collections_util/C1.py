import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

bad = None
cases = [([],1),([],5),([1],3),([1,2,3],10),([1,2,3],1),([1,2,3,4],2),([None,[1],'a'],2)]
for _ in range(300):
    cases.append(([r.randint(-5,5) for _ in range(r.randint(0,30))], r.randint(1,40)))
for xs,n in cases:
    try:
        out = chunk(xs,n)
        flat = [y for c in out for y in c]
        if flat != xs: bad = f"chunk({xs},{n})={out}"; break
    except Exception as e:
        bad = f"chunk({xs},{n}) raised {e!r}"; break
verdict('C1', bad is None, bad)
