import os, sys, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import paths as P

SEED = 20240607


def _eq(expr, got, exp):
    return (True, None) if got == exp and type(got) is type(exp) else (False, f"{expr} -> {got!r} vs. esperado {exp!r}")


def _simple(expr, f, exp):
    try:
        got = f()
    except Exception as e:
        return False, f"{expr} -> exceção {type(e).__name__}: {e}"
    return _eq(expr, got, exp)


def check_P01(): return _simple("join('a','b','c.txt')", lambda: P.join('a', 'b', 'c.txt'), 'a/b/c.txt')
def check_P02(): return _simple("join('/usr','bin')", lambda: P.join('/usr', 'bin'), '/usr/bin')
def check_P03(): return _simple("join('a/','/b')", lambda: P.join('a/', '/b'), 'a/b')
def check_P04(): return _simple("ext('foto.tar.gz')", lambda: P.ext('foto.tar.gz'), 'gz')
def check_P05(): return _simple("ext('dir.d/arquivo')", lambda: P.ext('dir.d/arquivo'), '')
def check_P06(): return _simple("ext('.bashrc')", lambda: P.ext('.bashrc'), '')
def check_P07(): return _simple("stem('relatorio.pdf')", lambda: P.stem('relatorio.pdf'), 'relatorio')
def check_P08(): return _simple("normalize('a/./b/../c')", lambda: P.normalize('a/./b/../c'), 'a/c')
def check_P09(): return _simple("normalize('/a/../..')", lambda: P.normalize('/a/../..'), '/')
def check_P10(): return _simple("normalize('../x')", lambda: P.normalize('../x'), '../x')


def check_P11():
    # exhaustive over alphabet {'', '.', '..', 'a', 'é'} joined by '/', up to 6 segments,
    # plus random strings
    segs = ['', '.', '..', 'a', 'é']
    cases = []
    for n in range(0, 7):
        for combo in itertools.product(segs, repeat=n):
            cases.append('/'.join(combo))
    cases += ['', '/', '//', '...', '.../a', 'a b/ /..', '\\..\\a']
    rng = random.Random(SEED)
    alpha = ['/', '.', 'a', 'b', ' ', 'é', '..', '日']
    for _ in range(20000):
        cases.append(''.join(rng.choice(alpha) for _ in range(rng.randint(0, 14))))
    for x in cases:
        try:
            a = P.normalize(x)
            b = P.normalize(a)
        except Exception as e:
            return False, f"normalize({x!r}) -> exceção {type(e).__name__}: {e}"
        if a != b:
            return False, f"x={x!r}: normalize(x)={a!r}, normalize(normalize(x))={b!r}"
    return True, None


def check_P12(): return _simple("is_hidden('.env')", lambda: P.is_hidden('.env'), True)
def check_P13(): return _simple("is_hidden('config/.git/HEAD')", lambda: P.is_hidden('config/.git/HEAD'), False)
def check_P14(): return _simple("depth('/a/b/c')", lambda: P.depth('/a/b/c'), 3)
def check_P15(): return _simple("depth('a//b/')", lambda: P.depth('a//b/'), 2)
def check_P16(): return _simple("parent('a/b/c')", lambda: P.parent('a/b/c'), 'a/b')
def check_P17(): return _simple("parent('/a')", lambda: P.parent('/a'), '/')


def check_P18():
    # Interpretação: "nomes" = strings não vazias de letras ASCII/dígitos.
    names = ['a', 'Z', '0', 'ab', 'a1', '123', 'x' * 30]
    cases = []
    for n in range(1, 5):
        for combo in itertools.product(names[:5], repeat=n):
            cases.append(list(combo))
    rng = random.Random(SEED)
    chars = 'abcXYZ0129'
    for _ in range(5000):
        cases.append([''.join(rng.choice(chars) for _ in range(rng.randint(1, 8)))
                      for _ in range(rng.randint(1, 8))])
    for parts in cases:
        try:
            d = P.depth(P.join(*parts))
        except Exception as e:
            return False, f"parts={parts!r} -> exceção {type(e).__name__}: {e}"
        if d != len(parts):
            return False, f"parts={parts!r}: depth(join(*parts))={d} vs. esperado {len(parts)}"
    return True, None


def check_P19():
    segs = ['', '.', 'a', 'é', '/', 'tar', ' ']
    cases = []
    for n in range(1, 6):
        for combo in itertools.product(segs, repeat=n):
            s = ''.join(combo)
            if '.' in s:
                cases.append(s)
    rng = random.Random(SEED)
    alpha = ['.', 'a', '/', 'é', ' ', '日', '..']
    for _ in range(20000):
        s = ''.join(rng.choice(alpha) for _ in range(rng.randint(1, 12)))
        if '.' in s:
            cases.append(s)
    for x in cases:
        try:
            r = P.stem(x) + '.' + P.ext(x)
        except Exception as e:
            return False, f"x={x!r} -> exceção {type(e).__name__}: {e}"
        if r != x:
            return False, f"x={x!r}: stem+'.'+ext={r!r} vs. esperado {x!r}"
    return True, None


def main():
    ids = [f"P{i:02d}" for i in range(1, 20)]
    sel = sys.argv[1:] or ids
    for i in sel:
        try:
            ok, msg = globals()['check_' + i]()
        except Exception as e:
            ok, msg = False, f"exceção no check: {type(e).__name__}: {e}"
        msg = (msg or '').replace('\t', ' ').replace('\n', ' ')
        print(f"{i}\t{'verdadeira' if ok else 'falsa'}\t{msg}")


main()
