import os, sys, string
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import Checker, rand_text, ROOT
from kit.records import *

c = Checker("records")
eq = lambda got, exp: None if got == exp else f"got {got!r}, expected {exp!r}"
AN = string.ascii_letters + string.digits

c.fixed("R01", lambda: eq(parse_kv('a=1;b=2'), {'a': '1', 'b': '2'}))
c.fixed("R02", lambda: eq(parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'}))
c.fixed("R03", lambda: eq(parse_kv('url=x=y'), {'url': 'x=y'}))
c.fixed("R04", lambda: eq(parse_kv('a=1;flag'), {'a': '1', 'flag': ''}))

def an(rng): return "".join(rng.choice(AN) for _ in range(rng.randint(1, 6)))
def gen_an(rng): return ({an(rng): an(rng) for _ in range(rng.randint(0, 5))},)
c.prop("R05", gen_an, lambda d: parse_kv(to_kv(d)) == d)
def rt(rng): return "".join(rng.choice("ab;=1 ") for _ in range(rng.randint(0, 5)))
def gen_any(rng): return ({rt(rng): rt(rng) for _ in range(rng.randint(0, 4))},)
c.prop("R06", gen_any, lambda d: parse_kv(to_kv(d)) == d)

c.fixed("R07", lambda: eq(pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1}))
def gen_pick(rng):
    return ({rng.choice("abcde"): 1 for _ in range(rng.randint(0, 5))}, [rng.choice("abcdef") for _ in range(rng.randint(0, 8))])
c.prop("R08", gen_pick, lambda d, k: len(pick(d, k)) <= len(d))
c.fixed("R09", lambda: eq(rename({'a': 1}, {'a': 'b'}), {'b': 1}))
def gen_ren(rng):
    return ({rng.choice("abcde"): 1 for _ in range(rng.randint(0, 5))}, {rng.choice("abcde"): rng.choice("abcde") for _ in range(rng.randint(0, 4))})
c.prop("R10", gen_ren, lambda d, m: len(rename(d, m)) == len(d))
c.fixed("R11", lambda: eq(group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
        {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}))
def gen_rows(rng): return ([{'k': rng.choice("abc"), 'i': i} for i in range(rng.randint(0, 10))],)
c.prop("R12", gen_rows, lambda rows: sum(len(g) for g in group_by(rows, 'k').values()) == len(rows))
def gen_sort(rng): return ([{'n': rng.randint(0, 3), 'i': i} for i in range(rng.randint(0, 12))],)
c.prop("R13", gen_sort, lambda rows: sort_by(rows, 'n') == sorted(rows, key=lambda r: (r['n'], r['i'])))
c.fixed("R14", lambda: eq(sort_by([{'n': 2}, {'x': 1}, {'n': 1}], 'n'), [{'n': 1}, {'n': 2}, {'x': 1}]))
c.fixed("R15", lambda: eq(deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1))
c.fixed("R16", lambda: eq(deep_get({'a': {'b': 0}}, 'a.b', 5), 0))
c.fixed("R17", lambda: eq(deep_get({'a': [1, 2]}, 'a.0'), 1))
def gen_d(rng): return ({rng.choice(["x", "y", "a.b"]): rng.choice([0, None, 1, {}, "s"]) for _ in range(rng.randint(0, 3))},)
c.prop("R18", gen_d, lambda d: deep_get(d, 'x') == d.get('x'))
c.fixed("R19", lambda: eq(to_kv({}), ''))
c.finish()
