import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
try:
    verdict("D4", is_leap(1900) is False, is_leap(1900))
except Exception as e:
    verdict("D4", False, repr(e))
