import sys, os, json, random, string
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.records import parse_kv, to_kv, pick, rename, group_by, sort_by, deep_get

SEED = 1234
N = 3000
ALNUM = string.ascii_letters + string.digits + 'éßΩж中'
NASTY = string.ascii_letters + '=;. é中'

def rs(rnd, alpha, lo=0, hi=5):
    return ''.join(rnd.choice(alpha) for _ in range(rnd.randint(lo, hi)))

def fixed(got, exp, desc):
    return ('', ) if got == exp else (f'{desc}: actual {got!r}, claimed {exp!r}',)

def run_eq(f, desc):
    try:
        return fixed(f(), True, desc)[0] if False else None
    except Exception as e:
        return f'{desc}: raised {e!r}'

def simple(expr_f, exp, desc):
    try:
        got = expr_f()
    except Exception as e:
        return f'{desc}: raised {type(e).__name__}({e})'
    return '' if got == exp else f'{desc}: actual {got!r}, claimed {exp!r}'

def R01(): return simple(lambda: parse_kv('a=1;b=2'), {'a':'1','b':'2'}, "parse_kv('a=1;b=2')")
def R02(): return simple(lambda: parse_kv('a=1;;b=2'), {'a':'1','b':'2'}, "parse_kv('a=1;;b=2')")
def R03(): return simple(lambda: parse_kv('url=x=y'), {'url':'x=y'}, "parse_kv('url=x=y')")
def R04(): return simple(lambda: parse_kv('a=1;flag'), {'a':'1','flag':''}, "parse_kv('a=1;flag')")

def roundtrip(gen):
    rnd = random.Random(SEED)
    cases = [{}, {'a': '1'}, {'é': 'ж'}, {'a': '', }, {'': ''}, {'': 'x'}, {'a': ';'}, {'a=': 'b'}, {'a;b': 'c'}, {'a': 'b=c'}]
    cases = [c for c in cases if gen(None, c)]
    for _ in range(N):
        d = {}
        for _ in range(rnd.randint(0, 5)):
            d[gen(rnd, None)[0]] = gen(rnd, None)[1]
        cases.append(d)
    return cases

def R05():
    rnd = random.Random(SEED)
    cases = [{}, {'a':'1'}, {'é':'ж'}, {'0':'0'}, {'中':'x','y':'ß'}]
    for _ in range(N):
        cases.append({rs(rnd, ALNUM, 1, 6): rs(rnd, ALNUM, 1, 6) for _ in range(rnd.randint(0, 6))})
    for d in cases:
        try:
            got = parse_kv(to_kv(d))
        except Exception as e:
            return f'd={d!r}: raised {e!r}'
        if got != d:
            return f'd={d!r}: actual {got!r}, claimed {d!r}'
    return ''

def R06():
    rnd = random.Random(SEED)
    cases = [{}, {'a':';'}, {'a=':'b'}, {'a;b':'c'}, {'':''}, {'':'x'}, {'a':''}, {'a':'b=c'}]
    for _ in range(N):
        cases.append({rs(rnd, NASTY): rs(rnd, NASTY) for _ in range(rnd.randint(0, 4))})
    best = None
    for d in cases:
        try:
            got = parse_kv(to_kv(d))
            bad = got != d
            msg = f'd={d!r}: parse_kv(to_kv(d)) = {got!r}, claimed {d!r}'
        except Exception as e:
            bad = True; msg = f'd={d!r}: raised {e!r}'
        if bad and (best is None or len(repr(d)) < len(best[0])):
            best = (repr(d), msg)
    return best[1] if best else ''

def R07(): return simple(lambda: pick({'a':1,'b':2}, ['a','c']), {'a':1}, "pick({'a':1,'b':2},['a','c'])")

def R08():
    rnd = random.Random(SEED)
    keyspace = list('abcde') + ['', 'é', 1, None, (1,)]
    cases = [({}, []), ({}, ['a']), ({'a':1}, ['a','a','a'])]
    for _ in range(N):
        d = {rnd.choice(keyspace): rnd.randint(-5,5) for _ in range(rnd.randint(0,5))}
        ks = [rnd.choice(keyspace) for _ in range(rnd.randint(0,10))]
        cases.append((d, ks))
    for d, ks in cases:
        try:
            r = pick(d, ks)
        except Exception as e:
            return f'pick({d!r},{ks!r}) raised {e!r}'
        if len(r) > len(d):
            return f'pick({d!r},{ks!r}) = {r!r}'
    return ''

