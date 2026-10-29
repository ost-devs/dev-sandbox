import sys, os, json, random, calendar
from datetime import date, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
import dates as K

SEED = 20240229
START, END = date(2000, 1, 1), date(2030, 12, 31)

def days(a=START, b=END):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)

def res(ok, ce=None):
    return (ok, None if ok else ce)

def rand_dates(n, rng):
    lo, hi = date(1, 1, 1).toordinal(), date(9999, 12, 31).toordinal()
    return [date.fromordinal(rng.randint(lo, hi)) for _ in range(n)]

def D01(): 
    r = K.add_months(date(2024, 1, 31), 1)
    return res(r == date(2024, 2, 29), f"add_months(2024-01-31,1)={r!r}, esperado 2024-02-29")
def D02():
    for x in days():
        r = K.add_months(x, 12)
        if (r.year, r.month, r.day) != (x.year + 1, x.month, x.day):
            return res(False, f"add_months({x!r},12)={r!r}, esperado dia/mes iguais em {x.year+1}")
    return res(True)
def D03():
    for x in days():
        r = K.add_months(K.add_months(x, 1), -1)
        if r != x:
            return res(False, f"add_months(add_months({x!r},1),-1)={r!r}, esperado {x!r}")
    return res(True)
def D04():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = K.days_between(a, b)
    return res(r >= 0, f"days_between({a!r},{b!r})={r}, esperado >=0")
def D05():
    rng = random.Random(SEED)
    ds = [date.min, date.max, date(2000, 1, 1), date(2024, 2, 29)] + rand_dates(2000, rng)
    for i in range(0, len(ds) - 1):
        for a, b in ((ds[i], ds[i+1]), (ds[i], ds[i])):
            if K.days_between(a, b) != -K.days_between(b, a):
                return res(False, f"a={a!r}, b={b!r}")
    return res(True)
def D06(): r = K.is_leap(1900); return res(r is False, f"is_leap(1900)={r!r}")
def D07(): r = K.is_leap(2000); return res(r is True, f"is_leap(2000)={r!r}")
def D08():
    for y in range(1, 10000):
        if K.is_leap(y) != calendar.isleap(y):
            return res(False, f"is_leap({y})={K.is_leap(y)}, calendar.isleap={calendar.isleap(y)}")
    return res(True)
def D09(): r = K.weekday_name(date(2024, 1, 1)); return res(r == 'Monday', f"got {r!r}")
def D10(): r = K.quarter(date(2024, 4, 1)); return res(r == 2, f"got {r!r}")
def D11():
    for x in days(date(1, 1, 1), date(9999, 12, 31)) if False else [date(y, m, 1) for y in range(1, 10000) for m in range(1, 13)] + [date(y, m, calendar.monthrange(y, m)[1]) for y in range(1, 10000) for m in range(1, 13)]:
        if K.quarter(x) not in (1, 2, 3, 4):
            return res(False, f"quarter({x!r})={K.quarter(x)}")
    return res(True)
def D12(): r = K.end_of_month(date(2023, 2, 10)); return res(r == date(2023, 2, 28), f"got {r!r}")
def D13():
    for x in days():
        if not K.end_of_month(x) >= x:
            return res(False, f"end_of_month({x!r})={K.end_of_month(x)!r}")
    return res(True)
def D14(): r = K.iso_week(date(2021, 1, 1)); return res(r == 1, f"iso_week(2021-01-01)={r}, esperado 1")
def D15(): r = K.parse_br('31/12/2024'); return res(r == date(2024, 12, 31), f"got {r!r}")
def D16():
    try:
        r = K.parse_br('1/2/2024')
    except ValueError:
        return res(True)
    except Exception as e:
        return res(False, f"parse_br('1/2/2024') levantou {type(e).__name__}, esperado ValueError")
    return res(False, f"parse_br('1/2/2024')={r!r}, esperado ValueError")
def D17():
    for x in days():
        for k in range(-1000, 1001):
            if K.add_days(x, k) - x != timedelta(days=k):
                return res(False, f"x={x!r}, k={k}, got {K.add_days(x,k)-x!r}")
    return res(True)
def D18():
    for x in days():
        for k in range(-30, 31):
            r = K.add_months(x, k)
            if not r.day <= x.day:
                return res(False, f"x={x!r}, k={k}, got {r!r}")
    return res(True)
def D19():
    for x in days():
        if K.weekday_name(K.add_days(x, 7)) != K.weekday_name(x):
            return res(False, f"x={x!r}")
    return res(True)

CHECKS = {f"D{i:02d}": globals()[f"D{i:02d}"] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))
