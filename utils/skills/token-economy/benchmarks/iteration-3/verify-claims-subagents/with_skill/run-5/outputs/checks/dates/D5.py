import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    d = date.min
    while d.year <= 9999:
        q = quarter(d)
        if not (1 <= q <= 4):
            return f"quarter({d}) = {q}"
        if d.year == 9999 and d.month == 12 and d.day == 31:
            break
        d += timedelta(days=1)
    return None

main("D5", test)
