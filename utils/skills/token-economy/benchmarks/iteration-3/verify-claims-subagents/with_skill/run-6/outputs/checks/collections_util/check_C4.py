import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.collections_util import *
SEED = 12345
r = rng(SEED)
def rl(): return [r.randint(0, 4) for _ in range(r.randint(0, 8))]

cex=None
cases=[([],0),([1,2,3],-1),([1,2,3],0),([1,2,3],10),([1,1,2],2)]+[(rl(),r.randint(-10,12)) for _ in range(2000)]
for xs,n in cases:
    try: ok=len(top_n(xs,n))==min(n,len(xs))
    except Exception: ok=False
    if not ok: cex=(xs,n); break
verdict("C4",cex is None,cex)
