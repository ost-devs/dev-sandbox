import os, sys, calendar
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, main
from datetime import date, timedelta
from kit.dates import *

D0 = date(2000, 1, 1)
DAYS = [D0 + timedelta(days=i) for i in range((date(2030, 12, 31) - D0).days + 1)]

def rdate(r):
    return date(r.randint(1, 9999), r.randint(1, 12), 1) + timedelta(days=r.randint(0, 27))

@claim("D01")
def d01():
    o = add_months(date(2024, 1, 31), 1)
    if o != date(2024, 2, 29): return f"got {o}"

@claim("D02")
def d02():
    for x in DAYS:
        o = add_months(x, 12)
        if (o.year, o.month, o.day) != (x.year + 1, x.month, x.day):
            return f"add_months({x!r}, 12) = {o!r}"

@claim("D03")
def d03():
    for x in DAYS:
        o = add_months(add_months(x, 1), -1)
        if o != x: return f"x={x!r}: add_months(add_months(x,1),-1) = {o!r}"

@claim("D04")
def d04():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    o = days_between(a, b)
    if o < 0: return f"days_between({a!r}, {b!r}) = {o}"

@claim("D05")
def d05():
    r = rng("D05")
    ps = [(date(1,1,1), date(9999,12,31)), (D0, D0)] + [(rdate(r), rdate(r)) for _ in range(3000)]
    for a, b in ps:
        if days_between(a, b) != -days_between(b, a): return f"a={a!r}, b={b!r}"

@claim("D06")
def d06():
    if is_leap(1900) is not False: return f"is_leap(1900) = {is_leap(1900)!r}"

@claim("D07")
def d07():
    if is_leap(2000) is not True: return f"is_leap(2000) = {is_leap(2000)!r}"

@claim("D08")
def d08():
    for y in range(1, 10000):
        if is_leap(y) != calendar.isleap(y): return f"y={y}: {is_leap(y)!r}"

@claim("D09")
def d09():
    o = weekday_name(date(2024, 1, 1))
    if o != 'Monday': return f"got {o!r}"

@claim("D10")
def d10():
    o = quarter(date(2024, 4, 1))
    if o != 2: return f"got {o!r}"

@claim("D11")
def d11():
    for m in range(1, 13):
        for d in (1, 28):
            o = quarter(date(2023, m, d))
            if o not in (1, 2, 3, 4): return f"{m}/{d}: {o!r}"
    r = rng("D11")
    for _ in range(3000):
        x = rdate(r)
        if quarter(x) not in (1, 2, 3, 4): return f"{x!r}: {quarter(x)!r}"

@claim("D12")
def d12():
    o = end_of_month(date(2023, 2, 10))
    if o != date(2023, 2, 28): return f"got {o!r}"

@claim("D13")
def d13():
    for x in DAYS:
        if end_of_month(x) < x: return f"{x!r}: {end_of_month(x)!r}"

@claim("D14")
def d14():
    o = iso_week(date(2021, 1, 1))
    if o != 1: return f"iso_week(date(2021,1,1)) = {o!r}"

@claim("D15")
def d15():
    o = parse_br('31/12/2024')
    if o != date(2024, 12, 31): return f"got {o!r}"

@claim("D16")
def d16():
    try:
        o = parse_br('1/2/2024')
    except ValueError:
        return None
    except Exception as e:
        return f"raised {type(e).__name__}"
    return f"parse_br('1/2/2024') = {o!r}, no ValueError"

@claim("D17")
def d17():
    r = rng("D17")
    ks = [-1000, -1, 0, 1, 1000] + [r.randint(-1000, 1000) for _ in range(5)]
    for x in DAYS:
        for k in ks:
            if add_days(x, k) - x != timedelta(days=k): return f"x={x!r}, k={k}"

@claim("D18")
def d18():
    r = rng("D18")
    ks = [-30, -1, 0, 1, 12, 30] + [r.randint(-30, 30) for _ in range(4)]
    for x in DAYS:
        for k in ks:
            o = add_months(x, k)
            if o.day > x.day: return f"add_months({x!r}, {k}) = {o!r}"

@claim("D19")
def d19():
    for x in DAYS:
        if weekday_name(add_days(x, 7)) != weekday_name(x): return f"x={x!r}"

if __name__ == "__main__":
    main()
