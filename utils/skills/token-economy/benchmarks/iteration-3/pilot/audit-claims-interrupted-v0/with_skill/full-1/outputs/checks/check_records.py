from common import *
from kit.records import *
import string

def words(r, al, lo=1, hi=4): return ''.join(r.choice(al) for _ in range(r.randint(lo, hi)))
def dicts(cid, al, lo=1, n=N):
    r = rng(cid)
    return [{words(r, al, lo): words(r, al, lo) for _ in range(r.randint(0, 4))} for _ in range(n)]
ALNUM = string.ascii_letters + string.digits

@claim('R01')
def _(): return eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@claim('R02')
def _(): return eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@claim('R03')
def _(): return eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'})
@claim('R04')
def _(): return eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
@claim('R05')
def _(): return forall(dicts('R05', ALNUM), lambda d: parse_kv(to_kv(d)) == d)
@claim('R06')
def _(): return forall(dicts('R06', 'ab=; ', lo=0), lambda d: parse_kv(to_kv(d)) == d)
@claim('R07')
def _(): return eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@claim('R08')
def _(): return forall(((d, list('abcdxyz')[:k]) for d in dicts('R08', 'abcd', 0, 2000) for k in range(8)), lambda d, ks: len(pick(d, ks)) <= len(d))
@claim('R09')
def _(): return eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})
@claim('R10')
def _():
    r = rng('R10'); K = 'abc'
    ins = [({k: i for i, k in enumerate(K) if r.random() < .6}, {k: r.choice(K) for k in K if r.random() < .6}) for _ in range(N)]
    return forall(ins, lambda d, m: len(rename(d, m)) == len(d))
@claim('R11')
def _():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq(lambda: group_by(rows, 't'), {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@claim('R12')
def _():
    r = rng('R12')
    ins = [([{'k': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 8))],) for _ in range(5000)]
    return forall(ins, lambda rows: sum(len(g) for g in group_by(rows, 'k').values()) == len(rows))
@claim('R13')
def _():
    r = rng('R13')
    ins = [([{'k': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))],) for _ in range(5000)]
    def stable(rows):
        out = sort_by(rows, 'k')
        return all(a['k'] < b['k'] or (a['k'] == b['k'] and a['i'] < b['i']) for a, b in zip(out, out[1:]))
    return forall(ins, stable)
@claim('R14')
def _(): return eq(lambda: [r.get('id') for r in sort_by([{'n': 2, 'id': 'a'}, {'id': 'nokey'}, {'n': 1, 'id': 'b'}], 'n')], ['b', 'a', 'nokey'])
@claim('R15')
def _(): return eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@claim('R16')
def _(): return eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@claim('R17')
def _(): return eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)
@claim('R18')
def _(): return forall(dicts('R18', 'xyz.', 0, 3000), lambda d: deep_get(d, 'x') == d.get('x'))
@claim('R19')
def _(): return eq(lambda: to_kv({}), '')

if __name__ == '__main__': main('records')
