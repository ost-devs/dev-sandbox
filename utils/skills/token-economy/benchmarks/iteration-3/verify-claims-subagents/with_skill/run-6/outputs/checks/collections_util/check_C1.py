import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.collections_util import *
SEED = 12345
r = rng(SEED)
def rl(): return [r.randint(0, 4) for _ in range(r.randint(0, 8))]

cex=None
cases=[([],1),([],3),([1],1),([1,2,3],5),([1,1,1],2)]+[(rl(),r.randint(1,10)) for _ in range(2000)]
for xs,n in cases:
    try:
        ok=[y for c in chunk(xs,n) for y in c]==xs
    except Exception as e: ok=False
    if not ok: cex=(xs,n); break
verdict("C1",cex is None,cex)
