import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import Checker, rand_text
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent

c = Checker("paths")
def eq(a, b): return None if a == b else f"got {a!r}, expected {b!r}"
c.fixed("P01", lambda: eq(join('a', 'b', 'c.txt'), 'a/b/c.txt'))
c.fixed("P02", lambda: eq(join('/usr', 'bin'), '/usr/bin'))
c.fixed("P03", lambda: eq(join('a/', '/b'), 'a/b'))
c.fixed("P04", lambda: eq(ext('foto.tar.gz'), 'gz'))
c.fixed("P05", lambda: eq(ext('dir.d/arquivo'), ''))
c.fixed("P06", lambda: eq(ext('.bashrc'), ''))
c.fixed("P07", lambda: eq(stem('relatorio.pdf'), 'relatorio'))
c.fixed("P08", lambda: eq(normalize('a/./b/../c'), 'a/c'))
c.fixed("P09", lambda: eq(normalize('/a/../..'), '/'))
c.fixed("P10", lambda: eq(normalize('../x'), '../x'))
c.prop("P11", lambda r: (rand_text(r, 14),), lambda x: normalize(normalize(x)) == normalize(x))
c.fixed("P12", lambda: eq(is_hidden('.env'), True))
c.fixed("P13", lambda: eq(is_hidden('config/.git/HEAD'), False))
c.fixed("P14", lambda: eq(depth('/a/b/c'), 3))
c.fixed("P15", lambda: eq(depth('a//b/'), 2))
c.fixed("P16", lambda: eq(parent('a/b/c'), 'a/b'))
c.fixed("P17", lambda: eq(parent('/a'), '/'))
L = "abcXYZ019"
c.prop("P18", lambda r: ([ "".join(r.choice(L) for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 6))],),
       lambda parts: depth(join(*parts)) == len(parts))
c.prop("P19", lambda r: (rand_text(r, 12) + ".",) if False else ((lambda s: (s[:(k:=r.randint(0,len(s)))] + "." + s[k:]))(rand_text(r, 12)),),
       lambda x: stem(x) + '.' + ext(x) == x)
c.finish()
