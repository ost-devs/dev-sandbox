import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from datetime import date, timedelta
from calc.dates import *
SEED = 12345
r = rng(SEED)
try:
    got = parse_iso("2026-02-30")
    verdict("D6", got == date(2026, 3, 2), got)
except Exception as e:
    verdict("D6", False, "parse_iso(\"2026-02-30\") raised " + repr(e))
