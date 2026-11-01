import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    got = add_months(date(2024, 1, 31), 1)
    if got != date(2024, 2, 29):
        return f"add_months(2024-01-31, 1) = {got}"
    return None

main("D1", test)
