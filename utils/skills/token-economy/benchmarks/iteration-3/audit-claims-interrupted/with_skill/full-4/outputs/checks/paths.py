import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.paths import *

def eq(actual, expected):
    return True if actual == expected else (False, 'got %r, expected %r' % (actual, expected))

@exact
def P01(): return eq(join('a', 'b', 'c.txt'), 'a/b/c.txt')
@exact
def P02(): return eq(join('/usr', 'bin'), '/usr/bin')
@exact
def P03(): return eq(join('a/', '/b'), 'a/b')
@exact
def P04(): return eq(ext('foto.tar.gz'), 'gz')
@exact
def P05(): return eq(ext('dir.d/arquivo'), '')
@exact
def P06(): return eq(ext('.bashrc'), '')
@exact
def P07(): return eq(stem('relatorio.pdf'), 'relatorio')
@exact
def P08(): return eq(normalize('a/./b/../c'), 'a/c')
@exact
def P09(): return eq(normalize('/a/../..'), '/')
@exact
def P10(): return eq(normalize('../x'), '../x')

PA = "ab./"
@prop
def P11(r):
    x = rand_str(r, 12, ALPHABET if r.random() < .3 else PA)
    a = normalize(x); b = normalize(a)
    if a != b:
        return 'x=%r normalize(x)=%r normalize(normalize(x))=%r' % (x, a, b)

@exact
def P12(): return eq(is_hidden('.env'), True)
@exact
def P13(): return eq(is_hidden('config/.git/HEAD'), False)
@exact
def P14(): return eq(depth('/a/b/c'), 3)
@exact
def P15(): return eq(depth('a//b/'), 2)
@exact
def P16(): return eq(parent('a/b/c'), 'a/b')
@exact
def P17(): return eq(parent('/a'), '/')

LD = string.ascii_letters + string.digits
@prop
def P18(r):
    parts = [''.join(r.choice(LD) for _ in range(r.randint(1, 6))) for _ in range(r.randint(1, 6))]
    d = depth(join(*parts))
    if d != len(parts):
        return 'parts=%r join=%r depth=%r' % (parts, join(*parts), d)

@prop
def P19(r):
    x = rand_str(r, 12, ALPHABET if r.random() < .5 else "ab./")
    if '.' not in x:
        x += '.' + rand_str(r, 3)
    got = stem(x) + '.' + ext(x)
    if got != x:
        return 'x=%r result=%r' % (x, got)

run({k: v for k, v in globals().items() if len(k) == 3 and k[0] == 'P' and k[1:].isdigit()})
