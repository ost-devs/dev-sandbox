import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import records as M
import string
AN = string.ascii_letters + string.digits
def gdict(r, alpha=ALPHABET, ne=False):
    lo = 1 if ne else 0
    return {''.join(r.choice(alpha) for _ in range(r.randint(lo,5))): ''.join(r.choice(alpha) for _ in range(r.randint(lo,5))) for _ in range(r.randint(0,5))}
def first(*xs):
    for x in xs:
        if x: return x
def R05():
    return forall('R05', lambda r: gdict(r, AN, True), lambda d: M.parse_kv(M.to_kv(d)) == d)
def R06():
    t = first(*[(lambda e,d: e and f'd={d!r}: {e}')(eq(lambda d=d: M.parse_kv(M.to_kv(d)), d), d) for d in [{}, {'a':''}, {'':''}, {'a':'b;c'}, {'a=b':'c'}, {'a;b':'1'}]])
    return t or forall('R06', gdict, lambda d: M.parse_kv(M.to_kv(d)) == d)
def R08():
    return forall('R08', lambda r: (gdict(r), [gen_str(r,3) for _ in range(r.randint(0,6))]), lambda d,k: len(M.pick(d,k)) <= len(d))
def R10():
    def g(r):
        d = gdict(r, 'abc'); m = gdict(r, 'abc'); return d, m
    t = eq(lambda: len(M.rename({'a':1,'b':2},{'a':'b'})), 2)
    return t or forall('R10', g, lambda d,m: len(M.rename(d,m)) == len(d))
def R12():
    def g(r):
        return [{'k': r.choice('abc'), 'v': r.randint(0,9)} for _ in range(r.randint(0,10))], 'k'
    return forall('R12', g, lambda rows,k: sum(len(x) for x in M.group_by(rows,k).values()) == len(rows))
def R13():
    def g(r):
        return [{'n': r.randint(0,3), 'i': i} for i in range(r.randint(0,12))],
    def p(rows):
        out = M.sort_by(rows,'n')
        return out == sorted(rows, key=lambda x:(x['n'], x['i']))
    return forall('R13', g, p)
def R14():
    t = eq(lambda: M.sort_by([{'x':1},{'n':1}],'n'), [{'n':1},{'x':1}])
    if t: return "rows=[{'x':1},{'n':1}]: "+t
    def g(r):
        return [({'n': r.randint(0,5)} if r.random()<.6 else {'x': i}) for i in range(r.randint(0,6))],
    def p(rows):
        out = M.sort_by(rows,'n'); seen = False
        for x in out:
            if 'n' not in x: seen = True
            elif seen: return False
        return True
    return forall('R14', g, p)
def R18():
    def g(r):
        d = gdict(r, 'xyz.')
        if r.random()<.5: d['x'] = r.choice([None, 0, '', [], {}, 'v', {'y':1}])
        return d,
    return forall('R18', g, lambda d: M.deep_get(d,'x') == d.get('x'))
run('records', {
 'R01': lambda: eq(lambda: M.parse_kv('a=1;b=2'), {'a':'1','b':'2'}),
 'R02': lambda: eq(lambda: M.parse_kv('a=1;;b=2'), {'a':'1','b':'2'}),
 'R03': lambda: eq(lambda: M.parse_kv('url=x=y'), {'url':'x=y'}),
 'R04': lambda: eq(lambda: M.parse_kv('a=1;flag'), {'a':'1','flag':''}),
 'R05': R05, 'R06': R06,
 'R07': lambda: eq(lambda: M.pick({'a':1,'b':2},['a','c']), {'a':1}),
 'R08': R08,
 'R09': lambda: eq(lambda: M.rename({'a':1},{'a':'b'}), {'b':1}),
 'R10': R10,
 'R11': lambda: eq(lambda: M.group_by([{'t':'x','v':1},{'t':'y','v':2},{'t':'x','v':3}],'t'), {'x':[{'t':'x','v':1},{'t':'x','v':3}],'y':[{'t':'y','v':2}]}),
 'R12': R12, 'R13': R13, 'R14': R14,
 'R15': lambda: eq(lambda: M.deep_get({'a':{'b':{'c':1}}},'a.b.c'), 1),
 'R16': lambda: eq(lambda: M.deep_get({'a':{'b':0}},'a.b',5), 0),
 'R17': lambda: eq(lambda: M.deep_get({'a':[1,2]},'a.0'), 1),
 'R18': R18,
 'R19': lambda: eq(lambda: M.to_kv({}), ''),
})
