import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

cases = [date(2024,1,1), date(2024,3,31), date(2024,4,1), date(2024,12,31)]
d = date(1,1,1)
while d < date(2101,1,1):
    cases.append(d); d += timedelta(days=1)
search("D5", cases, lambda d: quarter(d) in (1,2,3,4), "edge cases, then every date 0001-01-01..2100-12-31")
