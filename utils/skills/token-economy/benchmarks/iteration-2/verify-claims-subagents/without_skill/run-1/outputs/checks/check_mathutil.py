"""Verify claims M1..M6 about calc/mathutil.py by running code.

Usage: python3 checks/check_mathutil.py [ID ...]
Prints one line per claim: ID<TAB>TRUE|FALSE<TAB>evidence/counterexample.
Always exits 0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calc.mathutil as m  # noqa: E402

SEED = 20261029
TRIALS = 10000


def _call(fn, *args):
    """Return ('ok', value) or ('exc', exception type name)."""
    try:
        return "ok", fn(*args)
    except Exception as e:  # report exceptions as outcomes
        return "exc", type(e).__name__


def _show(name, args, outcome):
    kind, val = outcome
    call = "%s(%s)" % (name, ", ".join(repr(a) for a in args))
    return "%s -> %s" % (call, repr(val) if kind == "ok" else "raises " + val)


def check_M1():
    edges = []
    vals = [0, 1, -1, 5, -5, 0.5, -0.5, 2.5, 1e308, -1e308,
            math.inf, -math.inf]
    for lo in vals:
        for hi in vals:
            if lo <= hi:
                for x in vals + [math.nan]:
                    edges.append((x, lo, hi))

    def bad(x, lo, hi):
        out = _call(m.clamp, x, lo, hi)
        if out[0] != "ok" or not (lo <= out[1] <= hi):
            return "%s but expected value in [%r, %r]" % (
                _show("clamp", (x, lo, hi), out), lo, hi)
        return None

    for args in edges:
        r = bad(*args)
        if r:
            return False, r
    rng = random.Random(SEED)
    for i in range(TRIALS):
        if i % 2:
            a, b, x = (rng.randint(-100, 100) for _ in range(3))
        else:
            a, b, x = (rng.uniform(-100, 100) for _ in range(3))
        lo, hi = min(a, b), max(a, b)
        r = bad(x, lo, hi)
        if r:
            return False, r
    return True, "%d edge cases (incl. lo==hi, inf, nan x, floats) + %d random triples, seed %d" % (
        len(edges), TRIALS, SEED)


def check_M2():
    out = _call(m.mean, [])
    if out == ("ok", 0):
        return True, "mean([]) -> 0"
    return False, "%s but expected 0" % _show("mean", ([],), out)


def check_M3():
    out = _call(m.round_half, 2.5)
    if out == ("ok", 3):
        return True, "round_half(2.5) -> 3"
    return False, "%s but expected 3" % _show("round_half", (2.5,), out)


def check_M4():
    vals = [0, 1, -1, 2, -2, 4, -4, 6, -6, 12, -12, 17, -17,
            10 ** 18, -(10 ** 18), 2 ** 61 - 1]
    edges = [(a, b) for a in vals for b in vals]

    def bad(a, b):
        o1, o2 = _call(m.gcd, a, b), _call(m.gcd, b, a)
        if o1 != o2:
            return "%s but %s" % (_show("gcd", (a, b), o1), _show("gcd", (b, a), o2))
        return None

    for a, b in edges:
        r = bad(a, b)
        if r:
            return False, r
    rng = random.Random(SEED)
    for _ in range(TRIALS):
        a, b = rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)
        r = bad(a, b)
        if r:
            return False, r
    return True, "%d edge pairs (zero, negatives, large) + %d random pairs, seed %d" % (
        len(edges), TRIALS, SEED)


def _oracle_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def check_M5():
    for n in range(0, 1001):
        out = _call(m.is_prime, n)
        exp = _oracle_prime(n)
        if out != ("ok", exp):
            return False, "%s but expected %r" % (_show("is_prime", (n,), out), exp)
    return True, "exhaustive n=0..1000 vs trial-division oracle"


def check_M6():
    out = _call(m.percent, 1, 3)
    if out == ("ok", 33.3):
        return True, "percent(1, 3) -> 33.3"
    return False, "%s but expected 33.3" % _show("percent", (1, 3), out)


CHECKS = {"M1": check_M1, "M2": check_M2, "M3": check_M3,
          "M4": check_M4, "M5": check_M5, "M6": check_M6}


def main(argv):
    ids = argv or list(CHECKS)
    for cid in ids:
        fn = CHECKS.get(cid)
        if fn is None:
            print("%s\tFALSE\tunknown claim id" % cid)
            continue
        try:
            ok, msg = fn()
        except Exception as e:
            ok, msg = False, "checker error: %s: %s" % (type(e).__name__, e)
        print("%s\t%s\t%s" % (cid, "TRUE" if ok else "FALSE", msg))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
