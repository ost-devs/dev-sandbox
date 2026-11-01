import sys, os, random, calendar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from kit import dates as D

SEED = 12345


def days(y0=2000, y1=2030):
    d = date(y0, 1, 1)
    end = date(y1, 12, 31)
    while d <= end:
        yield d
        d += timedelta(days=1)


def run(f):
    try:
        return f()
    except Exception as e:
        return (False, "excecao inesperada: %s: %s" % (type(e).__name__, e))


def eq(expr_txt, got, exp):
    if got == exp:
        return (True, None)
    return (False, "%s -> %r vs. esperado %r" % (expr_txt, got, exp))


def check_D01():
    return eq("add_months(date(2024,1,31),1)", D.add_months(date(2024, 1, 31), 1), date(2024, 2, 29))


def check_D02():
    for x in days():
        r = D.add_months(x, 12)
        if (r.day, r.month, r.year) != (x.day, x.month, x.year + 1):
            return (False, "add_months(%r, 12) -> %r vs. esperado mesmo dia/mes em %d" % (x, r, x.year + 1))
    return (True, None)


def check_D03():
    for x in days():
        r = D.add_months(D.add_months(x, 1), -1)
        if r != x:
            return (False, "add_months(add_months(%r,1),-1) -> %r vs. esperado %r" % (x, r, x))
    return (True, None)


def check_D04():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = D.days_between(a, b)
    if r < 0:
        return (False, "days_between(%r, %r) -> %r vs. esperado >= 0" % (a, b, r))
    return (True, None)


def check_D05():
    rng = random.Random(SEED)
    pool = [date.min, date.max, date(2000, 1, 1), date(2024, 2, 29)]
    for _ in range(5000):
        pool.append(date.fromordinal(rng.randint(1, date.max.toordinal())))
    for a in pool:
        for b in pool[:60]:
            if D.days_between(a, b) != -D.days_between(b, a):
                return (False, "a=%r b=%r" % (a, b))
    return (True, None)


def check_D06():
    return eq("is_leap(1900)", D.is_leap(1900), False)


def check_D07():
    return eq("is_leap(2000)", D.is_leap(2000), True)


def check_D08():
    for y in range(1, 10000):
        if D.is_leap(y) != calendar.isleap(y):
            return (False, "is_leap(%d) -> %r vs. %r" % (y, D.is_leap(y), calendar.isleap(y)))
    return (True, None)


def check_D09():
    return eq("weekday_name(date(2024,1,1))", D.weekday_name(date(2024, 1, 1)), 'Monday')


def check_D10():
    return eq("quarter(date(2024,4,1))", D.quarter(date(2024, 4, 1)), 2)


def check_D11():
    for y in (1, 2000, 2024, 9999):
        for m in range(1, 13):
            for dd in (1, 15):
                q = D.quarter(date(y, m, dd))
                if q not in (1, 2, 3, 4):
                    return (False, "quarter(%r) -> %r" % (date(y, m, dd), q))
    return (True, None)


def check_D12():
    return eq("end_of_month(date(2023,2,10))", D.end_of_month(date(2023, 2, 10)), date(2023, 2, 28))


def check_D13():
    for x in days():
        r = D.end_of_month(x)
        if not r >= x:
            return (False, "end_of_month(%r) -> %r < x" % (x, r))
    return (True, None)


def check_D14():
    return eq("iso_week(date(2021,1,1))", D.iso_week(date(2021, 1, 1)), 1)


def check_D15():
    return eq("parse_br('31/12/2024')", D.parse_br('31/12/2024'), date(2024, 12, 31))


def check_D16():
    try:
        r = D.parse_br('1/2/2024')
    except ValueError:
        return (True, None)
    except Exception as e:
        return (False, "parse_br('1/2/2024') levantou %s em vez de ValueError" % type(e).__name__)
    return (False, "parse_br('1/2/2024') -> %r (sem ValueError) vs. esperado ValueError" % (r,))


def check_D17():
    for x in days():
        for k in range(-1000, 1001):
            if D.add_days(x, k) - x != timedelta(days=k):
                return (False, "add_days(%r, %d) - x -> %r" % (x, k, D.add_days(x, k) - x))
    return (True, None)


def check_D18():
    for x in days():
        for k in range(-30, 31):
            r = D.add_months(x, k)
            if not r.day <= x.day:
                return (False, "add_months(%r, %d).day -> %d vs. <= %d" % (x, k, r.day, x.day))
    return (True, None)


def check_D19():
    for x in days():
        if D.weekday_name(D.add_days(x, 7)) != D.weekday_name(x):
            return (False, "x=%r" % (x,))
    return (True, None)


IDS = ["D%02d" % i for i in range(1, 20)]

if __name__ == "__main__":
    want = sys.argv[1:] or IDS
    for i in want:
        ok, msg = run(globals()["check_" + i])
        print("%s\t%s\t%s" % (i, "verdadeira" if ok else "falsa", (msg or "").replace("\n", " ").replace("\t", " ")))
