import sys, os, calendar
from datetime import date, timedelta
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)
sys.path.insert(0, CH)
from lib import Checker
sys.path.insert(0, os.path.dirname(CH))
from kit.dates import *

c = Checker("dates")
START, END = date(2000, 1, 1), date(2030, 12, 31)
NDAYS = (END - START).days + 1
def alld():
    for i in range(NDAYS): yield START + timedelta(days=i)
def gdate(rng): return (START + timedelta(days=rng.randint(0, NDAYS - 1)),)
def gany(rng): return (date(1, 1, 1) + timedelta(days=rng.randint(0, 3000000)), date(1, 1, 1) + timedelta(days=rng.randint(0, 3000000)))

def first_bad(pred):
    for x in alld():
        if not pred(x): return f"x={x}"

c.fixed("D01", lambda: None if add_months(date(2024,1,31),1) == date(2024,2,29) else str(add_months(date(2024,1,31),1)))
c.fixed("D02", lambda: first_bad(lambda x: (lambda r: r.day == x.day and r.month == x.month and r.year == x.year + 1)(add_months(x, 12))))
c.fixed("D03", lambda: first_bad(lambda x: add_months(add_months(x, 1), -1) == x))
c.prop("D04", gany, lambda a, b: days_between(a, b) >= 0)
c.prop("D05", gany, lambda a, b: days_between(a, b) == -days_between(b, a))
c.fixed("D06", lambda: None if is_leap(1900) is False else "not False")
c.fixed("D07", lambda: None if is_leap(2000) is True else "not True")
c.fixed("D08", lambda: next((f"y={y}" for y in range(1, 10000) if is_leap(y) != calendar.isleap(y)), None))
c.fixed("D09", lambda: None if weekday_name(date(2024,1,1)) == 'Monday' else weekday_name(date(2024,1,1)))
c.fixed("D10", lambda: None if quarter(date(2024,4,1)) == 2 else str(quarter(date(2024,4,1))))
c.prop("D11", gdate, lambda x: quarter(x) in (1, 2, 3, 4))
c.fixed("D12", lambda: None if end_of_month(date(2023,2,10)) == date(2023,2,28) else str(end_of_month(date(2023,2,10))))
c.fixed("D13", lambda: first_bad(lambda x: end_of_month(x) >= x))
c.fixed("D14", lambda: None if iso_week(date(2021,1,1)) == 1 else f"iso_week={iso_week(date(2021,1,1))}")
c.fixed("D15", lambda: None if parse_br('31/12/2024') == date(2024,12,31) else "mismatch")
def d16():
    try: r = parse_br('1/2/2024')
    except ValueError: return None
    return f"no ValueError; returned {r}"
c.fixed("D16", d16)
c.prop("D17", lambda rng: gdate(rng) + (rng.randint(-1000, 1000),), lambda x, k: add_days(x, k) - x == timedelta(days=k))
c.prop("D18", lambda rng: gdate(rng) + (rng.randint(-30, 30),), lambda x, k: add_months(x, k).day <= x.day)
c.fixed("D19", lambda: first_bad(lambda x: weekday_name(add_days(x, 7)) == weekday_name(x)))
c.finish()
