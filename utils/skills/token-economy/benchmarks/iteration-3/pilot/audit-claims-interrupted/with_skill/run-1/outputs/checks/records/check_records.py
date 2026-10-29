import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit.records import *

AN = "abcXYZ019"
N = 3000

def fixed(cid, got_fn, expected):
    @claim(cid)
    def f():
        got = got_fn()
        return True if got == expected else (False, f"-> {got!r}")
    return f

fixed('R01', lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
fixed('R02', lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
fixed('R03', lambda: parse_kv('url=x=y'), {'url': 'x=y'})
fixed('R04', lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})

def rdict(r, alpha, nonempty):
    lo = 1 if nonempty else 0
    d = {}
    for _ in range(r.randint(0, 5)):
        k = ''.join(r.choice(alpha) for _ in range(r.randint(lo, 6)))
        v = ''.join(r.choice(alpha) for _ in range(r.randint(lo, 6)))
        d[k] = v
    return d

def rt(cid, alpha, nonempty, edges):
    r = rng(cid)
    cases = edges + [rdict(r, alpha, nonempty) for _ in range(N)]
    for d in cases:
        try:
            out = parse_kv(to_kv(d))
        except Exception as e:
            return (False, f"{d!r} -> exception {e!r}")
        if out != d:
            return (False, f"{d!r} -> {out!r}")
    return True

@claim('R05')
def r05():
    return rt('R05', AN, True, [{}, {'a': '1'}, {'a': 'b', 'c': 'd'}])

@claim('R06')
def r06():
    from harness import _ALPHA
    return rt('R06', _ALPHA + ';=', False, [{}, {'': ''}, {'a': ''}, {'a': 'b;c'}, {'a': 'b=c'}, {'a=b': 'c'}])

@claim('R07')
def r07():
    got = pick({'a': 1, 'b': 2}, ['a', 'c'])
    return True if got == {'a': 1} else (False, repr(got))

@claim('R08')
def r08():
    r = rng('R08')
    cases = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a'])]
    for _ in range(N):
        d = {r.randint(-5, 5): r.randint(0, 9) for _ in range(r.randint(0, 6))}
        keys = [r.randint(-7, 7) for _ in range(r.randint(0, 12))]
        cases.append((d, keys))
    for d, keys in cases:
        out = pick(d, keys)
        if len(out) > len(d):
            return (False, f"{d!r},{keys!r} -> {out!r}")
    return True

fixed('R09', lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})

@claim('R10')
def r10():
    r = rng('R10')
    cases = [({}, {}), ({'a': 1, 'b': 2}, {'a': 'b'}), ({'a': 1, 'b': 2}, {'a': 'c', 'b': 'c'})]
    for _ in range(N):
        d = {r.randint(0, 5): r.randint(0, 9) for _ in range(r.randint(0, 6))}
        m = {r.randint(0, 5): r.randint(0, 5) for _ in range(r.randint(0, 5))}
        cases.append((d, m))
    for d, m in cases:
        out = rename(d, m)
        if len(out) != len(d):
            return (False, f"{d!r},{m!r} -> {out!r}")
    return True

fixed('R11', lambda: group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
      {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})

@claim('R12')
def r12():
    r = rng('R12')
    cases = [[], [{'k': 1}], [{'k': None}, {'k': ''}, {'k': 0}, {'k': False}]]
    for _ in range(N):
        cases.append([{'k': r.choice([r.randint(-3, 3), rand_str(r, 3), None]), 'i': i}
                      for i in range(r.randint(0, 8))])
    for rows in cases:
        out = group_by(rows, 'k')
        if sum(len(g) for g in out.values()) != len(rows):
            return (False, f"{rows!r} -> {out!r}")
    return True

@claim('R13')
def r13():
    r = rng('R13')
    cases = [[], [{'n': 1, 'i': 0}, {'n': 1, 'i': 1}]]
    for _ in range(N):
        cases.append([{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 12))])
    for rows in cases:
        out = sort_by(rows, 'n')
        exp = [x for k in sorted({x['n'] for x in rows}) for x in rows if x['n'] == k]
        if out != exp:
            return (False, f"{rows!r} -> {out!r}")
    return True

@claim('R14')
def r14():
    r = rng('R14')
    cases = [[{'n': 1}, {'m': 2}], [{'m': 2}], [{'m': 1}, {'n': 0}]]
    for _ in range(N):
        cases.append([({'n': r.randint(-5, 5)} if r.random() < .6 else {'m': i}) for i in range(r.randint(0, 8))])
    for rows in cases:
        try:
            out = sort_by(rows, 'n')
        except Exception as e:
            return (False, f"{rows!r} -> exception {e!r}")
        has = [('n' in x) for x in out]
        if has != sorted(has, reverse=True):
            return (False, f"{rows!r} -> {out!r}")
    return True

fixed('R15', lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
fixed('R16', lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
fixed('R17', lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)

@claim('R18')
def r18():
    r = rng('R18')
    cases = [{}, {'x': None}, {'x': 0}, {'x': {}}, {'y': 1}, {'x': [1]}]
    for _ in range(N):
        d = {r.choice(['x', 'y', 'z', '', 'x.y']): r.choice([None, 0, '', [1], {'a': 1}, r.randint(-9, 9)])
             for _ in range(r.randint(0, 4))}
        cases.append(d)
    for d in cases:
        out = deep_get(d, 'x')
        if out != d.get('x'):
            return (False, f"{d!r} -> {out!r}")
    return True

fixed('R19', lambda: to_kv({}), '')

if __name__ == '__main__':
    run(__file__)
