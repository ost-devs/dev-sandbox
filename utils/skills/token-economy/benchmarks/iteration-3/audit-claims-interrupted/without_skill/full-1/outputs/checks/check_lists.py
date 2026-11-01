import itertools
from _common import Results, rng
from kit.lists import *

R = Results("lists")
r = rng()

def small_lists(maxlen=4, vals=(0, 1, 2)):
    for n in range(maxlen + 1):
        for t in itertools.product(vals, repeat=n):
            yield list(t)

def rand_lists(n=300):
    return [[r.randint(-5, 5) for _ in range(r.randint(0, 8))] for _ in range(n)]

def all_lists():
    return list(small_lists()) + rand_lists()

def forall(pred, cases):
    for c in cases:
        if not pred(*c):
            return False, c
    return True, None

def eq(cid, fn, expected):
    R.check(cid, lambda: ((v := fn()) == expected, v))

def raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False

eq("L01", lambda: chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]])
R.check("L02", lambda: forall(lambda xs, k: flatten(chunk(xs, k)) == xs,
        [(xs, k) for xs in all_lists() for k in range(1, 12)]))
R.check("L03", lambda: forall(lambda xs: raises(lambda: chunk(xs, 0), ValueError),
        [(xs,) for xs in ([], [1], [1, 2, 3])]))
eq("L04", lambda: dedupe([3, 1, 3, 2, 1]), [3, 1, 2])
def first_occ(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out
R.check("L05", lambda: forall(lambda xs: dedupe(xs) == first_occ(xs), [(x,) for x in all_lists()]))
R.check("L06", lambda: forall(lambda xs: len(dedupe(xs)) == len(set(xs)), [(x,) for x in all_lists()]))
eq("L07", lambda: flatten([[1, [2]], [3]]), [1, 2, 3])
eq("L08", lambda: top_n([5, 1, 4], 2), [5, 4])
R.check("L09", lambda: forall(lambda xs, k: len(top_n(xs, k)) == min(k, len(xs)),
        [(xs, k) for xs in all_lists() for k in range(0, 12)]))
eq("L10", lambda: top_n([3, 2, 1], -1), [])
eq("L11", lambda: rotate([1, 2, 3], 1), [2, 3, 1])
R.check("L12", lambda: forall(lambda xs, k: rotate(xs, k) == rotate(xs, k % len(xs)),
        [(xs, k) for xs in all_lists() if xs for k in range(0, 12)]))
R.check("L13", lambda: forall(lambda xs, k: len(rotate(xs, k)) == len(xs),
        [(xs, k) for xs in all_lists() for k in range(-12, 12)]))
eq("L14", lambda: interleave([1, 2, 3], [9]), [1, 9, 2, 3])
R.check("L15", lambda: forall(lambda a, b: len(interleave(a, b)) == 2 * min(len(a), len(b)),
        [(a, b) for a in all_lists()[:60] for b in all_lists()[:60]]))
eq("L16", lambda: frequencies('abca'), {'a': 2, 'b': 1, 'c': 1})
R.check("L17", lambda: forall(lambda xs: sum(frequencies(xs).values()) == len(xs), [(x,) for x in all_lists()]))
eq("L18", lambda: pairwise([1, 2, 3]), [(1, 2), (2, 3)])
R.check("L19", lambda: forall(lambda xs: len(pairwise(xs)) == len(xs) - 1, [(x,) for x in all_lists()]))
R.finish()
