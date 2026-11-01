import os, sys, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import dates as D
from datetime import date, timedelta

ALL = [date(2000, 1, 1) + timedelta(days=i) for i in range((date(2030, 12, 31) - date(2000, 1, 1)).days + 1)]

def first(pred_cex, items=ALL):
    for x in items:
        c = pred_cex(x)
        if c is not None: return c
    return None

def rdate(r): return date.fromordinal(r.randint(1, 3000000))

@claim("D01")
def d01(): return eq(D.add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
@claim("D02")
def d02():
    def f(x):
        y = D.add_months(x, 12)
        return None if (y.year, y.month, y.day) == (x.year + 1, x.month, x.day) else f"x={x} got {y}"
    return first(f)
@claim("D03")
def d03():
    def f(x):
        y = D.add_months(D.add_months(x, 1), -1)
        return None if y == x else f"x={x} got {y}"
    return first(f)
@claim("D04")
def d04():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    return None if D.days_between(a, b) >= 0 else f"days_between({a}, {b}) = {D.days_between(a, b)}"
@claim("D05")
def d05(): return forall(lambda r: (rdate(r), rdate(r)), lambda a, b: D.days_between(a, b) == -D.days_between(b, a))
@claim("D06")
def d06(): return eq(D.is_leap(1900), False)
@claim("D07")
def d07(): return eq(D.is_leap(2000), True)
@claim("D08")
def d08():
    for y in range(1, 10000):
        if D.is_leap(y) != calendar.isleap(y): return f"y={y} got {D.is_leap(y)}"
@claim("D09")
def d09(): return eq(D.weekday_name(date(2024, 1, 1)), 'Monday')
@claim("D10")
def d10(): return eq(D.quarter(date(2024, 4, 1)), 2)
@claim("D11")
def d11(): return first(lambda x: None if D.quarter(x) in (1, 2, 3, 4) else f"x={x} got {D.quarter(x)}")
@claim("D12")
def d12(): return eq(D.end_of_month(date(2023, 2, 10)), date(2023, 2, 28))
@claim("D13")
def d13(): return first(lambda x: None if D.end_of_month(x) >= x else f"x={x}")
@claim("D14")
def d14(): return eq(D.iso_week(date(2021, 1, 1)), 1)
@claim("D15")
def d15(): return eq(D.parse_br('31/12/2024'), date(2024, 12, 31))
@claim("D16")
def d16():
    try: v = D.parse_br('1/2/2024')
    except ValueError: return None
    return f"parse_br('1/2/2024') returned {v!r} without ValueError"
@claim("D17")
def d17():
    for x in ALL[::7] + [date(2030, 12, 31), date(2000, 1, 1)]:
        for k in range(-1000, 1001):
            if D.add_days(x, k) - x != timedelta(days=k): return f"x={x} k={k}"
@claim("D18")
def d18():
    for x in ALL:
        for k in range(-30, 31):
            if D.add_months(x, k).day > x.day: return f"x={x} k={k} got {D.add_months(x, k)}"
@claim("D19")
def d19(): return first(lambda x: None if D.weekday_name(D.add_days(x, 7)) == D.weekday_name(x) else f"x={x}")

if __name__ == "__main__":
    main("dates")
