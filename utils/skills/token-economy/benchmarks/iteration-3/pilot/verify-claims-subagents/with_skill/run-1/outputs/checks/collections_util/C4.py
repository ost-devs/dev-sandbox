import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

bad=None
cases=[([],0),([],3),([1,2],5),([1,2,3],0),([1,2,3],-1),([1,2,3],-5),([3,3,3],2),([1],1)]
for _ in range(300):
    cases.append(([r.randint(-9,9) for _ in range(r.randint(0,20))], r.randint(-25,25)))
for xs,n in cases:
    try:
        o=top_n(xs,n)
        if len(o)!=min(n,len(xs)): bad=f"top_n({xs},{n})={o}, len {len(o)} != {min(n,len(xs))}"; break
    except Exception as e:
        bad=f"top_n({xs},{n}) raised {e!r}"; break
verdict('C4', bad is None, bad)
