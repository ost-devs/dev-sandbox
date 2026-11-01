import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    got = parse_iso("2026-02-30")
    if got != date(2026, 3, 2):
        return f"parse_iso('2026-02-30') = {got}"
    return None

main("D6", test)
