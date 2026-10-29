from common import *
from kit.paths import *
import string

def paths(cid, n=N):
    r = rng(cid); al = 'ab./' + '.'  # dense in separators/dots
    yield from ['', '/', '.', '..', '//', '/..', 'a/..', '../..', './']
    for _ in range(n):
        yield ''.join(r.choice(al) for _ in range(r.randint(0, 9)))

@claim('P01')
def _(): return eq(lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt')
@claim('P02')
def _(): return eq(lambda: join('/usr', 'bin'), '/usr/bin')
@claim('P03')
def _(): return eq(lambda: join('a/', '/b'), 'a/b')
@claim('P04')
def _(): return eq(lambda: ext('foto.tar.gz'), 'gz')
@claim('P05')
def _(): return eq(lambda: ext('dir.d/arquivo'), '')
@claim('P06')
def _(): return eq(lambda: ext('.bashrc'), '')
@claim('P07')
def _(): return eq(lambda: stem('relatorio.pdf'), 'relatorio')
@claim('P08')
def _(): return eq(lambda: normalize('a/./b/../c'), 'a/c')
@claim('P09')
def _(): return eq(lambda: normalize('/a/../..'), '/')
@claim('P10')
def _(): return eq(lambda: normalize('../x'), '../x')
@claim('P11')
def _(): return forall(paths('P11'), lambda x: normalize(normalize(x)) == normalize(x))
@claim('P12')
def _(): return eq(lambda: is_hidden('.env'), True)
@claim('P13')
def _(): return eq(lambda: is_hidden('config/.git/HEAD'), False)
@claim('P14')
def _(): return eq(lambda: depth('/a/b/c'), 3)
@claim('P15')
def _(): return eq(lambda: depth('a//b/'), 2)
@claim('P16')
def _(): return eq(lambda: parent('a/b/c'), 'a/b')
@claim('P17')
def _(): return eq(lambda: parent('/a'), '/')
@claim('P18')
def _():
    r = rng('P18'); al = string.ascii_letters + string.digits
    ins = [tuple(''.join(r.choice(al) for _ in range(r.randint(1, 4))) for _ in range(r.randint(1, 5))) for _ in range(N)]
    return forall(ins, lambda *parts: depth(join(*parts)) == len(parts))
@claim('P19')
def _(): return forall([p for p in paths('P19') if '.' in p], lambda x: stem(x) + '.' + ext(x) == x)

if __name__ == '__main__': main('paths')
