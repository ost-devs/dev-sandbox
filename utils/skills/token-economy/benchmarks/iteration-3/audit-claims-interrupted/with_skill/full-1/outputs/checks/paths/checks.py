import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, rand_str, main
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent

def eq(expr_s, got, exp):
    if got != exp:
        return f"{expr_s} = {got!r}, expected {exp!r}"

def mk(cid, expr_s, f, exp):
    def fn():
        return eq(expr_s, f(), exp)
    claim(cid)(fn)

mk("P01", "join('a','b','c.txt')", lambda: join('a','b','c.txt'), 'a/b/c.txt')
mk("P02", "join('/usr','bin')", lambda: join('/usr','bin'), '/usr/bin')
mk("P03", "join('a/','/b')", lambda: join('a/','/b'), 'a/b')
mk("P04", "ext('foto.tar.gz')", lambda: ext('foto.tar.gz'), 'gz')
mk("P05", "ext('dir.d/arquivo')", lambda: ext('dir.d/arquivo'), '')
mk("P06", "ext('.bashrc')", lambda: ext('.bashrc'), '')
mk("P07", "stem('relatorio.pdf')", lambda: stem('relatorio.pdf'), 'relatorio')
mk("P08", "normalize('a/./b/../c')", lambda: normalize('a/./b/../c'), 'a/c')
mk("P09", "normalize('/a/../..')", lambda: normalize('/a/../..'), '/')
mk("P10", "normalize('../x')", lambda: normalize('../x'), '../x')
mk("P12", "is_hidden('.env')", lambda: is_hidden('.env'), True)
mk("P13", "is_hidden('config/.git/HEAD')", lambda: is_hidden('config/.git/HEAD'), False)
mk("P14", "depth('/a/b/c')", lambda: depth('/a/b/c'), 3)
mk("P15", "depth('a//b/')", lambda: depth('a//b/'), 2)
mk("P16", "parent('a/b/c')", lambda: parent('a/b/c'), 'a/b')
mk("P17", "parent('/a')", lambda: parent('/a'), '/')

PA = "/.abXY \t\n-_é漢😀"

@claim("P11")
def p11():
    r = rng("P11")
    cases = ["", "/", ".", "..", "/..", "../..", "a/..", "//", "./", "/a/../..", " ", "../x"]
    cases += [rand_str(r, 14, "/../.ab") for _ in range(4000)] + [rand_str(r) for _ in range(1000)]
    for x in cases:
        a = normalize(x); b = normalize(a)
        if a != b:
            return f"normalize(normalize({x!r})) = {b!r}, normalize({x!r}) = {a!r}"

@claim("P18")
def p18():
    r = rng("P18")
    al = "abcXYZ019"
    for parts in [["a"], ["a","b"], ["0"], ["Z"*20, "a"]] + [[ "".join(r.choice(al) for _ in range(r.randint(1,6))) for _ in range(r.randint(1,6))] for _ in range(3000)]:
        o = join(*parts)
        if depth(o) != len(parts):
            return f"depth(join(*{parts!r})) = {depth(o)} (join = {o!r}), expected {len(parts)}"

@claim("P19")
def p19():
    r = rng("P19")
    for x in [".", "a.", ".a", "..", "a.b", "a.b.c", "dir.d/f", "😀.é", "\n.\t"] + [rand_str(r) for _ in range(4000)]:
        if '.' not in x: continue
        o = stem(x) + '.' + ext(x)
        if o != x:
            return f"stem({x!r}) + '.' + ext({x!r}) = {o!r}"

if __name__ == "__main__":
    main()
