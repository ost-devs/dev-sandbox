import calendar, json, os, random, sys
from datetime import date, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit import dates as D

SEED = 20240229
N = 5000
LO, HI = date(2000, 1, 1), date(2030, 12, 31)
SPAN = (HI - LO).days


def rdates(rng, n=N):
    return [LO + timedelta(days=rng.randrange(SPAN + 1)) for _ in range(n)]


def edge_dates():
    e = [LO, HI, date(2000, 2, 29), date(2004, 2, 29), date(2024, 2, 29), date(2023, 2, 28),
         date(2024, 1, 31), date(2023, 1, 31), date(2030, 12, 31), date(2001, 1, 1)]
    return e


def all_dates():
    rng = random.Random(SEED)
    return edge_dates() + rdates(rng)


def universal(pred, items):
    """pred(item) -> None if ok, else string counterexample. Exceptions count as false."""
    for it in items:
        try:
            r = pred(it)
        except Exception as ex:
            return "entrada=%r excecao=%s: %s" % (it, type(ex).__name__, ex)
        if r is not None:
            return r
    return None


def point(f):
    try:
        return f()
    except Exception as ex:
        return "excecao %s: %s" % (type(ex).__name__, ex)


def eq(expr, got, want):
    return None if got == want else "%s -> %r (esperado %r)" % (expr, got, want)


def D01():
    return eq("add_months(date(2024,1,31),1)", D.add_months(date(2024, 1, 31), 1), date(2024, 2, 29))


def D02():
    def p(x):
        r = D.add_months(x, 12)
        if (r.day, r.month, r.year) != (x.day, x.month, x.year + 1):
            return "add_months(%r, 12) -> %r" % (x, r)
    # minimal first: leap days
    return universal(p, [date(2000, 2, 29)] + all_dates())


def D03():
    def p(x):
        r = D.add_months(D.add_months(x, 1), -1)
        if r != x:
            return "add_months(add_months(%r, 1), -1) -> %r" % (x, r)
    return universal(p, [date(2000, 1, 29), date(2000, 1, 30), date(2000, 1, 31)] + all_dates())


def D04():
    rng = random.Random(SEED)
    pairs = [(date(2000, 1, 2), date(2000, 1, 1))] + [(a, b) for a, b in zip(rdates(rng), rdates(rng))]

    def p(ab):
        r = D.days_between(*ab)
        if r < 0:
            return "days_between(%r, %r) -> %r" % (ab[0], ab[1], r)
    return universal(p, pairs)


def D05():
    rng = random.Random(SEED)
    pairs = [(date.min, date.max), (date.max, date.min), (date(2000, 1, 1), date(2000, 1, 1))]
    for _ in range(N):
        pairs.append((date.fromordinal(rng.randint(1, date.max.toordinal())),
                      date.fromordinal(rng.randint(1, date.max.toordinal()))))
    pairs += list(zip(rdates(rng), rdates(rng)))

    def p(ab):
        a, b = ab
        x, y = D.days_between(a, b), D.days_between(b, a)
        if x != -y:
            return "days_between(%r,%r)=%r, days_between(%r,%r)=%r" % (a, b, x, b, a, y)
    return universal(p, pairs)


def D06():
    return eq("is_leap(1900)", D.is_leap(1900), False)


def D07():
    return eq("is_leap(2000)", D.is_leap(2000), True)


def D08():
    def p(y):
        r = D.is_leap(y)
        if r != calendar.isleap(y):
            return "is_leap(%d) -> %r, calendar.isleap -> %r" % (y, r, calendar.isleap(y))
    return universal(p, range(1, 10000))


def D09():
    return eq("weekday_name(date(2024,1,1))", D.weekday_name(date(2024, 1, 1)), "Monday")


def D10():
    return eq("quarter(date(2024,4,1))", D.quarter(date(2024, 4, 1)), 2)


def D11():
    rng = random.Random(SEED)
    items = [date(y, m, 1) for y in (1, 2000, 9999) for m in range(1, 13)]
    items += [date.fromordinal(rng.randint(1, date.max.toordinal())) for _ in range(N)]

    def p(x):
        r = D.quarter(x)
        if r not in (1, 2, 3, 4):
            return "quarter(%r) -> %r" % (x, r)
    return universal(p, items)


def D12():
    return eq("end_of_month(date(2023,2,10))", D.end_of_month(date(2023, 2, 10)), date(2023, 2, 28))


def D13():
    def p(x):
        r = D.end_of_month(x)
        if not r >= x:
            return "end_of_month(%r) -> %r" % (x, r)
    return universal(p, all_dates())


def D14():
    return eq("iso_week(date(2021,1,1))", D.iso_week(date(2021, 1, 1)), 1)


def D15():
    return eq("parse_br('31/12/2024')", D.parse_br("31/12/2024"), date(2024, 12, 31))


def D16():
    try:
        r = D.parse_br("1/2/2024")
    except ValueError:
        return None
    except Exception as ex:
        return "parse_br('1/2/2024') levantou %s (esperado ValueError): %s" % (type(ex).__name__, ex)
    return "parse_br('1/2/2024') -> %r (nao levantou ValueError)" % (r,)


def D17():
    rng = random.Random(SEED)
    items = [(x, k) for x in edge_dates() for k in (-1000, -1, 0, 1, 1000)]
    items += [(x, rng.randint(-1000, 1000)) for x in rdates(rng)]

    def p(xk):
        x, k = xk
        r = D.add_days(x, k) - x
        if r != timedelta(days=k):
            return "add_days(%r, %d) - x -> %r" % (x, k, r)
    return universal(p, items)


def D18():
    rng = random.Random(SEED)
    items = [(x, k) for x in edge_dates() for k in (-30, -12, -1, 0, 1, 12, 30)]
    items += [(x, rng.randint(-30, 30)) for x in rdates(rng)]

    def p(xk):
        x, k = xk
        r = D.add_months(x, k)
        if not r.day <= x.day:
            return "add_months(%r, %d) -> %r" % (x, k, r)
    return universal(p, items)


def D19():
    def p(x):
        r = D.weekday_name(D.add_days(x, 7))
        if r != D.weekday_name(x):
            return "x=%r: %r vs %r" % (x, r, D.weekday_name(x))
    return universal(p, all_dates())


def main():
    ids = sorted(k for k in globals() if k[0] == "D" and k[1:].isdigit())
    if len(sys.argv) > 1:
        ids = [i for i in sys.argv[1:] if i in ids]
    for i in ids:
        ce = point(globals()[i])
        print(json.dumps({"id": i, "verdict": "verdadeira" if ce is None else "falsa",
                          "counterexample": ce}, ensure_ascii=False))


main()
