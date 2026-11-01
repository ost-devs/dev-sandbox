import sys, os, json, calendar, random
from datetime import date, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.dates import *

SEED = 12345
MODULE = "dates"


def all_dates():
    d = date(2000, 1, 1)
    while d <= date(2030, 12, 31):
        yield d
        d += timedelta(days=1)


def rand_dates(n=3000):
    r = random.Random(SEED)
    base = date(1, 1, 1).toordinal()
    top = date(9999, 12, 31).toordinal()
    return [date.fromordinal(r.randint(base, top)) for _ in range(n)]


def check_D01():
    v = add_months(date(2024, 1, 31), 1)
    return (v == date(2024, 2, 29), None) if v == date(2024, 2, 29) else (False, f"add_months(2024-01-31,1)={v}")


def check_D02():
    for x in all_dates():
        y = add_months(x, 12)
        if (y.day, y.month, y.year) != (x.day, x.month, x.year + 1):
            return False, f"add_months({x},12)={y}"
    return True, None


def check_D03():
    for x in all_dates():
        y = add_months(add_months(x, 1), -1)
        if y != x:
            return False, f"x={x}: add_months(add_months(x,1),-1)={y}"
    return True, None


def check_D04():
    a, b = date(2024, 1, 2), date(2024, 1, 1)
    v = days_between(a, b)
    return (True, None) if v >= 0 else (False, f"days_between({a},{b})={v}")


def check_D05():
    ds = rand_dates() + [date(1, 1, 1), date(9999, 12, 31)]
    r = random.Random(SEED)
    for _ in range(3000):
        a, b = r.choice(ds), r.choice(ds)
        if days_between(a, b) != -days_between(b, a):
            return False, f"a={a}, b={b}"
    return True, None


def check_D06():
    return (True, None) if is_leap(1900) is False else (False, "is_leap(1900) is not False")


def check_D07():
    return (True, None) if is_leap(2000) is True else (False, "is_leap(2000) is not True")


def check_D08():
    for y in range(1, 10000):
        if is_leap(y) != calendar.isleap(y):
            return False, f"y={y}"
    return True, None


def check_D09():
    v = weekday_name(date(2024, 1, 1))
    return (True, None) if v == 'Monday' else (False, f"got {v}")


def check_D10():
    v = quarter(date(2024, 4, 1))
    return (True, None) if v == 2 else (False, f"got {v}")


def check_D11():
    for x in all_dates():
        if quarter(x) not in (1, 2, 3, 4):
            return False, f"x={x}"
    for x in rand_dates():
        if quarter(x) not in (1, 2, 3, 4):
            return False, f"x={x}"
    return True, None


def check_D12():
    v = end_of_month(date(2023, 2, 10))
    return (True, None) if v == date(2023, 2, 28) else (False, f"got {v}")


def check_D13():
    for x in all_dates():
        if end_of_month(x) < x:
            return False, f"x={x}"
    return True, None


def check_D14():
    v = iso_week(date(2021, 1, 1))
    return (True, None) if v == 1 else (False, f"iso_week(2021-01-01)={v}")


def check_D15():
    v = parse_br('31/12/2024')
    return (True, None) if v == date(2024, 12, 31) else (False, f"got {v}")


def check_D16():
    try:
        v = parse_br('1/2/2024')
    except ValueError:
        return True, None
    return False, f"parse_br('1/2/2024') returned {v} without ValueError"


def check_D17():
    for x in all_dates():
        for k in range(-1000, 1001, 37):
            if add_days(x, k) - x != timedelta(days=k):
                return False, f"x={x}, k={k}"
    r = random.Random(SEED)
    ds = list(all_dates())
    for _ in range(3000):
        x, k = r.choice(ds), r.randint(-1000, 1000)
        if add_days(x, k) - x != timedelta(days=k):
            return False, f"x={x}, k={k}"
    return True, None


def check_D18():
    for x in all_dates():
        for k in range(-30, 31):
            if add_months(x, k).day > x.day:
                return False, f"x={x}, k={k}"
    return True, None


def check_D19():
    for x in all_dates():
        if weekday_name(add_days(x, 7)) != weekday_name(x):
            return False, f"x={x}"
    return True, None


def main():
    ids = sys.argv[1:] or sorted(n[6:] for n in globals() if n.startswith("check_"))
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": None if ok else ce,
                          "command": f"python3 -I checks/dates.py {i}"}, ensure_ascii=False))


main()
