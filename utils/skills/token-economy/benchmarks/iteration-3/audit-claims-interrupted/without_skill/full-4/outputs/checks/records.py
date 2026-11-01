import sys, os, json, random, string
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.records import parse_kv, to_kv, pick, rename, group_by, sort_by, deep_get

SEED = 12345
N = 3000
ALNUM = string.ascii_letters + string.digits
WILD = ALNUM + ';= é中-'


def rstr(r, alpha, lo=0, hi=5):
    return ''.join(r.choice(alpha) for _ in range(r.randint(lo, hi)))


def rdict(r, alpha, lo=0):
    return {rstr(r, alpha, lo): rstr(r, alpha, lo) for _ in range(r.randint(0, 4))}


def eq(expr_fn, expected):
    try:
        got = expr_fn()
    except Exception as e:
        return False, f"raised {type(e).__name__}: {e}"
    if got == expected:
        return True, None
    return False, f"got {got!r}, expected {expected!r}"


def check_R01(): return eq(lambda: parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
def check_R02(): return eq(lambda: parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
def check_R03(): return eq(lambda: parse_kv('url=x=y'), {'url': 'x=y'})
def check_R04():
    ok, m = eq(lambda: parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
    return (ok, None if ok else "parse_kv('a=1;flag'): " + m)


def check_R05():
    r = random.Random(SEED)
    for _ in range(N):
        d = rdict(r, ALNUM, 1)
        try:
            if parse_kv(to_kv(d)) != d:
                return False, f"d={d!r}"
        except Exception as e:
            return False, f"d={d!r} raised {e!r}"
    return True, None


def check_R06():
    cases = [{'a': 'x;y'}, {'a': 'b=c'}, {'a=b': 'c'}, {'': ''}, {'a': ''}, {'a;b': '1'}]
    r = random.Random(SEED)
    cases += [rdict(r, WILD) for _ in range(N)]
    for d in cases:
        try:
            back = parse_kv(to_kv(d))
        except Exception as e:
            return False, f"d={d!r} to_kv={to_kv(d)!r} raised {type(e).__name__}"
        if back != d:
            return False, f"d={d!r} to_kv={to_kv(d)!r} parse_kv={back!r}"
    return True, None


def check_R07(): return eq(lambda: pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})


def check_R08():
    r = random.Random(SEED)
    for _ in range(N):
        d = rdict(r, WILD)
        keys = [rstr(r, WILD) for _ in range(r.randint(0, 6))] + list(d)[:r.randint(0, 3)]
        r.shuffle(keys)
        if len(pick(d, keys)) > len(d):
            return False, f"d={d!r} keys={keys!r}"
    return True, None


def check_R09(): return eq(lambda: rename({'a': 1}, {'a': 'b'}), {'b': 1})


def check_R10():
    for d, m in [({'a': 1, 'b': 2}, {'a': 'b'}), ({'a': 1, 'b': 2}, {'a': 'c', 'b': 'c'})]:
        if len(rename(d, m)) != len(d):
            return False, f"rename({d!r}, {m!r}) = {rename(d, m)!r}"
    r = random.Random(SEED)
    for _ in range(N):
        d = rdict(r, 'abc'); m = rdict(r, 'abc')
        if len(rename(d, m)) != len(d):
            return False, f"rename({d!r}, {m!r}) = {rename(d, m)!r}"
    return True, None


def check_R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq(lambda: group_by(rows, 't'),
              {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})


def check_R12():
    r = random.Random(SEED)
    for _ in range(N):
        rows = [{'k': r.choice(['a', 'b', '', 'é', 0, 1, None, 1.0, True]), 'i': i}
                for i in range(r.randint(0, 8))]
        try:
            n = sum(len(g) for g in group_by(rows, 'k').values())
        except Exception as e:
            return False, f"rows={rows!r} raised {e!r}"
        if n != len(rows):
            return False, f"rows={rows!r}"
    return True, None


def check_R13():
    r = random.Random(SEED)
    for _ in range(N):
        rows = [{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))]
        out = sort_by(rows, 'n')
        exp = sorted(rows, key=lambda x: (x['n'], x['i']))
        if out != exp:
            return False, f"rows={rows!r} -> {out!r}"
    return True, None


def check_R14():
    rows = [{'n': 2}, {'x': 1}, {'n': 1}]
    try:
        out = sort_by(rows, 'n')
    except Exception as e:
        return False, f"sort_by({rows!r}, 'n') raised {type(e).__name__}: {e}"
    if out[-1] == {'x': 1}:
        return True, None
    return False, f"sort_by({rows!r}, 'n') = {out!r}"


def check_R15(): return eq(lambda: deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
def check_R16(): return eq(lambda: deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
def check_R17():
    ok, m = eq(lambda: deep_get({'a': [1, 2]}, 'a.0'), 1)
    return (ok, None if ok else "deep_get({'a': [1, 2]}, 'a.0'): " + m)


def check_R18():
    r = random.Random(SEED)
    cases = [{}, {'x': None}, {'x': 0}, {'x': {'y': 1}}, {'x': [1]}]
    for _ in range(N):
        d = rdict(r, 'xyz.')
        d.update({'x': r.choice([1, None, '', 'q', {}, {'a': 1}, [], False])} if r.random() < .6 else {})
        cases.append(d)
    for d in cases:
        if deep_get(d, 'x') != d.get('x'):
            return False, f"d={d!r}"
    return True, None


def check_R19(): return eq(lambda: to_kv({}), '')


def main():
    ids = sorted(k[6:] for k in globals() if k.startswith('check_'))
    sel = sys.argv[1:] or ids
    for i in sel:
        ok, ce = globals()['check_' + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": ce,
                          "command": f"python3 -I checks/records.py {i}"}, ensure_ascii=False))


main()
