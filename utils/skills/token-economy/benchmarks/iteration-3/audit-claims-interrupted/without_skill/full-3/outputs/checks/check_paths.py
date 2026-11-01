import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent

SEED = 12345
N = 5000

def eq(expr_repr, got, want):
    if got == want:
        return True, ""
    return False, "%s -> %r, claimed %r" % (expr_repr, got, want)

def fixed(label, f, want):
    try:
        got = f()
    except Exception as e:
        return False, "%s raised %r" % (label, e)
    return eq(label, got, want)

def P01(): return fixed("join('a','b','c.txt')", lambda: join('a','b','c.txt'), 'a/b/c.txt')
def P02(): return fixed("join('/usr','bin')", lambda: join('/usr','bin'), '/usr/bin')
def P03(): return fixed("join('a/','/b')", lambda: join('a/','/b'), 'a/b')
def P04(): return fixed("ext('foto.tar.gz')", lambda: ext('foto.tar.gz'), 'gz')
def P05(): return fixed("ext('dir.d/arquivo')", lambda: ext('dir.d/arquivo'), '')
def P06(): return fixed("ext('.bashrc')", lambda: ext('.bashrc'), '')
def P07(): return fixed("stem('relatorio.pdf')", lambda: stem('relatorio.pdf'), 'relatorio')
def P08(): return fixed("normalize('a/./b/../c')", lambda: normalize('a/./b/../c'), 'a/c')
def P09(): return fixed("normalize('/a/../..')", lambda: normalize('/a/../..'), '/')
def P10(): return fixed("normalize('../x')", lambda: normalize('../x'), '../x')
def P12(): return fixed("is_hidden('.env')", lambda: is_hidden('.env'), True)
def P13(): return fixed("is_hidden('config/.git/HEAD')", lambda: is_hidden('config/.git/HEAD'), False)
def P14(): return fixed("depth('/a/b/c')", lambda: depth('/a/b/c'), 3)
def P15(): return fixed("depth('a//b/')", lambda: depth('a//b/'), 2)
def P16(): return fixed("parent('a/b/c')", lambda: parent('a/b/c'), 'a/b')
def P17(): return fixed("parent('/a')", lambda: parent('/a'), '/')

ALPHA = list("ab./ ") + ['..', '.', '/', 'é', '日', '\n', '-', '\\', '\x00']
def rand_str(r):
    return ''.join(r.choice(ALPHA) for _ in range(r.randint(0, 10)))

def search(prop, gen, edges):
    r = random.Random(SEED)
    cases = list(edges) + [gen(r) for _ in range(N)]
    bad = []
    for c in cases:
        try:
            ok, msg = prop(c)
        except Exception as e:
            ok, msg = False, "raised %r" % (e,)
        if not ok:
            bad.append((c, msg))
    if not bad:
        return True, ""
    bad.sort(key=lambda t: (len(repr(t[0])), repr(t[0])))
    c, msg = bad[0]
    return False, "input %r: %s" % (c, msg)

def P11():
    def prop(x):
        a = normalize(x); b = normalize(a)
        return (a == b, "normalize(x)=%r, normalize(normalize(x))=%r" % (a, b))
    edges = ['', '/', '.', '..', '/..', '../..', '//', '///a', '//..', 'a/../..', '/a/../..', '../x', './', '...', '.hidden', 'é/../日', ' ', 'a//b']
    return search(prop, rand_str, edges)

def P18():
    def gen(r):
        pool = "abcXYZ019éß日"
        return [''.join(r.choice(pool) for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 6))]
    def prop(parts):
        d = depth(join(*parts))
        return (d == len(parts), "depth(join(*parts))=%r, len=%d" % (d, len(parts)))
    edges = [['a'], ['0'], ['a','b'], ['é'], ['日本','x'], ['a'*1000]*3]
    return search(prop, gen, edges)

def P19():
    def gen(r):
        s = rand_str(r)
        return s if '.' in s else s + '.'
    def prop(x):
        v = stem(x) + '.' + ext(x)
        return (v == x, "stem+'.'+ext=%r" % v)
    edges = ['.', '..', 'a.', '.a', 'a.b', 'a.b.c', '.bashrc', 'dir.d/arquivo', 'é.日', '/.', 'a/b.c/d']
    return search(prop, gen, edges)

CLAIMS = {k: v for k, v in globals().items() if k.startswith('P') and k[1:].isdigit()}

def main():
    ids = sys.argv[1:] or sorted(CLAIMS)
    for i in ids:
        ok, ce = CLAIMS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": "" if ok else ce, "note": ""}, ensure_ascii=False))

if __name__ == '__main__':
    main()
