import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import paths as P

A = lambda r: gen_str(r, 12, "ab./_- X1")
AN = "abcXYZ019"

@claim("P01")
def p01(): return eq(P.join('a', 'b', 'c.txt'), 'a/b/c.txt')
@claim("P02")
def p02(): return eq(P.join('/usr', 'bin'), '/usr/bin')
@claim("P03")
def p03(): return eq(P.join('a/', '/b'), 'a/b')
@claim("P04")
def p04(): return eq(P.ext('foto.tar.gz'), 'gz')
@claim("P05")
def p05(): return eq(P.ext('dir.d/arquivo'), '')
@claim("P06")
def p06(): return eq(P.ext('.bashrc'), '')
@claim("P07")
def p07(): return eq(P.stem('relatorio.pdf'), 'relatorio')
@claim("P08")
def p08(): return eq(P.normalize('a/./b/../c'), 'a/c')
@claim("P09")
def p09(): return eq(P.normalize('/a/../..'), '/')
@claim("P10")
def p10(): return eq(P.normalize('../x'), '../x')
@claim("P11")
def p11(): return forall(lambda r: (A(r),), lambda x: P.normalize(P.normalize(x)) == P.normalize(x))
@claim("P12")
def p12(): return None if P.is_hidden('.env') is True else f"got {P.is_hidden('.env')!r}"
@claim("P13")
def p13(): return None if P.is_hidden('config/.git/HEAD') is False else f"got {P.is_hidden('config/.git/HEAD')!r}"
@claim("P14")
def p14(): return eq(P.depth('/a/b/c'), 3)
@claim("P15")
def p15(): return eq(P.depth('a//b/'), 2)
@claim("P16")
def p16(): return eq(P.parent('a/b/c'), 'a/b')
@claim("P17")
def p17(): return eq(P.parent('/a'), '/')
@claim("P18")
def p18(): return forall(lambda r: (["".join(r.choice(AN) for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 5))],), lambda parts: P.depth(P.join(*parts)) == len(parts))
@claim("P19")
def p19(): return forall(lambda r: (A(r) + '.' + A(r),), lambda x: P.stem(x) + '.' + P.ext(x) == x)

if __name__ == "__main__":
    main("paths")
