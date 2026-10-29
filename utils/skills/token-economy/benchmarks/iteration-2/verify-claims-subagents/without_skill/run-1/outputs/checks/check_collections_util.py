"""Verify claims C1..C6 about calc/collections_util.py. Usage: python3 checks/check_collections_util.py [ID ...]"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calc import collections_util as cu  # noqa: E402

SEED = 20261029
TRIALS = 10000


def rand_list(rng, maxlen=10, lo=-5, hi=5):
    return [rng.randint(lo, hi) for _ in range(rng.randint(0, maxlen))]


def call(fn, *args):
    try:
        return ("ok", fn(*args))
    except Exception as e:  # noqa: BLE001
        return ("exc", type(e).__name__)


def fmt_call(name, args):
    return "%s(%s)" % (name, ", ".join(repr(a) for a in args))


def fixed(cid, name, args, expected):
    kind, val = call(getattr(cu, name), *args)
    c = fmt_call(name, args)
    if kind == "exc":
        return cid, False, "%s raises %s (expected %r)" % (c, val, expected)
    if val == expected:
        return cid, True, "%s -> %r" % (c, val)
    return cid, False, "%s -> %r, expected %r" % (c, val, expected)


def search(cid, edges, gen, bad, what):
    """Run bad() over edge cases, then TRIALS random cases from gen(rng)."""
    for args in edges:
        r = bad(*args)
        if r:
            return cid, False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        r = bad(*gen(rng))
        if r:
            return cid, False, r
    return cid, True, "%d edge cases + %d random %s, seed %d" % (len(edges), TRIALS, what, SEED)


# Shared edge lists: empty, singleton, duplicates, unhashable, mixed types, None.
EDGE_LISTS = [[], [1], [1, 1], [1, 2, 3], [3, 1, 2, 1, 3], [[1], [1], [2]], [{}, {"a": 1}],
              [1, "a", None, 2.5], [None, None], [1, True, 1.0], [(1, 2), (1, 2)], list(range(7))]


def check_C1():
    def bad(xs, n):
        c = fmt_call("chunk", [xs, n])
        kind, v = call(cu.chunk, xs, n)
        if kind == "exc":
            return "%s raises %s, expected concatenation == %r" % (c, v, xs)
        cat = [y for part in v for y in part]
        if cat != xs:
            return "%s -> %r (concat %r), expected concat %r" % (c, v, cat, xs)
        return None
    edges = [(xs, n) for xs in EDGE_LISTS
             for n in sorted({1, 2, 3, max(1, len(xs)), len(xs) + 1, 100})]
    return search("C1", edges, lambda r: (rand_list(r), r.randint(1, 12)), bad, "(xs, n>=1)")


def check_C2():
    def expected(xs):
        out = []
        for x in xs:
            if x not in out:  # equality-based, works for unhashables too
                out.append(x)
        return out

    def bad(xs):
        c = fmt_call("dedupe", [xs])
        exp = expected(xs)
        kind, v = call(cu.dedupe, xs)
        if kind == "exc":
            return "%s raises %s, expected %r" % (c, v, exp)
        if v != exp:
            return "%s -> %r, expected %r" % (c, v, exp)
        return None
    edges = [(xs,) for xs in EDGE_LISTS]
    return search("C2", edges, lambda r: (rand_list(r, 12, 0, 4),), bad, "int lists")


def check_C3():
    return fixed("C3", "flatten", [[[1, [2]], [3]]], [1, 2, 3])


def check_C4():
    def bad(xs, n):
        c = fmt_call("top_n", [xs, n])
        exp = min(n, len(xs))
        kind, v = call(cu.top_n, xs, n)
        if kind == "exc":
            return "%s raises %s, expected len %d" % (c, v, exp)
        if len(v) != exp:
            return "%s -> %r (len %d), expected len %d" % (c, v, len(v), exp)
        return None
    int_lists = [xs for xs in EDGE_LISTS if all(type(x) is int for x in xs)]
    other = [xs for xs in EDGE_LISTS if xs not in int_lists]
    edges = [(xs, n) for xs in int_lists for n in sorted({0, 1, len(xs), len(xs) + 1, 100})]
    edges += [(xs, n) for xs in int_lists for n in (-1, -2, -100)]
    edges += [(xs, n) for xs in other for n in (0, 1, len(xs))]
    return search("C4", edges, lambda r: (rand_list(r), r.randint(-12, 12)), bad, "(xs, n)")


def check_C5():
    def bad(a, b):
        c = fmt_call("merge_dicts", [a, b])
        kind, v = call(cu.merge_dicts, a, b)
        if kind == "exc":
            return "%s raises %s" % (c, v)
        for k in sorted(set(a) & set(b)):
            if k not in v or v[k] != a[k]:
                return "%s -> %r, expected [%r] == %r (from a)" % (c, v, k, a[k])
        return None
    edges = [({"k": 1}, {"k": 2}), ({}, {}), ({"k": 1}, {"k": 1}), ({1: "a", 2: "b"}, {2: "c"})]

    def gen(r):
        mk = lambda: {r.randint(0, 5): r.randint(0, 9) for _ in range(r.randint(0, 5))}  # noqa: E731
        return mk(), mk()
    return search("C5", edges, gen, bad, "dict pairs")


def check_C6():
    def bad(xs):
        c = fmt_call("rotate", [xs, len(xs)])
        kind, v = call(cu.rotate, xs, len(xs))
        if kind == "exc":
            return "%s raises %s, expected %r" % (c, v, xs)
        if v != xs:
            return "%s -> %r, expected %r" % (c, v, xs)
        return None
    edges = [(xs,) for xs in EDGE_LISTS]
    return search("C6", edges, lambda r: (rand_list(r, 15),), bad, "int lists")


CHECKS = {"C1": check_C1, "C2": check_C2, "C3": check_C3,
          "C4": check_C4, "C5": check_C5, "C6": check_C6}


def main(argv):
    ids = argv or list(CHECKS)
    for cid in ids:
        fn = CHECKS.get(cid)
        if fn is None:
            print("%s\tFALSE\tunknown claim id" % cid)
            continue
        try:
            cid, ok, ev = fn()
        except Exception as e:  # noqa: BLE001
            ok, ev = False, "checker raised %s: %s" % (type(e).__name__, e)
        print("%s\t%s\t%s" % (cid, "TRUE" if ok else "FALSE", ev))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
