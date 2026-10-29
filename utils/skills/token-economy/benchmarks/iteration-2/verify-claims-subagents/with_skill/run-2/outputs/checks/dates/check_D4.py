import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

a = is_leap(1900)
verdict("D4", a is False, f"got {a!r}", method="direct call")
