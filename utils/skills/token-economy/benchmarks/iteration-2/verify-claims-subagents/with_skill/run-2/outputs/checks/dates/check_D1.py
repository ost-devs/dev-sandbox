import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

a = add_months(date(2024, 1, 31), 1)
verdict("D1", a == date(2024, 2, 29), f"got {a}", method="direct call")
