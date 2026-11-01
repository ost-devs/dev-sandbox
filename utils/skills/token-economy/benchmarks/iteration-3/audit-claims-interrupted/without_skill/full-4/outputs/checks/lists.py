import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.lists import chunk, dedupe, flatten, top_n, rotate, interleave, frequencies, pairwise

SEED = 12345
N = 3000


def rlist(r, lo=-5, hi=5, maxlen=12):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]


def forall(pred, gen, edge=()):
    """pred(args) -> None if ok else message. Edge cases first, then random."""
    r = random.Random(SEED)
    for a in list(edge) + [gen(r) for _ in range(N)]:
        try:
            m = pred(*a)
        except Exception as e:
            m = "raised %s: %s" % (type(e).__name__, e)
        if m:
            return (False, "inputs %r: %s" % (a, m))
    return (True, None)


def eq(got, exp, label):
    return (True, None) if got == exp else (False, "%s -> %r, expected %r" % (label, got, exp))


def check_L01():
    return eq(chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]], "chunk(range(7),3)")


def check_L02():
    return forall(lambda xs, k: None if flatten(chunk(xs, k)) == xs else "got %r" % flatten(chunk(xs, k)),
                  lambda r: (rlist(r), r.randint(1, 15)), [([], 1), ([1], 5), ([1, 2], 1)])


def check_L03():
    for xs in ([], [1, 2, 3]):
        try:
            r = chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return (False, "chunk(%r, 0) raised %s" % (xs, type(e).__name__))
        return (False, "chunk(%r, 0) returned %r" % (xs, r))
    return (True, None)


def check_L04():
    return eq(dedupe([3, 1, 3, 2, 1]), [3, 1, 2], "dedupe([3,1,3,2,1])")


def check_L05():
    def ref(xs):
        seen, o = set(), []
        for x in xs:
            if x not in seen:
                seen.add(x); o.append(x)
        return o
    return forall(lambda xs: None if dedupe(xs) == ref(xs) else "got %r" % dedupe(xs),
                  lambda r: (rlist(r),), [([],), ([1, 1],)])


def check_L06():
    return forall(lambda xs: None if len(dedupe(xs)) == len(set(xs)) else "len %d vs %d" % (len(dedupe(xs)), len(set(xs))),
                  lambda r: (rlist(r),), [([],)])


def check_L07():
    return eq(flatten([[1, [2]], [3]]), [1, 2, 3], "flatten([[1,[2]],[3]])")


def check_L08():
    return eq(top_n([5, 1, 4], 2), [5, 4], "top_n([5,1,4],2)")


def check_L09():
    return forall(lambda xs, k: None if len(top_n(xs, k)) == min(k, len(xs)) else "len %d" % len(top_n(xs, k)),
                  lambda r: (rlist(r), r.randint(0, 15)), [([], 0), ([1], 0), ([], 3)])


def check_L10():
    return eq(top_n([3, 2, 1], -1), [], "top_n([3,2,1],-1)")


def check_L11():
    return eq(rotate([1, 2, 3], 1), [2, 3, 1], "rotate([1,2,3],1)")


def check_L12():
    return forall(lambda xs, k: None if rotate(xs, k) == rotate(xs, k % len(xs)) else
                  "rotate(xs,k)=%r but rotate(xs,%d)=%r" % (rotate(xs, k), k % len(xs), rotate(xs, k % len(xs))),
                  lambda r: (rlist(r, maxlen=12)[:] or [0], r.randint(0, 30)), [([1, 2, 3], 4)])


def check_L13():
    return forall(lambda xs, k: None if len(rotate(xs, k)) == len(xs) else "len %d" % len(rotate(xs, k)),
                  lambda r: (rlist(r), r.randint(-30, 30)), [([], 0), ([], -3), ([1], 5)])


def check_L14():
    return eq(interleave([1, 2, 3], [9]), [1, 9, 2, 3], "interleave([1,2,3],[9])")


def check_L15():
    return forall(lambda a, b: None if len(interleave(a, b)) == 2 * min(len(a), len(b)) else "len %d" % len(interleave(a, b)),
                  lambda r: (rlist(r), rlist(r)), [([], []), ([1], [])])


def check_L16():
    return eq(frequencies('abca'), {'a': 2, 'b': 1, 'c': 1}, "frequencies('abca')")


def check_L17():
    return forall(lambda xs: None if sum(frequencies(xs).values()) == len(xs) else "sum mismatch",
                  lambda r: (rlist(r),), [([],)])


def check_L18():
    return eq(pairwise([1, 2, 3]), [(1, 2), (2, 3)], "pairwise([1,2,3])")


def check_L19():
    return forall(lambda xs: None if len(pairwise(xs)) == len(xs) - 1 else "len(pairwise)=%d, len(xs)-1=%d" % (len(pairwise(xs)), len(xs) - 1),
                  lambda r: (rlist(r),), [([],), ([1],), ([1, 2],)])


def main():
    ids = sys.argv[1:] or sorted(k[6:] for k in globals() if k.startswith("check_"))
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce,
                          "command": "python3 -I checks/lists.py " + i}, ensure_ascii=False))


if __name__ == "__main__":
    main()
