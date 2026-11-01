import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from common import rng, report, ROOT
sys.path.insert(0, ROOT)
from datetime import date, timedelta
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

def rdates(r, n):
    lo = date(1, 1, 1).toordinal(); hi = date(9999, 12, 31).toordinal()
    return [date.fromordinal(r.randint(lo, hi)) for _ in range(n)]

EDGE = [date(2024,2,29), date(2023,2,28), date(2024,1,31), date(2024,12,31), date(1900,2,28),
        date(2000,2,29), date(1,1,1), date(9999,12,31), date(2023,3,31), date(2024,1,1)]

def first_fail(cands, pred):
    """smallest (by sorted order) candidate where pred fails or raises"""
    for c in (sorted(set(cands)) if not isinstance(cands[0], tuple) else cands):
        try:
            if not pred(c):
                return c, None
        except Exception as e:
            return c, f"raises {type(e).__name__}: {e}"
    return None

def emit(cid, res, fmt):
    if res is None: report(cid, True)
    else: report(cid, False, fmt(*res))

# D1
try: ok = add_months(date(2024,1,31),1) == date(2024,2,29); ex = add_months(date(2024,1,31),1)
except Exception as e: ok, ex = False, f"raises {e}"
report('D1', ok, '' if ok else f"add_months(2024-01-31,1)={ex}")

# D2
r = rng('D2')
c = EDGE + rdates(r, 5000) + [date(y,2,29) for y in range(4,9997,4) if y%100 or y%400==0]
def p2(d):
    n = add_months(d, 12)
    return (n.year, n.month, n.day) == (d.year+1, d.month, d.day)
emit('D2', first_fail(c, p2), lambda d,e: f"add_months({d},12)=" + (e or str(add_months(d,12))))

# D3
r = rng('D3')
pairs = [(date(2024,2,29), date(2024,2,28)), (date(2024,1,1), date(2023,12,31)), (date(2024,3,1), date(2024,2,29)),
         (date(2024,1,1), date(2024,1,1))] + [tuple(rdates(r,2)) for _ in range(2000)]
pairs.sort(key=lambda p: abs((p[1]-p[0]).days))
emit('D3', first_fail(pairs, lambda p: days_between(*p) >= 0),
     lambda p,e: f"days_between({p[0]},{p[1]})=" + (e or str(days_between(*p))))

# D4
try: ok = is_leap(1900) is False
except Exception as e: ok = False
report('D4', ok, '' if ok else f"is_leap(1900)={is_leap(1900)}")

# D5
c = EDGE + rdates(rng('D5'), 5000) + [date(2024,m,d) for m in range(1,13) for d in (1,28)]
emit('D5', first_fail(c, lambda d: quarter(d) in (1,2,3,4)), lambda d,e: f"quarter({d})=" + (e or str(quarter(d))))

# D6
s = '2026-02-30'
try:
    v = parse_iso(s); ok = v == date(2026,3,2); ex = f"parse_iso({s!r})={v}"
except Exception as e:
    ok, ex = False, f"parse_iso({s!r}) raises {type(e).__name__}: {e}"
report('D6', ok, '' if ok else ex)
