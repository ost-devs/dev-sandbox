import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.records import *

AL = "abcXYZ019"
def ralnum(r):
    return "".join(r.choice(AL) for _ in range(r.randint(1, 5)))
def rdict_alnum(r):
    return ({ralnum(r): ralnum(r) for _ in range(r.randint(0, 5))},)
def rdict_str(r):
    def t(): return "".join(r.choice("ab;=é ") for _ in range(r.randint(0, 4)))
    return ({t(): t() for _ in range(r.randint(0, 4))},)

def eq(actual, expected):
    if actual != expected:
        raise Counter(f"actual={actual!r} expected={expected!r}")

@claim("R01")
def r01(): eq(parse_kv('a=1;b=2'), {'a': '1', 'b': '2'})
@claim("R02")
def r02(): eq(parse_kv('a=1;;b=2'), {'a': '1', 'b': '2'})
@claim("R03")
def r03(): eq(parse_kv('url=x=y'), {'url': 'x=y'})
@claim("R04")
def r04(): eq(parse_kv('a=1;flag'), {'a': '1', 'flag': ''})
@claim("R05")
def r05(): forall("R05", rdict_alnum, lambda d: parse_kv(to_kv(d)) == d)
@claim("R06")
def r06(): forall("R06", rdict_str, lambda d: parse_kv(to_kv(d)) == d)
@claim("R07")
def r07(): eq(pick({'a': 1, 'b': 2}, ['a', 'c']), {'a': 1})
@claim("R08")
def r08():
    def gen(r):
        d = {r.choice("abcde"): r.randint(0, 9) for _ in range(r.randint(0, 5))}
        return d, [r.choice("abcdefg") for _ in range(r.randint(0, 10))]
    forall("R08", gen, lambda d, k: len(pick(d, k)) <= len(d))
@claim("R09")
def r09(): eq(rename({'a': 1}, {'a': 'b'}), {'b': 1})
@claim("R10")
def r10():
    def gen(r):
        d = {r.choice("abcd"): r.randint(0, 9) for _ in range(r.randint(0, 4))}
        m = {r.choice("abcd"): r.choice("abcd") for _ in range(r.randint(0, 4))}
        return d, m
    forall("R10", gen, lambda d, m: len(rename(d, m)) == len(d))
@claim("R11")
def r11():
    eq(group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't'),
       {'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]})
@claim("R12")
def r12():
    def gen(r):
        return ([{'k': r.choice("abc"), 'i': i} for i in range(r.randint(0, 8))], 'k')
    forall("R12", gen, lambda rows, k: sum(len(g) for g in group_by(rows, k).values()) == len(rows))
@claim("R13")
def r13():
    def gen(r):
        return ([{'n': r.randint(0, 3), 'i': i} for i in range(r.randint(0, 10))],)
    def pred(rows):
        out = sort_by(rows, 'n')
        return all(not (a['n'] == b['n'] and a['i'] > b['i']) for a, b in zip(out, out[1:])) and len(out) == len(rows)
    forall("R13", gen, pred)
@claim("R14")
def r14():
    rows = [{'n': 2}, {'x': 1}, {'n': 1}]
    out = sort_by(rows, 'n')
    eq(out, [{'n': 1}, {'n': 2}, {'x': 1}])
@claim("R15")
def r15(): eq(deep_get({'a': {'b': {'c': 1}}}, 'a.b.c'), 1)
@claim("R16")
def r16(): eq(deep_get({'a': {'b': 0}}, 'a.b', 5), 0)
@claim("R17")
def r17(): eq(deep_get({'a': [1, 2]}, 'a.0'), 1)
@claim("R18")
def r18():
    def gen(r):
        return ({r.choice(["x", "y", "a.b"]): r.choice([None, 0, 1, "s", {}]) for _ in range(r.randint(0, 3))},)
    forall("R18", gen, lambda d: deep_get(d, 'x') == d.get('x'))
@claim("R19")
def r19(): eq(to_kv({}), '')

if __name__=='__main__': main('records')
