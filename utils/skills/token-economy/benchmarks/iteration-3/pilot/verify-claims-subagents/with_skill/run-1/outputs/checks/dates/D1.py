import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
r = rng()
def rand_dates(n=2000):
    b = date(1,1,1).toordinal()
    return [date.fromordinal(r.randint(b, date(9999,12,31).toordinal())) for _ in range(n)]

try:
    got = add_months(date(2024,1,31),1)
except Exception as e:
    got = repr(e)
verdict('D1', got == date(2024,2,29), f'add_months(2024-01-31,1)={got}')
