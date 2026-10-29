"""Builds files/ (package kit/ + claims.md) and truth.json for this case.

Each claim carries the verdict expected by reading the code and a check that
decides it by running the code; the build fails if the two disagree.
Run: python3 -I build_files.py
"""
import importlib
import itertools
import json
import random
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = HERE / "files"

MODULES = {
    "text": '''import re
import unicodedata


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def truncate(s, n, suffix='...'):
    return s if len(s) <= n else s[:n - len(suffix)] + suffix


def count_words(s):
    return len(s.split())


def title_case(s):
    return ' '.join(w[:1].upper() + w[1:] for w in s.split(' '))


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def pad_left(s, n, ch=' '):
    return s.rjust(n, ch)


def is_palindrome(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
''',
    "numbers": '''def clamp(x, lo, hi):
    return max(lo, min(x, hi))


def mean(xs):
    return sum(xs) / len(xs) if xs else 0


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def round_half(x):
    return round(x)


def percent(part, total, digits=1):
    return round(100 * part / total, digits)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5)):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def digits_sum(n):
    return sum(int(c) for c in str(n))
''',
    "dates": '''import calendar
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
''',
    "lists": '''def chunk(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def dedupe(xs):
    return list(dict.fromkeys(xs))


def flatten(xs):
    return [y for x in xs for y in x]


def top_n(xs, n):
    return sorted(xs, reverse=True)[:n]


def rotate(xs, k):
    return xs[k:] + xs[:k]


def interleave(a, b):
    return [x for pair in zip(a, b) for x in pair]


def frequencies(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


def pairwise(xs):
    return list(zip(xs, xs[1:]))
''',
    "money": '''def to_cents(s):
    reais, _, cents = s.partition(',')
    return int(reais.replace('.', '')) * 100 + int(cents.ljust(2, '0')[:2])


def format_brl(cents):
    return 'R$ ' + f'{cents // 100:,}'.replace(',', '.') + f',{cents % 100:02d}'


def split_bill(total, n):
    return [total // n] * n


def installments(total, n):
    base, rest = divmod(total, n)
    return [base + 1 if i < rest else base for i in range(n)]


def apply_discount(cents, pct):
    return round(cents * (100 - pct) / 100)


def add_tax(cents, rate):
    return int(cents * (1 + rate))
''',
    "intervals": '''def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def length(a):
    return a[1] - a[0]


def contains(a, x):
    return a[0] <= x <= a[1]


def merge(intervals):
    s = sorted(intervals)
    out = [s[0]]
    for start, end in s[1:]:
        last_start, last_end = out[-1]
        if start <= last_end:
            out[-1] = (last_start, max(last_end, end))
        else:
            out.append((start, end))
    return out


def intersect(a, b):
    if not overlaps(a, b):
        return None
    return (max(a[0], b[0]), min(a[1], b[1]))


def total_covered(intervals):
    return sum(length(i) for i in merge(intervals))
''',
    "paths": '''def join(*parts):
    return '/'.join(p.strip('/') for p in parts if p)


def ext(p):
    return p.rsplit('.', 1)[1] if '.' in p else ''


def stem(name):
    return name.rsplit('.', 1)[0]


def normalize(p):
    absolute = p.startswith('/')
    stack = []
    for part in p.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if stack:
                stack.pop()
            continue
        stack.append(part)
    body = '/'.join(stack)
    if absolute:
        return '/' + body
    return body or '.'


def is_hidden(p):
    return p.rstrip('/').rsplit('/', 1)[-1].startswith('.')


def depth(p):
    return len([x for x in p.split('/') if x])


def parent(p):
    return p.rsplit('/', 1)[0] if '/' in p else ''
''',
    "records": '''def parse_kv(s):
    return dict(pair.split('=', 1) for pair in s.split(';') if pair)


def to_kv(d):
    return ';'.join(f'{k}={v}' for k, v in d.items())


def pick(d, keys):
    return {k: d[k] for k in keys if k in d}


def rename(d, mapping):
    return {mapping.get(k, k): v for k, v in d.items()}


def group_by(rows, key):
    out = {}
    for r in rows:
        out.setdefault(r[key], []).append(r)
    return out


def sort_by(rows, key):
    return sorted(rows, key=lambda r: r[key])


def deep_get(d, path, default=None):
    for part in path.split('.'):
        if not isinstance(d, dict) or part not in d:
            return default
        d = d[part]
    return d
''',
}

R = random.Random(20261029)


def ints(lo, hi, k=400):
    return [R.randint(lo, hi) for _ in range(k)]


def int_lists(k=400, maxlen=8, lo=-5, hi=5):
    return [[R.randint(lo, hi) for _ in range(R.randint(0, maxlen))] for _ in range(k)]


