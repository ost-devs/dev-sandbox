import sys, os, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from datetime import date, timedelta
from kit.dates import *

LO, HI = date(2000, 1, 1).toordinal(), date(2030, 12, 31).toordinal()
def rd(r): return date.fromordinal(r.randint(LO, HI))
def rd_any(r): return date.fromordinal(r.randint(1, date.max.toordinal()))

@exact
def D01(): return add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)

@prop
def D02(r):
    x = rd(r); y = add_months(x, 12)
    if not (y.day == x.day and y.month == x.month and y.year == x.year + 1):
        return 'x=%r add_months(x,12)=%r' % (x, y)

@prop
def D03(r):
    x = rd(r); y = add_months(add_months(x, 1), -1)
    if y != x: return 'x=%r result=%r' % (x, y)

@prop
def D04(r):
    a, b = rd_any(r), rd_any(r); v = days_between(a, b)
    if v < 0: return 'a=%r b=%r days_between=%r' % (a, b, v)

@prop
def D05(r):
    a, b = rd_any(r), rd_any(r)
    if days_between(a, b) != -days_between(b, a): return 'a=%r b=%r' % (a, b)

@exact
def D06(): return is_leap(1900) is False
@exact
def D07(): return is_leap(2000) is True

@exact
def D08():
    for y in range(1, 10000):
        if is_leap(y) != calendar.isleap(y): return (False, 'y=%d is_leap=%r' % (y, is_leap(y)))
    return True

@exact
def D09(): return weekday_name(date(2024, 1, 1)) == 'Monday'
@exact
def D10(): return quarter(date(2024, 4, 1)) == 2

@prop
def D11(r):
    x = rd_any(r); q = quarter(x)
    if q not in (1, 2, 3, 4): return 'x=%r quarter=%r' % (x, q)

@exact
def D12(): return end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)

@prop
def D13(r):
    x = rd(r)
    if not end_of_month(x) >= x: return 'x=%r' % (x,)

@exact
def D14():
    v = iso_week(date(2021, 1, 1))
    return (v == 1, 'iso_week=%r' % v)

@exact
def D15(): return parse_br('31/12/2024') == date(2024, 12, 31)

@exact
def D16():
    try: v = parse_br('1/2/2024')
    except ValueError: return True
    return (False, "no ValueError; returned %r" % (v,))

@prop
def D17(r):
    x = rd(r); k = r.randint(-1000, 1000)
    if add_days(x, k) - x != timedelta(days=k): return 'x=%r k=%r' % (x, k)

@prop
def D18(r):
    x = rd(r); k = r.randint(-30, 30); y = add_months(x, k)
    if not y.day <= x.day: return 'x=%r k=%r result=%r' % (x, k, y)

@prop
def D19(r):
    x = rd(r)
    if weekday_name(add_days(x, 7)) != weekday_name(x): return 'x=%r' % (x,)

run({k: v for k, v in globals().items() if k[0] == 'D' and k[1:].isdigit()})
