import sys, os, json, random, calendar
from datetime import date, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.dates import *

SEED = 20261101


def days(y0=2000, y1=2030):
    d = date(y0, 1, 1)
    end = date(y1, 12, 31)
    while d <= end:
        yield d
        d += timedelta(days=1)


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def D01():
    return eq(lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29))


def D02():
    for x in days():
        r = add_months(x, 12)
        if (r.year, r.month, r.day) != (x.year + 1, x.month, x.day):
            return False, f'x={x!r}: add_months(x, 12)={r!r}, expected {date(x.year+1, x.month, x.day) if not (x.month==2 and x.day==29) else "same day/month in "+str(x.year+1)}'
    return True, None


def D03():
    for x in days():
        r = add_months(add_months(x, 1), -1)
        if r != x:
            return False, f'x={x!r}: add_months(add_months(x,1),-1)={r!r}, expected {x!r}'
    return True, None


def D04():
    rng = random.Random(SEED)
    a, b = date(2024, 1, 10), date(2024, 1, 1)
    cases = [(a, b)] + [(date.fromordinal(rng.randint(1, 3000000)), date.fromordinal(rng.randint(1, 3000000))) for _ in range(20000)]
    for a, b in cases:
        if days_between(a, b) < 0:
            return False, f'a={a!r}, b={b!r}: days_between={days_between(a, b)} (<0)'
    return True, None


def D05():
    rng = random.Random(SEED)
    cases = [(date(2024, 1, 1), date(2024, 1, 1)), (date.min, date.max)] + [(date.fromordinal(rng.randint(1, 3000000)), date.fromordinal(rng.randint(1, 3000000))) for _ in range(20000)]
    for a, b in cases:
        if days_between(a, b) != -days_between(b, a):
            return False, f'a={a!r}, b={b!r}: {days_between(a, b)} != {-days_between(b, a)}'
    return True, None


def D06():
    return eq(lambda: is_leap(1900), False)


def D07():
    return eq(lambda: is_leap(2000), True)


def D08():
    for y in range(1, 10000):
        if is_leap(y) != calendar.isleap(y):
            return False, f'y={y}: is_leap={is_leap(y)!r}, calendar.isleap={calendar.isleap(y)!r}'
    return True, None


def D09():
    return eq(lambda: weekday_name(date(2024, 1, 1)), 'Monday')


def D10():
    return eq(lambda: quarter(date(2024, 4, 1)), 2)


def D11():
    for x in days(1, 9999):
        if quarter(x) not in (1, 2, 3, 4):
            return False, f'x={x!r}: quarter={quarter(x)!r}'
    return True, None


def D12():
    return eq(lambda: end_of_month(date(2023, 2, 10)), date(2023, 2, 28))


def D13():
    for x in days():
        if not end_of_month(x) >= x:
            return False, f'x={x!r}: end_of_month={end_of_month(x)!r}'
    return True, None


def D14():
    return eq(lambda: iso_week(date(2021, 1, 1)), 1)


def D15():
    return eq(lambda: parse_br('31/12/2024'), date(2024, 12, 31))


def D16():
    try:
        r = parse_br('1/2/2024')
    except ValueError:
        return True, None
    except Exception as e:
        return False, f"parse_br('1/2/2024') raised {e!r}, expected ValueError"
    return False, f"parse_br('1/2/2024') returned {r!r} instead of raising ValueError"


def D17():
    for x in days():
        for k in range(-1000, 1001):
            if add_days(x, k) - x != timedelta(days=k):
                return False, f'x={x!r}, k={k}: {add_days(x, k) - x!r}'
    return True, None


def D18():
    for x in days():
        for k in range(-30, 31):
            try:
                r = add_months(x, k)
            except Exception as e:
                return False, f'x={x!r}, k={k}: raised {e!r}'
            if not r.day <= x.day:
                return False, f'x={x!r}, k={k}: result {r!r}'
    return True, None


def D19():
    for x in days():
        if weekday_name(add_days(x, 7)) != weekday_name(x):
            return False, f'x={x!r}'
    return True, None


CHECKS = {f'D{i:02d}': globals()[f'D{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa', 'counterexample': ce,
                          'command': f'python3 checks/check_dates.py {i}'}, ensure_ascii=False))
