import json, os, random, string, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.records import parse_kv, to_kv, pick, rename, group_by, sort_by, deep_get

SEED = 20240607
N = 5000
ALNUM = string.ascii_letters + string.digits
ANY = ALNUM + ";=. \n"


def point(f):
    """f returns (ok, description_of_input_and_output)."""
    return f


def rs(rng, alpha, lo, hi):
    return ''.join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def rdict(rng, alpha, lo):
    return {rs(rng, alpha, lo, 4): rs(rng, alpha, lo, 4) for _ in range(rng.randint(0, 5))}


def eq(expr_in, got, want):
    return (got == want, f"{expr_in} -> {got!r}, esperado {want!r}")


def R01(): return eq("parse_kv('a=1;b=2')", parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
def R02(): return eq("parse_kv('a=1;;b=2')", parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
def R03(): return eq("parse_kv('url=x=y')", parse_kv('url=x=y'), {'url': 'x=y'})
def R04():
    try:
        return eq("parse_kv('a=1;flag')", parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
    except Exception as e:
        return False, f"parse_kv('a=1;flag') excecao {type(e).__name__}: {e}"


def roundtrip(gen_cases):
    for d in gen_cases:
        got = parse_kv(to_kv(d))
        if got != d:
            return False, f"d={d!r}: to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={got!r}"
    return True, None


def R05():
    rng = random.Random(SEED)
    cases = [{}, {'a': '1'}, {'A9': 'z', 'b': 'Q'}]
    cases += [{rs(rng, ALNUM, 1, 4): rs(rng, ALNUM, 1, 4) for _ in range(rng.randint(0, 5))} for _ in range(N)]
    return roundtrip(cases)


def R06():
    rng = random.Random(SEED)
    fixed = [{}, {'a': ''}, {'': ''}, {'a': ';'}, {'a': '1;b=2'}, {'a=b': 'c'}, {'': 'x'}, {'a': 'b'}]
    for d in fixed:
        try:
            got = parse_kv(to_kv(d))
        except Exception as e:
            return False, f"d={d!r}: to_kv={to_kv(d)!r}, excecao {type(e).__name__}: {e}"
        if got != d:
            return False, f"d={d!r}: to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={got!r}"
    cases = [rdict(rng, ANY, 0) for _ in range(N)]
    try:
        return roundtrip(cases)
    except Exception as e:
        return False, f"excecao {type(e).__name__}: {e}"


def R07(): return eq("pick({'a':1,'b':2},['a','c'])", pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})


def R08():
    rng = random.Random(SEED)
    pool = list('abcdef')
    cases = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a', 'a'])]
    for _ in range(N):
        d = {rng.choice(pool): rng.randint(0, 9) for _ in range(rng.randint(0, 5))}
        cases.append((d, [rng.choice(pool) for _ in range(rng.randint(0, 10))]))
    for d, k in cases:
        try:
            r = pick(d, k)
        except Exception as e:
            return False, f"pick({d!r},{k!r}) excecao {type(e).__name__}: {e}"
        if len(r) > len(d):
            return False, f"pick({d!r},{k!r}) -> {r!r}"
    return True, None


def R09(): return eq("rename({'a':1},{'a':'b'})", rename({'a': 1}, {'a': 'b'}), {'b': 1})


def R10():
    rng = random.Random(SEED)
    pool = list('abcd')
    cases = [({'a': 1, 'b': 2}, {'a': 'b'}), ({}, {}), ({'a': 1}, {})]
    for _ in range(N):
        d = {rng.choice(pool): rng.randint(0, 9) for _ in range(rng.randint(0, 4))}
        m = {rng.choice(pool): rng.choice(pool) for _ in range(rng.randint(0, 4))}
        cases.append((d, m))
    for d, m in cases:
        try:
            r = rename(d, m)
        except Exception as e:
            return False, f"rename({d!r},{m!r}) excecao {type(e).__name__}: {e}"
        if len(r) != len(d):
            return False, f"rename({d!r},{m!r}) -> {r!r} (len {len(r)} != {len(d)})"
    return True, None


def R11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq("group_by(rows,'t')", group_by(rows, 't'),
              {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})


def R12():
    rng = random.Random(SEED)
    cases = [([], 'k')]
    for _ in range(N):
        cases.append(([{'k': rng.choice(['a', 'b', 1, None, (1,), ''])} for _ in range(rng.randint(0, 8))], 'k'))
    for rows, key in cases:
        try:
            r = group_by(rows, key)
        except Exception as e:
            return False, f"group_by({rows!r},{key!r}) excecao {type(e).__name__}: {e}"
        if sum(len(g) for g in r.values()) != len(rows):
            return False, f"group_by({rows!r},{key!r}) -> {r!r}"
    return True, None


def R13():
    rng = random.Random(SEED)
    cases = [[{'n': 1, 'i': 0}, {'n': 1, 'i': 1}], []]
    for _ in range(N):
        cases.append([{'n': rng.randint(0, 3), 'i': i} for i in range(rng.randint(0, 10))])
    for rows in cases:
        try:
            r = sort_by(rows, 'n')
        except Exception as e:
            return False, f"sort_by({rows!r},'n') excecao {type(e).__name__}: {e}"
        for a, b in zip(r, r[1:]):
            if a['n'] == b['n'] and a['i'] > b['i']:
                return False, f"sort_by({rows!r},'n') -> {r!r}"
    return True, None


def R14():
    rows = [{'x': 1}, {'n': 1}]
    try:
        r = sort_by(rows, 'n')
    except Exception as e:
        return False, f"sort_by({rows!r},'n') excecao {type(e).__name__}: {e}"
    ok = r == [{'n': 1}, {'x': 1}]
    return ok, f"sort_by({rows!r},'n') -> {r!r}"


def R15(): return eq("deep_get({'a':{'b':{'c':1}}},'a.b.c')", deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
def R16(): return eq("deep_get({'a':{'b':0}},'a.b',5)", deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
def R17(): return eq("deep_get({'a':[1,2]},'a.0')", deep_get({'a': [1, 2]}, 'a.0'), 1)


def R18():
    rng = random.Random(SEED)
    cases = [{}, {'x': 0}, {'x': None}, {'x': {'y': 1}}, {'x.y': 1}, {'': 1}]
    for _ in range(N):
        cases.append({rng.choice(['x', 'y', 'x.y', '']): rng.choice([0, 1, None, 's', [1], {'x': 1}]) for _ in range(rng.randint(0, 3))})
    for d in cases:
        try:
            r = deep_get(d, 'x')
        except Exception as e:
            return False, f"deep_get({d!r},'x') excecao {type(e).__name__}: {e}"
        if r != d.get('x'):
            return False, f"deep_get({d!r},'x') -> {r!r}, d.get('x')={d.get('x')!r}"
    return True, None


def R19(): return eq("to_kv({})", to_kv({}), '')


def main():
    ids = [f"R{i:02d}" for i in range(1, 20)]
    sel = sys.argv[1:] or ids
    for i in sel:
        try:
            ok, msg = globals()[i]()
        except Exception as e:
            ok, msg = False, f"excecao inesperada {type(e).__name__}: {e}"
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": None if ok else msg}, ensure_ascii=False))


main()
