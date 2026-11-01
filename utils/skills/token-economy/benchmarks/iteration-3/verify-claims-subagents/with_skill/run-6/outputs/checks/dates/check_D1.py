import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
try:
    got = add_months(date(2024, 1, 31), 1)
    verdict("D1", got == date(2024, 2, 29), got)
except Exception as e:
    verdict("D1", False, repr(e))
