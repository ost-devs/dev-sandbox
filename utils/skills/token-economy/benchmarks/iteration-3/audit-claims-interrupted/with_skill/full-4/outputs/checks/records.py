import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.records import *

ALNUM = string.ascii_letters + string.digits
KVA = ALPHABET + ";="

def rdict(r, alpha, minlen=0):
    return {rand_str(r, 6, alpha) if minlen == 0 else ''.join(r.choice(alpha) for _ in range(r.randint(1, 6))):
            (rand_str(r, 6, alpha) if minlen == 0 else ''.join(r.choice(alpha) for _ in range(r.randint(1, 6))))
            for _ in range(r.randint(0, 5))}

def eq(actual, expected):
    return True if actual == expected else (False, 'got %r, expected %r' % (actual, expected))

def guard(fn, r, desc):
    try:
        return fn()
    except Exception as e:
        return '%s -> exception %s: %s' % (desc, type(e).__name__, e)

@exact
def R01(): return eq(parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@exact
def R02(): return eq(parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@exact
def R03(): return eq(parse_kv('url=x=y'), {'url': 'x=y'})
@exact
def R04(): return eq(parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
@exact
def R07(): return eq(pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@exact
def R09(): return eq(rename({'a': 1}, {'a': 'b'}), {'b': 1})
@exact
def R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq(group_by(rows, 't'), {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@exact
def R15(): return eq(deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@exact
def R16(): return eq(deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@exact
def R17(): return eq(deep_get({'a': [1, 2]}, 'a.0'), 1)
@exact
def R19(): return eq(to_kv({}), '')

@prop
def R05(r):
    d = rdict(r, ALNUM, 1)
    got = parse_kv(to_kv(d))
    if got != d: return 'd=%r -> %r' % (d, got)

@prop
def R06(r):
    d = rdict(r, KVA)
    got = parse_kv(to_kv(d))
    if got != d: return 'd=%r to_kv=%r -> %r' % (d, to_kv(d), got)

@prop
def R08(r):
    d = rdict(r, ALNUM)
    keys = [rand_str(r, 3, ALNUM) for _ in range(r.randint(0, 8))] + list(d)[:r.randint(0, 3)]
    r.shuffle(keys)
    n = len(pick(d, keys))
    if n > len(d): return 'd=%r keys=%r len=%d' % (d, keys, n)

@prop
def R10(r):
    d = rdict(r, "abc")
    m = {k: r.choice("abcd") for k in "abcd" if r.random() < .6}
    out = rename(d, m)
    if len(out) != len(d): return 'd=%r mapping=%r -> %r' % (d, m, out)

@prop
def R12(r):
    rows = [{'k': r.choice("abc"), 'i': i} for i in range(r.randint(0, 8))]
    out = group_by(rows, 'k')
    if sum(len(g) for g in out.values()) != len(rows): return 'rows=%r -> %r' % (rows, out)

@prop
def R13(r):
    rows = [{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))]
    out = sort_by(rows, 'n')
    for a, b in zip(out, out[1:]):
        if a['n'] == b['n'] and a['i'] > b['i']: return 'rows=%r -> %r' % (rows, out)

@prop
def R14(r):
    rows = [({'n': r.randint(0, 5), 'i': i} if r.random() < .6 else {'i': i}) for i in range(r.randint(1, 8))]
    if all('n' in x for x in rows): rows[0] = {'i': 99}
    try:
        out = sort_by(rows, 'n')
    except Exception as e:
        return 'rows=%r -> exception %s: %r' % (rows, type(e).__name__, e)
    seen = False
    for x in out:
        if 'n' not in x: seen = True
        elif seen: return 'rows=%r -> %r' % (rows, out)

@prop
def R18(r):
    d = rdict(r, ALNUM + "x.")
    if r.random() < .5: d['x'] = r.choice([None, 0, '', 'v', {'y': 1}, [1]])
    got = deep_get(d, 'x')
    if got != d.get('x'): return 'd=%r -> %r' % (d, got)

run({k: v for k, v in globals().items() if k[0] == 'R' and k[1:].isdigit()})
