import os, sys, random, itertools, string
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.records import parse_kv, to_kv, pick, rename, group_by, sort_by, deep_get

SEED = 20240611


def _eq(expr, got, exp):
    return (True, None) if got == exp else (False, f"{expr} -> {got!r} vs. esperado {exp!r}")


def _try(expr, f, exp):
    try:
        got = f()
    except Exception as e:
        return False, f"{expr} -> exceção {type(e).__name__}: {e} vs. esperado {exp!r}"
    return _eq(expr, got, exp)


def check_R01(): return _try("parse_kv('a=1;b=2')", lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
def check_R02(): return _try("parse_kv('a=1;;b=2')", lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
def check_R03(): return _try("parse_kv('url=x=y')", lambda: parse_kv('url=x=y'), {'url': 'x=y'})
def check_R04(): return _try("parse_kv('a=1;flag')", lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})


def check_R05():
    rng = random.Random(SEED)
    alpha = string.ascii_letters + string.digits
    w = lambda: ''.join(rng.choice(alpha) for _ in range(rng.randint(1, 6)))
    cases = [{}, {'a': '1'}, {'0': '0', 'Z': 'z'}]
    for _ in range(3000):
        cases.append({w(): w() for _ in range(rng.randint(0, 6))})
    for d in cases:
        try:
            got = parse_kv(to_kv(d))
        except Exception as e:
            return False, f"d={d!r} -> exceção {e!r}"
        if got != d:
            return False, f"d={d!r} -> {got!r} vs. {d!r}"
    return True, None


def check_R06():
    # leitura literal: qualquer dict str->str; contraexemplos mínimos
    for d in [{'a=b': 'c'}, {'a': 'b;c'}, {'a;b': 'c'}]:
        try:
            got = parse_kv(to_kv(d))
        except Exception as e:
            return False, f"d={d!r}: to_kv={to_kv(d)!r} -> exceção {type(e).__name__}: {e} vs. {d!r}"
        if got != d:
            return False, f"d={d!r}: to_kv={to_kv(d)!r} -> {got!r} vs. {d!r}"
    return True, None


def check_R07(): return _try("pick({'a':1,'b':2},['a','c'])", lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})


def check_R08():
    rng = random.Random(SEED)
    pool = ['', 'a', 'b', 'c', 'é', '日', 0, 1, -1, None, (1, 2)]
    cases = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a', 'a'])]
    for _ in range(3000):
        d = {rng.choice(pool): rng.randint(-3, 3) for _ in range(rng.randint(0, 5))}
        ks = [rng.choice(pool) for _ in range(rng.randint(0, 10))]
        cases.append((d, ks))
    for d, ks in cases:
        try:
            r = pick(d, ks)
        except Exception as e:
            return False, f"pick({d!r},{ks!r}) -> exceção {e!r}"
        if len(r) > len(d):
            return False, f"pick({d!r},{ks!r}) -> {r!r} len {len(r)} > {len(d)}"
    return True, None


def check_R09(): return _try("rename({'a':1},{'a':'b'})", lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})


def check_R10():
    d, m = {'a': 1, 'b': 2}, {'a': 'b'}
    try:
        r = rename(d, m)
    except Exception as e:
        return False, f"rename({d!r},{m!r}) -> exceção {e!r}"
    if len(r) != len(d):
        return False, f"rename({d!r},{m!r}) -> {r!r} len {len(r)} vs. {len(d)}"
    return True, None


def check_R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    exp = {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}
    return _try("group_by(rows,'t')", lambda: group_by(rows, 't'), exp)


def check_R12():
    rng = random.Random(SEED)
    pool = ['', 'a', 'é', 0, 1, -1, None, False, (1,)]
    cases = [[]]
    for _ in range(3000):
        cases.append([{'k': rng.choice(pool), 'i': i} for i in range(rng.randint(0, 12))])
    for rows in cases:
        try:
            g = group_by(rows, 'k')
        except Exception as e:
            return False, f"rows={rows!r} -> exceção {e!r}"
        s = sum(len(x) for x in g.values())
        if s != len(rows):
            return False, f"rows={rows!r} -> soma {s} vs. {len(rows)}"
    return True, None


def check_R13():
    rng = random.Random(SEED)
    for _ in range(3000):
        rows = [{'n': rng.choice([-1, 0, 1, 2, 2.0, 'x'][:5]), 'i': i} for i in range(rng.randint(0, 15))]
        try:
            r = sort_by(rows, 'n')
        except Exception as e:
            return False, f"rows={rows!r} -> exceção {e!r}"
        exp = sorted(rows, key=lambda x: x['n'])
        if r != exp or any(a['n'] == b['n'] and a['i'] > b['i'] for a, b in zip(r, r[1:])):
            return False, f"rows={rows!r} -> {r!r}"
    return True, None


def check_R14():
    rows = [{'n': 2}, {'x': 1}, {'n': 1}]
    try:
        r = sort_by(rows, 'n')
    except Exception as e:
        return False, f"sort_by({rows!r},'n') -> exceção {type(e).__name__}: {e} vs. linha sem 'n' no fim"
    if r[-1] != {'x': 1}:
        return False, f"sort_by({rows!r},'n') -> {r!r}"
    return True, None


def check_R15(): return _try("deep_get({'a':{'b':{'c':1}}},'a.b.c')", lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
def check_R16(): return _try("deep_get({'a':{'b':0}},'a.b',5)", lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
def check_R17(): return _try("deep_get({'a':[1,2]},'a.0')", lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)


def check_R18():
    rng = random.Random(SEED)
    vals = [None, 0, 1, '', 'v', [], {}, {'x': 1}, False, -1]
    cases = [{}, {'x': None}, {'x': 0}, {'x': {'y': 1}}, {'': 1}, {'é': 1}]
    for _ in range(3000):
        cases.append({k: rng.choice(vals) for k in rng.sample(['x', 'y', 'xx', 'X', '', 'x.x'], rng.randint(0, 4))})
    for d in cases:
        try:
            got = deep_get(d, 'x')
        except Exception as e:
            return False, f"d={d!r} -> exceção {e!r}"
        if got != d.get('x'):
            return False, f"d={d!r} -> {got!r} vs. {d.get('x')!r}"
    return True, None


def check_R19(): return _try("to_kv({})", lambda: to_kv({}), '')


CHECKS = {f"R{i:02d}": globals()[f"check_R{i:02d}"] for i in range(1, 20)}


def main(argv):
    ids = argv or list(CHECKS)
    for i in ids:
        try:
            ok, msg = CHECKS[i]()
        except Exception as e:
            ok, msg = False, f"exceção inesperada: {e!r}"
        print(f"{i}\t{'verdadeira' if ok else 'falsa'}\t{'' if ok else msg}")


if __name__ == '__main__':
    main(sys.argv[1:])
