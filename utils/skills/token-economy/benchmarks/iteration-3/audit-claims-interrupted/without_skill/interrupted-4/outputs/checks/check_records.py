import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.records import *

SEED = 20261101
ALNUM = 'abcXYZ019'
WILD = ['a', 'b', 'x', '=', ';', '', ' ', 'é', 'ç', '😀', '́', '1', 'k', '.']


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def rs(rng, alpha, lo, hi):
    return ''.join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def R01():
    return eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})


def R02():
    return eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})


def R03():
    return eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'})


def R04():
    return eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})


def R05():
    rng = random.Random(SEED)
    cases = [{}, {'a': '1'}] + [
        {rs(rng, ALNUM, 1, 4): rs(rng, ALNUM, 1, 4) for _ in range(rng.randint(0, 5))} for _ in range(20000)]
    for d in cases:
        try:
            r = parse_kv(to_kv(d))
        except Exception as e:
            return False, f'd={d!r}: raised {e!r}'
        if r != d:
            return False, f'd={d!r}: to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={r!r}'
    return True, None


def R06():
    fixed = [{'a=b': 'c'}, {'a;b': 'c'}, {'a': 'b;c'}, {'': ''}, {'a': ''}, {'': 'v'}]
    rng = random.Random(SEED)
    cases = fixed + [{rs(rng, WILD, 0, 4): rs(rng, WILD, 0, 4) for _ in range(rng.randint(0, 4))} for _ in range(20000)]
    for d in cases:
        try:
            r = parse_kv(to_kv(d))
        except Exception as e:
            return False, f'd={d!r}: to_kv={to_kv(d)!r}, raised {e!r}'
        if r != d:
            return False, f'd={d!r}: to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={r!r}'
    return True, None


def R07():
    return eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})


def R08():
    rng = random.Random(SEED)
    for _ in range(20000):
        d = {rng.randint(0, 6): 1 for _ in range(rng.randint(0, 6))}
        keys = [rng.randint(0, 8) for _ in range(rng.randint(0, 12))]
        if len(pick(d, keys)) > len(d):
            return False, f'd={d!r}, keys={keys!r}: {pick(d, keys)!r}'
    return True, None


def R09():
    return eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})


def R10():
    fixed = [({'a': 1, 'b': 2}, {'a': 'b'})]
    rng = random.Random(SEED)
    cases = fixed + [({rng.choice('abcd'): rng.randint(0, 9) for _ in range(rng.randint(0, 4))},
                      {rng.choice('abcd'): rng.choice('abcd') for _ in range(rng.randint(0, 4))}) for _ in range(20000)]
    for d, m in cases:
        try:
            r = rename(d, m)
        except Exception as e:
            return False, f'd={d!r}, mapping={m!r}: raised {e!r}'
        if len(r) != len(d):
            return False, f'd={d!r}, mapping={m!r}: got {r!r} (len {len(r)}), expected len {len(d)}'
    return True, None


def R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq(lambda: group_by(rows, 't'),
              {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})


def R12():
    rng = random.Random(SEED)
    for _ in range(20000):
        rows = [{'k': rng.randint(0, 4), 'i': i} for i in range(rng.randint(0, 8))]
        try:
            n = sum(len(g) for g in group_by(rows, 'k').values())
        except Exception as e:
            return False, f'rows={rows!r}: raised {e!r}'
        if n != len(rows):
            return False, f'rows={rows!r}: total {n} != {len(rows)}'
    return True, None


def R13():
    rng = random.Random(SEED)
    for _ in range(20000):
        rows = [{'n': rng.randint(0, 3), 'i': i} for i in range(rng.randint(0, 8))]
        try:
            out = sort_by(rows, 'n')
        except Exception as e:
            return False, f'rows={rows!r}: raised {e!r}'
        exp = sorted(rows, key=lambda r: (r['n'], r['i']))
        if out != exp:
            return False, f'rows={rows!r}: got {out!r}, expected {exp!r}'
    return True, None


def R14():
    cases = [[{'n': 2}, {'x': 1}, {'n': 1}], [{'x': 1}, {'n': 1}], [{'n': 1}, {'x': 1}]]
    for rows in cases:
        try:
            out = sort_by(rows, 'n')
        except Exception as e:
            return False, f'rows={rows!r}: raised {e!r}, expected rows without "n" at the end'
        has = [('n' in r) for r in out]
        if has != sorted(has, reverse=True):
            return False, f'rows={rows!r}: got {out!r}'
    return True, None


def R15():
    return eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)


def R16():
    return eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)


def R17():
    return eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)


def R18():
    rng = random.Random(SEED)
    cases = [{}, {'x': None}, {'x': 0}, {'x': {'y': 1}}, {'x': [1]}] + [
        {rng.choice(['x', 'y', 'z', 'x.y', '']): rng.choice([0, None, '', 1, {}, [], {'x': 1}]) for _ in range(rng.randint(0, 4))}
        for _ in range(20000)]
    for d in cases:
        try:
            r = deep_get(d, 'x')
        except Exception as e:
            return False, f'd={d!r}: raised {e!r}'
        if r != d.get('x'):
            return False, f'd={d!r}: got {r!r}, expected {d.get("x")!r}'
    return True, None


def R19():
    return eq(lambda: to_kv({}), '')


CHECKS = {f'R{i:02d}': globals()[f'R{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        try:
            ok, ce = CHECKS[i]()
        except Exception as e:
            ok, ce = False, f'check itself raised {e!r}'
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa', 'counterexample': ce,
                          'command': f'python3 checks/check_records.py {i}'}, ensure_ascii=False))
