#!/usr/bin/env python3
import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.paths import *

SEED = 20240611
N = 5000
EDGE = ['', '/', '//', '.', '..', './', '../', '/..', '/.', 'a/', '/a', 'a//b', '.a', 'a.', '..a', 'a..', 'a.b.c',
        '/a/../..', '../x', '../../x', 'a/../..', 'dir.d/f', '.bashrc', '...', '/./', 'a/./b/../c']

def strings(alpha='a./', maxlen=6):
    for e in EDGE:
        yield e
    for n in range(maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            yield ''.join(t)
    r = random.Random(SEED)
    al = list('ab.//..x1 ')
    for _ in range(N):
        yield ''.join(r.choice(al) for _ in range(r.randint(0, 14)))

def eq(expr, got, want):
    return None if got == want else "%s -> %r, esperado %r" % (expr, got, want)

def concrete(expr, f, want):
    try:
        got = f()
    except Exception as e:
        return "%s lançou %s, esperado %r" % (expr, type(e).__name__, want)
    return eq(expr, got, want)

def forall(pred, gen, fmt):
    best = None
    for s in gen:
        try:
            ok = pred(s)
        except Exception as e:
            ok = False
            msg = "exceção %s" % type(e).__name__
        else:
            msg = None
        if not ok:
            if best is None or len(repr(s)) < len(repr(best[0])):
                best = (s, msg)
    if best is None:
        return None
    return fmt(best[0]) + (" (%s)" % best[1] if best[1] else "")

C = {}
def claim(i):
    def d(f):
        C[i] = f
        return f
    return d

claim('P01')(lambda: concrete("join('a','b','c.txt')", lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt'))
claim('P02')(lambda: concrete("join('/usr','bin')", lambda: join('/usr', 'bin'), '/usr/bin'))
claim('P03')(lambda: concrete("join('a/','/b')", lambda: join('a/', '/b'), 'a/b'))
claim('P04')(lambda: concrete("ext('foto.tar.gz')", lambda: ext('foto.tar.gz'), 'gz'))
claim('P05')(lambda: concrete("ext('dir.d/arquivo')", lambda: ext('dir.d/arquivo'), ''))
claim('P06')(lambda: concrete("ext('.bashrc')", lambda: ext('.bashrc'), ''))
claim('P07')(lambda: concrete("stem('relatorio.pdf')", lambda: stem('relatorio.pdf'), 'relatorio'))
claim('P08')(lambda: concrete("normalize('a/./b/../c')", lambda: normalize('a/./b/../c'), 'a/c'))
claim('P09')(lambda: concrete("normalize('/a/../..')", lambda: normalize('/a/../..'), '/'))
claim('P10')(lambda: concrete("normalize('../x')", lambda: normalize('../x'), '../x'))

@claim('P11')
def _():
    return forall(lambda x: normalize(normalize(x)) == normalize(x), strings(),
                  lambda x: "x=%r: normalize(normalize(x))=%r != normalize(x)=%r" % (x, normalize(normalize(x)), normalize(x)))

claim('P12')(lambda: concrete("is_hidden('.env')", lambda: is_hidden('.env'), True))
claim('P13')(lambda: concrete("is_hidden('config/.git/HEAD')", lambda: is_hidden('config/.git/HEAD'), False))
claim('P14')(lambda: concrete("depth('/a/b/c')", lambda: depth('/a/b/c'), 3))
claim('P15')(lambda: concrete("depth('a//b/')", lambda: depth('a//b/'), 2))
claim('P16')(lambda: concrete("parent('a/b/c')", lambda: parent('a/b/c'), 'a/b'))
claim('P17')(lambda: concrete("parent('/a')", lambda: parent('/a'), '/'))

@claim('P18')
def _():
    # nomes de letras e dígitos (não vazios); listas não vazias
    r = random.Random(SEED)
    names = ['a', 'B', '0', 'ab1', 'Z9z']
    cases = []
    for n in range(1, 5):
        cases += [list(t) for t in itertools.product(names, repeat=n)] if n <= 3 else []
    for _ in range(N):
        cases.append([''.join(r.choice('abcXYZ019') for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 8))])
    bad = None
    for p in cases:
        if depth(join(*p)) != len(p):
            if bad is None or len(repr(p)) < len(repr(bad)):
                bad = p
    if bad is None:
        return None
    return "parts=%r: depth(join(*parts))=%r != %r" % (bad, depth(join(*bad)), len(bad))

@claim('P19')
def _():
    return forall(lambda x: stem(x) + '.' + ext(x) == x, (s for s in strings() if '.' in s),
                  lambda x: "x=%r: stem+'.'+ext=%r" % (x, stem(x) + '.' + ext(x)))

def main():
    ids = sys.argv[1:] or sorted(C)
    for i in ids:
        ce = C[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ce is None else "falsa", "counterexample": ce}, ensure_ascii=False))

if __name__ == '__main__':
    main()
