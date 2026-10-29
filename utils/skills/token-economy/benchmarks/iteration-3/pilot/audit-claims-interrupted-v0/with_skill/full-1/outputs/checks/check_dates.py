from common import *
from kit.dates import *
from datetime import date, timedelta
import calendar

D0, D1 = date(2000, 1, 1), date(2030, 12, 31)
ALL = [D0 + timedelta(days=i) for i in range((D1 - D0).days + 1)]  # exhaustive 2000-2030

def dates(cid, n=5000):
    r = rng(cid)
    return [date(1, 1, 1) + timedelta(days=r.randint(0, 3_000_000)) for _ in range(n)]

@claim('D01')
def _(): return eq(lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
@claim('D02')
def _(): return forall(ALL, lambda x: (lambda y: (y.year, y.month, y.day) == (x.year + 1, x.month, x.day))(add_months(x, 12)))
@claim('D03')
def _(): return forall(ALL, lambda x: add_months(add_months(x, 1), -1) == x)
@claim('D04')
def _(): return forall([(date(2024, 1, 2), date(2024, 1, 1))] + [(a, b) for a, b in zip(dates('D04'), dates('D04b'))], lambda a, b: days_between(a, b) >= 0)
@claim('D05')
def _(): return forall(zip(dates('D05'), dates('D05b')), lambda a, b: days_between(a, b) == -days_between(b, a))
@claim('D06')
def _(): return eq(lambda: is_leap(1900), False)
@claim('D07')
def _(): return eq(lambda: is_leap(2000), True)
@claim('D08')
def _(): return forall(range(1, 10000), lambda y: is_leap(y) == calendar.isleap(y))
@claim('D09')
def _(): return eq(lambda: weekday_name(date(2024, 1, 1)), 'Monday')
@claim('D10')
def _(): return eq(lambda: quarter(date(2024, 4, 1)), 2)
@claim('D11')
def _(): return forall(ALL + dates('D11'), lambda x: quarter(x) in (1, 2, 3, 4))
@claim('D12')
def _(): return eq(lambda: end_of_month(date(2023, 2, 10)), date(2023, 2, 28))
@claim('D13')
def _(): return forall(ALL + dates('D13'), lambda x: end_of_month(x) >= x)
@claim('D14')
def _(): return eq(lambda: iso_week(date(2021, 1, 1)), 1)
@claim('D15')
def _(): return eq(lambda: parse_br('31/12/2024'), date(2024, 12, 31))
@claim('D16')
def _(): return raises(lambda: parse_br('1/2/2024'), ValueError)
@claim('D17')
def _():
    r = rng('D17')
    ins = [(x, r.randint(-100000, 100000)) for x in dates('D17', 3000)]
    ins = [(x, k) for x, k in ins if date.min <= x + timedelta(0) and 1 <= (x.toordinal() + k) <= date.max.toordinal()]  # result representable
    return forall(ins, lambda x, k: add_days(x, k) - x == timedelta(days=k))
@claim('D18')
def _():
    r = rng('D18')
    ins = [(x, r.randint(-2000, 2000)) for x in ALL[::7]]
    ins = [(x, k) for x, k in ins if 1 <= x.year * 12 + x.month - 1 + k < 9999 * 12]
    return forall(ins, lambda x, k: add_months(x, k).day <= x.day)
@claim('D19')
def _(): return forall([x for x in ALL + dates('D19') if x < date(9999, 12, 1)], lambda x: weekday_name(add_days(x, 7)) == weekday_name(x))

if __name__ == '__main__': main('dates')