def R09(): return simple(lambda: rename({'a':1},{'a':'b'}), {'b':1}, "rename({'a':1},{'a':'b'})")

def R10():
    rnd = random.Random(SEED)
    ks = list('abcd')
    cases = [({}, {}), ({'a':1,'b':2}, {'a':'b'})]
    for _ in range(N):
        d = {rnd.choice(ks): rnd.randint(0,9) for _ in range(rnd.randint(0,4))}
        m = {rnd.choice(ks): rnd.choice(ks) for _ in range(rnd.randint(0,4))}
        cases.append((d, m))
    best = None
    for d, m in cases:
        r = rename(d, m)
        if len(r) != len(d):
            msg = f'rename({d!r},{m!r}) = {r!r}: len {len(r)} != {len(d)}'
            if best is None or len(msg) < len(best): best = msg
    return best or ''

def R11():
    rows = [{'t':'x','v':1},{'t':'y','v':2},{'t':'x','v':3}]
    return simple(lambda: group_by(rows,'t'), {'x':[{'t':'x','v':1},{'t':'x','v':3}],'y':[{'t':'y','v':2}]}, 'group_by example')

def R12():
    rnd = random.Random(SEED)
    cases = [([], 'k')]
    for _ in range(N):
        rows = [{'k': rnd.choice(['a','b','',None,0,1,'é',(1,)]), 'i': i} for i in range(rnd.randint(0,8))]
        cases.append((rows,'k'))
    for rows, k in cases:
        try:
            g = group_by(rows,k)
        except Exception as e:
            return f'group_by({rows!r},{k!r}) raised {e!r}'
        if sum(len(x) for x in g.values()) != len(rows):
            return f'group_by({rows!r},{k!r}) = {g!r}'
    return ''

def R13():
    rnd = random.Random(SEED)
    cases = [[]]
    for _ in range(N):
        cases.append([{'n': rnd.randint(-3,3), 'i': i} for i in range(rnd.randint(0,10))])
        cases.append([{'n': rnd.choice([0.0,-0.0,0,False,1,True,1.0]), 'i': i} for i in range(rnd.randint(0,6))])
    for rows in cases:
        try:
            out = sort_by(rows,'n')
        except Exception as e:
            return f'sort_by({rows!r}) raised {e!r}'
        for a, b in zip(out, out[1:]):
            if a['n'] == b['n'] and a['i'] > b['i']:
                return f'sort_by({rows!r}) = {out!r}'
    return ''

def R14():
    rows = [{'x': 1}, {'n': 1}]
    return simple(lambda: sort_by(rows,'n'), [{'n':1},{'x':1}], f'sort_by({rows!r},"n")')

def R15(): return simple(lambda: deep_get({'a':{'b':{'c':1}}},'a.b.c'), 1, "deep_get nested")
def R16(): return simple(lambda: deep_get({'a':{'b':0}},'a.b',5), 0, "deep_get({'a':{'b':0}},'a.b',5)")
def R17(): return simple(lambda: deep_get({'a':[1,2]},'a.0'), 1, "deep_get({'a':[1,2]},'a.0')")

def R18():
    rnd = random.Random(SEED)
    vals = [None, 0, '', [], {}, {'y':1}, 'v', float('inf'), -1, False]
    cases = [{}, {'x': None}, {'': 1}, {'x.y': 1}, {'x': {'y': 1}}]
    for _ in range(N):
        cases.append({rnd.choice(['x','y','',' ','é','x.y']): rnd.choice(vals) for _ in range(rnd.randint(0,4))})
    for d in cases:
        try:
            got = deep_get(d,'x')
        except Exception as e:
            return f'd={d!r}: raised {e!r}'
        if got is not d.get('x') and got != d.get('x'):
            return f'd={d!r}: actual {got!r}, claimed {d.get("x")!r}'
    return ''

def R19(): return simple(lambda: to_kv({}), '', 'to_kv({})')

def main():
    ids = sys.argv[1:] or [f'R{i:02d}' for i in range(1,20)]
    for i in ids:
        ce = globals()[i]()
        print(json.dumps({"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce, "note": ""}, ensure_ascii=False))

main()
