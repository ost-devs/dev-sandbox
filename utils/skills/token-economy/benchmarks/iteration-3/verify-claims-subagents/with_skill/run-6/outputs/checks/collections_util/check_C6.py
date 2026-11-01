import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.collections_util import *
SEED = 12345
r = rng(SEED)
def rl(): return [r.randint(0, 4) for _ in range(r.randint(0, 8))]

cex=None
for xs in [[],[1],[1,2,3],[1,1]]+[rl() for _ in range(2000)]:
    try: ok=rotate(xs,len(xs))==xs
    except Exception: ok=False
    if not ok: cex=xs; break
verdict("C6",cex is None,cex)
