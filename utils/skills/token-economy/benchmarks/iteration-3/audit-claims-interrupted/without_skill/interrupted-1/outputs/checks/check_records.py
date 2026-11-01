import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.records import *

SEED = 20240607
N = 3000
rng_ = lambda: random.Random(SEED)
NOTE_INF = f"bordas manuais + amostragem semeada (SEED={SEED}, N={N}); nenhum contraexemplo achado"
NOTE_ONE = "execucao unica da entrada literal"

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

def eq(f, code):
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", NOTE_ONE
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), NOTE_ONE

def forall(pred, cases, show):
    for c in cases:
        try:
            if not pred(c):
                return show(c)
        except Exception as e:
            return f"entrada {c!r} -> excecao {type(e).__name__}: {e}"
    return None

claim('R01')(lambda: eq(lambda: (parse_kv('a=1;b=2'), {'a': '1', 'b': '2'}), "parse_kv('a=1;b=2')"))
claim('R02')(lambda: eq(lambda: (parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'}), "parse_kv('a=1;;b=2')"))
claim('R03')(lambda: eq(lambda: (parse_kv('url=x=y'), {'url': 'x=y'}), "parse_kv('url=x=y')"))
claim('R04')(lambda: eq(lambda: (parse_kv('a=1;flag'), {'a': '1', 'flag': ''}), "parse_kv('a=1;flag')"))

AL = 'abcXYZ019'
def rdicts(rng, alpha, n, allow_empty):
    out = []
    for _ in range(n):
        d = {}
        for _ in range(rng.randint(0, 4)):
            mk = lambda: ''.join(rng.choice(alpha) for _ in range(rng.randint(0 if allow_empty else 1, 3)))
            d[mk()] = mk()
        out.append(d)
    return out

def r05():
    cases = [{}, {'a': '1'}, {'a': 'b', 'c': 'd'}, {'A9': 'z0'}] + rdicts(rng_(), AL, N, False)
    return forall(lambda d: parse_kv(to_kv(d)) == d, cases,
                  lambda d: f"d={d!r}, to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={parse_kv(to_kv(d))!r}"), NOTE_INF
claim('R05')(r05)

def r06():
    edge = [{}, {'': ''}, {'a': ''}, {'': 'a'}, {'a;b': 'c'}, {'a': 'b;c'}, {'a=b': 'c'}, {'a': 'b=c'}, {'a': '1', '': ''}]
    cases = edge + rdicts(rng_(), 'ab;= ', N, True)
    return forall(lambda d: parse_kv(to_kv(d)) == d, cases,
                  lambda d: f"d={d!r}, to_kv={to_kv(d)!r}, parse_kv(to_kv(d))={parse_kv(to_kv(d))!r}"), NOTE_INF
claim('R06')(r06)

claim('R07')(lambda: eq(lambda: (pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1}), "pick({'a':1,'b':2},['a','c'])"))

def r08():
    rng = rng_()
    cases = [({}, []), ({}, ['a']), ({'a': 1}, ['a', 'a']), ({'a': 1}, ['a', 'a', 'a']), ({'a': 1, 'b': 2}, ['b', 'a', 'b'])]
    for _ in range(N):
        d = {rng.choice('abcd'): rng.randint(0, 9) for _ in range(rng.randint(0, 4))}
        ks = [rng.choice('abcde') for _ in range(rng.randint(0, 8))]
        cases.append((d, ks))
    return forall(lambda c: len(pick(*c)) <= len(c[0]), cases, lambda c: f"pick({c[0]!r}, {c[1]!r}) = {pick(*c)!r}"), NOTE_INF
claim('R08')(r08)

claim('R09')(lambda: eq(lambda: (rename({'a': 1}, {'a': 'b'}), {'b': 1}), "rename({'a':1},{'a':'b'})"))

def r10():
    rng = rng_()
    cases = [({'a': 1, 'b': 2}, {'a': 'b'}), ({}, {}), ({'a': 1}, {})]
    for _ in range(N):
        d = {rng.choice('abcd'): rng.randint(0, 9) for _ in range(rng.randint(0, 4))}
        m = {rng.choice('abcd'): rng.choice('abcd') for _ in range(rng.randint(0, 3))}
        cases.append((d, m))
    # minimal first
    cases.sort(key=lambda c: len(c[0]) + len(c[1]))
    return forall(lambda c: len(rename(*c)) == len(c[0]), cases, lambda c: f"rename({c[0]!r}, {c[1]!r}) = {rename(*c)!r}"), NOTE_INF
claim('R10')(r10)

def r11():
    rows = [{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}]
    return eq(lambda: (group_by(rows, 't'), {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}), "group_by(3 rows, 't')")
claim('R11')(r11)

def r12():
    rng = rng_()
    cases = [[]]
    for _ in range(N):
        cases.append([{'k': rng.choice(['a', 'b', 'c', 1, None, (1,)]), 'i': i} for i in range(rng.randint(0, 8))])
    return forall(lambda rows: sum(len(g) for g in group_by(rows, 'k').values()) == len(rows), cases,
                  lambda rows: f"rows={rows!r}, group_by={group_by(rows,'k')!r}"), NOTE_INF
claim('R12')(r12)

def r13():
    rng = rng_()
    cases = [[{'n': 1, 'i': 0}, {'n': 1, 'i': 1}]]
    for _ in range(N):
        cases.append([{'n': rng.randint(0, 3), 'i': i} for i in range(rng.randint(0, 10))])
    def ok(rows):
        out = sort_by(rows, 'n')
        return all(out[a]['n'] != out[a+1]['n'] or out[a]['i'] < out[a+1]['i'] for a in range(len(out)-1)) and len(out) == len(rows)
    return forall(ok, cases, lambda rows: f"rows={rows!r}, sort_by={sort_by(rows,'n')!r}"), NOTE_INF
claim('R13')(r13)

def r14():
    rows = [{'n': 2}, {'x': 1}, {'n': 1}]
    try:
        out = sort_by(rows, 'n')
    except Exception as e:
        return f"sort_by({rows!r}, 'n') -> excecao {type(e).__name__}: {e}", NOTE_ONE
    return (None if out[-1] == {'x': 1} else f"sort_by({rows!r}, 'n') = {out!r}"), NOTE_ONE
claim('R14')(r14)

claim('R15')(lambda: eq(lambda: (deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1), "deep_get({'a':{'b':{'c':1}}},'a.b.c')"))
claim('R16')(lambda: eq(lambda: (deep_get({'a': {'b': 0}}, 'a.b', 5), 0), "deep_get({'a':{'b':0}},'a.b',5)"))
claim('R17')(lambda: eq(lambda: (deep_get({'a': [1, 2]}, 'a.0'), 1), "deep_get({'a':[1,2]},'a.0')"))

def r18():
    rng = rng_()
    cases = [{}, {'x': None}, {'x': 0}, {'x': {'y': 1}}, {'x': [1]}, {'a': 1}, {'x.y': 1}, {'': 1}]
    for _ in range(N):
        cases.append({rng.choice(['x', 'y', 'x.y', '']): rng.choice([None, 0, '', 'v', [1], {'x': 1}]) for _ in range(rng.randint(0, 3))})
    return forall(lambda d: deep_get(d, 'x') == d.get('x'), cases, lambda d: f"deep_get({d!r},'x') = {deep_get(d,'x')!r}, d.get = {d.get('x')!r}"), NOTE_INF
claim('R18')(r18)

claim('R19')(lambda: eq(lambda: (to_kv({}), ''), "to_kv({})"))

def main():
    ids = sys.argv[1:] or sorted(R)
    res = []
    for i in ids:
        try:
            ce, note = R[i]()
        except Exception as e:
            ce, note = f"excecao {type(e).__name__}: {e}", "erro na checagem"
        if ce: note = note.replace("; nenhum contraexemplo achado", "; contraexemplo encontrado")
        line = {"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce, "note": note}
        res.append(line)
        print(json.dumps(line, ensure_ascii=False))
    if not sys.argv[1:]:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_records.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
