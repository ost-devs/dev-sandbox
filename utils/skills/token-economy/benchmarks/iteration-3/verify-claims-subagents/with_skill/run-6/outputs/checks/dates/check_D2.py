import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
cex = None
cands = [date(2024,2,29), date(2024,1,31), date(2023,2,28), date(2000,2,29), date(2024,12,31)]
cands += [date(1,1,1) + timedelta(days=r.randrange(0, 3000000)) for _ in range(20000)]
for d in cands:
    try:
        e = add_months(d, 12)
        if (e.year, e.month, e.day) != (d.year+1, d.month, d.day):
            cex = (d, e); break
    except Exception as ex:
        cex = (d, repr(ex)); break
verdict("D2", cex is None, cex)
