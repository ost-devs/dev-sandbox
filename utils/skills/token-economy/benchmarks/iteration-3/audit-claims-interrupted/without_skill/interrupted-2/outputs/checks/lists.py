import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.lists import chunk, dedupe, flatten, top_n, rotate, interleave, frequencies, pairwise

CMD = "python3 -I checks/lists.py"
R = random.Random(12345)
def rl(maxn=8):
    return [R.randint(-5, 5) for _ in range(R.randint(0, maxn))]
LISTS = [[], [0], [1, 1], [3, 1, 3, 2, 1], [-1, -2, -3], list(range(7)), [5, 1, 4], [1, 2, 3]] + [rl() for _ in range(300)]
KS = [-5, -2, -1, 0, 1, 2, 3, 7, 8, 20, 100]

def first_fail(cases, pred):
    """cases: iterable of (label, input args); pred(*args) -> (ok, result)."""
    for args in cases:
        try:
            ok, res = pred(*args)
        except Exception as e:
            return "input=%r raised %r" % (args, e)
        if not ok:
            return "input=%r result=%r" % (args, res)
    return ""

def eq(expected, f, *a):
    r = f(*a)
    return r == expected, "%s%r -> %r" % (f.__name__, a, r)

out = {}
out["L01"] = first_fail([()], lambda: eq([[0,1,2],[3,4,5],[6]], chunk, list(range(7)), 3))
out["L02"] = first_fail(((xs, k) for xs in LISTS for k in KS if k >= 1),
    lambda xs, k: (lambda r: (r == xs, r))(flatten(chunk(xs, k))))
def l03(xs):
    try:
        r = chunk(xs, 0)
    except ValueError:
        return True, None
    return False, r
out["L03"] = first_fail([([],), ([1],), ([1, 2, 3],)], l03)
out["L04"] = first_fail([()], lambda: eq([3,1,2], dedupe, [3,1,2][0:0] + [3,1,3,2,1]))
def first_occ(xs):
    seen = []
    for x in xs:
        if x not in seen: seen.append(x)
    return seen
out["L05"] = first_fail(((xs,) for xs in LISTS), lambda xs: (lambda r: (r == first_occ(xs), r))(dedupe(xs)))
out["L06"] = first_fail(((xs,) for xs in LISTS), lambda xs: (lambda r: (len(r) == len(set(xs)), r))(dedupe(xs)))
out["L07"] = first_fail([()], lambda: eq([1,2,3], flatten, [[1,[2]],[3]]))
out["L08"] = first_fail([()], lambda: eq([5,4], top_n, [5,1,4], 2))
out["L09"] = first_fail(((xs, k) for xs in LISTS for k in KS if k >= 0),
    lambda xs, k: (lambda r: (len(r) == min(k, len(xs)), r))(top_n(xs, k)))
out["L10"] = first_fail([()], lambda: eq([], top_n, [3,2,1], -1))
out["L11"] = first_fail([()], lambda: eq([2,3,1], rotate, [1,2,3], 1))
out["L12"] = first_fail(((xs, k) for xs in LISTS if xs for k in KS + list(range(0, 12)) if k >= 0),
    lambda xs, k: (lambda a, b: (a == b, a))(rotate(xs, k), rotate(xs, k % len(xs))))
out["L13"] = first_fail(((xs, k) for xs in LISTS for k in KS),
    lambda xs, k: (lambda r: (len(r) == len(xs), r))(rotate(xs, k)))
out["L14"] = first_fail([()], lambda: eq([1,9,2,3], interleave, [1,2,3], [9]))
out["L15"] = first_fail(((a, b) for a in LISTS[:60] for b in LISTS[:60]),
    lambda a, b: (lambda r: (len(r) == 2 * min(len(a), len(b)), r))(interleave(a, b)))
out["L16"] = first_fail([()], lambda: eq({'a':2,'b':1,'c':1}, frequencies, 'abca'))
out["L17"] = first_fail(((xs,) for xs in LISTS), lambda xs: (lambda r: (sum(r.values()) == len(xs), r))(frequencies(xs)))
out["L18"] = first_fail([()], lambda: eq([(1,2),(2,3)], pairwise, [1,2,3]))
out["L19"] = first_fail(((xs,) for xs in LISTS), lambda xs: (lambda r: (len(r) == len(xs) - 1, r))(pairwise(xs)))

for i in range(1, 20):
    k = "L%02d" % i
    ce = out[k].replace("\t", " ").replace("\n", " ")
    print("%s\t%s\t%s\t%s" % (k, "falsa" if ce else "verdadeira", ce, CMD))