def strs(k=600):
    alphabet = 'abcXYZ -_.!çãéßøİ\t\n09'
    return ['', '-', 'ß', 'ßa', 'İ', 'a-', '-a'] + [
        ''.join(R.choice(alphabet) for _ in range(R.randint(0, 10))) for _ in range(k)]


def all_dates():
    from datetime import date, timedelta
    d = date(2000, 1, 1)
    out = []
    while d <= date(2030, 12, 31):
        out.append(d)
        d += timedelta(days=1)
    return out


def raises(f, exc=Exception):
    try:
        f()
    except exc:
        return True
    return False


def safe(pred):
    """A universal claim fails on an exception, too."""
    def run(*a):
        try:
            return pred(*a)
        except Exception:
            return False
    return run


def forall(xs, pred):
    p = safe(pred)
    return all(p(x) for x in xs)


def build_claims(m):
    t, n, d, l, mo, iv, p, r = (m[k] for k in MODULES)
    from datetime import date, timedelta
    import calendar
    dates = all_dates()
    pairs = [(R.choice(dates), R.choice(dates)) for _ in range(2000)]
    ivs = [(a, a + R.randint(1, 6)) for a in ints(-5, 10, 300)]
    iv_lists = [[(a, a + R.randint(1, 5)) for a in ints(-5, 15, R.randint(1, 6))] for _ in range(300)]
    names = ['a', 'bb', 'c1', 'x.y', 'a.b.c', 'dir.d/arq', '.env', 'z']
    path_alpha = ['a', 'b', '.', '..', '']
    paths_gen = ['/'.join(c) for k in range(1, 5) for c in itertools.product(path_alpha, repeat=k)]
    paths_gen += ['/' + x for x in paths_gen]
    words = ['a', 'b', 'x1', 'k', 'zz', '9']
    simple_dicts = [{R.choice(words): R.choice(words) for _ in range(R.randint(0, 4))} for _ in range(300)]
    any_dicts = [{'k': 'a;b'}] + [{R.choice(['a', 'b']): R.choice(['1', 'x;y', '=', '']) for _ in range(R.randint(0, 3))} for _ in range(300)]
    rows = [[{'t': R.choice('xyz'), 'v': i} for i in range(R.randint(0, 6))] for _ in range(300)]

    return [
        # text
        ("T01", "text", "`slugify('Café Noir') == 'cafe-noir'`.", False, lambda: t.slugify('Café Noir') == 'cafe-noir'),
        ("T02", "text", "`slugify(s)` never starts or ends with `-`, for any string `s`.", True, lambda: forall(strs(), lambda s: not t.slugify(s).startswith('-') and not t.slugify(s).endswith('-'))),
        ("T03", "text", "`slugify(s)` contains only `a-z`, `0-9` and `-`, for any string `s`.", True, lambda: forall(strs(), lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in t.slugify(s)))),
        ("T04", "text", "`slugify(slugify(s)) == slugify(s)` for any string `s`.", True, lambda: forall(strs(), lambda s: t.slugify(t.slugify(s)) == t.slugify(s))),
        ("T05", "text", "`len(truncate(s, n)) <= n` for every string `s` and every integer `n >= 0`.", False, lambda: forall([(s, k) for s in strs(100) for k in range(0, 8)], lambda a: len(t.truncate(*a)) <= a[1])),
        ("T06", "text", "`truncate('abcdef', 5) == 'ab...'`.", True, lambda: t.truncate('abcdef', 5) == 'ab...'),
        ("T07", "text", "`truncate(s, n) == s` whenever `len(s) <= n`.", True, lambda: forall([(s, len(s) + k) for s in strs(200) for k in range(3)], lambda a: t.truncate(*a) == a[0])),
        ("T08", "text", "`count_words('a  b\\tc\\n') == 3`.", True, lambda: t.count_words('a  b\tc\n') == 3),
        ("T09", "text", "`count_words('') == 0`.", True, lambda: t.count_words('') == 0),
        ("T10", "text", "`title_case('a  b') == 'A  B'` (the double space is kept).", True, lambda: t.title_case('a  b') == 'A  B'),
        ("T11", "text", "`title_case('élan vital') == 'Élan Vital'`.", True, lambda: t.title_case('élan vital') == 'Élan Vital'),
        ("T12", "text", "`len(title_case(s)) == len(s)` for any string `s`.", False, lambda: forall(strs(), lambda s: len(t.title_case(s)) == len(s))),
        ("T13", "text", "`strip_accents('Ação') == 'Acao'`.", True, lambda: t.strip_accents('Ação') == 'Acao'),
        ("T14", "text", "`strip_accents('ø') == 'o'`.", False, lambda: t.strip_accents('ø') == 'o'),
        ("T15", "text", "`pad_left('7', 3, '0') == '007'`.", True, lambda: t.pad_left('7', 3, '0') == '007'),
        ("T16", "text", "`len(pad_left(s, n)) == max(len(s), n)` for any string `s` and integer `n >= 0`.", True, lambda: forall([(s, k) for s in strs(100) for k in range(0, 12)], lambda a: len(t.pad_left(*a)) == max(len(a[0]), a[1]))),
        ("T17", "text", "`is_palindrome('')` is `True`.", True, lambda: t.is_palindrome('') is True),
        ("T18", "text", "`is_palindrome('A man, a plan, a canal: Panama')` is `True`.", True, lambda: t.is_palindrome('A man, a plan, a canal: Panama') is True),
        ("T19", "text", "`is_palindrome(s) == is_palindrome(s[::-1])` for any string `s`.", True, lambda: forall(strs(), lambda s: t.is_palindrome(s) == t.is_palindrome(s[::-1]))),
        # numbers
        ("N01", "numbers", "For integers `lo <= hi`, `clamp(x, lo, hi)` is always within `[lo, hi]`.", True, lambda: forall([(x, a, a + b) for x, a, b in zip(ints(-20, 20), ints(-10, 10), ints(0, 10))], lambda v: v[1] <= n.clamp(*v) <= v[2])),
        ("N02", "numbers", "`clamp(5, 10, 0) == 0`.", False, lambda: n.clamp(5, 10, 0) == 0),
        ("N03", "numbers", "`mean([]) == 0`.", True, lambda: n.mean([]) == 0),
        ("N04", "numbers", "`mean([1, 2]) == 1.5`.", True, lambda: n.mean([1, 2]) == 1.5),
        ("N05", "numbers", "`median([3, 1, 2]) == 2`.", True, lambda: n.median([3, 1, 2]) == 2),
        ("N06", "numbers", "`median([])` returns `None`.", False, lambda: (not raises(lambda: n.median([]))) and n.median([]) is None),
        ("N07", "numbers", "`median(xs) == median(sorted(xs))` for every non-empty list of integers `xs`.", True, lambda: forall([x for x in int_lists() if x], lambda x: n.median(x) == n.median(sorted(x)))),
        ("N08", "numbers", "`round_half(2.5) == 3`.", False, lambda: n.round_half(2.5) == 3),
        ("N09", "numbers", "`round_half(3.5) == 4`.", True, lambda: n.round_half(3.5) == 4),
        ("N10", "numbers", "`percent(1, 3) == 33.3`.", True, lambda: n.percent(1, 3) == 33.3),
        ("N11", "numbers", "`percent(x, 0)` returns `0.0` for any number `x`.", False, lambda: forall([0, 1, 5], lambda x: n.percent(x, 0) == 0.0)),
        ("N12", "numbers", "`is_prime(n)` is correct for every `n` from 0 to 1000.", False, lambda: forall(range(1001), lambda k: n.is_prime(k) == (k > 1 and all(k % i for i in range(2, k))))),
        ("N13", "numbers", "`is_prime(97)` is `True`.", True, lambda: n.is_prime(97) is True),
        ("N14", "numbers", "`is_prime(2)` is `True`.", True, lambda: n.is_prime(2) is True),
        ("N15", "numbers", "`gcd(a, b) == gcd(b, a)` for all integers `a`, `b` in `[-50, 50]`.", False, lambda: forall([(a, b) for a in range(-50, 51) for b in range(-50, 51)], lambda v: n.gcd(*v) == n.gcd(v[1], v[0]))),
        ("N16", "numbers", "`gcd(12, 18) == 6`.", True, lambda: n.gcd(12, 18) == 6),
        ("N17", "numbers", "`gcd(a, 0) == a` for every integer `a`.", True, lambda: forall(range(-200, 201), lambda a: n.gcd(a, 0) == a)),
        ("N18", "numbers", "`digits_sum(1234) == 10`.", True, lambda: n.digits_sum(1234) == 10),
        ("N19", "numbers", "`digits_sum(n)` returns a non-negative integer for every integer `n`.", False, lambda: forall(range(-50, 51), lambda k: n.digits_sum(k) >= 0)),
        # dates
        ("D01", "dates", "`add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)`.", True, lambda: d.add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)),
        ("D02", "dates", "For every date `x` from 2000 to 2030, `add_months(x, 12)` has the same day and month as `x`, one year later.", False, lambda: forall(dates, lambda x: d.add_months(x, 12) == date(x.year + 1, x.month, x.day))),
        ("D03", "dates", "`add_months(add_months(x, 1), -1) == x` for every date `x` from 2000 to 2030.", False, lambda: forall(dates, lambda x: d.add_months(d.add_months(x, 1), -1) == x)),
        ("D04", "dates", "`days_between(a, b)` is never negative.", False, lambda: forall(pairs, lambda v: d.days_between(*v) >= 0)),
        ("D05", "dates", "`days_between(a, b) == -days_between(b, a)` for all dates `a`, `b`.", True, lambda: forall(pairs, lambda v: d.days_between(*v) == -d.days_between(v[1], v[0]))),
        ("D06", "dates", "`is_leap(1900)` is `False`.", True, lambda: d.is_leap(1900) is False),
        ("D07", "dates", "`is_leap(2000)` is `True`.", True, lambda: d.is_leap(2000) is True),
        ("D08", "dates", "`is_leap(y) == calendar.isleap(y)` for every year `y` from 1 to 9999.", True, lambda: forall(range(1, 10000), lambda y: d.is_leap(y) == calendar.isleap(y))),
        ("D09", "dates", "`weekday_name(date(2024, 1, 1)) == 'Monday'`.", True, lambda: d.weekday_name(date(2024, 1, 1)) == 'Monday'),
        ("D10", "dates", "`quarter(date(2024, 4, 1)) == 2`.", True, lambda: d.quarter(date(2024, 4, 1)) == 2),
        ("D11", "dates", "`quarter(x)` is always one of 1, 2, 3, 4.", True, lambda: forall(dates, lambda x: d.quarter(x) in (1, 2, 3, 4))),
        ("D12", "dates", "`end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)`.", True, lambda: d.end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)),
        ("D13", "dates", "`end_of_month(x) >= x` for every date `x` from 2000 to 2030.", True, lambda: forall(dates, lambda x: d.end_of_month(x) >= x)),
        ("D14", "dates", "`iso_week(date(2021, 1, 1)) == 1`.", False, lambda: d.iso_week(date(2021, 1, 1)) == 1),
        ("D15", "dates", "`parse_br('31/12/2024') == date(2024, 12, 31)`.", True, lambda: d.parse_br('31/12/2024') == date(2024, 12, 31)),
        ("D16", "dates", "`parse_br('1/2/2024')` raises `ValueError` (day and month need two digits).", False, lambda: raises(lambda: d.parse_br('1/2/2024'), ValueError)),
        ("D17", "dates", "`add_days(x, k) - x == timedelta(days=k)` for every date `x` from 2000 to 2030 and integer `k` from -1000 to 1000.", True, lambda: forall([(x, k) for x, k in zip(R.sample(dates, 400), ints(-1000, 1000))], lambda v: d.add_days(*v) - v[0] == timedelta(days=v[1]))),
        ("D18", "dates", "`add_months(x, k).day <= x.day` for every date `x` from 2000 to 2030 and integer `k` from -30 to 30.", True, lambda: forall([(x, k) for x, k in zip(R.sample(dates, 400), ints(-30, 30))], lambda v: d.add_months(*v).day <= v[0].day)),
        ("D19", "dates", "`weekday_name(add_days(x, 7)) == weekday_name(x)` for every date `x` from 2000 to 2030.", True, lambda: forall(dates, lambda x: d.weekday_name(d.add_days(x, 7)) == d.weekday_name(x))),
        # lists
        ("L01", "lists", "`chunk(list(range(7)), 3) == [[0, 1, 2], [3, 4, 5], [6]]`.", True, lambda: l.chunk(list(range(7)), 3) == [[0, 1, 2], [3, 4, 5], [6]]),
        ("L02", "lists", "`flatten(chunk(xs, k)) == xs` for every list of integers `xs` and integer `k >= 1`.", True, lambda: forall([(x, k) for x in int_lists(100) for k in range(1, 5)], lambda v: l.flatten(l.chunk(*v)) == v[0])),
        ("L03", "lists", "`chunk(xs, 0)` raises `ValueError`.", True, lambda: raises(lambda: l.chunk([1, 2], 0), ValueError) and raises(lambda: l.chunk([], 0), ValueError)),
        ("L04", "lists", "`dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]`.", True, lambda: l.dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]),
        ("L05", "lists", "For every list of integers, `dedupe` keeps the order of first occurrences.", True, lambda: forall(int_lists(), lambda x: l.dedupe(x) == [v for i, v in enumerate(x) if v not in x[:i]])),
        ("L06", "lists", "`len(dedupe(xs)) == len(set(xs))` for every list of integers `xs`.", True, lambda: forall(int_lists(), lambda x: len(l.dedupe(x)) == len(set(x)))),
        ("L07", "lists", "`flatten([[1, [2]], [3]]) == [1, 2, 3]`.", False, lambda: l.flatten([[1, [2]], [3]]) == [1, 2, 3]),
        ("L08", "lists", "`top_n([5, 1, 4], 2) == [5, 4]`.", True, lambda: l.top_n([5, 1, 4], 2) == [5, 4]),
        ("L09", "lists", "`len(top_n(xs, k)) == min(k, len(xs))` for every list of integers and integer `k >= 0`.", True, lambda: forall([(x, k) for x in int_lists(100) for k in range(0, 10)], lambda v: len(l.top_n(*v)) == min(v[1], len(v[0])))),
        ("L10", "lists", "`top_n([3, 2, 1], -1) == []`.", False, lambda: l.top_n([3, 2, 1], -1) == []),
        ("L11", "lists", "`rotate([1, 2, 3], 1) == [2, 3, 1]`.", True, lambda: l.rotate([1, 2, 3], 1) == [2, 3, 1]),
        ("L12", "lists", "`rotate(xs, k) == rotate(xs, k % len(xs))` for every non-empty list `xs` and integer `k >= 0`.", False, lambda: forall([(x, k) for x in int_lists(100) if x for k in range(0, 12)], lambda v: l.rotate(*v) == l.rotate(v[0], v[1] % len(v[0])))),
        ("L13", "lists", "`len(rotate(xs, k)) == len(xs)` for every list `xs` and integer `k`.", True, lambda: forall([(x, k) for x in int_lists(100) for k in range(-12, 12)], lambda v: len(l.rotate(*v)) == len(v[0]))),
        ("L14", "lists", "`interleave([1, 2, 3], [9]) == [1, 9, 2, 3]`.", False, lambda: l.interleave([1, 2, 3], [9]) == [1, 9, 2, 3]),
        ("L15", "lists", "`len(interleave(a, b)) == 2 * min(len(a), len(b))` for all lists `a`, `b`.", True, lambda: forall(list(zip(int_lists(), int_lists())), lambda v: len(l.interleave(*v)) == 2 * min(len(v[0]), len(v[1])))),
        ("L16", "lists", "`frequencies('abca') == {'a': 2, 'b': 1, 'c': 1}`.", True, lambda: l.frequencies('abca') == {'a': 2, 'b': 1, 'c': 1}),
        ("L17", "lists", "`sum(frequencies(xs).values()) == len(xs)` for every list of integers `xs`.", True, lambda: forall(int_lists(), lambda x: sum(l.frequencies(x).values()) == len(x))),
        ("L18", "lists", "`pairwise([1, 2, 3]) == [(1, 2), (2, 3)]`.", True, lambda: l.pairwise([1, 2, 3]) == [(1, 2), (2, 3)]),
        ("L19", "lists", "`len(pairwise(xs)) == len(xs) - 1` for every list `xs`.", False, lambda: forall(int_lists(), lambda x: len(l.pairwise(x)) == len(x) - 1)),
        # money
        ("M01", "money", "`to_cents('12,34') == 1234`.", True, lambda: mo.to_cents('12,34') == 1234),
        ("M02", "money", "`to_cents('1.234,5') == 123450`.", True, lambda: mo.to_cents('1.234,5') == 123450),
        ("M03", "money", "`to_cents('-1,50') == -150`.", False, lambda: mo.to_cents('-1,50') == -150),
        ("M04", "money", "`to_cents('7') == 700`.", True, lambda: mo.to_cents('7') == 700),
        ("M05", "money", "`format_brl(123456) == 'R$ 1.234,56'`.", True, lambda: mo.format_brl(123456) == 'R$ 1.234,56'),
        ("M06", "money", "`format_brl(5) == 'R$ 0,05'`.", True, lambda: mo.format_brl(5) == 'R$ 0,05'),
        ("M07", "money", "`format_brl(-150) == 'R$ -1,50'`.", False, lambda: mo.format_brl(-150) == 'R$ -1,50'),
        ("M08", "money", "`to_cents(format_brl(c)[3:]) == c` for every integer `c` from 0 to 1,000,000.", True, lambda: forall(range(0, 1_000_001), lambda c: mo.to_cents(mo.format_brl(c)[3:]) == c)),
        ("M09", "money", "`sum(split_bill(total, k)) == total` for every integer `total >= 0` and `k >= 1`.", False, lambda: forall([(a, k) for a in range(0, 200) for k in range(1, 8)], lambda v: sum(mo.split_bill(*v)) == v[0])),
        ("M10", "money", "`split_bill(900, 3) == [300, 300, 300]`.", True, lambda: mo.split_bill(900, 3) == [300, 300, 300]),
        ("M11", "money", "`sum(installments(total, k)) == total` for every integer `total >= 0` and `k >= 1`.", True, lambda: forall([(a, k) for a in range(0, 500) for k in range(1, 13)], lambda v: sum(mo.installments(*v)) == v[0])),
        ("M12", "money", "In `installments(total, k)`, the largest and smallest installment differ by at most 1.", True, lambda: forall([(a, k) for a in range(0, 500) for k in range(1, 13)], lambda v: max(mo.installments(*v)) - min(mo.installments(*v)) <= 1)),
        ("M13", "money", "`installments(100, 3) == [34, 33, 33]`.", True, lambda: mo.installments(100, 3) == [34, 33, 33]),
        ("M14", "money", "`apply_discount(1000, 10) == 900`.", True, lambda: mo.apply_discount(1000, 10) == 900),
        ("M15", "money", "`apply_discount(c, 0) == c` for every integer `c` from 0 to 1,000,000.", True, lambda: forall(range(0, 1_000_001), lambda c: mo.apply_discount(c, 0) == c)),
        ("M16", "money", "`apply_discount(c, p) <= c` for every integer `c` from 0 to 1,000,000 and every integer `p` from 0 to 100.", True, lambda: forall([(c, k) for c in list(range(0, 300)) + ints(0, 10**6, 300) for k in range(0, 101, 7)], lambda v: mo.apply_discount(*v) <= v[0])),
        ("M17", "money", "`add_tax(100, 0.15) == 115`.", False, lambda: mo.add_tax(100, 0.15) == 115),
        ("M18", "money", "`add_tax(c, 0) == c` for every integer `c` from 0 to 1,000,000.", True, lambda: forall(range(0, 1_000_001), lambda c: mo.add_tax(c, 0) == c)),
        ("M19", "money", "`add_tax(c, r) >= c` for every integer `c` from 0 to 1,000,000 and every rate `r` from 0 to 1.", True, lambda: forall([(c, rr) for c in list(range(0, 400)) + ints(0, 10**6, 300) for rr in (0, 0.01, 0.07, 0.1, 0.15, 0.5, 1, R.random(), R.random())], lambda v: mo.add_tax(*v) >= v[0])),
        # intervals
        ("I01", "intervals", "`overlaps((0, 5), (5, 10))` is `False`.", True, lambda: iv.overlaps((0, 5), (5, 10)) is False),
        ("I02", "intervals", "`overlaps(a, b) == overlaps(b, a)` for all intervals `a`, `b`.", True, lambda: forall(list(zip(ivs, reversed(ivs))), lambda v: iv.overlaps(*v) == iv.overlaps(v[1], v[0]))),
        ("I03", "intervals", "`merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]`.", True, lambda: iv.merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]),
        ("I04", "intervals", "`merge([(1, 2), (2, 3)]) == [(1, 3)]`.", True, lambda: iv.merge([(1, 2), (2, 3)]) == [(1, 3)]),
        ("I05", "intervals", "For every non-empty list of intervals with start < end, `merge` returns intervals sorted by start with no two overlapping.", True, lambda: forall(iv_lists, lambda x: all(a[0] <= b[0] and not iv.overlaps(a, b) for a, b in zip(iv.merge(x), iv.merge(x)[1:])))),
        ("I06", "intervals", "`merge(merge(xs)) == merge(xs)` for every non-empty list of intervals with start < end.", True, lambda: forall(iv_lists, lambda x: iv.merge(iv.merge(x)) == iv.merge(x))),
        ("I07", "intervals", "`contains((0, 5), 5)` is `False` (intervals are half-open, the end is excluded).", False, lambda: iv.contains((0, 5), 5) is False),
        ("I08", "intervals", "`contains(a, a[0])` is `True` for every interval with start < end.", True, lambda: forall(ivs, lambda a: iv.contains(a, a[0]) is True)),
        ("I09", "intervals", "`intersect((0, 5), (3, 8)) == (3, 5)`.", True, lambda: iv.intersect((0, 5), (3, 8)) == (3, 5)),
        ("I10", "intervals", "`intersect((0, 2), (5, 6))` is `None`.", True, lambda: iv.intersect((0, 2), (5, 6)) is None),
        ("I11", "intervals", "`intersect((0, 5), (5, 8))` is `None`.", True, lambda: iv.intersect((0, 5), (5, 8)) is None),
        ("I12", "intervals", "`total_covered([(0, 5), (3, 8)]) == 8`.", True, lambda: iv.total_covered([(0, 5), (3, 8)]) == 8),
        ("I13", "intervals", "`total_covered(xs) <= sum(length(i) for i in xs)` for every non-empty list of intervals with start < end.", True, lambda: forall(iv_lists, lambda x: iv.total_covered(x) <= sum(iv.length(i) for i in x))),
        ("I14", "intervals", "For intervals with start < end that overlap, `length(intersect(a, b)) <= min(length(a), length(b))`.", True, lambda: forall([v for v in itertools.product(ivs[:60], ivs[60:120]) if iv.overlaps(*v)], lambda v: iv.length(iv.intersect(*v)) <= min(iv.length(v[0]), iv.length(v[1])))),
        ("I15", "intervals", "`merge([]) == []`.", False, lambda: iv.merge([]) == []),
        ("I16", "intervals", "`overlaps(a, a)` is `True` for every interval with start < end.", True, lambda: forall(ivs, lambda a: iv.overlaps(a, a) is True)),
        ("I17", "intervals", "`merge([(5, 7), (1, 2)]) == [(1, 2), (5, 7)]`.", True, lambda: iv.merge([(5, 7), (1, 2)]) == [(1, 2), (5, 7)]),
        ("I18", "intervals", "For integer intervals, `contains(a, x)` implies `overlaps(a, (x, x + 1))`.", False, lambda: forall([(a, x) for a in ivs[:100] for x in range(a[0] - 1, a[1] + 2)], lambda v: (not iv.contains(*v)) or iv.overlaps(v[0], (v[1], v[1] + 1)))),
        ("I19", "intervals", "`length((3, 1))` returns `0` for an inverted interval.", False, lambda: iv.length((3, 1)) == 0),
        # paths
        ("P01", "paths", "`join('a', 'b', 'c.txt') == 'a/b/c.txt'`.", True, lambda: p.join('a', 'b', 'c.txt') == 'a/b/c.txt'),
        ("P02", "paths", "`join('/usr', 'bin') == '/usr/bin'`.", False, lambda: p.join('/usr', 'bin') == '/usr/bin'),
        ("P03", "paths", "`join('a/', '/b') == 'a/b'`.", True, lambda: p.join('a/', '/b') == 'a/b'),
        ("P04", "paths", "`ext('foto.tar.gz') == 'gz'`.", True, lambda: p.ext('foto.tar.gz') == 'gz'),
        ("P05", "paths", "`ext('dir.d/arquivo') == ''`.", False, lambda: p.ext('dir.d/arquivo') == ''),
        ("P06", "paths", "`ext('.bashrc') == ''`.", False, lambda: p.ext('.bashrc') == ''),
        ("P07", "paths", "`stem('relatorio.pdf') == 'relatorio'`.", True, lambda: p.stem('relatorio.pdf') == 'relatorio'),
        ("P08", "paths", "`normalize('a/./b/../c') == 'a/c'`.", True, lambda: p.normalize('a/./b/../c') == 'a/c'),
        ("P09", "paths", "`normalize('/a/../..') == '/'`.", True, lambda: p.normalize('/a/../..') == '/'),
        ("P10", "paths", "`normalize('../x') == '../x'`.", False, lambda: p.normalize('../x') == '../x'),
        ("P11", "paths", "`normalize(normalize(x)) == normalize(x)` for every path string `x`.", True, lambda: forall(paths_gen, lambda x: p.normalize(p.normalize(x)) == p.normalize(x))),
        ("P12", "paths", "`is_hidden('.env')` is `True`.", True, lambda: p.is_hidden('.env') is True),
        ("P13", "paths", "`is_hidden('config/.git/HEAD')` is `False`.", True, lambda: p.is_hidden('config/.git/HEAD') is False),
        ("P14", "paths", "`depth('/a/b/c') == 3`.", True, lambda: p.depth('/a/b/c') == 3),
        ("P15", "paths", "`depth('a//b/') == 2`.", True, lambda: p.depth('a//b/') == 2),
        ("P16", "paths", "`parent('a/b/c') == 'a/b'`.", True, lambda: p.parent('a/b/c') == 'a/b'),
        ("P17", "paths", "`parent('/a') == '/'`.", False, lambda: p.parent('/a') == '/'),
        ("P18", "paths", "`depth(join(*parts)) == len(parts)` for every non-empty list of names made of letters and digits.", True, lambda: forall([[R.choice(words) for _ in range(R.randint(1, 5))] for _ in range(300)], lambda ps: p.depth(p.join(*ps)) == len(ps))),
        ("P19", "paths", "`stem(x) + '.' + ext(x) == x` for every string `x` that contains a dot.", True, lambda: forall([x for x in names + strs() if '.' in x], lambda x: p.stem(x) + '.' + p.ext(x) == x)),
        # records
        ("R01", "records", "`parse_kv('a=1;b=2') == {'a': '1', 'b': '2'}`.", True, lambda: r.parse_kv('a=1;b=2') == {'a': '1', 'b': '2'}),
        ("R02", "records", "`parse_kv('a=1;;b=2') == {'a': '1', 'b': '2'}`.", True, lambda: r.parse_kv('a=1;;b=2') == {'a': '1', 'b': '2'}),
        ("R03", "records", "`parse_kv('url=x=y') == {'url': 'x=y'}`.", True, lambda: r.parse_kv('url=x=y') == {'url': 'x=y'}),
        ("R04", "records", "`parse_kv('a=1;flag') == {'a': '1', 'flag': ''}`.", False, lambda: r.parse_kv('a=1;flag') == {'a': '1', 'flag': ''}),
        ("R05", "records", "`parse_kv(to_kv(d)) == d` for every dict whose keys and values are non-empty strings of letters and digits.", True, lambda: forall(simple_dicts, lambda x: r.parse_kv(r.to_kv(x)) == x)),
        ("R06", "records", "`parse_kv(to_kv(d)) == d` for every dict of strings to strings.", False, lambda: forall(any_dicts, lambda x: r.parse_kv(r.to_kv(x)) == x)),
        ("R07", "records", "`pick({'a': 1, 'b': 2}, ['a', 'c']) == {'a': 1}`.", True, lambda: r.pick({'a': 1, 'b': 2}, ['a', 'c']) == {'a': 1}),
        ("R08", "records", "`len(pick(d, keys)) <= len(d)` for every dict `d` and list `keys`.", True, lambda: forall([(x, [R.choice(words) for _ in range(4)]) for x in simple_dicts], lambda v: len(r.pick(*v)) <= len(v[0]))),
        ("R09", "records", "`rename({'a': 1}, {'a': 'b'}) == {'b': 1}`.", True, lambda: r.rename({'a': 1}, {'a': 'b'}) == {'b': 1}),
        ("R10", "records", "`len(rename(d, mapping)) == len(d)` for every dict `d` and dict `mapping`.", False, lambda: forall([({'a': 1, 'b': 2}, {'a': 'b'})] + [(x, {R.choice(words): R.choice(words)}) for x in simple_dicts], lambda v: len(r.rename(*v)) == len(v[0]))),
        ("R11", "records", "`group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't')` returns `{'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}`.", True, lambda: r.group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't') == {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}),
        ("R12", "records", "`sum(len(g) for g in group_by(rows, key).values()) == len(rows)` whenever every row has `key`.", True, lambda: forall(rows, lambda x: sum(len(g) for g in r.group_by(x, 't').values()) == len(x))),
        ("R13", "records", "`sort_by` is stable: rows with equal keys keep their relative order.", True, lambda: forall(rows, lambda x: [row['v'] for row in r.sort_by(x, 't')] == [row['v'] for k in sorted({row['t'] for row in x}) for row in x if row['t'] == k])),
        ("R14", "records", "`sort_by(rows, 'n')` puts rows that have no key `'n'` at the end.", False, lambda: (not raises(lambda: r.sort_by([{'n': 2}, {}, {'n': 1}], 'n'))) and r.sort_by([{'n': 2}, {}, {'n': 1}], 'n')[-1] == {}),
        ("R15", "records", "`deep_get({'a': {'b': {'c': 1}}}, 'a.b.c') == 1`.", True, lambda: r.deep_get({'a': {'b': {'c': 1}}}, 'a.b.c') == 1),
        ("R16", "records", "`deep_get({'a': {'b': 0}}, 'a.b', 5) == 0`.", True, lambda: r.deep_get({'a': {'b': 0}}, 'a.b', 5) == 0),
        ("R17", "records", "`deep_get({'a': [1, 2]}, 'a.0') == 1`.", False, lambda: r.deep_get({'a': [1, 2]}, 'a.0') == 1),
        ("R18", "records", "`deep_get(d, 'x') == d.get('x')` for every dict `d`.", True, lambda: forall([{'x': 1}, {'x': None}, {}, {'x': {'y': 2}}] + simple_dicts, lambda x: r.deep_get(x, 'x') == x.get('x'))),
        ("R19", "records", "`to_kv({}) == ''`.", True, lambda: r.to_kv({}) == ''),
    ]


