import itertools, string
from _common import Results, rng
from kit.records import *

R = Results("records")
def eq(f, exp):
    def fn():
        got = f()
        return got == exp, got
    return fn

R.check("R01", eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'}))
R.check("R02", eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'}))
R.check("R03", eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'}))
R.check("R04", eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''}))

def r05():
    g = rng(); al = string.ascii_letters + string.digits
    w = lambda: ''.join(g.choice(al) for _ in range(g.randint(1, 6)))
    for _ in range(2000):
        d = {w(): w() for _ in range(g.randint(0, 5))}
        if parse_kv(to_kv(d)) != d: return False, d
    return True, None
R.check("R05", r05)

def r06():
    al = ['a', ';', '=', '']
    strs = [''.join(p) for n in range(3) for p in itertools.product(al, repeat=n)]
    strs = sorted(set(strs), key=lambda s: (len(s), s))
    cands = [{}] + [{k: v} for k in strs for v in strs]
    for d in sorted(cands, key=lambda d: len(repr(d))):
        try: ok = parse_kv(to_kv(d)) == d
        except Exception: ok = False
        if not ok: return False, d
    return True, None
R.check("R06", r06)

R.check("R07", eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1}))
def r08():
    g = rng()
    for _ in range(2000):
        d = {g.choice('abcde'): 1 for _ in range(g.randint(0, 4))}
        ks = [g.choice('abcdef') for _ in range(g.randint(0, 8))]
        if len(pick(d, ks)) > len(d): return False, (d, ks)
    d = {'a': 1}
    if len(pick(d, ['a', 'a'])) > 1: return False, (d, ['a', 'a'])
    return True, None
R.check("R08", r08)
R.check("R09", eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1}))
def r10():
    ks = 'abc'
    for d in [{}] + [dict(zip(c, range(len(c)))) for n in (1, 2, 3) for c in itertools.combinations(ks, n)]:
        for m in [{}] + [{a: b} for a in ks for b in ks]:
            if len(rename(d, m)) != len(d): return False, (d, m)
    return True, None
R.check("R10", r10)

rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
R.check("R11", eq(lambda: group_by(rows, 't'), {'x': [rows[0], rows[2]], 'y': [rows[1]]}))
def r12():
    g = rng()
    for _ in range(1000):
        rs = [{'k': g.choice([0, 1, '', None, 'a', (1,)]), 'i': i} for i in range(g.randint(0, 8))]
        if sum(len(x) for x in group_by(rs, 'k').values()) != len(rs): return False, rs
    return True, None
R.check("R12", r12)
def r13():
    g = rng()
    for _ in range(1000):
        rs = [{'n': g.randint(0, 3), 'i': i} for i in range(g.randint(0, 10))]
        out = sort_by(rs, 'n')
        for a, b in zip(out, out[1:]):
            if a['n'] == b['n'] and a['i'] > b['i']: return False, rs
    return True, None
R.check("R13", r13)
def r14():
    rs = [{'x': 1}, {'n': 1}]
    return sort_by(rs, 'n')[-1] == {'x': 1}, rs
R.check("R14", r14)
R.check("R15", eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1))
R.check("R16", eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0))
R.check("R17", eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1))
def r18():
    for d in [{}, {'x': None}, {'x': 0}, {'x': {}}, {'y': 1}, {'x': [1]}, {'x.y': 1}, {'': 1}]:
        if deep_get(d, 'x') != d.get('x'): return False, d
    return True, None
R.check("R18", r18)
R.check("R19", eq(lambda: to_kv({}), ''))
R.finish()
