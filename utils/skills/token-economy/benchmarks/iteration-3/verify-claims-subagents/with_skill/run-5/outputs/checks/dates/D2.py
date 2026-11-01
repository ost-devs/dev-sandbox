import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    # exhaustive sweep over all dates in order; stop at first counterexample
    d = date.min
    one = date.max
    while d.year <= 9998:
        try:
            got = add_months(d, 12)
        except Exception as e:
            return f"add_months({d}, 12) raised {type(e).__name__}: {e}"
        if (got.month, got.day) != (d.month, d.day) or got.year != d.year + 1:
            return f"add_months({d}, 12) = {got}"
        d += timedelta(days=1)
    return None

main("D2", test)
