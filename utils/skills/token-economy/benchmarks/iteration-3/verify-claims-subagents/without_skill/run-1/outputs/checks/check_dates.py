import sys, os
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.dates import add_months, days_between, is_leap, quarter, parse_iso

def all_days(y0, y1):
    d = date(y0, 1, 1)
    while d.year <= y1:
        yield d
        d += timedelta(days=1)

def first_counter(pred, items):
    """pred(item) -> True if ok. Exceptions count as failure."""
    for it in items:
        try:
            if not pred(it):
                return it
        except Exception as e:
            return (it, repr(e))
    return None

def out(i, ce):
    print(f"{i} VERDADEIRA" if ce is None else f"{i} FALSA contraexemplo={ce!r}")

# D1
try:
    r = add_months(date(2024, 1, 31), 1)
    out("D1", None if r == date(2024, 2, 29) else r)
except Exception as e:
    out("D1", repr(e))

# D2: todos os dias de 1896..2104 (inclui 29/fev, fins de mes, seculos) + extremos
def d2(d):
    r = add_months(d, 12)
    return (r.year, r.month, r.day) == (d.year + 1, d.month, d.day)
items = list(all_days(1896, 2104)) + [date(9999, 1, 1), date(1, 1, 1)]
ce = first_counter(d2, items)
if ce is not None and not isinstance(ce, tuple):
    ce = (ce, add_months(ce, 12))
out("D2", ce)

# D3: pares em ordem normal e invertida
pairs = [(date(2024, 1, 2), date(2024, 1, 1)), (date(2024, 1, 1), date(2024, 1, 2)),
         (date(2024, 2, 29), date(2023, 2, 28)), (date(2024, 3, 1), date(2024, 3, 1))]
ce = first_counter(lambda p: days_between(*p) >= 0, pairs)
out("D3", ce)

# D4
out("D4", None if is_leap(1900) is False else is_leap(1900))

# D5
out("D5", first_counter(lambda d: 1 <= quarter(d) <= 4, all_days(1999, 2101)))

# D6
try:
    r = parse_iso('2026-02-30')
    out("D6", None if r == date(2026, 3, 2) else r)
except Exception as e:
    out("D6", repr(e))
