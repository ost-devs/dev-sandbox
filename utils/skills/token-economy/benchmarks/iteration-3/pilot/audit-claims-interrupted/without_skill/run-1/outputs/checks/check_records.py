import sys, os, json, random, string, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.records import *

SEED = 20240611
ALNUM = string.ascii_letters + string.digits


def attempt(f):
    try:
        return ('ok', f())
    except Exception as e:
        return ('exc', e)


def exact(f, expected):
    r = attempt(f)
    if r[0] == 'ok' and r[1] == expected:
        return None
    got = repr(r[1]) if r[0] == 'ok' else f'{type(r[1]).__name__}: {r[1]}'
    return f'obtido {got} vs esperado {expected!r}'


def rnd_str(rng, alpha, lo, hi):
    return ''.join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def rnd_dict(rng, alpha, lo):
    return {rnd_str(rng, alpha, lo, 4): rnd_str(rng, alpha, lo, 4) for _ in range(rng.randint(0, 4))}


def roundtrip(d):
    r = attempt(lambda: parse_kv(to_kv(d)))
    if r[0] == 'ok' and r[1] == d:
        return None
    got = repr(r[1]) if r[0] == 'ok' else f'{type(r[1]).__name__}: {r[1]}'
    return f'd={d!r}: parse_kv(to_kv(d)) obtido {got} vs esperado {d!r}'


def R01(): return exact(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
def R02(): return exact(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
def R03(): return exact(lambda: parse_kv('url=x=y'), {'url': 'x=y'})
def R04(): return exact(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})


def R05():
    rng = random.Random(SEED)
    for _ in range(3000):
        d = rnd_dict(rng, ALNUM, 1)
        c = roundtrip(d)
        if c: return c
    return roundtrip({})


def R06():
    for d in [{}, {'': ''}, {'a': ''}, {'a=b': 'c'}, {'a': 'b;c'}, {'a;b': 'c'}, {'=': ''}, {'a': '=' }]:
        c = roundtrip(d)
        if c: return c
    rng = random.Random(SEED)
    for _ in range(3000):
        c = roundtrip(rnd_dict(rng, 'ab=;', 0))
        if c: return c
    return None


def R07(): return exact(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})


def R08():
    rng = random.Random(SEED)
    for _ in range(3000):
        d = rnd_dict(rng, 'abc', 0)
        keys = [rnd_str(rng, 'abc', 0, 2) for _ in range(rng.randint(0, 6))]
        keys += rng.choice([[], list(d)])  # duplicates
        r = attempt(lambda: len(pick(d, keys)))
        if r[0] != 'ok' or r[1] > len(d):
            return f'd={d!r}, keys={keys!r}: obtido {r[1]!r}, esperado <= {len(d)}'
    return None


def R09(): return exact(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})


def R10():
    for d, m in [({}, {}), ({'a': 1}, {}), ({'a': 1, 'b': 2}, {'a': 'b'}), ({'a': 1, 'b': 2}, {'a': 'c', 'b': 'c'})]:
        r = attempt(lambda: len(rename(d, m)))
        if r[0] != 'ok' or r[1] != len(d):
            return f'rename({d!r}, {m!r}): len obtido {r[1]!r} (resultado {rename(d, m)!r}) vs esperado {len(d)}'
    return None


def R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return exact(lambda: group_by(rows, 't'),
                 {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})


def R12():
    rng = random.Random(SEED)
    cases = [[]]
    for _ in range(3000):
        cases.append([{'k': rng.choice([0, None, '', 'a', 1, False, (1,)]), 'i': i} for i in range(rng.randint(0, 6))])
    for rows in cases:
        r = attempt(lambda: sum(len(g) for g in group_by(rows, 'k').values()))
        if r[0] != 'ok' or r[1] != len(rows):
            return f'rows={rows!r}: obtido {r[1]!r} vs esperado {len(rows)}'
    return None


def R13():
    rng = random.Random(SEED)
    for _ in range(3000):
        rows = [{'n': rng.randint(0, 3), 'i': i} for i in range(rng.randint(0, 8))]
        r = attempt(lambda: sort_by(rows, 'n'))
        exp = [x for n in range(4) for x in rows if x['n'] == n]
        if r[0] != 'ok' or r[1] != exp:
            return f'rows={rows!r}: obtido {r[1]!r} vs esperado {exp!r}'
    return None


def R14():
    rows = [{'x': 1}, {'n': 1}]
    exp = [{'n': 1}, {'x': 1}]
    return exact(lambda: sort_by(rows, 'n'), exp)


def R15(): return exact(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
def R16(): return exact(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
def R17(): return exact(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)


def R18():
    rng = random.Random(SEED)
    vals = [0, None, '', False, [], {}, 'v', 1, {'x': 1}]
    ds = [{}, {'x': None}, {'x': 0}, {'x': {}}, {'y': 1}, {'x.y': 1}, {'x': {'y': 1}}, {1: 2}, {'': 1}]
    for _ in range(3000):
        ds.append({rng.choice(['x', 'y', 'x.y', '', 1]): rng.choice(vals) for _ in range(rng.randint(0, 3))})
    for d in ds:
        r = attempt(lambda: deep_get(d, 'x'))
        if r[0] != 'ok' or r[1] != d.get('x'):
            return f'd={d!r}: obtido {r[1]!r} vs esperado {d.get("x")!r}'
    return None


def R19(): return exact(lambda: to_kv({}), '')


CHECKS = {f'R{i:02d}': globals()[f'R{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ce = CHECKS[i]()
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ce is None else 'falsa', 'counterexample': ce}, ensure_ascii=False))
