import calendar
from datetime import date, datetime, timedelta

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def add_days(d, n):
    return d + timedelta(days=n)


def add_months(d, n):
    m = d.month - 1 + n
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def days_between(a, b):
    return (b - a).days


def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def weekday_name(d):
    return WEEKDAYS[d.weekday()]


def quarter(d):
    return (d.month - 1) // 3 + 1


def end_of_month(d):
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])


def iso_week(d):
    return d.isocalendar()[1]


def parse_br(s):
    return datetime.strptime(s, '%d/%m/%Y').date()
