import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit import paths as P

def eq(expr, got, want):
    return True if got == want else (False, f"{expr} -> {got!r}, expected {want!r}")

@claim('P01')
def p01(): return eq("join('a','b','c.txt')", P.join('a', 'b', 'c.txt'), 'a/b/c.txt')
@claim('P02')
def p02(): return eq("join('/usr','bin')", P.join('/usr', 'bin'), '/usr/bin')
@claim('P03')
def p03(): return eq("join('a/','/b')", P.join('a/', '/b'), 'a/b')
@claim('P04')
def p04(): return eq("ext('foto.tar.gz')", P.ext('foto.tar.gz'), 'gz')
@claim('P05')
def p05(): return eq("ext('dir.d/arquivo')", P.ext('dir.d/arquivo'), '')
@claim('P06')
def p06(): return eq("ext('.bashrc')", P.ext('.bashrc'), '')
@claim('P07')
def p07(): return eq("stem('relatorio.pdf')", P.stem('relatorio.pdf'), 'relatorio')
@claim('P08')
def p08(): return eq("normalize('a/./b/../c')", P.normalize('a/./b/../c'), 'a/c')
@claim('P09')
def p09(): return eq("normalize('/a/../..')", P.normalize('/a/../..'), '/')
@claim('P10')
def p10(): return eq("normalize('../x')", P.normalize('../x'), '../x')

@claim('P11')
def p11():
    edge = ['', '/', '.', '..', '../x', '/..', 'a/../..', '//', './', 'a//b/', '/a/../../b', '中/../é', '...', '\\']
    r = rng('P11')
    segs = ['a', 'b', '..', '.', '', '中', '...', 'x y']
    cases = edge + [('/' if r.random() < .4 else '') + '/'.join(r.choice(segs) for _ in range(r.randint(0, 7))) for _ in range(3000)]
    cases += [rand_str(r) for _ in range(1000)]
    for x in cases:
        a = P.normalize(x); b = P.normalize(a)
        if a != b: return (False, f"x={x!r} -> {a!r} -> {b!r}")
    return True

@claim('P12')
def p12(): return eq("is_hidden('.env')", P.is_hidden('.env'), True)
@claim('P13')
def p13(): return eq("is_hidden('config/.git/HEAD')", P.is_hidden('config/.git/HEAD'), False)
@claim('P14')
def p14(): return eq("depth('/a/b/c')", P.depth('/a/b/c'), 3)
@claim('P15')
def p15(): return eq("depth('a//b/')", P.depth('a//b/'), 2)
@claim('P16')
def p16(): return eq("parent('a/b/c')", P.parent('a/b/c'), 'a/b')
@claim('P17')
def p17(): return eq("parent('/a')", P.parent('/a'), '/')

@claim('P18')
def p18():
    # names: non-empty strings of letters and digits
    r = rng('P18')
    al = "abcXYZ019éçãØ中"
    cases = [['a'], ['0'], ['a', 'b'], ['中'], ['é', 'ç', 'Ø']]
    for _ in range(3000):
        cases.append([''.join(r.choice(al) for _ in range(r.randint(1, 6))) for _ in range(r.randint(1, 8))])
    for ps in cases:
        j = P.join(*ps); d = P.depth(j)
        if d != len(ps): return (False, f"parts={ps!r} -> join={j!r}, depth={d}")
    return True

@claim('P19')
def p19():
    r = rng('P19')
    edge = ['.', 'a.b', '.bashrc', 'a.', 'a.b.c', 'dir.d/arquivo', '..', 'x/y.z/w', '.a/b', '中.é']
    cases = edge + [rand_str(r, 12, "ab./.中") for _ in range(3000)]
    for x in cases:
        if '.' not in x: continue
        got = P.stem(x) + '.' + P.ext(x)
        if got != x: return (False, f"x={x!r} -> stem={P.stem(x)!r}, ext={P.ext(x)!r}, joined={got!r}")
    return True

if __name__ == '__main__':
    run(__file__)
