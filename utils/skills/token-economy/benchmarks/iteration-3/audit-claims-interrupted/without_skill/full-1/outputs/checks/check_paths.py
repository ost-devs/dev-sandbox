import itertools, string
from _common import Results, rng
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent

R = Results("paths")

def eq(f, args, exp):
    def fn():
        got = f(*args)
        return got == exp, (args, got)
    return fn

def allstrs(alpha, n):
    for k in range(n + 1):
        for t in itertools.product(alpha, repeat=k):
            yield ''.join(t)

R.check("P01", eq(join, ('a', 'b', 'c.txt'), 'a/b/c.txt'))
R.check("P02", eq(join, ('/usr', 'bin'), '/usr/bin'))
R.check("P03", eq(join, ('a/', '/b'), 'a/b'))
R.check("P04", eq(ext, ('foto.tar.gz',), 'gz'))
R.check("P05", eq(ext, ('dir.d/arquivo',), ''))
R.check("P06", eq(ext, ('.bashrc',), ''))
R.check("P07", eq(stem, ('relatorio.pdf',), 'relatorio'))
R.check("P08", eq(normalize, ('a/./b/../c',), 'a/c'))
R.check("P09", eq(normalize, ('/a/../..',), '/'))
R.check("P10", eq(normalize, ('../x',), '../x'))

def p11():
    r = rng()
    cands = list(allstrs('a./', 7))
    al = 'ab./é \n'
    cands += [''.join(r.choice(al) for _ in range(r.randint(0, 15))) for _ in range(5000)]
    for x in cands:
        if normalize(normalize(x)) != normalize(x):
            return False, (x, normalize(x), normalize(normalize(x)))
    return True, None
R.check("P11", p11)
R.check("P12", lambda: (is_hidden('.env') is True, is_hidden('.env')))
R.check("P13", lambda: (is_hidden('config/.git/HEAD') is False, is_hidden('config/.git/HEAD')))
R.check("P14", eq(depth, ('/a/b/c',), 3))
R.check("P15", eq(depth, ('a//b/',), 2))
R.check("P16", eq(parent, ('a/b/c',), 'a/b'))
R.check("P17", eq(parent, ('/a',), '/'))

def p18():
    r = rng()
    names = list(string.ascii_letters + string.digits) + ['ab', 'Z9', 'é', 'x1y2']
    for n in range(1, 5):
        for parts in itertools.product(names[:12], repeat=n):
            if depth(join(*parts)) != len(parts):
                return False, parts
    for _ in range(3000):
        parts = [''.join(r.choice(string.ascii_letters + string.digits) for _ in range(r.randint(1, 6))) for _ in range(r.randint(1, 8))]
        if depth(join(*parts)) != len(parts):
            return False, parts
    return True, None
R.check("P18", p18)

def p19():
    r = rng()
    cands = [x for x in allstrs('a./', 7) if '.' in x]
    al = 'ab./é \n'
    cands += [x for x in (''.join(r.choice(al) for _ in range(r.randint(1, 15))) for _ in range(5000)) if '.' in x]
    for x in cands:
        if stem(x) + '.' + ext(x) != x:
            return False, x
    return True, None
R.check("P19", p19)
R.finish()
