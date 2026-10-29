from harness import *
import itertools
from kit.paths import *


@claim('P01')
def _(): return eq("join('a','b','c.txt')", lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt')
@claim('P02')
def _(): return eq("join('/usr','bin')", lambda: join('/usr', 'bin'), '/usr/bin')
@claim('P03')
def _(): return eq("join('a/','/b')", lambda: join('a/', '/b'), 'a/b')
@claim('P04')
def _(): return eq("ext('foto.tar.gz')", lambda: ext('foto.tar.gz'), 'gz')
@claim('P05')
def _(): return eq("ext('dir.d/arquivo')", lambda: ext('dir.d/arquivo'), '')
@claim('P06')
def _(): return eq("ext('.bashrc')", lambda: ext('.bashrc'), '')
@claim('P07')
def _(): return eq("stem('relatorio.pdf')", lambda: stem('relatorio.pdf'), 'relatorio')
@claim('P08')
def _(): return eq("normalize('a/./b/../c')", lambda: normalize('a/./b/../c'), 'a/c')
@claim('P09')
def _(): return eq("normalize('/a/../..')", lambda: normalize('/a/../..'), '/')
@claim('P10')
def _(): return eq("normalize('../x')", lambda: normalize('../x'), '../x')
@claim('P11')
def _():
    # exaustivo: todas as strings de comprimento <= 6 sobre {'/', '.', 'a'}
    cases = [''.join(t) for n in range(0, 7) for t in itertools.product('/.a', repeat=n)]
    return forall(cases, lambda x: normalize(normalize(x)) == normalize(x) or f'{normalize(x)!r} -> {normalize(normalize(x))!r}')
@claim('P12')
def _(): return eq("is_hidden('.env')", lambda: is_hidden('.env'), True)
@claim('P13')
def _(): return eq("is_hidden('config/.git/HEAD')", lambda: is_hidden('config/.git/HEAD'), False)
@claim('P14')
def _(): return eq("depth('/a/b/c')", lambda: depth('/a/b/c'), 3)
@claim('P15')
def _(): return eq("depth('a//b/')", lambda: depth('a//b/'), 2)
@claim('P16')
def _(): return eq("parent('a/b/c')", lambda: parent('a/b/c'), 'a/b')
@claim('P17')
def _(): return eq("parent('/a')", lambda: parent('/a'), '/')
@claim('P18')
def _():
    r = rng('P18')
    al = 'abcXYZ0189'
    cases = [[''.join(r.choice(al) for _ in range(r.randint(1, 6))) for _ in range(r.randint(1, 6))] for _ in range(5000)]
    return forall(cases, lambda ps: depth(join(*ps)) == len(ps))
@claim('P19')
def _():
    cases = [''.join(t) for n in range(1, 8) for t in itertools.product('a./', repeat=n) if '.' in t]
    return forall(cases, lambda x: stem(x) + '.' + ext(x) == x)

if __name__ == '__main__':
    sys.exit(main())
