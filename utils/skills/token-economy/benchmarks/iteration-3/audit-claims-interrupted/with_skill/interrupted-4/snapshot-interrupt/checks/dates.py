import calendar
from datetime import date, timedelta
from lib import ints, first_fail, eq, rng
from kit.dates import *

D0 = date(2000, 1, 1)
ALL = [D0 + timedelta(days=i) for i in range((date(2030, 12, 31) - D0).days + 1)]


def rdates(tag, n=3000):
    r = rng(tag)
    for _ in range(n):
        yield date(1900, 1, 1) + timedelta(days=r.randint(0, 80000))


def rpairs(tag):
    r = rdates(tag + 'a')
    s = rdates(tag + 'b')
    yield (date(2024, 1, 2), date(2024, 1, 1))
    yield from zip(r, s)


def d16():
    try:
        v = parse_br('1/2/2024')
    except ValueError:
        return None
    except Exception as e:
        return f'raised {type(e).__name__}'
    return f"parse_br('1/2/2024') returned {v!r}, no ValueError"


def d17():
    ks = list(ints('d17', n=40, lo=-1000, hi=1000))
    return first_fail(((x, k) for x in ALL[::7] for k in ks), lambda c: add_days(c[0], c[1]) - c[0] == timedelta(days=c[1]))


def d18():
    ks = list(ints('d18', n=30, lo=-30, hi=30)) + list(range(-30, 31))
    return first_fail(((x, k) for x in ALL[::3] for k in ks), lambda c: add_months(c[0], c[1]).day <= c[0].day)


CHECKS = {
    'D01': lambda: eq(lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29), 'add_months(2024-01-31,1)'),
    'D02': lambda: first_fail(ALL, lambda x: add_months(x, 12) == date(x.year + 1, x.month, x.day) if not (x.month == 2 and x.day == 29) else add_months(x, 12) == date(x.year + 1, 2, x.day)),
    'D03': lambda: first_fail(ALL, lambda x: add_months(add_months(x, 1), -1) == x),
    'D04': lambda: first_fail(rpairs('d4'), lambda p: days_between(*p) >= 0),
    'D05': lambda: first_fail(rpairs('d5'), lambda p: days_between(*p) == -days_between(p[1], p[0])),
    'D06': lambda: eq(lambda: is_leap(1900), False, 'is_leap(1900)'),
    'D07': lambda: eq(lambda: is_leap(2000), True, 'is_leap(2000)'),
    'D08': lambda: first_fail(range(1, 10000), lambda y: is_leap(y) == calendar.isleap(y)),
    'D09': lambda: eq(lambda: weekday_name(date(2024, 1, 1)), 'Monday', 'weekday_name(2024-01-01)'),
    'D10': lambda: eq(lambda: quarter(date(2024, 4, 1)), 2, 'quarter(2024-04-01)'),
    'D11': lambda: first_fail(rdates('d11'), lambda x: quarter(x) in (1, 2, 3, 4)),
    'D12': lambda: eq(lambda: end_of_month(date(2023, 2, 10)), date(2023, 2, 28), 'end_of_month(2023-02-10)'),
    'D13': lambda: first_fail(ALL, lambda x: end_of_month(x) >= x),
    'D14': lambda: eq(lambda: iso_week(date(2021, 1, 1)), 1, 'iso_week(2021-01-01)'),
    'D15': lambda: eq(lambda: parse_br('31/12/2024'), date(2024, 12, 31), "parse_br('31/12/2024')"),
    'D16': d16,
    'D17': d17,
    'D18': d18,
    'D19': lambda: first_fail(ALL, lambda x: weekday_name(add_days(x, 7)) == weekday_name(x)),
}
