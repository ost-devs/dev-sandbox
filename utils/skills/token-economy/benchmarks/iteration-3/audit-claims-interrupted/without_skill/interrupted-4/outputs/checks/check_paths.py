import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.paths import *

SEED = 20261101
N = 30000
ALPHA = list('ab.-_/ ') + ['..', '.', '/', 'é', 'ñ', '日', '😀', '́', '\t', 'Z', '0', '//', './', '../']
ALNUM = list('abcXYZ019') + ['é', 'ñ', '日', 'ß']


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def rand_str(rng, maxlen=10):
    return ''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, maxlen)))


def P01(): return eq(lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt')
def P02(): return eq(lambda: join('/usr', 'bin'), '/usr/bin')
def P03(): return eq(lambda: join('a/', '/b'), 'a/b')
def P04(): return eq(lambda: ext('foto.tar.gz'), 'gz')
def P05(): return eq(lambda: ext('dir.d/arquivo'), '')
def P06(): return eq(lambda: ext('.bashrc'), '')
def P07(): return eq(lambda: stem('relatorio.pdf'), 'relatorio')
def P08(): return eq(lambda: normalize('a/./b/../c'), 'a/c')
def P09(): return eq(lambda: normalize('/a/../..'), '/')
def P10(): return eq(lambda: normalize('../x'), '../x')


def P11():
    rng = random.Random(SEED)
    fixed = ['', '.', '..', '/', '//', '../x', '/..', 'a/../..', '../..', './..', 'a/..', '/a/..', '日/..', ' ', '...', '́/../.']
    cases = fixed + [rand_str(rng) for _ in range(N)]
    for x in cases:
        try:
            a = normalize(x)
            b = normalize(a)
        except Exception as e:
            return False, f'x={x!r}: raised {e!r}'
        if a != b:
            return False, f'x={x!r}: normalize(x)={a!r}, normalize(normalize(x))={b!r}'
    return True, None


def P12(): return eq(lambda: is_hidden('.env'), True)
def P13(): return eq(lambda: is_hidden('config/.git/HEAD'), False)
def P14(): return eq(lambda: depth('/a/b/c'), 3)
def P15(): return eq(lambda: depth('a//b/'), 2)
def P16(): return eq(lambda: parent('a/b/c'), 'a/b')
def P17(): return eq(lambda: parent('/a'), '/')


def P18():
    rng = random.Random(SEED)
    cases = [['a'], ['a', 'b'], ['é'], ['日', '😀'.replace('😀', 'x')], ['0', '1', '2']]
    cases += [[''.join(rng.choice(ALNUM) for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 6))] for _ in range(N)]
    for parts in cases:
        try:
            d = depth(join(*parts))
        except Exception as e:
            return False, f'parts={parts!r}: raised {e!r}'
        if d != len(parts):
            return False, f'parts={parts!r}: depth(join)={d}, expected {len(parts)}'
    return True, None


def P19():
    rng = random.Random(SEED)
    fixed = ['.', 'a.', '.a', 'a.b', 'a.b.c', '..', 'dir.d/arquivo', '.bashrc', 'é.日', 'a/.b/c', '/.', 'x. ', '́.́']
    cases = fixed + [x for x in (rand_str(rng) for _ in range(N * 2)) if '.' in x]
    for x in cases:
        try:
            r = stem(x) + '.' + ext(x)
        except Exception as e:
            return False, f'x={x!r}: raised {e!r}'
        if r != x:
            return False, f'x={x!r}: stem={stem(x)!r}, ext={ext(x)!r}, got {r!r}, expected {x!r}'
    return True, None


CHECKS = {f'P{i:02d}': globals()[f'P{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        try:
            ok, ce = CHECKS[i]()
        except Exception as e:
            ok, ce = False, f'check crashed: {e!r}'
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa', 'counterexample': ce,
                          'command': f'python3 checks/check_paths.py {i}'}, ensure_ascii=False))
