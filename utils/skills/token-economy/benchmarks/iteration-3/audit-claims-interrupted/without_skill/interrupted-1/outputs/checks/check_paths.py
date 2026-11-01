import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.paths import *

SEED = 12345
N = 3000
ALPHA = ['a', 'b', '.', '/', '..', 'x', '1']

def strings():
    """Exhaustive: all concatenations of up to 5 tokens from ALPHA, plus seeded random longer ones."""
    out = []
    for n in range(0, 6):
        for t in itertools.product(ALPHA, repeat=n):
            out.append(''.join(t))
    rng = random.Random(SEED)
    for _ in range(N):
        out.append(''.join(rng.choice(ALPHA) for _ in range(rng.randint(6, 14))))
    return out

_S = None
def S_():
    global _S
    if _S is None: _S = strings()
    return _S

def forall(pred, cases, show):
    for c in cases:
        try:
            if not pred(c):
                return show(c)
        except Exception as e:
            return show(c) + f" -> excecao {type(e).__name__}: {e}"
    return None

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

def eq(f, code):
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", "execucao unica"
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), "execucao unica"

claim('P01')(lambda: eq(lambda: (join('a', 'b', 'c.txt'), 'a/b/c.txt'), "join('a', 'b', 'c.txt')"))
claim('P02')(lambda: eq(lambda: (join('/usr', 'bin'), '/usr/bin'), "join('/usr', 'bin')"))
claim('P03')(lambda: eq(lambda: (join('a/', '/b'), 'a/b'), "join('a/', '/b')"))
claim('P04')(lambda: eq(lambda: (ext('foto.tar.gz'), 'gz'), "ext('foto.tar.gz')"))
claim('P05')(lambda: eq(lambda: (ext('dir.d/arquivo'), ''), "ext('dir.d/arquivo')"))
claim('P06')(lambda: eq(lambda: (ext('.bashrc'), ''), "ext('.bashrc')"))
claim('P07')(lambda: eq(lambda: (stem('relatorio.pdf'), 'relatorio'), "stem('relatorio.pdf')"))
claim('P08')(lambda: eq(lambda: (normalize('a/./b/../c'), 'a/c'), "normalize('a/./b/../c')"))
claim('P09')(lambda: eq(lambda: (normalize('/a/../..'), '/'), "normalize('/a/../..')"))
claim('P10')(lambda: eq(lambda: (normalize('../x'), '../x'), "normalize('../x')"))

def p11():
    r = forall(lambda s: normalize(normalize(s)) == normalize(s), S_(),
               lambda s: f"normalize({s!r}) = {normalize(s)!r}, dupla = {normalize(normalize(s))!r}")
    return r, f"exaustivo ate 5 tokens de {ALPHA} + {N} amostras longas com semente {SEED}; nenhum contraexemplo achado"
claim('P11')(p11)

claim('P12')(lambda: eq(lambda: (is_hidden('.env'), True), "is_hidden('.env')"))
claim('P13')(lambda: eq(lambda: (is_hidden('config/.git/HEAD'), False), "is_hidden('config/.git/HEAD')"))
claim('P14')(lambda: eq(lambda: (depth('/a/b/c'), 3), "depth('/a/b/c')"))
claim('P15')(lambda: eq(lambda: (depth('a//b/'), 2), "depth('a//b/')"))
claim('P16')(lambda: eq(lambda: (parent('a/b/c'), 'a/b'), "parent('a/b/c')"))
claim('P17')(lambda: eq(lambda: (parent('/a'), '/'), "parent('/a')"))

def p18():
    rng = random.Random(SEED)
    names = ['a', 'Z', '0', 'ab1', 'X9y', 'abc123']
    cases = []
    for n in range(1, 5):
        for t in itertools.product(names, repeat=n):
            cases.append(list(t))
    chars = 'abcXYZ0129'
    for _ in range(N):
        cases.append([''.join(rng.choice(chars) for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 8))])
    r = forall(lambda p: depth(join(*p)) == len(p), cases,
               lambda p: f"join(*{p!r}) = {join(*p)!r}, depth = {depth(join(*p))}, len = {len(p)}")
    return r, f"nomes nao vazios alfanumericos; exaustivo ate 4 de {len(names)} nomes + {N} amostras com semente {SEED}; nenhum contraexemplo achado"
claim('P18')(p18)

def p19():
    cases = [s for s in S_() if '.' in s]
    r = forall(lambda s: stem(s) + '.' + ext(s) == s, cases,
               lambda s: f"stem={stem(s)!r}, ext={ext(s)!r}")
    return r, f"{len(cases)} strings com ponto (exaustivo ate 5 tokens + amostras, semente {SEED}); nenhum contraexemplo achado"
claim('P19')(p19)

def main():
    ids = sys.argv[1:] or sorted(R)
    res = []
    for i in ids:
        try:
            ce, note = R[i]()
        except Exception as e:
            ce, note = f"excecao {type(e).__name__}: {e}", "erro na checagem"
        if ce: note = note.replace("; nenhum contraexemplo achado", "; contraexemplo encontrado")
        line = {"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce, "note": note}
        res.append(line)
        print(json.dumps(line, ensure_ascii=False))
    if not sys.argv[1:]:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_paths.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
