import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.paths import *

def eq(a, b):
    if a != b:
        raise Counter(f"actual={a!r} expected={b!r}")

def _ex(cid, expr, expected):
    claim(cid)(lambda: eq(expr(), expected))

_ex("P01", lambda: join('a', 'b', 'c.txt'), 'a/b/c.txt')
_ex("P02", lambda: join('/usr', 'bin'), '/usr/bin')
_ex("P03", lambda: join('a/', '/b'), 'a/b')
_ex("P04", lambda: ext('foto.tar.gz'), 'gz')
_ex("P05", lambda: ext('dir.d/arquivo'), '')
_ex("P06", lambda: ext('.bashrc'), '')
_ex("P07", lambda: stem('relatorio.pdf'), 'relatorio')
_ex("P08", lambda: normalize('a/./b/../c'), 'a/c')
_ex("P09", lambda: normalize('/a/../..'), '/')
_ex("P10", lambda: normalize('../x'), '../x')
_ex("P12", lambda: is_hidden('.env'), True)
_ex("P13", lambda: is_hidden('config/.git/HEAD'), False)
_ex("P14", lambda: depth('/a/b/c'), 3)
_ex("P15", lambda: depth('a//b/'), 2)
_ex("P16", lambda: parent('a/b/c'), 'a/b')
_ex("P17", lambda: parent('/a'), '/')

def pathstr(r):
    pool = r.choice(["ab/.", "ab/..", "a/.b", "abc/./.."])
    return ("".join(r.choice(pool) for _ in range(r.randint(0, 12))),)

@claim("P11")
def p11():
    forall("P11", pathstr, lambda x: normalize(normalize(x)) == normalize(x))

@claim("P18")
def p18():
    def gen(r):
        al = "abcXYZ019"
        return ([ "".join(r.choice(al) for _ in range(r.randint(1, 5))) for _ in range(r.randint(1, 6))],)
    forall("P18", gen, lambda parts: depth(join(*parts)) == len(parts))

@claim("P19")
def p19():
    def gen(r):
        s = rand_str(r)
        i = r.randint(0, len(s))
        return (s[:i] + "." + s[i:],)
    forall("P19", gen, lambda x: stem(x) + '.' + ext(x) == x)

if __name__=='__main__': main('paths')
