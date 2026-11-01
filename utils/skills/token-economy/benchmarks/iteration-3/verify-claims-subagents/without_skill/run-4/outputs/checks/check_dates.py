import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

print("seed: none (deterministic exhaustive search)")

def all_dates():
    d, end = date(1, 1, 1), date(9998, 12, 31)
    while d <= end:
        yield d
        d += timedelta(days=1)

def d1():
    try:
        r = add_months(date(2024, 1, 31), 1)
    except Exception as e:
        return False, f"raised {e!r}"
    return r == date(2024, 2, 29), f"add_months(date(2024, 1, 31), 1) = {r!r}"

def d2():
    # years 1..9998 so +12 months stays in range
    for d in all_dates():
        if d.year > 9998: break
        try:
            r = add_months(d, 12)
        except Exception as e:
            return False, f"add_months({d!r}, 12) raised {e!r}"
        if (r.year, r.month, r.day) != (d.year + 1, d.month, d.day):
            return False, f"add_months({d!r}, 12) = {r!r}"
    return True, "none"

def d3():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = days_between(a, b)
    if r < 0: return False, f"days_between({a!r}, {b!r}) = {r}"
    return True, "none"

def d4():
    r = is_leap(1900)
    return r is False, f"is_leap(1900) = {r!r}"

def d5():
    for d in all_dates():
        q = quarter(d)
        if not (1 <= q <= 4):
            return False, f"quarter({d!r}) = {q}"
    return True, "none"

def d6():
    try:
        r = parse_iso('2026-02-30')
    except Exception as e:
        return False, f"parse_iso('2026-02-30') raised {e!r}"
    return r == date(2026, 3, 2), f"parse_iso('2026-02-30') = {r!r}"

for name, f in [("D1", d1), ("D2", d2), ("D3", d3), ("D4", d4), ("D5", d5), ("D6", d6)]:
    ok, ce = f()
    print(name, "VERDADEIRA" if ok else "FALSA", ce if not ok else "none")
sys.exit(0)
