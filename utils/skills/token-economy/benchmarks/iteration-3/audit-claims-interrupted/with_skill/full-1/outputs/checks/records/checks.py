import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, rand_str, main
from kit.records import *
import string

def ex(cid, expr_fn, expected, label):
    try:
        out = expr_fn()
    except Exception as e:
        return f"{label} raised {type(e).__name__}: {e}"
    if out != expected:
        return f"{label} = {out!r}"

def _mk(cid, f, e, l):
    claim(cid)(lambda: ex(cid, f, e, l))

_mk("R01", lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'}, "parse_kv('a=1;b=2')")
_mk("R02", lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'}, "parse_kv('a=1;;b=2')")
_mk("R03", lambda: parse_kv('url=x=y'), {'url': 'x=y'}, "parse_kv('url=x=y')")
_mk("R04", lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''}, "parse_kv('a=1;flag')")
_mk("R07", lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1}, "pick")
_mk("R09", lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1}, "rename")
_mk("R15", lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1, "deep_get nested")
_mk("R16", lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0, "deep_get({'a':{'b':0}},'a.b',5)")
_mk("R17", lambda: deep_get({'a': [1, 2]}, 'a.0'), 1, "deep_get({'a':[1,2]},'a.0')")
_mk("R19", lambda: to_kv({}), '', "to_kv({})")
_mk("R11", lambda: group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
    {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}, "group_by example")

AN = string.ascii_letters + string.digits

@claim("R05")
def r05():
    r = rng("R05")
    for _ in range(3000):
        d = {}
        for _ in range(r.randint(0, 5)):
            d["".join(r.choice(AN) for _ in range(r.randint(1, 6)))] = "".join(r.choice(AN) for _ in range(r.randint(1, 6)))
        try:
            if parse_kv(to_kv(d)) != d:
                return f"d={d!r} -> {parse_kv(to_kv(d))!r}"
        except Exception as e:
            return f"d={d!r} raised {e!r}"

@claim("R06")
def r06():
    for d in [{'a': ''}, {'a': 'b;c'}, {'a;b': 'c'}, {'a=b': 'c'}, {'': ''}, {'': 'x'}, {'a': 'b=c'}]:
        try:
            out = parse_kv(to_kv(d))
        except Exception as e:
            return f"d={d!r} raised {e!r}"
        if out != d:
            return f"d={d!r}: to_kv={to_kv(d)!r} -> parse_kv={out!r}"

@claim("R08")
def r08():
    r = rng("R08")
    for _ in range(3000):
        d = {r.randint(0, 6): 1 for _ in range(r.randint(0, 6))}
        keys = [r.randint(0, 6) for _ in range(r.randint(0, 12))]
        if len(pick(d, keys)) > len(d):
            return f"pick({d!r},{keys!r})"

@claim("R10")
def r10():
    for d, m in [({'a': 1, 'b': 2}, {'a': 'b'}), ({}, {}), ({'a': 1}, {'a': 'a'})]:
        out = rename(d, m)
        if len(out) != len(d):
            return f"rename({d!r},{m!r}) = {out!r}"

@claim("R12")
def r12():
    r = rng("R12")
    for rows in [[]] + [[{'k': r.choice(['a', 'b', '', None, 1, 1.0, True])} for _ in range(r.randint(0, 8))] for _ in range(3000)]:
        n = sum(len(g) for g in group_by(rows, 'k').values())
        if n != len(rows):
            return f"rows={rows!r} total={n}"

@claim("R13")
def r13():
    r = rng("R13")
    for _ in range(3000):
        rows = [{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))]
        out = sort_by(rows, 'n')
        for a, b in zip(out, out[1:]):
            if a['n'] == b['n'] and a['i'] > b['i']:
                return f"rows={rows!r} -> {out!r}"

@claim("R14")
def r14():
    rows = [{'x': 1}, {'n': 2}]
    try:
        out = sort_by(rows, 'n')
    except Exception as e:
        return f"sort_by({rows!r}, 'n') raised {type(e).__name__}: {e}"
    if out[-1] != {'x': 1}:
        return f"sort_by({rows!r}, 'n') = {out!r}"

@claim("R18")
def r18():
    r = rng("R18")
    cands = ['x', '', 'x.y', '.', 'a b']
    for _ in range(3000):
        d = {r.choice(['x', '', 'y', 'x.y']): r.choice([None, 0, '', 1, {}, {'y': 2}, [1]]) for _ in range(r.randint(0, 3))}
        for p in ['x']:
            if deep_get(d, p) != d.get(p):
                return f"d={d!r}: deep_get={deep_get(d,p)!r} get={d.get(p)!r}"
    for d in [{}, {'x': None}, {'x': {}}, {'x': 0}]:
        if deep_get(d, 'x') != d.get('x'):
            return f"d={d!r}"

if __name__ == "__main__":
    main()
