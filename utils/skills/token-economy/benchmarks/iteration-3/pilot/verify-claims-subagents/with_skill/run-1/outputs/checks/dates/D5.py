import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
r = rng()
def rand_dates(n=2000):
    b = date(1,1,1).toordinal()
    return [date.fromordinal(r.randint(b, date(9999,12,31).toordinal())) for _ in range(n)]

ds = [date(y,m,dd) for y in (1,2024,9999) for m in range(1,13) for dd in (1,28)] + [date(2024,2,29),date(2023,12,31)] + rand_dates()
for d in ds:
    q = quarter(d)
    if not 1 <= q <= 4:
        verdict('D5', False, f'quarter({d})={q}')
verdict('D5', True)
