import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
r = rng()
def rand_dates(n=2000):
    b = date(1,1,1).toordinal()
    return [date.fromordinal(r.randint(b, date(9999,12,31).toordinal())) for _ in range(n)]

edges = [date(2024,2,29), date(2023,12,31), date(2024,1,31), date(2000,2,29), date(1,1,1), date(9998,12,31), date(2024,12,31)]
for d in edges + rand_dates():
    try:
        x = add_months(d,12)
    except Exception as e:
        verdict('D2', False, f'add_months({d},12) raised {e!r}')
    if (x.year, x.month, x.day) != (d.year+1, d.month, d.day):
        verdict('D2', False, f'add_months({d},12)={x}')
verdict('D2', True)
