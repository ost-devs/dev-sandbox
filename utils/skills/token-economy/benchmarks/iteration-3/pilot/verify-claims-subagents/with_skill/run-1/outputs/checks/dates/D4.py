import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
r = rng()
def rand_dates(n=2000):
    b = date(1,1,1).toordinal()
    return [date.fromordinal(r.randint(b, date(9999,12,31).toordinal())) for _ in range(n)]

verdict('D4', is_leap(1900) is False, f'is_leap(1900)={is_leap(1900)}')
