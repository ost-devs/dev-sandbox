import os, sys, random
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

SEED = 12345
rng = random.Random(SEED)
print(f"seed={SEED}")
MIN, MAX = date.min, date.max
NDAYS = (MAX - MIN).days + 1

def all_dates():
    d = MIN
    one = timedelta(days=1)
    for i in range(NDAYS):
        yield d
        if i < NDAYS - 1:
            d += one

def report(i, ok, cex=""):
    print(f"{i}: {'TRUE' if ok else 'FALSE'} | {cex if not ok else 'no counterexample found'}")

def attempt(f, *a):
    try:
        return f(*a), None
    except Exception as e:
        return None, f"raised {type(e).__name__}: {e}"

# D1
r, err = attempt(add_months, date(2024, 1, 31), 1)
report("D1", err is None and r == date(2024, 2, 29), err or f"add_months(date(2024, 1, 31), 1) = {r!r}")

# D2: exhaustive over every date, then random
def d2():
    for d in all_dates():
        r, err = attempt(add_months, d, 12)
        if err or (r.month, r.day) != (d.month, d.day) or r.year != d.year + 1:
            return f"add_months({d!r}, 12) -> {err or repr(r)}"
    return None
c = d2()
report("D2", c is None, c)

# D3: fixed + random
def d3():
    cases = [(date(2024, 1, 2), date(2024, 1, 1))]
    for _ in range(10000):
        cases.append((MIN + timedelta(days=rng.randrange(NDAYS)), MIN + timedelta(days=rng.randrange(NDAYS))))
    for a, b in cases:
        r, err = attempt(days_between, a, b)
        if err or r < 0:
            return f"days_between({a!r}, {b!r}) -> {err or r}"
d3c = d3()
report("D3", d3c is None, d3c)

# D4
r, err = attempt(is_leap, 1900)
report("D4", err is None and r is False, err or f"is_leap(1900) = {r!r}")

# D5: exhaustive
def d5():
    for d in all_dates():
        r, err = attempt(quarter, d)
        if err or r not in (1, 2, 3, 4):
            return f"quarter({d!r}) -> {err or r}"
c = d5()
report("D5", c is None, c)

# D6
r, err = attempt(parse_iso, '2026-02-30')
report("D6", err is None and r == date(2026, 3, 2), f"parse_iso('2026-02-30') -> {err or repr(r)}")
