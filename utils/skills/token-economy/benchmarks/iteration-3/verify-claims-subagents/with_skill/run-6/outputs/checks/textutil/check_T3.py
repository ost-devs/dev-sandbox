import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.textutil import *
SEED = 12345
r = rng(SEED)
edge = ["", " ", "a", "ab", "abc", "!!!", "日本語", "é"*5, "x"*50]
rand = ["".join(r.choice("ab é日.") for _ in range(r.randint(0, 10))) for _ in range(2000)]
bad = None
for s in edge + rand:
    for n in range(0, 15):
        if len(truncate(s, n)) > n:
            bad = (s, n, truncate(s, n)); break
    if bad: break
verdict("T3", bad is None, bad)
