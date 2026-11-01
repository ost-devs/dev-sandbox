import sys, os, random, calendar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from datetime import date, timedelta
from _lib import Checker
from kit.dates import *
c = Checker('dates')
D0 = date(2000, 1, 1)
ALL = [D0 + timedelta(days=i) for i in range((date(2030, 12, 31) - D0).days + 1)]
R = random.Random(1905)
PAIRS = [(date(2024,1,1), date(2024,1,1)), (date(2024,1,2), date(2024,1,1)), (date(2024,1,1), date(2024,1,2))] + \
        [(R.choice(ALL), R.choice(ALL)) for _ in range(2000)]

@c.claim('D01')
def _(): return c.eq(add_months(date(2024,1,31),1), date(2024,2,29))
@c.claim('D02')
def _(): return c.forall(ALL, lambda x: (lambda y: (y.day, y.month, y.year) == (x.day, x.month, x.year+1))(add_months(x,12)))
@c.claim('D03')
def _(): return c.forall(ALL, lambda x: add_months(add_months(x,1),-1) == x)
@c.claim('D04')
def _(): return c.forall(PAIRS, lambda p: days_between(*p) >= 0)
@c.claim('D05')
def _(): return c.forall(PAIRS, lambda p: days_between(*p) == -days_between(p[1], p[0]))
@c.claim('D06')
def _(): return c.eq(is_leap(1900), False)
@c.claim('D07')
def _(): return c.eq(is_leap(2000), True)
@c.claim('D08')
def _(): return c.forall(range(1,10000), lambda y: is_leap(y) == calendar.isleap(y))
@c.claim('D09')
def _(): return c.eq(weekday_name(date(2024,1,1)), 'Monday')
@c.claim('D10')
def _(): return c.eq(quarter(date(2024,4,1)), 2)
@c.claim('D11')
def _(): return c.forall(ALL, lambda x: quarter(x) in (1,2,3,4))
@c.claim('D12')
def _(): return c.eq(end_of_month(date(2023,2,10)), date(2023,2,28))
@c.claim('D13')
def _(): return c.forall(ALL, lambda x: end_of_month(x) >= x)
@c.claim('D14')
def _(): return c.eq(iso_week(date(2021,1,1)), 1)
@c.claim('D15')
def _(): return c.eq(parse_br('31/12/2024'), date(2024,12,31))
@c.claim('D16')
def _():
    try: r = parse_br('1/2/2024')
    except ValueError: return c.ok()
    return c.fail(f"parse_br('1/2/2024') returned {r!r}, no ValueError")
@c.claim('D17')
def _():
    for x in ALL:
        for k in range(-1000, 1001):
            if add_days(x,k) - x != timedelta(days=k): return c.fail(f'x={x!r}, k={k}')
    return c.ok('all x, all k')
@c.claim('D18')
def _():
    for x in ALL:
        for k in range(-30, 31):
            if add_months(x,k).day > x.day: return c.fail(f'x={x!r}, k={k}')
    return c.ok('all x, all k')
@c.claim('D19')
def _(): return c.forall(ALL, lambda x: weekday_name(add_days(x,7)) == weekday_name(x))
c.main()
