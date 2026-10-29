import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
r = rng()
def rand_dates(n=2000):
    b = date(1,1,1).toordinal()
    return [date.fromordinal(r.randint(b, date(9999,12,31).toordinal())) for _ in range(n)]

pairs = [(date(2024,3,1), date(2024,2,29)), (date(2025,1,1), date(2024,12,31)), (date(2024,2,29), date(2024,2,29))]
pairs += [(a,b) for a,b in zip(rand_dates(500), rand_dates(500))]
for a,b in pairs:
    if days_between(a,b) < 0:
        verdict('D3', False, f'days_between({a},{b})={days_between(a,b)}')
verdict('D3', True)
