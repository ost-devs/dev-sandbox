import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.collections_util import *
SEED = 12345
r = rng(SEED)
def rl(): return [r.randint(0, 4) for _ in range(r.randint(0, 8))]

a={"k":"a"}; b={"k":"b"}
try: got=merge_dicts(a,b); ok=got["k"]=="a"
except Exception: ok=False
verdict("C5",ok,(a,b,"merge_dicts ->",merge_dicts(a,b)))
