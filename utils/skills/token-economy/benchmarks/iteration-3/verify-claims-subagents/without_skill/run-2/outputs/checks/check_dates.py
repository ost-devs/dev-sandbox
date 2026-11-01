import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

rng = random.Random(12345)
START, END = date(1, 1, 1), date(9999, 12, 31)

def sample_dates():
    out = [date(2024, 2, 29), date(2023, 1, 31), date(2000, 2, 29), date(1900, 2, 28)]
    # every day of a leap year plus a non-leap year, then random dates
    d = date(2024, 1, 1)
    while d.year == 2024:
        out.append(d); d += timedelta(1)
    for _ in range(3000):
        out.append(date.fromordinal(rng.randint(1, date(9998, 12, 31).toordinal())))
    return out

DATES = sample_dates()
res = {}

def d1():
    try:
        r = add_months(date(2024, 1, 31), 1)
    except Exception as e:
        return False, repr(e)
    return (True, '-') if r == date(2024, 2, 29) else (False, repr(r))

def d2():
    for d in DATES:
        try:
            r = add_months(d, 12)
        except Exception as e:
            return False, f"{d!r} -> {e!r}"
        if (r.year, r.month, r.day) != (d.year + 1, d.month, d.day):
            return False, f"add_months({d!r}, 12) = {r!r}"
    return True, '-'

def d3():
    a, b = date(2024, 3, 1), date(2024, 1, 1)
    n = days_between(a, b)
    return (False, f"days_between({a!r}, {b!r}) = {n}") if n < 0 else (True, '-')

def d4():
    return (True, '-') if is_leap(1900) is False else (False, repr(is_leap(1900)))

def d5():
    for d in DATES:
        if quarter(d) not in (1, 2, 3, 4):
            return False, f"quarter({d!r}) = {quarter(d)}"
    return True, '-'

def d6():
    try:
        r = parse_iso('2026-02-30')
    except Exception as e:
        return False, f"parse_iso('2026-02-30') raised {e!r}"
    return (True, '-') if r == date(2026, 3, 2) else (False, repr(r))

for k, f in [('D1', d1), ('D2', d2), ('D3', d3), ('D4', d4), ('D5', d5), ('D6', d6)]:
    ok, ce = f()
    print(f"{k} {'TRUE' if ok else 'FALSE'} {ce}")
