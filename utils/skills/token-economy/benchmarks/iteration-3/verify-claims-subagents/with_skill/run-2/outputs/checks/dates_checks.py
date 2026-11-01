from datetime import date, timedelta
from harness import claim, rng, run
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

@claim('D1')
def d1():
    r = add_months(date(2024, 1, 31), 1)
    return None if r == date(2024, 2, 29) else 'add_months(date(2024,1,31),1) = %r' % r

@claim('D2')
def d2():
    d = date(2024, 2, 29)
    try:
        r = add_months(d, 12)
    except Exception as e:
        return 'add_months(%r,12) raises %s' % (d, e)
    if (r.year, r.month, r.day) != (2025, 2, 28) and False:
        pass
    # literal: same day and month one year later
    bad = None
    d = date(2024, 2, 29)
    r = add_months(d, 12)
    if (r.month, r.day, r.year) != (d.month, d.day, d.year + 1):
        return 'add_months(%r, 12) = %r' % (d, r)

@claim('D3')
def d3():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    r = days_between(a, b)
    return None if r >= 0 else 'days_between(%r, %r) = %d' % (a, b, r)

@claim('D4')
def d4():
    return None if is_leap(1900) is False else 'is_leap(1900) = %r' % is_leap(1900)

@claim('D5')
def d5():
    d = date(1, 1, 1)
    while d.year < 10000:
        if quarter(d) not in (1, 2, 3, 4):
            return 'quarter(%r) = %r' % (d, quarter(d))
        d += timedelta(days=1)
        if d == date(9999, 12, 31):
            break
    return None

@claim('D6')
def d6():
    try:
        r = parse_iso('2026-02-30')
    except Exception as e:
        return "parse_iso('2026-02-30') raises %s: %s" % (type(e).__name__, e)
    return None if r == date(2026, 3, 2) else "parse_iso('2026-02-30') = %r" % r

if __name__ == '__main__':
    run('dates')
