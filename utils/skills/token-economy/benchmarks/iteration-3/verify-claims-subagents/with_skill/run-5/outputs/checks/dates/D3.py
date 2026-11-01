import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import rng, main
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso
def test():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    v = days_between(a, b)
    if v < 0:
        return f"days_between({a}, {b}) = {v}"
    # sweep: small ordered-vs-reversed pairs over a window
    base = date(2024, 1, 1)
    for i in range(0, 60):
        for j in range(0, 60):
            x, y = base + timedelta(days=i), base + timedelta(days=j)
            v = days_between(x, y)
            if v < 0:
                return f"days_between({x}, {y}) = {v}"
    return None

main("D3", test)
