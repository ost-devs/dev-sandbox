import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.records import parse_kv, to_kv, pick, rename, group_by, sort_by, deep_get

CMD = 'python3 -I checks/records.py'
R = random.Random(12345)
ALNUM = 'abcXYZ019'
SPECIAL = ['', ';', '=', 'a;b', 'a=b', '=;', 'x', 'a', 'b', '0']


def rs(alphabet, lo, hi):
    return ''.join(R.choice(alphabet) for _ in range(R.randint(lo, hi)))


def first_fail(cases, pred):
    """pred(case) -> (ok, result). Exceptions count as failures."""
    for c in cases:
        try:
            ok, res = pred(c)
        except Exception as e:
            return f'input={c!r} raised {type(e).__name__}: {e}'
        if not ok:
            return f'input={c!r} result={res!r}'
    return ''


def eq(f, expected):
    try:
        got = f()
    except Exception as e:
        return f'raised {type(e).__name__}: {e} (expected {expected!r})'
    return '' if got == expected and type(got) == type(expected) else f'result={got!r} expected={expected!r}'


out = {}

out['R01'] = eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
out['R02'] = eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
out['R03'] = eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'})
out['R04'] = (lambda r: f"parse_kv('a=1;flag') {r}")(eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})) if eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''}) else ''

# R05
d5 = [{}, {'a': '1'}, {'a': 'b', 'c': 'd'}]
for _ in range(500):
    d5.append({rs(ALNUM, 1, 4): rs(ALNUM, 1, 4) for _ in range(R.randint(0, 5))})
out['R05'] = first_fail(d5, lambda d: (parse_kv(to_kv(d)) == d, parse_kv(to_kv(d))))

# R06
d6 = [{}, {'': ''}, {'a': ''}, {'': 'a'}, {'a': 'b;c'}, {'a;b': '1'}, {'a=b': '1'}, {'a': '1=2'}, {'a': ';'}, {'a': '1', 'b': ''}]
for _ in range(500):
    d6.append({rs('ab;=', 0, 3): rs('ab;=', 0, 3) for _ in range(R.randint(0, 4))})
out['R06'] = first_fail(d6, lambda d: (parse_kv(to_kv(d)) == d, parse_kv(to_kv(d))))

# R07
out['R07'] = eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})

# R08
c8 = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a', 'a']), ({'a': 1, 'b': 2}, ['a', 'b', 'a', 'z']), ({'a': 1}, [])]
for _ in range(500):
    d = {R.choice('abcde'): R.randint(0, 9) for _ in range(R.randint(0, 5))}
    c8.append((d, [R.choice('abcdefg') for _ in range(R.randint(0, 10))]))
out['R08'] = first_fail(c8, lambda c: (len(pick(*c)) <= len(c[0]), pick(*c)))

# R09
out['R09'] = eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})

# R10
c10 = [({}, {}), ({'a': 1}, {}), ({'a': 1, 'b': 2}, {'a': 'b'}), ({'a': 1, 'b': 2}, {'a': 'c', 'b': 'c'}), ({'a': 1, 'b': 2}, {'a': 'b', 'b': 'a'}), ({'a': 1}, {'x': 'y'})]
for _ in range(500):
    d = {R.choice('abcde'): R.randint(0, 9) for _ in range(R.randint(0, 5))}
    m = {R.choice('abcdef'): R.choice('abcdef') for _ in range(R.randint(0, 5))}
    c10.append((d, m))
out['R10'] = first_fail(c10, lambda c: (len(rename(*c)) == len(c[0]), rename(*c)))

# R11
rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
out['R11'] = eq(lambda: group_by(rows, 't'), {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})

# R12
c12 = [([], 'k'), ([{'k': None}], 'k'), ([{'k': 1}, {'k': 1}], 'k'), ([{'k': ''}, {'k': 0}, {'k': False}], 'k'), ([{'k': (1, 2)}], 'k')]
for _ in range(500):
    c12.append(([{'k': R.randint(0, 3), 'v': i} for i in range(R.randint(0, 8))], 'k'))
out['R12'] = first_fail(c12, lambda c: (sum(len(g) for g in group_by(*c).values()) == len(c[0]), group_by(*c)))

# R13
c13 = [[], [{'n': 1, 'i': 0}], [{'n': 1, 'i': 0}, {'n': 1, 'i': 1}, {'n': 0, 'i': 2}]]
for _ in range(500):
    c13.append([{'n': R.randint(0, 3), 'i': i} for i in range(R.randint(0, 10))])
def p13(rs_):
    res = sort_by(rs_, 'n')
    ok = all(not (a['n'] == b['n'] and a['i'] > b['i']) for a, b in zip(res, res[1:])) and len(res) == len(rs_)
    return ok, res
out['R13'] = first_fail(c13, p13)

# R14
c14 = [[{'n': 1}, {'x': 0}], [{'x': 0}], [{'x': 0}, {'n': 1}], [{'n': 2}, {}, {'n': 1}], [{}]]
for _ in range(200):
    c14.append([({'n': R.randint(0, 5)} if R.random() < .6 else {'z': 1}) for _ in range(R.randint(1, 6))])
def p14(rs_):
    res = sort_by(rs_, 'n')
    seen_missing = False
    for r in res:
        if 'n' not in r:
            seen_missing = True
        elif seen_missing:
            return False, res
    return True, res
out['R14'] = first_fail(c14, p14)

# R15-R17
out['R15'] = eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
out['R16'] = eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
out['R17'] = eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)

# R18
c18 = [{}, {'x': None}, {'x': 0}, {'x': {}}, {'x': {'y': 1}}, {'y': 1}, {'x': [1]}, {'': 1}, {'x': ''}]
for _ in range(300):
    c18.append({R.choice('xyz.'): R.choice([None, 0, 1, 'a', [], {}]) for _ in range(R.randint(0, 3))})
out['R18'] = first_fail(c18, lambda d: (deep_get(d, 'x') == d.get('x'), deep_get(d, 'x')))

# R19
out['R19'] = eq(lambda: to_kv({}), '')

for i in range(1, 20):
    k = f'R{i:02d}'
    v = out[k]
    print(f"{k}\t{'falsa' if v else 'verdadeira'}\t{v.replace(chr(9), ' ').replace(chr(10), ' ')}\t{CMD}")
