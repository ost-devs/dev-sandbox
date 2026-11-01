from lib import strings, ints, first_fail, eq, rng, N
from kit.records import *
import string

AN = string.ascii_letters + string.digits
SEP = 'ab;=x1 '


def rstr(r, alpha, lo, hi):
    return ''.join(r.choice(alpha) for _ in range(r.randint(lo, hi)))


def dicts(tag, alpha, lo=0, n=N):
    r = rng(tag)
    for _ in range(n):
        yield {rstr(r, alpha, lo, 4): rstr(r, alpha, lo, 4) for _ in range(r.randint(0, 5))}


def keylists(tag, n=N):
    r = rng(tag)
    for _ in range(n):
        d = {rstr(r, 'abc', 0, 2): r.randint(0, 9) for _ in range(r.randint(0, 5))}
        yield d, [rstr(r, 'abc', 0, 2) for _ in range(r.randint(0, 6))]


def renames(tag, n=N):
    r = rng(tag)
    for _ in range(n):
        d = {rstr(r, 'abc', 0, 1): r.randint(0, 9) for _ in range(r.randint(0, 4))}
        m = {rstr(r, 'abc', 0, 1): rstr(r, 'abc', 0, 1) for _ in range(r.randint(0, 4))}
        yield d, m


def rows_with_key(tag, key='k', n=N):
    r = rng(tag)
    for _ in range(n):
        yield [{key: r.choice('abc'), 'i': i} for i in range(r.randint(0, 8))]


def r12(rows):
    g = group_by(rows, 'k')
    return sum(len(x) for x in g.values()) == len(rows)


def r13(rows):
    out = sort_by(rows, 'k')
    for a, b in zip(out, out[1:]):
        if a['k'] == b['k'] and a['i'] > b['i']:
            return False
    return len(out) == len(rows)


def r14_rows(tag, n=500):
    r = rng(tag)
    for _ in range(n):
        yield [({'n': r.randint(0, 5)} if r.random() < .6 else {'m': i}) for i in range(r.randint(0, 6))]


def r14(rows):
    out = sort_by(rows, 'n')
    seen_missing = False
    for x in out:
        if 'n' not in x:
            seen_missing = True
        elif seen_missing:
            return False
    return True


def r18(d):
    return deep_get(d, 'x') == d.get('x')


def r18_dicts(tag):
    r = rng(tag)
    yield {}
    yield {'x': None}
    yield {'x': 0}
    yield {'x': {'y': 1}}
    for _ in range(N):
        yield {r.choice('xyz'): r.choice([0, 1, None, '', [], {}]) for _ in range(r.randint(0, 3))}


CHECKS = {
    'R01': lambda: eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'}, "parse_kv('a=1;b=2')"),
    'R02': lambda: eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'}, "parse_kv('a=1;;b=2')"),
    'R03': lambda: eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'}, "parse_kv('url=x=y')"),
    'R04': lambda: eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''}, "parse_kv('a=1;flag')"),
    'R05': lambda: first_fail(dicts('r5', AN, lo=1), lambda d: parse_kv(to_kv(d)) == d),
    'R06': lambda: first_fail([{'a': 'b;c'}, {'a=b': 'c'}, {'a': ''}, {'': ''}, {'': 'x'}] + list(dicts('r6', SEP)),
                              lambda d: parse_kv(to_kv(d)) == d),
    'R07': lambda: eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1}, 'pick'),
    'R08': lambda: first_fail(keylists('r8'), lambda p: len(pick(*p)) <= len(p[0])),
    'R09': lambda: eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1}, 'rename'),
    'R10': lambda: first_fail(renames('r10'), lambda p: len(rename(*p)) == len(p[0])),
    'R11': lambda: eq(lambda: group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
                      {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}, 'group_by'),
    'R12': lambda: first_fail(rows_with_key('r12'), r12),
    'R13': lambda: first_fail(rows_with_key('r13'), r13),
    'R14': lambda: first_fail(r14_rows('r14'), r14),
    'R15': lambda: eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1, 'deep_get'),
    'R16': lambda: eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0, 'deep_get default'),
    'R17': lambda: eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1, "deep_get({'a':[1,2]},'a.0')"),
    'R18': lambda: first_fail(r18_dicts('r18'), r18),
    'R19': lambda: eq(lambda: to_kv({}), '', 'to_kv({})'),
}
