from lib import rng, first_fail, eq, N
from kit.paths import *

PATH_ALPHA = ['a', 'b', '.', '..', '/', '/', 'x', '.', '']
EDGE = ['', '/', '.', '..', '/..', '../x', 'a/../..', '//', './', '/a/..', 'a/', '/a//b/./c/..']


def paths(tag, n=N):
    r = rng(tag)
    yield from EDGE
    for _ in range(n):
        yield ''.join(r.choice(PATH_ALPHA) for _ in range(r.randint(0, 8)))


def dotted(tag, n=N):
    for s in paths(tag, n):
        if '.' in s:
            yield s
    yield from ['a.b', '.', '.bashrc', 'a.', 'dir.d/arquivo', 'a.b.c']


def name_lists(tag, n=N):
    r = rng(tag)
    al = 'abcXYZ0129'
    for _ in range(n):
        yield [''.join(r.choice(al) for _ in range(r.randint(1, 4))) for _ in range(r.randint(1, 5))]
    yield ['a']


CHECKS = {
    'P01': lambda: eq(lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt', 'join'),
    'P02': lambda: eq(lambda: join('/usr', 'bin'), '/usr/bin', "join('/usr','bin')"),
    'P03': lambda: eq(lambda: join('a/', '/b'), 'a/b', "join('a/','/b')"),
    'P04': lambda: eq(lambda: ext('foto.tar.gz'), 'gz', 'ext'),
    'P05': lambda: eq(lambda: ext('dir.d/arquivo'), '', "ext('dir.d/arquivo')"),
    'P06': lambda: eq(lambda: ext('.bashrc'), '', "ext('.bashrc')"),
    'P07': lambda: eq(lambda: stem('relatorio.pdf'), 'relatorio', 'stem'),
    'P08': lambda: eq(lambda: normalize('a/./b/../c'), 'a/c', 'normalize'),
    'P09': lambda: eq(lambda: normalize('/a/../..'), '/', "normalize('/a/../..')"),
    'P10': lambda: eq(lambda: normalize('../x'), '../x', "normalize('../x')"),
    'P11': lambda: first_fail(paths('p11'), lambda x: normalize(normalize(x)) == normalize(x)),
    'P12': lambda: eq(lambda: is_hidden('.env'), True, "is_hidden('.env')"),
    'P13': lambda: eq(lambda: is_hidden('config/.git/HEAD'), False, 'is_hidden'),
    'P14': lambda: eq(lambda: depth('/a/b/c'), 3, 'depth'),
    'P15': lambda: eq(lambda: depth('a//b/'), 2, 'depth'),
    'P16': lambda: eq(lambda: parent('a/b/c'), 'a/b', 'parent'),
    'P17': lambda: eq(lambda: parent('/a'), '/', "parent('/a')"),
    'P18': lambda: first_fail(name_lists('p18'), lambda ps: depth(join(*ps)) == len(ps)),
    'P19': lambda: first_fail(dotted('p19'), lambda x: stem(x) + '.' + ext(x) == x),
}
