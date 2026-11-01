import sys, os, random, string
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker, rand_strings
from kit.records import *
c = Checker('records')

def rdicts(seed, alpha, minlen, n=1500):
    r = random.Random(seed)
    out = [{}]
    for _ in range(n):
        out.append({''.join(r.choice(alpha) for _ in range(r.randint(minlen, 5))):
                    ''.join(r.choice(alpha) for _ in range(r.randint(minlen, 5)))
                    for _ in range(r.randint(0, 5))})
    return out

@c.claim('R01')
def _(): return c.eq(parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@c.claim('R02')
def _(): return c.eq(parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@c.claim('R03')
def _(): return c.eq(parse_kv('url=x=y'), {'url': 'x=y'})
@c.claim('R04')
def _(): return c.eq(parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
@c.claim('R05')
def _():
    al = string.ascii_letters + string.digits
    return c.forall(rdicts(5, al, 1), lambda d: parse_kv(to_kv(d)) == d)
@c.claim('R06')
def _():
    cands = [{'a': 'b'}, {'': ''}, {'a=': '1'}, {'a': ';'}, {'a;b': '1'}, {'a': ''}, {'': 'x'}] + \
            rdicts(6, string.ascii_letters + '=; ', 0)
    return c.forall(cands, lambda d: parse_kv(to_kv(d)) == d)
@c.claim('R07')
def _(): return c.eq(pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@c.claim('R08')
def _():
    r = random.Random(8)
    cases = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a']), ({'a': 1}, [])]
    for _ in range(1500):
        d = {r.choice('abcde'): r.randint(0, 9) for _ in range(r.randint(0, 5))}
        cases.append((d, [r.choice('abcdef') for _ in range(r.randint(0, 8))]))
    return c.forall(cases, lambda x: len(pick(*x)) <= len(x[0]))
@c.claim('R09')
def _(): return c.eq(rename({'a': 1}, {'a': 'b'}), {'b': 1})
@c.claim('R10')
def _():
    r = random.Random(10)
    cases = [({'a': 1, 'b': 2}, {'a': 'b'}), ({}, {}), ({'a': 1}, {'a': 'b'})]
    for _ in range(1500):
        d = {r.choice('abcde'): r.randint(0, 9) for _ in range(r.randint(0, 5))}
        m = {r.choice('abcde'): r.choice('abcde') for _ in range(r.randint(0, 4))}
        cases.append((d, m))
    return c.forall(cases, lambda x: len(rename(*x)) == len(x[0]))
@c.claim('R11')
def _():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return c.eq(group_by(rows, 't'), {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@c.claim('R12')
def _():
    r = random.Random(12)
    cases = [[]] + [[{'k': r.choice('abc'), 'i': i} for i in range(r.randint(0, 8))] for _ in range(1500)]
    return c.forall(cases, lambda rows: sum(len(g) for g in group_by(rows, 'k').values()) == len(rows))
@c.claim('R13')
def _():
    r = random.Random(13)
    cases = [[{'n': 1, 'i': 0}, {'n': 1, 'i': 1}]] + \
            [[{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))] for _ in range(1500)]
    return c.forall(cases, lambda rows: sort_by(rows, 'n') == sorted(rows, key=lambda x: (x['n'], x['i'])))
@c.claim('R14')
def _():
    rows = [{'x': 1}, {'n': 1}]
    try:
        out = sort_by(rows, 'n')
    except Exception as e:
        return c.fail(f"sort_by({rows!r}, 'n') raised {type(e).__name__}: {e}")
    return c.eq(out, [{'n': 1}, {'x': 1}])
@c.claim('R15')
def _(): return c.eq(deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@c.claim('R16')
def _(): return c.eq(deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@c.claim('R17')
def _(): return c.eq(deep_get({'a': [1, 2]}, 'a.0'), 1)
@c.claim('R18')
def _():
    r = random.Random(18)
    cases = [{}, {'x': None}, {'x': 0}, {'x': {'y': 1}}, {'y': 1}]
    for _ in range(1500):
        cases.append({r.choice(['x', 'y', 'xx', '']): r.choice([None, 0, '', [], 1]) for _ in range(r.randint(0, 3))})
    return c.forall(cases, lambda d: deep_get(d, 'x') == d.get('x'))
@c.claim('R19')
def _(): return c.eq(to_kv({}), '')

c.main()
