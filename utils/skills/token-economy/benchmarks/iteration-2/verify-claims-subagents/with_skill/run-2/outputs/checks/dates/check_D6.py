import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import rng, verdict, search
from datetime import date, timedelta
from calc.dates import *

try:
    a = parse_iso('2026-02-30')
except Exception as e:
    a = f"raised {type(e).__name__}: {e}"
verdict("D6", a == date(2026,3,2), f"got {a}", method="direct call")
