import sys, os, json, random, calendar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date, timedelta
from kit.dates import *

SEED = 12345
D0, D1 = date(2000, 1, 1), date(2030, 12, 31)

def all_dates():
    d = D0
    while d <= D1:
        yield d
        d += timedelta(days=1)

def R(ok, ce=""):
    return ("verdadeira", "") if ok else ("falsa", ce)

def eq(actual, claimed):
    return R(actual == claimed, f"actual={actual!r} claimed={claimed!r}")

def forall(pairs, pred):
    # pairs: iterable of (input, ) ; pred returns (ok, detail); exceptions => falsa
    best = None
    for x in pairs:
        try:
            ok, detail = pred(x)
        except Exception as e:
            ok, detail = False, f"raised {e!r}"
        if not ok:
            if best is None or repr(x) < repr(best[0]) and False:
                best = (x, detail)
            break
    return ("verdadeira", "") if best is None else ("falsa", f"input={best[0]!r}: {best[1]}")

def D01(): return eq(add_months(date(2024,1,31),1), date(2024,2,29))
def D02():
    def p(x):
        r = add_months(x, 12)
        return (r.day, r.month, r.year) == (x.day, x.month, x.year+1), f"add_months={r!r}"
    return forall([date(2000,2,29)] + list(all_dates()), p)
def D03():
    def p(x):
        r = add_months(add_months(x,1),-1)
        return r == x, f"result={r!r}"
    return forall([date(2000,1,29)] + list(all_dates()), p)
def D04():
    rng = random.Random(SEED)
    cases = [(date(2024,1,2), date(2024,1,1))] + [(date.fromordinal(rng.randint(1,3652059)), date.fromordinal(rng.randint(1,3652059))) for _ in range(3000)]
    return forall(cases, lambda ab: (days_between(*ab) >= 0, f"days_between={days_between(*ab)}"))
def D05():
    rng = random.Random(SEED)
    cases = [(date.min, date.max), (date.max, date.min), (date(2024,1,1),)*2] + [(date.fromordinal(rng.randint(1,3652059)), date.fromordinal(rng.randint(1,3652059))) for _ in range(3000)]
    return forall(cases, lambda ab: (days_between(*ab) == -days_between(ab[1], ab[0]), "mismatch"))
def D06(): return eq(is_leap(1900), False)
def D07(): return eq(is_leap(2000), True)
def D08(): return forall(range(1,10000), lambda y: (is_leap(y) == calendar.isleap(y), f"is_leap={is_leap(y)} calendar={calendar.isleap(y)}"))
def D09(): return eq(weekday_name(date(2024,1,1)), 'Monday')
def D10(): return eq(quarter(date(2024,4,1)), 2)
def D11(): return forall(list(all_dates()) + [date.min, date.max], lambda x: (quarter(x) in (1,2,3,4), f"quarter={quarter(x)}"))
def D12(): return eq(end_of_month(date(2023,2,10)), date(2023,2,28))
def D13(): return forall(all_dates(), lambda x: (end_of_month(x) >= x, f"eom={end_of_month(x)}"))
def D14(): return eq(iso_week(date(2021,1,1)), 1)
def D15(): return eq(parse_br('31/12/2024'), date(2024,12,31))
def D16():
    try:
        r = parse_br('1/2/2024')
    except ValueError:
        return "verdadeira", ""
    except Exception as e:
        return "falsa", f"input='1/2/2024' raised {e!r}, not ValueError"
    return "falsa", f"input='1/2/2024' returned {r!r} instead of raising ValueError"
def D17():
    # exhaustive over dates x k in [-1000,1000] is ~23M; use all dates with edge ks + random ks
    rng = random.Random(SEED)
    ks = [-1000,-1,0,1,1000]
    def p(x):
        for k in ks + [rng.randint(-1000,1000) for _ in range(20)]:
            if add_days(x,k) - x != timedelta(days=k):
                return False, f"k={k}"
        return True, ""
    return forall(all_dates(), p)
def D18():
    def p(x):
        for k in range(-30,31):
            r = add_months(x,k)
            if not r.day <= x.day:
                return False, f"k={k} result={r!r}"
        return True, ""
    return forall(all_dates(), p)
def D19(): return forall(all_dates(), lambda x: (weekday_name(add_days(x,7)) == weekday_name(x), "mismatch"))

def main():
    ids = sys.argv[1:] or [f"D{i:02d}" for i in range(1,20)]
    for i in ids:
        v, ce = globals()[i]()
        print(json.dumps({"id": i, "verdict": v, "counterexample": ce, "note": ""}))
main()
