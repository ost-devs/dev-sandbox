import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.collections_util import *
SEED = 12345
r = rng(SEED)
def rl(): return [r.randint(0, 4) for _ in range(r.randint(0, 8))]

try:
    got=flatten([[1,[2]],[3]]); ok=got==[1,2,3]; cex=got
except Exception as e: ok=False; cex="raised %r"%e
verdict("C3",ok,cex)
