from harness import *
from kit.records import *

ALNUM = 'abcXYZ0189'


def rand_str(r, al, lo=0, hi=5):
    return ''.join(r.choice(al) for _ in range(r.randint(lo, hi)))


def rand_dicts(cid, al, lo=0, n=4000):
    r = rng(cid)
    return [{rand_str(r, al, max(lo, 0), 4): rand_str(r, al, lo, 4) for _ in range(r.randint(0, 5))} for _ in range(n)]


@claim('R01')
def _(): return eq("parse_kv('a=1;b=2')", lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@claim('R02')
def _(): return eq("parse_kv('a=1;;b=2')", lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@claim('R03')
def _(): return eq("parse_kv('url=x=y')", lambda: parse_kv('url=x=y'), {'url': 'x=y'})
@claim('R04')
def _(): return eq("parse_kv('a=1;flag')", lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
@claim('R05')
def _():
    r = rng('R05')
    ds = [{rand_str(r, ALNUM, 1, 4): rand_str(r, ALNUM, 1, 4) for _ in range(r.randint(0, 5))} for _ in range(5000)]
    return forall(ds, lambda d: parse_kv(to_kv(d)) == d)
@claim('R06')
def _():
    fixed = [{'a': '1;b'}, {'a=b': 'c'}, {'a': '1=2'}, {'a;b': 'c'}, {'': ''}, {'a': ''}]
    return forall(fixed + rand_dicts('R06', 'ab;= '),
                  lambda d: parse_kv(to_kv(d)) == d or f'to_kv = {to_kv(d)!r}, parse_kv = {parse_kv(to_kv(d))!r}')
@claim('R07')
def _(): return eq("pick({'a':1,'b':2}, ['a','c'])", lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@claim('R08')
def _():
    r = rng('R08')
    return forall([(d, [rand_str(r, 'abc', 0, 2) for _ in range(r.randint(0, 6))]) for d in rand_dicts('R08', 'abc', 0, 3000)],
                  lambda d, ks: len(pick(d, ks)) <= len(d))
@claim('R09')
def _(): return eq("rename({'a':1},{'a':'b'})", lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})
@claim('R10')
def _():
    fixed = [({'a': 1, 'b': 2}, {'a': 'b'})]
    r = rng('R10')
    rand = [(d, {rand_str(r, 'abc', 1, 2): rand_str(r, 'abc', 1, 2) for _ in range(r.randint(0, 3))}) for d in rand_dicts('R10', 'abc', 0, 3000)]
    return forall(fixed + rand, lambda d, m: len(rename(d, m)) == len(d) or f'rename = {rename(d, m)}')
@claim('R11')
def _():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq('group_by(rows, "t")', lambda: group_by(rows, 't'),
              {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@claim('R12')
def _():
    r = rng('R12')
    cases = [([{'k': r.choice('abc'), 'i': i} for i in range(r.randint(0, 8))],) for _ in range(3000)]
    return forall(cases, lambda rows: sum(len(g) for g in group_by(rows, 'k').values()) == len(rows))
@claim('R13')
def _():
    r = rng('R13')
    cases = [([{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))],) for _ in range(3000)]
    def prop(rows):
        out = sort_by(rows, 'n')
        return all(not (a['n'] == b['n'] and a['i'] > b['i']) for a, b in zip(out, out[1:])) and [x['n'] for x in out] == sorted(x['n'] for x in rows)
    return forall(cases, prop)
@claim('R14')
def _(): return eq("sort_by([{'n':2},{'x':1},{'n':1}], 'n')", lambda: sort_by([{'n': 2}, {'x': 1}, {'n': 1}], 'n'), [{'n': 1}, {'n': 2}, {'x': 1}])
@claim('R15')
def _(): return eq("deep_get(.., 'a.b.c')", lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@claim('R16')
def _(): return eq("deep_get({'a':{'b':0}}, 'a.b', 5)", lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@claim('R17')
def _(): return eq("deep_get({'a':[1,2]}, 'a.0')", lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)
@claim('R18')
def _():
    r = rng('R18')
    ds = [{rand_str(r, 'xyz', 1, 1): r.choice([None, 0, '', 1, [1], {'q': 1}]) for _ in range(r.randint(0, 4))} for _ in range(3000)]
    return forall(ds, lambda d: deep_get(d, 'x') == d.get('x'))
@claim('R19')
def _(): return eq('to_kv({})', lambda: to_kv({}), '')

if __name__ == '__main__':
    sys.exit(main())
