from datetime import date
from harness import claim, example, forall, run
from calc.dates import *

def rand_date(r):
    return date.fromordinal(r.randint(date.min.toordinal(), date.max.toordinal()))

EDGE = [date(2024, 2, 29), date(2023, 12, 31), date(2024, 1, 31), date(1, 1, 1), date(9999, 12, 31), date(9999, 1, 1), date(2000, 2, 29)]

@claim('D1')
def _():
    return example(lambda: add_months(date(2024, 1, 31), 1), date(2024, 2, 29))

@claim('D2')
def _():
    return forall(lambda r: (rand_date(r),),
                  lambda d: (lambda e: (e.year, e.month, e.day) == (d.year + 1, d.month, d.day))(add_months(d, 12)),
                  seed=2, n=3000, cases=[(d,) for d in EDGE])

@claim('D3')
def _():
    return forall(lambda r: (rand_date(r), rand_date(r)), lambda a, b: days_between(a, b) >= 0,
                  seed=3, n=3000, cases=[(date(2024, 1, 2), date(2024, 1, 1)), (date(9999, 12, 31), date(1, 1, 1))])

@claim('D4')
def _():
    return example(lambda: is_leap(1900), False)

@claim('D5')
def _():
    return forall(lambda r: (rand_date(r),), lambda d: quarter(d) in (1, 2, 3, 4),
                  seed=5, n=3000, cases=[(d,) for d in EDGE] + [(date(2024, m, 1),) for m in range(1, 13)])

@claim('D6')
def _():
    return example(lambda: parse_iso('2026-02-30'), date(2026, 3, 2))

if __name__ == '__main__':
    run()
