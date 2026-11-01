import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    got = is_leap(1900)
    if got is not False:
        return f"is_leap(1900) = {got!r}"
    return None

main("D4", test)
