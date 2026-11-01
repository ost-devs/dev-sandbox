import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import paths as P

CMD = 'python3 -I checks/paths.py'
rng = random.Random(20240601)

def run(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return 'EXC:%s' % type(e).__name__

def eq(id_, call, expected, label):
    r = run(*call)
    if r == expected:
        return None
    return '%s -> %r (esperado %r)' % (label, r, expected)

ALPH = ['a', 'b', '.', '/', '..', '', 'x']
def rand_paths(n=3000):
    out = ['', '/', '//', '.', '..', '/..', 'a//b', 'a/', '/a/', '../..', './a', 'a/..', '/a/../..',
           '../x', '/../x', 'a/../../b', '...', 'a/./', '//a', './/.', '..//a', '../', '/.', 'a/b/../../..']
    for _ in range(n):
        out.append(''.join(rng.choice(ALPH) for _ in range(rng.randint(0, 8))))
    return out
PATHS = rand_paths()

def simple(call, expected):
    f = call[0]
    return eq(None, call, expected, '%s%r' % (f.__name__, call[1:]))

res = {}
res['P01'] = simple((P.join, 'a', 'b', 'c.txt'), 'a/b/c.txt')
res['P02'] = simple((P.join, '/usr', 'bin'), '/usr/bin')
res['P03'] = simple((P.join, 'a/', '/b'), 'a/b')
res['P04'] = simple((P.ext, 'foto.tar.gz'), 'gz')
res['P05'] = simple((P.ext, 'dir.d/arquivo'), '')
res['P06'] = simple((P.ext, '.bashrc'), '')
res['P07'] = simple((P.stem, 'relatorio.pdf'), 'relatorio')
res['P08'] = simple((P.normalize, 'a/./b/../c'), 'a/c')
res['P09'] = simple((P.normalize, '/a/../..'), '/')
res['P10'] = simple((P.normalize, '../x'), '../x')

def p11():
    for x in PATHS:
        a = run(P.normalize, x)
        b = run(P.normalize, a) if not str(a).startswith('EXC:') else a
        if a != b or str(a).startswith('EXC:'):
            return 'x=%r normalize(x)=%r normalize(normalize(x))=%r' % (x, a, b)
res['P11'] = p11()
res['P12'] = simple((P.is_hidden, '.env'), True)
res['P13'] = simple((P.is_hidden, 'config/.git/HEAD'), False)
res['P14'] = simple((P.depth, '/a/b/c'), 3)
res['P15'] = simple((P.depth, 'a//b/'), 2)
res['P16'] = simple((P.parent, 'a/b/c'), 'a/b')
res['P17'] = simple((P.parent, '/a'), '/')

def p18():
    cases = [['a'], ['a', 'b'], ['A1', 'b2', 'c3'], ['0'], ['x'] * 5]
    for _ in range(2000):
        cases.append([''.join(rng.choice('abcXYZ019') for _ in range(rng.randint(1, 5)))
                      for _ in range(rng.randint(1, 6))])
    for parts in cases:
        r = run(lambda: P.depth(P.join(*parts)))
        if r != len(parts):
            return 'parts=%r depth(join(*parts))=%r' % (parts, r)
res['P18'] = p18()

def p19():
    xs = ['.', 'a.b', '..', '.a', 'a.', 'a.b.c', '/.', './', 'dir.d/f', 'a..b', '.bashrc', 'a/b.c/d']
    for _ in range(3000):
        xs.append(''.join(rng.choice('ab./') for _ in range(rng.randint(1, 8))))
    for x in xs:
        if '.' not in x:
            continue
        r = run(lambda: P.stem(x) + '.' + P.ext(x))
        if r != x:
            return 'x=%r stem(x)+"."+ext(x)=%r' % (x, r)
res['P19'] = p19()

for i in range(1, 20):
    k = 'P%02d' % i
    c = res[k]
    print('\t'.join([k, 'falsa' if c else 'verdadeira', (c or '').replace('\t', ' ').replace('\n', ' '), CMD]))
