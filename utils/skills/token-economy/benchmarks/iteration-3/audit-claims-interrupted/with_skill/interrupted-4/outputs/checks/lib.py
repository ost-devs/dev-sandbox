"""Shared helpers for claim checks. Seed is fixed (SEED) so every run is identical."""
import random

SEED = 20261101
N = 3000  # samples per property check

EDGE_STRINGS = ['', ' ', '-', '--', 'a', 'A', ' a ', 'a  b', '\t\n', 'Café', 'ø', 'ß', 'İ', 'ǆ',
                'ﬁ', 'Ação', '日本語', '😀', 'é', '-a-', 'a-b', 'A man, a plan', '١٢٣', '_', '!!']
ALPHABET = list('abcXYZ019 -_\t\n.,:é ñøßİﬁ日😀') + ['é']


def rng(tag=''):
    return random.Random(f'{SEED}:{tag}')


def strings(tag='', n=N, maxlen=12):
    r = rng(tag)
    yield from EDGE_STRINGS
    for _ in range(n):
        yield ''.join(r.choice(ALPHABET) for _ in range(r.randint(0, maxlen)))


def ints(tag='', n=N, lo=-50, hi=50):
    r = rng(tag)
    yield from [lo, hi, 0, 1, -1]
    for _ in range(n):
        yield r.randint(lo, hi)


def int_lists(tag='', n=N, maxlen=8, lo=-20, hi=20, min_len=0):
    r = rng(tag)
    for _ in range(n):
        yield [r.randint(lo, hi) for _ in range(r.randint(min_len, maxlen))]


def first_fail(cases, prop):
    """cases: iterable of args tuples/values; prop(case)->bool. Returns None if all hold,
    else a string describing the first counterexample (exceptions count as failure)."""
    for c in cases:
        try:
            ok = prop(c)
        except Exception as e:
            return f'{c!r} raised {type(e).__name__}: {e}'
        if not ok:
            return f'{c!r}'
    return None


def eq(actual_fn, expected, desc):
    """Fixed-input check: returns None if actual_fn() == expected."""
    try:
        a = actual_fn()
    except Exception as e:
        return f'{desc} raised {type(e).__name__}: {e}'
    return None if a == expected and type(a) == type(expected) else f'{desc} -> {a!r}, expected {expected!r}'
