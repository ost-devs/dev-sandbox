import sys, os, calendar
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from datetime import date, timedelta
from kit import dates as D

START, END = date(2000, 1, 1), date(2030, 12, 31)
NDAYS = (END - START).days + 1
ALL = [START + timedelta(days=i) for i in range(NDAYS)]

def rdate(r, lo=date.min, hi=date.max):
    return lo + timedelta(days=r.randint(0, (hi - lo).days))

def forall(cid, pred, n=3000):
    """exhaustive over 2000-2030 dates; pred(x) -> None if ok else message"""
    for x in ALL:
        m = pred(x)
        if m is not None: return (False, m)
    return True

@claim('D01')
def d01(): return D.add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)

@claim('D02')
def d02():
    def p(x):
        y = D.add_months(x, 12)
        if (y.day, y.month, y.year) != (x.day, x.month, x.year + 1): return f"{x} -> {y}"
    return forall('D02', p)

@claim('D03')
def d03():
    def p(x):
        y = D.add_months(D.add_months(x, 1), -1)
        if y != x: return f"{x} -> {y}"
    return forall('D03', p)

@claim('D04')
def d04():
    r = rng('D04')
    cases = [(date(2024,1,2), date(2024,1,1)), (date.max, date.min)]
    cases += [(rdate(r), rdate(r)) for _ in range(2000)]
    for a, b in cases:
        v = D.days_between(a, b)
        if v < 0: return (False, f"({a}, {b}) -> {v}")
    return True

@claim('D05')
def d05():
    r = rng('D05')
    cases = [(date.min, date.max), (date(2024,1,1), date(2024,1,1))]
    cases += [(rdate(r), rdate(r)) for _ in range(2000)]
    for a, b in cases:
        if D.days_between(a, b) != -D.days_between(b, a): return (False, f"({a}, {b})")
    return True

@claim('D06')
def d06(): return D.is_leap(1900) is False

@claim('D07')
def d07(): return D.is_leap(2000) is True

@claim('D08')
def d08():
    for y in range(1, 10000):
        if D.is_leap(y) != calendar.isleap(y): return (False, f"{y} -> {D.is_leap(y)}")
    return True

@claim('D09')
def d09(): return D.weekday_name(date(2024, 1, 1)) == 'Monday'

@claim('D10')
def d10(): return D.quarter(date(2024, 4, 1)) == 2

@claim('D11')
def d11():
    r = rng('D11')
    for x in [date.min, date.max] + ALL + [rdate(r) for _ in range(2000)]:
        if D.quarter(x) not in (1, 2, 3, 4): return (False, f"{x} -> {D.quarter(x)}")
    return True

@claim('D12')
def d12(): return D.end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)

@claim('D13')
def d13():
    def p(x):
        if not D.end_of_month(x) >= x: return f"{x} -> {D.end_of_month(x)}"
    return forall('D13', p)

@claim('D14')
def d14():
    v = D.iso_week(date(2021, 1, 1))
    return True if v == 1 else (False, f"iso_week(2021-01-01) -> {v}")

@claim('D15')
def d15(): return D.parse_br('31/12/2024') == date(2024, 12, 31)

@claim('D16')
def d16():
    try:
        v = D.parse_br('1/2/2024')
    except ValueError:
        return True
    return (False, f"parse_br('1/2/2024') -> {v!r} (no ValueError)")

@claim('D17')
def d17():
    r = rng('D17')
    ks = [-1000, 1000, 0, 1, -1]
    for x in (START, END, date(2024, 2, 29)):
        for k in ks + list(range(-1000, 1001, 7)):
            if D.add_days(x, k) - x != timedelta(days=k): return (False, f"({x}, {k})")
    for _ in range(20000):
        x, k = r.choice(ALL), r.randint(-1000, 1000)
        if D.add_days(x, k) - x != timedelta(days=k): return (False, f"({x}, {k})")
    return True

@claim('D18')
def d18():
    r = rng('D18')
    for x in ALL:
        for k in (-30, -13, -12, -1, 0, 1, 12, 13, 30, r.randint(-30, 30), r.randint(-30, 30)):
            y = D.add_months(x, k)
            if not y.day <= x.day: return (False, f"({x}, {k}) -> {y}")
    return True

@claim('D19')
def d19():
    def p(x):
        if D.weekday_name(D.add_days(x, 7)) != D.weekday_name(x): return str(x)
    return forall('D19', p)

if __name__ == '__main__': run(__file__)
