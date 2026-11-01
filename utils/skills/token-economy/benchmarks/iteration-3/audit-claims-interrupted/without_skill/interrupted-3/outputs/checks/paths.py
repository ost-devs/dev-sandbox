import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit import paths as P

SEED = 20240611
N = 5000


def pt(expr, f, expected):
    def run():
        try:
            got = f()
        except Exception as e:
            return False, "%s -> exceção %r" % (expr, e)
        if got == expected and type(got) == type(expected):
            return True, None
        return False, "%s -> %r (esperado %r)" % (expr, got, expected)
    return run


def univ_norm():
    rng = random.Random(SEED)
    alpha = ['a', 'b', '.', '..', '', '/', 'x.y', '.h']
    fixed = ['', '/', '.', '..', '../x', '/..', '//', 'a/..', './', '../..', '/a/../..', '...']
    def gen():
        for x in fixed:
            yield x
        for _ in range(N):
            yield ''.join(rng.choice(alpha) if rng.random() < .7 else '/' for _ in range(rng.randint(0, 8)))
    for x in gen():
        try:
            a = P.normalize(x); b = P.normalize(a)
        except Exception as e:
            return False, "normalize(%r) -> exceção %r" % (x, e)
        if a != b:
            return False, "x=%r: normalize(x)=%r, normalize(normalize(x))=%r" % (x, a, b)
    return True, None


def univ_depth():
    rng = random.Random(SEED)
    chars = 'abcXYZ019'
    cases = [['a'], ['a', 'b'], ['0'], ['Z'] * 5]
    for _ in range(N):
        cases.append([''.join(rng.choice(chars) for _ in range(rng.randint(1, 6)))
                      for _ in range(rng.randint(1, 8))])
    for parts in cases:
        try:
            j = P.join(*parts); d = P.depth(j)
        except Exception as e:
            return False, "parts=%r -> exceção %r" % (parts, e)
        if d != len(parts):
            return False, "parts=%r: join=%r depth=%r" % (parts, j, d)
    return True, None


def univ_stem():
    rng = random.Random(SEED)
    alpha = 'ab./ _-'
    cases = ['.', 'a.b', '.a', 'a.', 'a.b.c', '..', 'd.d/f', '/.']
    for _ in range(N):
        s = ''.join(rng.choice(alpha) for _ in range(rng.randint(1, 8)))
        if '.' in s:
            cases.append(s)
    for x in cases:
        try:
            r = P.stem(x) + '.' + P.ext(x)
        except Exception as e:
            return False, "x=%r -> exceção %r" % (x, e)
        if r != x:
            return False, "x=%r: stem=%r ext=%r, stem+'.'+ext=%r" % (x, P.stem(x), P.ext(x), r)
    return True, None


C = {
 'P01': pt("join('a','b','c.txt')", lambda: P.join('a', 'b', 'c.txt'), 'a/b/c.txt'),
 'P02': pt("join('/usr','bin')", lambda: P.join('/usr', 'bin'), '/usr/bin'),
 'P03': pt("join('a/','/b')", lambda: P.join('a/', '/b'), 'a/b'),
 'P04': pt("ext('foto.tar.gz')", lambda: P.ext('foto.tar.gz'), 'gz'),
 'P05': pt("ext('dir.d/arquivo')", lambda: P.ext('dir.d/arquivo'), ''),
 'P06': pt("ext('.bashrc')", lambda: P.ext('.bashrc'), ''),
 'P07': pt("stem('relatorio.pdf')", lambda: P.stem('relatorio.pdf'), 'relatorio'),
 'P08': pt("normalize('a/./b/../c')", lambda: P.normalize('a/./b/../c'), 'a/c'),
 'P09': pt("normalize('/a/../..')", lambda: P.normalize('/a/../..'), '/'),
 'P10': pt("normalize('../x')", lambda: P.normalize('../x'), '../x'),
 'P11': univ_norm,
 'P12': pt("is_hidden('.env')", lambda: P.is_hidden('.env'), True),
 'P13': pt("is_hidden('config/.git/HEAD')", lambda: P.is_hidden('config/.git/HEAD'), False),
 'P14': pt("depth('/a/b/c')", lambda: P.depth('/a/b/c'), 3),
 'P15': pt("depth('a//b/')", lambda: P.depth('a//b/'), 2),
 'P16': pt("parent('a/b/c')", lambda: P.parent('a/b/c'), 'a/b'),
 'P17': pt("parent('/a')", lambda: P.parent('/a'), '/'),
 'P18': univ_depth,
 'P19': univ_stem,
}

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(C)
    for i in ids:
        ok, ce = C[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))