def main():
    if FILES.exists():
        shutil.rmtree(FILES)
    pkg = FILES / "kit"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    for name, src in MODULES.items():
        (pkg / f"{name}.py").write_text(src)
    sys.path.insert(0, str(FILES))
    sys.dont_write_bytecode = True
    mods = {k: importlib.import_module(f"kit.{k}") for k in MODULES}
    claims = build_claims(mods)
    truth, bad = {}, []
    for cid, _mod, _text, expected, check in claims:
        try:
            got = bool(check())
        except Exception as e:  # a concrete claim that raises is false
            got = False
            print(f"{cid}: check raised {type(e).__name__}: {e}")
        truth[cid] = got
        if got != expected:
            bad.append(cid)
    ids = [c[0] for c in claims]
    assert len(ids) == len(set(ids)) == 152, len(ids)
    if bad:
        sys.exit(f"expected verdict differs from the code: {bad}")
    lines = ["# Claims about kit/", "", "| id | module | claim |", "|---|---|---|"]
    lines += [f"| {cid} | {mod} | {text} |" for cid, mod, text, _e, _c in claims]
    (FILES / "claims.md").write_text("\n".join(lines) + "\n")
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1) + "\n")
    print(f"{len(truth)} claims, {sum(not v for v in truth.values())} false")


if __name__ == "__main__":
    main()
