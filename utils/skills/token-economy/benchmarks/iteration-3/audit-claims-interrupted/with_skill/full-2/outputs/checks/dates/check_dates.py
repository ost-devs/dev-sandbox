import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.dates import *
import calendar
from datetime import date, timedelta

def alld():
    d = date(2000,1,1)
    while d <= date(2030,12,31):
        yield d
        d += timedelta(days=1)

def anyd(r):
    return date.fromordinal(r.randint(1, 3000000))

@claim("D01")
def d01(): assert add_months(date(2024,1,31),1) == date(2024,2,29)

@claim("D02")
def d02():
    for x in alld():
        y = add_months(x,12)
        if (y.year,y.month,y.day) != (x.year+1,x.month,x.day):
            raise Counter(f"x={x} got {y}, expected same day/month in {x.year+1}")

@claim("D03")
def d03():
    for x in alld():
        y = add_months(add_months(x,1),-1)
        if y != x: raise Counter(f"x={x} got {y}")

@claim("D04")
def d04():
    a,b = date(2024,1,2), date(2024,1,1)
    if days_between(a,b) < 0: raise Counter(f"a={a} b={b} got {days_between(a,b)}")

@claim("D05")
def d05():
    forall("D05", lambda r:(anyd(r),anyd(r)), lambda a,b: days_between(a,b) == -days_between(b,a))

@claim("D06")
def d06(): assert is_leap(1900) is False

@claim("D07")
def d07(): assert is_leap(2000) is True

@claim("D08")
def d08():
    for y in range(1,10000):
        if is_leap(y) != calendar.isleap(y): raise Counter(f"y={y}")

@claim("D09")
def d09(): assert weekday_name(date(2024,1,1)) == 'Monday'

@claim("D10")
def d10(): assert quarter(date(2024,4,1)) == 2

@claim("D11")
def d11():
    forall("D11", lambda r:(anyd(r),), lambda x: quarter(x) in (1,2,3,4))

@claim("D12")
def d12(): assert end_of_month(date(2023,2,10)) == date(2023,2,28)

@claim("D13")
def d13():
    for x in alld():
        if not end_of_month(x) >= x: raise Counter(f"x={x}")

@claim("D14")
def d14(): assert iso_week(date(2021,1,1)) == 1, f"got {iso_week(date(2021,1,1))}"

@claim("D15")
def d15(): assert parse_br('31/12/2024') == date(2024,12,31)

@claim("D16")
def d16():
    try: v = parse_br('1/2/2024')
    except ValueError: return
    raise Counter(f"parse_br('1/2/2024') returned {v} instead of raising ValueError")

@claim("D17")
def d17():
    for x in alld():
        for k in range(-1000,1001,37):
            if add_days(x,k)-x != timedelta(days=k): raise Counter(f"x={x} k={k}")
    for k in (-1000,1000,0,1,-1):
        for x in (date(2000,1,1),date(2030,12,31)):
            assert add_days(x,k)-x == timedelta(days=k)

@claim("D18")
def d18():
    for x in alld():
        for k in range(-30,31):
            y = add_months(x,k)
            if not y.day <= x.day: raise Counter(f"x={x} k={k} got {y}")

@claim("D19")
def d19():
    for x in alld():
        if weekday_name(add_days(x,7)) != weekday_name(x): raise Counter(f"x={x}")

if __name__=='__main__': main('dates')
