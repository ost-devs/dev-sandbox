import json, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.lists import *  # noqa

SEED = 20240611
N = 3000


def rand_list(r, lo=-5, hi=5, maxlen=12):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]


def point(expr, f, expected):
    def run():
        try:
            got = f()
        except Exception as e:
            return False, "%s raised %s: %s" % (expr, type(e).__name__, e)
        if got == expected:
            return True, None
        return False, "%s -> %r (esperado %r)" % (expr, got, expected)
    return run


def univ(gen, pred, desc):
    """gen(r) -> args tuple; pred(*args) -> bool. Edge cases first, then random."""
    def run():
        r = random.Random(SEED)
        cases = list(EDGE[desc]) + [gen(r) for _ in range(N)]
        for args in cases:
            try:
                ok, got = pred(*args)
            except Exception as e:
                return False, "%s com entrada %r: exceção %s: %s" % (desc, args, type(e).__name__, e)
            if not ok:
                return False, "%s com entrada %r -> %r" % (desc, args, got)
        return True, None
    return run


def p_throws(xs, k):
    try:
        chunk(xs, k)
    except ValueError:
        return True
    except Exception as e:
        return False
    return False

L = [[], [0], [1, 2, 3], [3, 3], [-1, 0, 1]]
EDGE = {
    "L02": [(x, k) for x in L for k in (1, 2, 3, 10)],
    "L05": [(x,) for x in L],
    "L06": [(x,) for x in L],
    "L09": [(x, k) for x in L for k in (0, 1, 2, 5)],
    "L12": [(x, k) for x in L[1:] for k in (0, 1, 2, 3, 4, 5, 7)],
    "L13": [(x, k) for x in L for k in (-5, -1, 0, 1, 5)],
    "L15": [(a, b) for a in L for b in L],
    "L17": [(x,) for x in L],
    "L19": [(x,) for x in L],
}


def first_occ(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

EDGE["L05"] = [(x,) for x in L]


def chk(name, f):
    def p(*a):
        v, got = f(*a)
        return v, got
    return p

CLAIMS = {
 "L01": point("chunk(list(range(7)), 3)", lambda: chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]]),
 "L02": univ(lambda r: (rand_list(r), r.randint(1, 8)), lambda xs, k: (lambda g: (g == xs, g))(flatten(chunk(xs, k))), "L02"),
 "L03": None,
 "L04": point("dedupe([3,1,3,2,1])", lambda: dedupe([3,1,3,2,1]), [3,1,2]),
 "L05": univ(lambda r: (rand_list(r),), lambda xs: (lambda g: (g == first_occ(xs), g))(dedupe(xs)), "L05"),
 "L06": univ(lambda r: (rand_list(r),), lambda xs: (lambda g: (len(g) == len(set(xs)), g))(dedupe(xs)), "L06"),
 "L07": point("flatten([[1,[2]],[3]])", lambda: flatten([[1,[2]],[3]]), [1,2,3]),
 "L08": point("top_n([5,1,4],2)", lambda: top_n([5,1,4],2), [5,4]),
 "L09": univ(lambda r: (rand_list(r), r.randint(0, 15)), lambda xs, k: (lambda g: (len(g) == min(k, len(xs)), g))(top_n(xs, k)), "L09"),
 "L10": point("top_n([3,2,1],-1)", lambda: top_n([3,2,1],-1), []),
 "L11": point("rotate([1,2,3],1)", lambda: rotate([1,2,3],1), [2,3,1]),
 "L12": univ(lambda r: (rand_list(r, maxlen=8) or [0], r.randint(0, 30)), lambda xs, k: (lambda g: (g == rotate(xs, k % len(xs)), g))(rotate(xs, k)), "L12"),
 "L13": univ(lambda r: (rand_list(r), r.randint(-30, 30)), lambda xs, k: (lambda g: (len(g) == len(xs), g))(rotate(xs, k)), "L13"),
 "L14": point("interleave([1,2,3],[9])", lambda: interleave([1,2,3],[9]), [1,9,2,3]),
 "L15": univ(lambda r: (rand_list(r), rand_list(r)), lambda a, b: (lambda g: (len(g) == 2*min(len(a), len(b)), g))(interleave(a, b)), "L15"),
 "L16": point("frequencies('abca')", lambda: frequencies('abca'), {'a':2,'b':1,'c':1}),
 "L17": univ(lambda r: (rand_list(r),), lambda xs: (lambda g: (sum(g.values()) == len(xs), g))(frequencies(xs)), "L17"),
 "L18": point("pairwise([1,2,3])", lambda: pairwise([1,2,3]), [(1,2),(2,3)]),
 "L19": univ(lambda r: (rand_list(r),), lambda xs: (lambda g: (len(g) == len(xs)-1, g))(pairwise(xs)), "L19"),
}


def l03():
    cases = [([], 0), ([1], 0), ([1, 2, 3], 0)]
    r = random.Random(SEED)
    cases += [(rand_list(r), 0) for _ in range(N)]
    for xs, k in cases:
        try:
            got = chunk(xs, k)
        except ValueError:
            continue
        except Exception as e:
            return False, "chunk(%r, 0) levantou %s: %s (esperado ValueError)" % (xs, type(e).__name__, e)
        return False, "chunk(%r, 0) -> %r (sem ValueError)" % (xs, got)
    return True, None

CLAIMS["L03"] = l03


def main():
    ids = sys.argv[1:] or sorted(CLAIMS)
    for i in ids:
        ok, ce = CLAIMS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))

main()
