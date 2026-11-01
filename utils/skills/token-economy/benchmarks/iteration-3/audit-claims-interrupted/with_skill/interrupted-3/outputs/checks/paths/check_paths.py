import sys, os, random, string
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker, rand_strings
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent
c = Checker('paths')

def eq(expr, got, want): return c.eq(got, want)

@c.claim('P01')
def _(): return c.eq(join('a', 'b', 'c.txt'), 'a/b/c.txt')
@c.claim('P02')
def _(): return c.eq(join('/usr', 'bin'), '/usr/bin')
@c.claim('P03')
def _(): return c.eq(join('a/', '/b'), 'a/b')
@c.claim('P04')
def _(): return c.eq(ext('foto.tar.gz'), 'gz')
@c.claim('P05')
def _(): return c.eq(ext('dir.d/arquivo'), '')
@c.claim('P06')
def _(): return c.eq(ext('.bashrc'), '')
@c.claim('P07')
def _(): return c.eq(stem('relatorio.pdf'), 'relatorio')
@c.claim('P08')
def _(): return c.eq(normalize('a/./b/../c'), 'a/c')
@c.claim('P09')
def _(): return c.eq(normalize('/a/../..'), '/')
@c.claim('P10')
def _(): return c.eq(normalize('../x'), '../x')

@c.claim('P11')
def _():
    r = random.Random(1011)
    alpha = 'ab./' 
    ins = rand_strings(1011, 2000) + [''.join(r.choice(alpha) for _ in range(r.randint(0, 8))) for _ in range(3000)]
    return c.forall(ins, lambda x: normalize(normalize(x)) == normalize(x))

@c.claim('P12')
def _(): return c.eq(is_hidden('.env'), True)
@c.claim('P13')
def _(): return c.eq(is_hidden('config/.git/HEAD'), False)
@c.claim('P14')
def _(): return c.eq(depth('/a/b/c'), 3)
@c.claim('P15')
def _(): return c.eq(depth('a//b/'), 2)
@c.claim('P16')
def _(): return c.eq(parent('a/b/c'), 'a/b')
@c.claim('P17')
def _(): return c.eq(parent('/a'), '/')

@c.claim('P18')
def _():
    r = random.Random(1018)
    al = string.ascii_letters + string.digits
    ins = [['a'], ['0'], ['a', 'b'], ['A9', 'z']]
    for _ in range(3000):
        ins.append([''.join(r.choice(al) for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 6))])
    res = c.forall(ins, lambda p: depth(join(*p)) == len(p))
    res.note = 'names taken as non-empty (letters/digits)'
    return res

@c.claim('P19')
def _():
    ins = [x for x in rand_strings(1019, 3000) if '.' in x] + ['.bashrc', 'a.', '.', '..', 'a.b.c', '/a.b/c']
    return c.forall(ins, lambda x: stem(x) + '.' + ext(x) == x)

c.main()
