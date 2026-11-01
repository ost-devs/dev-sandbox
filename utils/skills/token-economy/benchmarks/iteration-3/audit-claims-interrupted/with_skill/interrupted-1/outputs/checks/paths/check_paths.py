import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import paths as M

PA = string.ascii_letters + string.digits
PATHALPHA = 'ab./_ é中'
def gpath(r): return ''.join(r.choice(PATHALPHA + '///..') for _ in range(r.randint(0, 12)))
def gname(r): return ''.join(r.choice(PA) for _ in range(r.randint(1, 6)))
def gdot(r):
    s = gpath(r) + '.' + gpath(r); return s

def p11():
    for x in ['', '/', '..', '../x', '/..', 'a/../..', '.', './']:
        if M.normalize(M.normalize(x)) != M.normalize(x): return f'args={x!r}'
    return forall('p11', gpath, lambda x: M.normalize(M.normalize(x)) == M.normalize(x))
def p18():
    return forall('p18', lambda r: [gname(r) for _ in range(r.randint(1, 6))],
                  lambda ps: M.depth(M.join(*ps)) == len(ps))
def p19():
    for x in ['.', 'a.', '.a', 'a.b.c', 'a/b.c/d']:
        if M.stem(x) + '.' + M.ext(x) != x: return f'args={x!r} -> {M.stem(x)!r},{M.ext(x)!r}'
    return forall('p19', gdot, lambda x: M.stem(x) + '.' + M.ext(x) == x)

run('paths', {
 'P01': lambda: eq(lambda: M.join('a','b','c.txt'), 'a/b/c.txt'),
 'P02': lambda: eq(lambda: M.join('/usr','bin'), '/usr/bin'),
 'P03': lambda: eq(lambda: M.join('a/','/b'), 'a/b'),
 'P04': lambda: eq(lambda: M.ext('foto.tar.gz'), 'gz'),
 'P05': lambda: eq(lambda: M.ext('dir.d/arquivo'), ''),
 'P06': lambda: eq(lambda: M.ext('.bashrc'), ''),
 'P07': lambda: eq(lambda: M.stem('relatorio.pdf'), 'relatorio'),
 'P08': lambda: eq(lambda: M.normalize('a/./b/../c'), 'a/c'),
 'P09': lambda: eq(lambda: M.normalize('/a/../..'), '/'),
 'P10': lambda: eq(lambda: M.normalize('../x'), '../x'),
 'P11': p11,
 'P12': lambda: eq(lambda: M.is_hidden('.env'), True),
 'P13': lambda: eq(lambda: M.is_hidden('config/.git/HEAD'), False),
 'P14': lambda: eq(lambda: M.depth('/a/b/c'), 3),
 'P15': lambda: eq(lambda: M.depth('a//b/'), 2),
 'P16': lambda: eq(lambda: M.parent('a/b/c'), 'a/b'),
 'P17': lambda: eq(lambda: M.parent('/a'), '/'),
 'P18': p18,
 'P19': p19,
})
