"""Verify claims D1..D6 about calc/dates.py. Usage: python3 checks/check_dates.py [ID ...]"""
import os
import random
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calc.dates import add_months, days_between, is_leap, quarter, parse_iso  # noqa: E402

SEED = 20261029
TRIALS = 20000


def _call(fn, *args):
    """Return ('ok', value) or ('exc', exception)."""
    try:
        return 'ok', fn(*args)
    except Exception as e:  # noqa: BLE001
        return 'exc', e


def _fmt(kind, val):
    return repr(val) if kind == 'ok' else f'raises {type(val).__name__}: {val}'


def _args(*args):
    return ', '.join(repr(a) for a in args)


def _rand_date(rng):
    return date.fromordinal(rng.randint(date.min.toordinal(), date.max.toordinal()))


def check_D1():
    arg, exp = date(2024, 1, 31), date(2024, 2, 29)
    kind, val = _call(add_months, arg, 1)
    call = f'add_months({_args(arg, 1)}) -> {_fmt(kind, val)}'
    if kind == 'ok' and val == exp:
        return True, call
    return False, f'{call}, expected {exp!r}'


def check_D2():
    def bad(d):
        kind, val = _call(add_months, d, 12)
        if kind == 'ok' and (val.year, val.month, val.day) == (d.year + 1, d.month, d.day):
            return None
        if d.year + 1 > date.max.year:
            exp = 'no valid date (year 10000)'
        else:
            try:
                exp = repr(date(d.year + 1, d.month, d.day))
            except ValueError:
                exp = f'{d.month}/{d.day} in year {d.year + 1} (does not exist)'
        return f'add_months({_args(d, 12)}) -> {_fmt(kind, val)}, expected {exp}'

    edges = [date(2024, 2, 29), date(2023, 2, 28), date(2024, 1, 31), date(2024, 12, 31),
             date(2025, 1, 1), date.min, date.max, date(1900, 2, 28), date(2000, 2, 29)]
    for d in edges:
        r = bad(d)
        if r:
            return False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        r = bad(_rand_date(rng))
        if r:
            return False, r
    return True, f'{len(edges)} edge cases + {TRIALS} random dates (seed {SEED})'


def check_D3():
    def bad(a, b):
        kind, val = _call(days_between, a, b)
        if kind == 'ok' and val >= 0:
            return None
        return f'days_between({_args(a, b)}) -> {_fmt(kind, val)}, expected >= 0'

    edges = [(date(2024, 1, 2), date(2024, 1, 1)), (date(2024, 1, 1), date(2024, 1, 1)),
             (date.max, date.min), (date.min, date.max), (date(2025, 1, 1), date(2024, 12, 31))]
    for a, b in edges:
        r = bad(a, b)
        if r:
            return False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        r = bad(_rand_date(rng), _rand_date(rng))
        if r:
            return False, r
    return True, f'{len(edges)} edge pairs + {TRIALS} random pairs (seed {SEED})'


def check_D4():
    kind, val = _call(is_leap, 1900)
    call = f'is_leap(1900) -> {_fmt(kind, val)}'
    if kind == 'ok' and val is False:
        return True, call
    return False, f'{call}, expected False'


def check_D5():
    def bad(d):
        kind, val = _call(quarter, d)
        if kind == 'ok' and val in (1, 2, 3, 4):
            return None
        return f'quarter({d!r}) -> {_fmt(kind, val)}, expected 1..4'

    edges = [date.min, date.max, date(2024, 2, 29), date(2024, 3, 31), date(2024, 4, 1),
             date(2024, 12, 31), date(2025, 1, 1)]
    for d in edges:
        r = bad(d)
        if r:
            return False, r
    n = 0
    for year in (2023, 2024):
        d = date(year, 1, 1)
        while d.year == year:
            r = bad(d)
            if r:
                return False, r
            d += timedelta(days=1)
            n += 1
    return True, f'{len(edges)} edge cases (incl. date.min/date.max) + every day of 2023 and 2024 ({n} dates)'


def check_D6():
    arg, exp = '2026-02-30', date(2026, 3, 2)
    kind, val = _call(parse_iso, arg)
    call = f'parse_iso({arg!r}) -> {_fmt(kind, val)}'
    if kind == 'ok' and val == exp:
        return True, call
    return False, f'{call}, expected {exp!r}'


CHECKS = {'D1': check_D1, 'D2': check_D2, 'D3': check_D3,
          'D4': check_D4, 'D5': check_D5, 'D6': check_D6}


def main(argv):
    ids = argv or list(CHECKS)
    for cid in ids:
        fn = CHECKS.get(cid)
        if fn is None:
            print(f'{cid}\tFALSE\tunknown claim id')
            continue
        try:
            ok, msg = fn()
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f'checker crashed: {type(e).__name__}: {e}'
        print(f'{cid}\t{"TRUE" if ok else "FALSE"}\t{msg}')
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)
