import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

cases = [date(2024,2,29), date(2023,2,28), date(2000,2,29), date(1900,2,28), date(2024,12,31), date(2024,1,31), date(9999,1,1), date(9999,12,31)]
d = date(1, 1, 1)
while d < date(2101,1,1):
    cases.append(d); d += timedelta(days=1)
def prop(d):
    r = add_months(d, 12)
    return (r.year, r.month, r.day) == (d.year+1, d.month, d.day)
search("D2", cases, prop, "edge cases (leap days, year bounds), then every date 0001-01-01..2100-12-31")
