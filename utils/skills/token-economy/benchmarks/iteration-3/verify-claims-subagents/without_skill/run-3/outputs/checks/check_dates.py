import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

def d1():
    r = add_months(date(2024, 1, 31), 1)
    return r == date(2024, 2, 29), f"got {r}"

def d2():
    d = date.min
    while True:
        try:
            r = add_months(d, 12)
            if (r.month, r.day) != (d.month, d.day) or r.year != d.year + 1:
                return False, f"add_months({d!r},12)={r!r}"
        except Exception as e:
            return False, f"add_months({d!r},12) raised {type(e).__name__}: {e}"
        if d == date.max: return True, ""
        d += timedelta(days=1)

def d3():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = days_between(a, b)
    return r >= 0, f"days_between({a!r},{b!r})={r}"

def d4():
    return is_leap(1900) is False, f"got {is_leap(1900)}"

def d5():
    d = date.min
    while True:
        if quarter(d) not in (1, 2, 3, 4): return False, f"quarter({d!r})={quarter(d)}"
        if d == date.max: return True, ""
        d += timedelta(days=1)

def d6():
    try:
        r = parse_iso('2026-02-30')
    except Exception as e:
        return False, f"parse_iso('2026-02-30') raised {type(e).__name__}: {e}"
    return r == date(2026, 3, 2), f"got {r}"

for name, f in [("D1",d1),("D2",d2),("D3",d3),("D4",d4),("D5",d5),("D6",d6)]:
    ok, info = f()
    print(f"{name} {'TRUE' if ok else 'FALSE'} {info}".rstrip())
