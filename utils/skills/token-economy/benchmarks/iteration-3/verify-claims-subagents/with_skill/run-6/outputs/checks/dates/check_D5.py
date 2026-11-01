import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
cex = None
d = date(1,1,1)
for i in range(0, 3650000, 7):
    x = d + timedelta(days=i) if i < 2900000 else None
    if x is None: break
    if quarter(x) not in (1,2,3,4): cex = x; break
for m in range(1, 13):
    for day in (1, 28, 29, 30, 31):
        try: x = date(2024, m, day)
        except ValueError: continue
        if quarter(x) not in (1,2,3,4): cex = x
verdict("D5", cex is None, cex)
