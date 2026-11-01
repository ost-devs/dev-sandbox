import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run, SEED
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

def rand_date(rng):
    return date.fromordinal(rng.randint(date(1, 1, 1).toordinal(), date(9998, 12, 31).toordinal()))

def check_D1(rng):
    r = add_months(date(2024, 1, 31), 1)
    return (True, None) if r == date(2024, 2, 29) else (False, repr(r))

def check_D2(rng):
    cands = [date(2024, 2, 29)] + [rand_date(rng) for _ in range(2000)]
    for d in cands:
        try:
            r = add_months(d, 12)
        except Exception as e:
            return False, f"add_months({d!r}, 12) raised {e}"
        if (r.month, r.day) != (d.month, d.day):
            return False, f"add_months({d!r}, 12) = {r!r}"
    return True, None

def check_D3(rng):
    cands = [(date(2024, 1, 2), date(2024, 1, 1))] + [(rand_date(rng), rand_date(rng)) for _ in range(2000)]
    for a, b in cands:
        if days_between(a, b) < 0:
            return False, f"days_between({a!r}, {b!r}) = {days_between(a, b)}"
    return True, None

def check_D4(rng):
    return (True, None) if is_leap(1900) is False else (False, repr(is_leap(1900)))

def check_D5(rng):
    for y in (1, 2024, 9999):
        for m in range(1, 13):
            d = date(y, m, 1)
            if quarter(d) not in (1, 2, 3, 4):
                return False, f"quarter({d!r}) = {quarter(d)}"
    for _ in range(2000):
        d = rand_date(rng)
        if quarter(d) not in (1, 2, 3, 4):
            return False, f"quarter({d!r}) = {quarter(d)}"
    return True, None

def check_D6(rng):
    r = parse_iso('2026-02-30')
    return (True, None) if r == date(2026, 3, 2) else (False, repr(r))

if __name__ == "__main__":
    run(globals())
