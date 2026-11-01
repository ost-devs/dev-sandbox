import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.paths import join, ext, stem, normalize, is_hidden, depth, parent

SEED = 12345
N = 4000


def eq(expr, got, want):
    if got == want:
        return True, None
    return False, "%s -> %r, esperado %r" % (expr, got, want)


def check_P01(): return eq("join('a','b','c.txt')", join('a', 'b', 'c.txt'), 'a/b/c.txt')
def check_P02(): return eq("join('/usr','bin')", join('/usr', 'bin'), '/usr/bin')
def check_P03(): return eq("join('a/','/b')", join('a/', '/b'), 'a/b')
def check_P04(): return eq("ext('foto.tar.gz')", ext('foto.tar.gz'), 'gz')
def check_P05(): return eq("ext('dir.d/arquivo')", ext('dir.d/arquivo'), '')
def check_P06(): return eq("ext('.bashrc')", ext('.bashrc'), '')
def check_P07(): return eq("stem('relatorio.pdf')", stem('relatorio.pdf'), 'relatorio')
def check_P08(): return eq("normalize('a/./b/../c')", normalize('a/./b/../c'), 'a/c')
def check_P09(): return eq("normalize('/a/../..')", normalize('/a/../..'), '/')
def check_P10(): return eq("normalize('../x')", normalize('../x'), '../x')
def check_P12(): return eq("is_hidden('.env')", is_hidden('.env'), True)
def check_P13(): return eq("is_hidden('config/.git/HEAD')", is_hidden('config/.git/HEAD'), False)
def check_P14(): return eq("depth('/a/b/c')", depth('/a/b/c'), 3)
def check_P15(): return eq("depth('a//b/')", depth('a//b/'), 2)
def check_P16(): return eq("parent('a/b/c')", parent('a/b/c'), 'a/b')
def check_P17(): return eq("parent('/a')", parent('/a'), '/')


ALPHA = list("ab/.. /\t") + ['é', '日', '', '-', 'x', '..', '.', '//']


def rand_str(r):
    return ''.join(r.choice(ALPHA) for _ in range(r.randint(0, 10)))


def check_P11():
    r = random.Random(SEED)
    cases = ['', '/', '.', '..', '/..', '../x', '/a/../..', 'a/..', '//', ' ', 'a//b/', './.']
    cases += [rand_str(r) for _ in range(N)]
    for x in cases:
        a = normalize(x)
        if normalize(a) != a:
            return False, "x=%r: normalize(x)=%r, normalize(normalize(x))=%r" % (x, a, normalize(a))
    return True, None


def check_P18():
    r = random.Random(SEED)
    pool = list("abcXYZ019éß日")
    cases = [['a'], ['a', 'b'], ['1'] * 5, ['é', '日']]
    for _ in range(N):
        cases.append([''.join(r.choice(pool) for _ in range(r.randint(1, 6)))
                      for _ in range(r.randint(1, 6))])
    for parts in cases:
        if depth(join(*parts)) != len(parts):
            return False, "parts=%r: join=%r depth=%d" % (parts, join(*parts), depth(join(*parts)))
    return True, None


def check_P19():
    r = random.Random(SEED)
    cases = ['.', 'a.b', '.bashrc', 'a.', 'a..b', '.a.', 'dir.d/arquivo', '...']
    cases += [x for x in (rand_str(r) for _ in range(N * 2)) if '.' in x]
    for x in cases:
        if stem(x) + '.' + ext(x) != x:
            return False, "x=%r: stem=%r ext=%r" % (x, stem(x), ext(x))
    return True, None


IDS = ["P%02d" % i for i in range(1, 20)]

if __name__ == '__main__':
    ids = sys.argv[1:] or IDS
    for i in ids:
        ok, ce = globals()['check_' + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": ce,
                          "command": "python3 -I checks/paths.py " + i}, ensure_ascii=False))
