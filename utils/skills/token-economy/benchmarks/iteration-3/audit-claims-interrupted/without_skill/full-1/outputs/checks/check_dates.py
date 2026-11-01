import os, sys, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import Results, rng
from datetime import date, timedelta
from kit.dates import *

R = Results("dates")
D0, D1 = date(2000, 1, 1), date(2030, 12, 31)
def days():
    x = D0
    while x <= D1:
        yield x
        x += timedelta(days=1)

def forall(pred):
    for x in days():
        if not pred(x):
            return False, x
    return True, None

R.check("D01", lambda: (add_months(date(2024,1,31),1) == date(2024,2,29), add_months(date(2024,1,31),1)))
R.check("D02", lambda: forall(lambda x: (lambda y: (y.day, y.month, y.year) == (x.day, x.month, x.year+1))(add_months(x,12))) if True else None)
R.check("D03", lambda: forall(lambda x: add_months(add_months(x,1),-1) == x))

def d04():
    r = rng()
    a, b = date(2024,1,2), date(2024,1,1)
    if days_between(a,b) < 0: return False, (a,b)
    return True, None
R.check("D04", d04)

def d05():
    r = rng()
    for _ in range(20000):
        a = date.fromordinal(r.randint(1, 3652059)); b = date.fromordinal(r.randint(1, 3652059))
        if days_between(a,b) != -days_between(b,a): return False, (a,b)
    a = date.min; b = date.max
    if days_between(a,b) != -days_between(b,a): return False, (a,b)
    return True, None
R.check("D05", d05)
R.check("D06", lambda: (is_leap(1900) is False, is_leap(1900)))
R.check("D07", lambda: (is_leap(2000) is True, is_leap(2000)))
R.check("D08", lambda: next(((False, y) for y in range(1,10000) if is_leap(y) != calendar.isleap(y)), (True, None)))
R.check("D09", lambda: (weekday_name(date(2024,1,1)) == 'Monday', weekday_name(date(2024,1,1))))
R.check("D10", lambda: (quarter(date(2024,4,1)) == 2, quarter(date(2024,4,1))))
R.check("D11", lambda: forall(lambda x: quarter(x) in (1,2,3,4)))
R.check("D12", lambda: (end_of_month(date(2023,2,10)) == date(2023,2,28), end_of_month(date(2023,2,10))))
R.check("D13", lambda: forall(lambda x: end_of_month(x) >= x))
R.check("D14", lambda: (iso_week(date(2021,1,1)) == 1, iso_week(date(2021,1,1))))
R.check("D15", lambda: (parse_br('31/12/2024') == date(2024,12,31), None))

def d16():
    try:
        v = parse_br('1/2/2024')
    except ValueError:
        return True, None
    return False, ("1/2/2024 -> %r, no ValueError" % v)
R.check("D16", d16)

def d17():
    for x in days():
        for k in range(-1000, 1001):
            if add_days(x,k) - x != timedelta(days=k): return False, (x,k)
    return True, None
R.check("D17", d17)

def d18():
    for x in days():
        for k in range(-30, 31):
            if add_months(x,k).day > x.day: return False, (x,k)
    return True, None
R.check("D18", d18)
R.check("D19", lambda: forall(lambda x: weekday_name(add_days(x,7)) == weekday_name(x)))
R.finish()
