import sys, os, random, datetime
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

SEED = 20240229
rng = random.Random(SEED)

def out(i, ok, detail):
    print(i, 'TRUE' if ok else 'FALSE', detail)

def first_cex(pred, items):
    for it in items:
        try:
            if not pred(it):
                return it
        except Exception as e:
            return (it, 'EXC', repr(e))
    return None

def all_dates(y0, y1):
    d = date(y0, 1, 1)
    end = date(y1, 12, 31)
    while True:
        yield d
        if d >= end:
            return
        d += timedelta(days=1)

# D1
try:
    r = add_months(date(2024, 1, 31), 1)
    out('D1', r == date(2024, 2, 29), 'got %r' % (r,))
except Exception as e:
    out('D1', False, repr(e))

# D2: exhaustive years 1..2100 plus seeded random + extremes
def d2(d):
    r = add_months(d, 12)
    return (r.year, r.month, r.day) == (d.year + 1, d.month, d.day)
c = first_cex(d2, all_dates(1, 2100))
if c is None:
    rand = [date.fromordinal(rng.randint(1, date.max.toordinal())) for _ in range(20000)]
    c = first_cex(d2, rand + [date(9999, 1, 1), date.max])
if c is None: out('D2', True, 'no counterexample (sweep years 1-2100 + 20000 random seed=%d)' % SEED)
else:
    d = c if isinstance(c, date) else c[0]
    try: got = repr(add_months(d, 12))
    except Exception as e: got = 'EXC ' + repr(e)
    out('D2', False, 'd=%r add_months(d,12)=%s' % (d, got))

# D3
adv = [(date(2024, 1, 2), date(2024, 1, 1)), (date(2024, 3, 1), date(2024, 2, 29)), (date.max, date.min)]
adv += [(date.fromordinal(rng.randint(1, date.max.toordinal())), date.fromordinal(rng.randint(1, date.max.toordinal()))) for _ in range(20000)]
c = first_cex(lambda p: days_between(*p) >= 0, adv)
if c is None: out('D3', True, 'no counterexample')
else: out('D3', False, 'days_between%r = %r' % (c, days_between(*c)))

# D4
try: out('D4', is_leap(1900) is False, 'is_leap(1900)=%r' % is_leap(1900))
except Exception as e: out('D4', False, repr(e))

# D5: exhaustive over all dates
bad = None
for d in all_dates(1, 9999):
    q = quarter(d)
    if not (isinstance(q, int) and 1 <= q <= 4):
        bad = (d, q); break
if bad is None: out('D5', True, 'all dates 0001-01-01..9999-12-31 give 1..4')
else: out('D5', False, 'quarter%r' % (bad,))

# D6
try:
    r = parse_iso('2026-02-30')
    out('D6', r == date(2026, 3, 2), 'got %r' % (r,))
except Exception as e:
    out('D6', False, "parse_iso('2026-02-30') raised %r" % e)
sys.exit(0)
