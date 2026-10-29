import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

def ref(xs):
    seen=[];
    for x in xs:
        if x not in seen: seen.append(x)
    return seen
bad=None
cases=[[],[1,1,2],[3,1,3,2,1],[1,1.0,True],['a','b','a'],[[1],[1]],[{1},{1}],[{'a':1}]]
for _ in range(300):
    cases.append([r.randint(0,8) for _ in range(r.randint(0,30))])
for xs in cases:
    try:
        o=dedupe(xs)
        if o!=ref(xs): bad=f"dedupe({xs})={o}, expected {ref(xs)}"; break
    except Exception as e:
        bad=f"dedupe({xs}) raised {e!r}"; break
verdict('C2', bad is None, bad)
