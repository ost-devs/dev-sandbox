import calendar
from datetime import date

NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def add_months(d, k):
    m = d.month - 1 + k
    y, m = d.year + m // 12, m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def weekday_name(d):
    return NAMES[d.weekday()]


def days_between(a, b):
    return (b - a).days


def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def quarter(d):
    return (d.month - 1) // 3 + 1


def parse_iso(s):
    return date.fromisoformat(s)
