import os, sys, random
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

SEED = 20240229
rng = random.Random(SEED)


def run(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"{type(e).__name__}: {e}"


def all_dates(y0=1, y1=9999):
    for o in range(date(y0, 1, 1).toordinal(), date(y1, 12, 31).toordinal() + 1):
        yield date.fromordinal(o)


def d1():
    r = run(add_months, date(2024, 1, 31), 1)
    if r == date(2024, 2, 29):
        return "D1: VERDADEIRA"
    return f"D1: FALSA | contraexemplo: add_months(date(2024,1,31),1) = {r!r}"


def d2():
    n = 0
    bad = None
    # edge cases first, then exhaustive sweep years 1..9998 (9999 would overflow)
    for d in [date(2024, 2, 29)] + list(all_dates(1, 2100)):
        n += 1
        r = run(add_months, d, 12)
        exp = (d.year + 1, d.month, d.day)
        if not isinstance(r, date) or (r.year, r.month, r.day) != exp:
            bad = (d, r)
            break
    if bad:
        return f"D2: FALSA | contraexemplo: add_months({bad[0]!r}, 12) = {bad[1]!r} (esperado mesmo dia/mes em {bad[0].year+1})"
    return f"D2: VERDADEIRA ({n} casos)"


def d3():
    cases = [(date(2024, 1, 1), date(2024, 1, 1)), (date(2024, 1, 2), date(2024, 1, 1))]
    for _ in range(2000):
        cases.append((date.fromordinal(rng.randint(1, 3652059)), date.fromordinal(rng.randint(1, 3652059))))
    for i, (a, b) in enumerate(cases):
        r = run(days_between, a, b)
        if not isinstance(r, int) or r < 0:
            return f"D3: FALSA | contraexemplo: days_between({a!r}, {b!r}) = {r!r}"
    return f"D3: VERDADEIRA ({len(cases)} casos)"


def d4():
    r = run(is_leap, 1900)
    if r is False:
        return "D4: VERDADEIRA (is_leap(1900) is False)"
    return f"D4: FALSA | contraexemplo: is_leap(1900) = {r!r}"


def d5():
    n = 0
    for d in all_dates():
        n += 1
        r = run(quarter, d)
        if not (isinstance(r, int) and 1 <= r <= 4):
            return f"D5: FALSA | contraexemplo: quarter({d!r}) = {r!r}"
    return f"D5: VERDADEIRA ({n} datas, anos 1..9999)"


def d6():
    r = run(parse_iso, "2026-02-30")
    if r == date(2026, 3, 2):
        return "D6: VERDADEIRA"
    return f"D6: FALSA | contraexemplo: parse_iso('2026-02-30') = {r!r}"


for f in (d1, d2, d3, d4, d5, d6):
    print(f())
sys.exit(0)
