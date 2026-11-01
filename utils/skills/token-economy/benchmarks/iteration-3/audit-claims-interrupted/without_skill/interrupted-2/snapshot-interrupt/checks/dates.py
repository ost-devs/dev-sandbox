import os, sys, random, calendar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from kit.dates import *

CMD = 'python3 -I checks/dates.py'
rng = random.Random(12345)
D0, D1 = date(2000, 1, 1), date(2030, 12, 31)
DOM = [D0 + timedelta(days=i) for i in range((D1 - D0).days + 1)]
res = {}


def run(i, f):
    """f returns None if holds, else counterexample string."""
    try:
        r = f()
    except Exception as e:
        r = 'exceção inesperada: %r' % (e,)
    res[i] = r


def eq(expr_fn, expected):
    def f():
        got = expr_fn()
        return None if got == expected else 'resultado=%r esperado=%r' % (got, expected)
    return f


def forall(items, pred, show):
    def f():
        for it in items:
            try:
                ok = pred(it)
            except Exception as e:
                return 'entrada=%r exceção=%r' % (it, e)
            if not ok:
                return show(it)
        return None
    return f


run('D01', eq(lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29)))
run('D02', forall(DOM, lambda x: (lambda r: (r.year, r.month, r.day) == (x.year + 1, x.month, x.day))(add_months(x, 12)),
    lambda x: 'add_months(%r, 12) = %r' % (x, add_months(x, 12))))
run('D03', forall(DOM, lambda x: add_months(add_months(x, 1), -1) == x,
    lambda x: 'x=%r add_months(add_months(x,1),-1)=%r' % (x, add_months(add_months(x, 1), -1))))
hand = [date(1, 1, 1), date(9999, 12, 31), date(2024, 2, 29), date(2000, 1, 1), date(2024, 12, 31)]
pairs = [(a, b) for a in hand for b in hand] + [(rng.choice(DOM), rng.choice(DOM)) for _ in range(2000)]
run('D04', forall(pairs, lambda p: days_between(*p) >= 0,
    lambda p: 'days_between(%r, %r) = %r' % (p[0], p[1], days_between(*p))))
run('D05', forall(pairs, lambda p: days_between(*p) == -days_between(p[1], p[0]),
    lambda p: 'a,b=%r' % (p,)))
run('D06', eq(lambda: is_leap(1900), False))
run('D07', eq(lambda: is_leap(2000), True))
run('D08', forall(range(1, 10000), lambda y: is_leap(y) == calendar.isleap(y),
    lambda y: 'y=%r is_leap=%r calendar.isleap=%r' % (y, is_leap(y), calendar.isleap(y))))
run('D09', eq(lambda: weekday_name(date(2024, 1, 1)), 'Monday'))
run('D10', eq(lambda: quarter(date(2024, 4, 1)), 2))
run('D11', forall(DOM + hand, lambda x: quarter(x) in (1, 2, 3, 4),
    lambda x: 'quarter(%r)=%r' % (x, quarter(x))))
run('D12', eq(lambda: end_of_month(date(2023, 2, 10)), date(2023, 2, 28)))
run('D13', forall(DOM, lambda x: end_of_month(x) >= x,
    lambda x: 'end_of_month(%r)=%r' % (x, end_of_month(x))))
run('D14', eq(lambda: iso_week(date(2021, 1, 1)), 1))
run('D15', eq(lambda: parse_br('31/12/2024'), date(2024, 12, 31)))
def d16():
    try:
        r = parse_br('1/2/2024')
    except ValueError:
        return None
    except Exception as e:
        return "parse_br('1/2/2024') levantou %r, não ValueError" % (e,)
    return "parse_br('1/2/2024') = %r (sem ValueError)" % (r,)
run('D16', d16)
def d17():
    for x in DOM:
        for k in range(-1000, 1001):
            if add_days(x, k) - x != timedelta(days=k):
                return 'x=%r k=%r add_days=%r' % (x, k, add_days(x, k))
    return None
run('D17', d17)
def d18():
    for x in DOM:
        for k in range(-30, 31):
            r = add_months(x, k)
            if not r.day <= x.day:
                return 'add_months(%r, %r) = %r' % (x, k, r)
    return None
run('D18', d18)
run('D19', forall(DOM, lambda x: weekday_name(add_days(x, 7)) == weekday_name(x),
    lambda x: 'x=%r' % (x,)))

for i in ['D%02d' % n for n in range(1, 20)]:
    r = res[i]
    print('\t'.join([i, 'verdadeira' if r is None else 'falsa', r or '', CMD]))
