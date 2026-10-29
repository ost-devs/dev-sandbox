"""Verify claims T1..T6 about calc/textutil.py. Usage: python3 checks/check_textutil.py [ID ...]"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calc import textutil  # noqa: E402

SEED = 20261029
TRIALS = 10000

ALPHABET = list("abcXYZ09 -_!.\t\n") + ["é", "É", "ß", "İ", "…", "中", "́", "ﬁ", "💡"]


def rand_str(rng, maxlen=12):
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randint(0, maxlen)))


def call(fn, *args):
    try:
        return ("ok", fn(*args))
    except Exception as e:  # noqa: BLE001
        return ("exc", type(e).__name__)


def fmt_call(name, args):
    return "%s(%s)" % (name, ", ".join(repr(a) for a in args))


def fixed(cid, name, args, expected):
    kind, val = call(getattr(textutil, name), *args)
    c = fmt_call(name, args)
    if kind == "exc":
        return cid, False, "%s raises %s (expected %r)" % (c, val, expected)
    if val == expected:
        return cid, True, "%s -> %r" % (c, val)
    return cid, False, "%s -> %r, expected %r" % (c, val, expected)


SLUG_EDGES = ["", "-", "---", "!", "!a", "a!", "!a!", " a ", "-a-", "é", "café", "a--b",
              "İ", "ß", "中文", "💡", "...", "\t\n", "a", "A B", "-_-", "́á"]


def check_T1():
    def bad(s):
        kind, v = call(textutil.slugify, s)
        if kind == "exc":
            return "%s raises %s" % (fmt_call("slugify", [s]), v)
        if v.startswith("-") or v.endswith("-"):
            return "%s -> %r (starts/ends with '-')" % (fmt_call("slugify", [s]), v)
        return None
    for s in SLUG_EDGES:
        r = bad(s)
        if r:
            return "T1", False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        r = bad(rand_str(rng))
        if r:
            return "T1", False, r
    return "T1", True, "%d edge cases + %d random strings, seed %d" % (len(SLUG_EDGES), TRIALS, SEED)


def check_T2():
    return fixed("T2", "slugify", ["Café Noir"], "cafe-noir")


def check_T3():
    strs = ["", "a", "ab", "abc", "hello world", "é", "💡💡", "…"]
    ns = [0, 1, 2, 3, 5, 100]
    edges = [(s, n) for n in ns for s in strs]  # n ascending, then short strings first

    def bad(s, n):
        kind, v = call(textutil.truncate, s, n)
        c = fmt_call("truncate", [s, n])
        if kind == "exc":
            return "%s raises %s" % (c, v)
        if len(v) > n:
            return "%s -> %r (len %d > %d)" % (c, v, len(v), n)
        return None
    for s, n in edges:
        r = bad(s, n)
        if r:
            return "T3", False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        s, n = rand_str(rng, 20), rng.randint(0, 25)
        r = bad(s, n)
        if r:
            return "T3", False, r
    return "T3", True, "%d edge cases + %d random (s, n), seed %d" % (len(edges), TRIALS, SEED)


def check_T4():
    return fixed("T4", "count_words", ["a  b\tc\n"], 3)


def check_T5():
    return fixed("T5", "capitalize_words", ["a  b"], "A  B")


def check_T6():
    return fixed("T6", "is_palindrome", [""], True)


CHECKS = {"T1": check_T1, "T2": check_T2, "T3": check_T3,
          "T4": check_T4, "T5": check_T5, "T6": check_T6}


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
