import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

r = rng()
cases = [(date(2024,1,2), date(2024,1,1)), (date(2024,1,1), date(2024,1,1)), (date(9999,12,31), date(1,1,1))]
for _ in range(20000):
    cases.append((date.fromordinal(r.randint(1, 3652059)), date.fromordinal(r.randint(1, 3652059))))
search("D3", cases, lambda c: days_between(*c) >= 0, "edge cases (a>b, a==b, extremes), then 20000 seeded random pairs")
