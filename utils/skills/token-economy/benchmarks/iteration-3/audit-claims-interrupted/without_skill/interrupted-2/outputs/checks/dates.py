import sys, os, random, calendar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from kit.dates import *

CMD = 'python3 -I checks/dates.py'
START, END = date(2000, 1, 1), date(2030, 12, 31)
def alldays():
    d = START
    while d <= END:
        yield d
        d += timedelta(days=1)

def safe(f):
    try:
        return f()
    except Exception as e:
        return 'EXC ' + repr(e)

R = {}
def claim(i):
    def deco(f):
        try:
            r = f()
        except Exception as e:
            r = 'exception: ' + repr(e)
        R[i] = r
        return f
    return deco

def eq(expr_repr, got, want):
    return None if got == want else '%s -> %r (esperado %r)' % (expr_repr, got, want)

rng = random.Random(12345)
rand_dates = [date(1, 1, 1), date(9999, 12, 31), date(2024, 2, 29), date(2000, 2, 29)] + \
    [date.fromordinal(rng.randint(1, 3652059)) for _ in range(2000)]

@claim('D01')
def _(): return eq('add_months(date(2024,1,31),1)', add_months(date(2024,1,31),1), date(2024,2,29))

@claim('D02')
def _():
    for x in alldays():
        r = safe(lambda: add_months(x, 12))
        if r != 'x' and (isinstance(r, str) or (r.day, r.month, r.year) != (x.day, x.month, x.year + 1)):
            return 'x=%r add_months(x,12) -> %r' % (x, r)

@claim('D03')
def _():
    for x in alldays():
        r = add_months(add_months(x, 1), -1)
        if r != x:
            return 'x=%r add_months(add_months(x,1),-1) -> %r' % (x, r)

@claim('D04')
def _():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = days_between(a, b)
    if r < 0: return 'days_between(%r, %r) -> %r' % (a, b, r)

@claim('D05')
def _():
    ds = rand_dates[:300] + [date(2024,1,1), date(2024,1,2)]
    for a in ds:
        for b in ds[:40]:
            if days_between(a, b) != -days_between(b, a):
                return 'a=%r b=%r' % (a, b)

@claim('D06')
def _(): return eq('is_leap(1900)', is_leap(1900), False)
@claim('D07')
def _(): return eq('is_leap(2000)', is_leap(2000), True)
@claim('D08')
def _():
    for y in range(1, 10000):
        if is_leap(y) != calendar.isleap(y):
            return 'is_leap(%r) -> %r' % (y, is_leap(y))
@claim('D09')
def _(): return eq('weekday_name(date(2024,1,1))', weekday_name(date(2024,1,1)), 'Monday')
@claim('D10')
def _(): return eq('quarter(date(2024,4,1))', quarter(date(2024,4,1)), 2)
@claim('D11')
def _():
    for x in rand_dates + [date(2024, m, 1) for m in range(1, 13)] + [date(2024, m, 28) for m in range(1, 13)]:
        if quarter(x) not in (1, 2, 3, 4):
            return 'quarter(%r) -> %r' % (x, quarter(x))
@claim('D12')
def _(): return eq('end_of_month(date(2023,2,10))', end_of_month(date(2023,2,10)), date(2023,2,28))
@claim('D13')
def _():
    for x in alldays():
        if not end_of_month(x) >= x:
            return 'end_of_month(%r) -> %r' % (x, end_of_month(x))
@claim('D14')
def _(): return eq('iso_week(date(2021,1,1))', iso_week(date(2021,1,1)), 1)
@claim('D15')
def _(): return eq("parse_br('31/12/2024')", parse_br('31/12/2024'), date(2024,12,31))
@claim('D16')
def _():
    try:
        r = parse_br('1/2/2024')
    except ValueError:
        return None
    return "parse_br('1/2/2024') -> %r (nao levantou ValueError)" % (r,)
@claim('D17')
def _():
    for x in alldays():
        for k in (-1000, -999, -365, -1, 0, 1, 7, 365, 999, 1000):
            if add_days(x, k) - x != timedelta(days=k):
                return 'x=%r k=%r' % (x, k)
    # varredura completa de k em amostra de datas
    for x in alldays():
        if x.toordinal() % 97 == 0:
            for k in range(-1000, 1001):
                if add_days(x, k) - x != timedelta(days=k):
                    return 'x=%r k=%r' % (x, k)
@claim('D18')
def _():
    for x in alldays():
        for k in range(-30, 31):
            r = add_months(x, k)
            if not r.day <= x.day:
                return 'x=%r k=%r add_months -> %r' % (x, k, r)
@claim('D19')
def _():
    for x in alldays():
        if weekday_name(add_days(x, 7)) != weekday_name(x):
            return 'x=%r' % (x,)

for i in range(1, 20):
    k = 'D%02d' % i
    r = R[k]
    if r is None:
        print('%s\tverdadeira\t\t%s' % (k, CMD))
    else:
        print('%s\tfalsa\t%s\t%s' % (k, r.replace('\t', ' ').replace('\n', ' '), CMD))
