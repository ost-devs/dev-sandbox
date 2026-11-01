import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import records as R

AN = "abAB019"
SP = "ab;=1"
def gd(r, alpha, nonempty=False):
    lo = 1 if nonempty else 0
    return {"".join(r.choice(alpha) for _ in range(r.randint(lo, 3))): "".join(r.choice(alpha) for _ in range(r.randint(lo, 3))) for _ in range(r.randint(0, 4))}
def gany(r):
    return {r.choice("abc"): r.randint(0, 3) for _ in range(r.randint(0, 4))}

@claim("R01")
def r01(): return eq(R.parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@claim("R02")
def r02(): return eq(R.parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@claim("R03")
def r03(): return eq(R.parse_kv('url=x=y'), {'url': 'x=y'})
@claim("R04")
def r04(): return eq(R.parse_kv('a=1;flag'), {'a': '1', 'flag': ''})  # 'flag' has no '=' -> dict() ValueError
@claim("R05")
def r05(): return forall(lambda r: (gd(r, AN, True),), lambda d: R.parse_kv(R.to_kv(d)) == d)
@claim("R06")
def r06(): return forall(lambda r: (gd(r, SP),), lambda d: R.parse_kv(R.to_kv(d)) == d)
@claim("R07")
def r07(): return eq(R.pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@claim("R08")
def r08(): return forall(lambda r: (gany(r), [r.choice("abcd") for _ in range(r.randint(0, 6))]), lambda d, k: len(R.pick(d, k)) <= len(d))
@claim("R09")
def r09(): return eq(R.rename({'a': 1}, {'a': 'b'}), {'b': 1})
@claim("R10")
def r10(): return forall(lambda r: (gany(r), {r.choice("abc"): r.choice("abc") for _ in range(r.randint(0, 3))}), lambda d, m: len(R.rename(d, m)) == len(d))
@claim("R11")
def r11(): return eq(R.group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
                     {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@claim("R12")
def r12():
    def g(r): return ([{'k': r.choice("abc"), 'i': i} for i in range(r.randint(0, 8))],)
    return forall(g, lambda rows: sum(len(x) for x in R.group_by(rows, 'k').values()) == len(rows))
@claim("R13")
def r13():
    def g(r): return ([{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))],)
    return forall(g, lambda rows: R.sort_by(rows, 'n') == sorted(rows, key=lambda x: (x['n'], x['i'])))
@claim("R14")
def r14():
    rows = [{'x': 1}, {'n': 2}]
    return eq(R.sort_by(rows, 'n'), [{'n': 2}, {'x': 1}][::-1])  # rows w/o 'n' must be last
@claim("R15")
def r15(): return eq(R.deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@claim("R16")
def r16(): return eq(R.deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@claim("R17")
def r17(): return eq(R.deep_get({'a': [1, 2]}, 'a.0'), 1)
@claim("R18")
def r18(): return forall(lambda r: (gany(r) | ({'x': r.randint(0, 3)} if r.random() < .5 else {}),), lambda d: R.deep_get(d, 'x') == d.get('x'))
@claim("R19")
def r19(): return eq(R.to_kv({}), '')

if __name__ == "__main__":
    main("records")
