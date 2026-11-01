import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
cex = None
pairs = [(date(2024,3,1), date(2024,2,29)), (date(2024,2,29), date(2024,2,29)), (date(2024,2,29), date(2025,2,28))]
pairs += [(date(1,1,1)+timedelta(days=r.randrange(3000000)), date(1,1,1)+timedelta(days=r.randrange(3000000))) for _ in range(5000)]
for a, b in pairs:
    try:
        if days_between(a, b) < 0:
            cex = (a, b, days_between(a, b)); break
    except Exception as ex:
        cex = (a, b, repr(ex)); break
verdict("D3", cex is None, cex)
