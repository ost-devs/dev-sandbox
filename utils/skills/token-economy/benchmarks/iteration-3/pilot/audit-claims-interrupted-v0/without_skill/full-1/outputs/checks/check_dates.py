from harness import *
from datetime import date, timedelta
import calendar
from kit.dates import *

D0 = date(2000, 1, 1)
DAYS_2000_2030 = [D0 + timedelta(days=i) for i in range((date(2030, 12, 31) - D0).days + 1)]


def rand_dates(cid, n=3000):
    r = rng(cid)
    return [date.fromordinal(r.randint(1, date.max.toordinal())) for _ in range(n)]


@claim('D01')
def _(): return eq('add_months(2024-01-31, 1)', lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
@claim('D02')
def _(): return forall(DAYS_2000_2030, lambda x: (lambda y: (y.year, y.month, y.day) == (x.year + 1, x.month, x.day) or f'add_months = {y}')(add_months(x, 12)))
@claim('D03')
def _(): return forall(DAYS_2000_2030, lambda x: add_months(add_months(x, 1), -1) == x or f'ida e volta = {add_months(add_months(x, 1), -1)}')
@claim('D04')
def _():
    r = rng('D04')
    return forall([(date.fromordinal(r.randint(700000, 740000)), date.fromordinal(r.randint(700000, 740000))) for _ in range(2000)],
                  lambda a, b: days_between(a, b) >= 0 or f'days_between = {days_between(a, b)}')
@claim('D05')
def _():
    r = rng('D05')
    return forall([(date.fromordinal(r.randint(1, date.max.toordinal())), date.fromordinal(r.randint(1, date.max.toordinal()))) for _ in range(5000)],
                  lambda a, b: days_between(a, b) == -days_between(b, a))
@claim('D06')
def _(): return eq('is_leap(1900)', lambda: is_leap(1900), False)
@claim('D07')
def _(): return eq('is_leap(2000)', lambda: is_leap(2000), True)
@claim('D08')
def _(): return forall(range(1, 10000), lambda y: is_leap(y) == calendar.isleap(y))
@claim('D09')
def _(): return eq('weekday_name(2024-01-01)', lambda: weekday_name(date(2024, 1, 1)), 'Monday')
@claim('D10')
def _(): return eq('quarter(2024-04-01)', lambda: quarter(date(2024, 4, 1)), 2)
@claim('D11')
def _(): return forall(DAYS_2000_2030 + rand_dates('D11'), lambda x: quarter(x) in (1, 2, 3, 4))
@claim('D12')
def _(): return eq('end_of_month(2023-02-10)', lambda: end_of_month(date(2023, 2, 10)), date(2023, 2, 28))
@claim('D13')
def _(): return forall(DAYS_2000_2030 + rand_dates('D13'), lambda x: end_of_month(x) >= x)
@claim('D14')
def _(): return eq('iso_week(2021-01-01)', lambda: iso_week(date(2021, 1, 1)), 1)
@claim('D15')
def _(): return eq("parse_br('31/12/2024')", lambda: parse_br('31/12/2024'), date(2024, 12, 31))
@claim('D16')
def _(): return raises("parse_br('1/2/2024')", lambda: parse_br('1/2/2024'), ValueError)
@claim('D17')
def _():
    # domínio: resultado representável como date (fora disso é OverflowError do próprio datetime)
    r = rng('D17')
    cases = []
    for x in rand_dates('D17', 3000):
        k = r.randint(-800000, 800000)
        if 1 <= x.toordinal() + k <= date.max.toordinal():
            cases.append((x, k))
    return forall(cases, lambda x, k: add_days(x, k) - x == timedelta(days=k))
@claim('D18')
def _():
    r = rng('D18')
    cases = [(x, k) for x in DAYS_2000_2030[::7] for k in range(-30, 31)]
    cases += [(x, r.randint(-1000, 1000)) for x in rand_dates('D18', 1500) if 600 < x.year < 9000]
    return forall(cases, lambda x, k: add_months(x, k).day <= x.day)
@claim('D19')
def _():
    return forall([x for x in DAYS_2000_2030 + rand_dates('D19') if x.toordinal() + 7 <= date.max.toordinal()],
                  lambda x: weekday_name(add_days(x, 7)) == weekday_name(x))

if __name__ == '__main__':
    sys.exit(main())
