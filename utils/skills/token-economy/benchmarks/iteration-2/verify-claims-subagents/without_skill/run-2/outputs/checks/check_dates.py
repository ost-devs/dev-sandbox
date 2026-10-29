"""Deterministic verification of claims D1-D6 about calc/dates.py (stdlib only)."""
import os
import random
import sys
from datetime import date, timedelta

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKDIR)

from calc.dates import add_months, days_between, is_leap, quarter, parse_iso  # noqa: E402

SEED = 20261029
N_RANDOM = 20000
MIN_ORD = date(1, 1, 1).toordinal()
MAX_ORD = date(9999, 12, 31).toordinal()

rng = random.Random(SEED)


def rand_date():
    return date.fromordinal(rng.randint(MIN_ORD, MAX_ORD))


def report(cid, failure):
    if failure is None:
        print(f"{cid} | TRUE")
    else:
        print(f"{cid} | FALSE | counterexample: {failure}")


def call(fn, *args):
    try:
        return fn(*args), None
    except Exception as e:  # exception counts as failure
        return None, f"{type(e).__name__}: {e}"


# D1
def check_d1():
    exp = date(2024, 2, 29)
    got, err = call(add_months, date(2024, 1, 31), 1)
    if err:
        return f"add_months(date(2024, 1, 31), 1) -> raised {err} vs expected {exp!r}"
    if got != exp:
        return f"add_months(date(2024, 1, 31), 1) -> {got!r} vs expected {exp!r}"
    return None


# D2: collect all failures, then pick the clearest (prefer small year / wrong value over exception)
def check_d2():
    fixed = [
        date(2024, 2, 29), date(2000, 2, 29), date(1600, 2, 29), date(4, 2, 29),
        date(2023, 2, 28), date(2024, 2, 28), date(2024, 1, 31), date(2024, 12, 31),
        date(1, 1, 1), date(9998, 12, 31), date(9999, 1, 1), date(9999, 12, 31),
    ]
    # every day of several years including leap years
    for y in (1, 1899, 1900, 2000, 2023, 2024, 9998):
        d = date(y, 1, 1)
        while d.year == y:
            fixed.append(d)
            d += timedelta(days=1)
    candidates = fixed + [rand_date() for _ in range(N_RANDOM)]
    failures = []
    for d in candidates:
        got, err = call(add_months, d, 12)
        if err:
            failures.append((1, d, f"add_months({d!r}, 12) -> raised {err} vs expected same day/month in year {d.year + 1}"))
            continue
        if not (got.year == d.year + 1 and got.month == d.month and got.day == d.day):
            failures.append((0, d, f"add_months({d!r}, 12) -> {got!r} vs expected same day/month one year later (date({d.year + 1}, {d.month}, {d.day}) does not exist)" if (d.month, d.day) == (2, 29) else f"add_months({d!r}, 12) -> {got!r} vs expected date({d.year + 1}, {d.month}, {d.day})"))
    if not failures:
        return None
    # clearest: wrong value before exception, then most recent/familiar year near 2024
    failures.sort(key=lambda t: (t[0], abs(t[1].year - 2024), t[1]))
    first = failures[0][2]
    exc = [f for f in failures if f[0] == 1]
    if exc and failures[0][0] == 0:
        first += f"; also {exc[0][2]}"
    return first


# D3
def check_d3():
    fixed = [(date(2024, 1, 2), date(2024, 1, 1)), (date(2024, 1, 1), date(2024, 1, 1)),
             (date(1, 1, 1), date(9999, 12, 31)), (date(9999, 12, 31), date(1, 1, 1))]
    pairs = fixed + [(rand_date(), rand_date()) for _ in range(N_RANDOM)]
    failures = []
    for a, b in pairs:
        got, err = call(days_between, a, b)
        if err:
            failures.append((1, 0, f"days_between({a!r}, {b!r}) -> raised {err} vs expected >= 0"))
        elif got < 0:
            failures.append((0, -got, f"days_between({a!r}, {b!r}) -> {got} vs expected >= 0"))
    if not failures:
        return None
    failures.sort(key=lambda t: (t[0], t[1]))
    return failures[0][2]


# D4
def check_d4():
    got, err = call(is_leap, 1900)
    if err:
        return f"is_leap(1900) -> raised {err} vs expected False"
    if got is not False:
        return f"is_leap(1900) -> {got!r} vs expected False"
    return None


# D5
def check_d5():
    days = []
    for y in (1, 1900, 2000, 2023, 2024, 2100, 9999):
        d = date(y, 1, 1)
        while d.year == y:
            days.append(d)
            if d == date.max:
                break
            d += timedelta(days=1)
    days += [rand_date() for _ in range(N_RANDOM)]
    for d in days:
        got, err = call(quarter, d)
        if err:
            return f"quarter({d!r}) -> raised {err} vs expected in 1..4"
        if got not in (1, 2, 3, 4):
            return f"quarter({d!r}) -> {got!r} vs expected in 1..4"
        exp = (1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4)[d.month - 1]
        if got != exp:
            return f"quarter({d!r}) -> {got!r} vs expected {exp}"
    return None


# D6
def check_d6():
    exp = date(2026, 3, 2)
    got, err = call(parse_iso, '2026-02-30')
    if err:
        return f"parse_iso('2026-02-30') -> raised {err} vs expected {exp!r}"
    if got != exp:
        return f"parse_iso('2026-02-30') -> {got!r} vs expected {exp!r}"
    return None


if __name__ == "__main__":
    for cid, fn in (("D1", check_d1), ("D2", check_d2), ("D3", check_d3),
                    ("D4", check_d4), ("D5", check_d5), ("D6", check_d6)):
        try:
            report(cid, fn())
        except Exception as e:
            report(cid, f"checker crashed: {type(e).__name__}: {e}")
    sys.exit(0)
