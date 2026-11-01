import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.numbers import clamp, mean, median, round_half, percent, is_prime, gcd, digits_sum

SEED = 20240607


def exc(e):
    return "%s: %s" % (type(e).__name__, e)


def point(call, expected):
    """call: (description, thunk). Returns counterexample or None."""
    desc, thunk = call
    try:
        got = thunk()
    except Exception as e:
        return "%s raised %s" % (desc, exc(e))
    if got != expected or (type(got) is bool) != (type(expected) is bool):
        return "%s -> %r (expected %r)" % (desc, got, expected)
    return None


def p(desc, thunk, expected):
    return lambda: point((desc, thunk), expected)


def rng():
    return random.Random(SEED)


def ints(r, n=3000, lim=10**6):
    edge = [0, 1, -1, 2, -2, 10, -10, 99, 100, 12345, -12345, 10**18, -10**18]
    return edge + [r.randint(-lim, lim) for _ in range(n)]


def n01():
    r = rng()
    cases = [(0, 0, 0), (5, 0, 10), (-5, -3, -3), (7, 7, 7), (-1, -10, 10)]
    cases += [(x, min(a, b), max(a, b)) for x, a, b in
              ((r.randint(-1000, 1000), r.randint(-1000, 1000), r.randint(-1000, 1000)) for _ in range(5000))]
    for x, lo, hi in cases:
        try:
            v = clamp(x, lo, hi)
        except Exception as e:
            return "clamp(%r,%r,%r) raised %s" % (x, lo, hi, exc(e))
        if not (lo <= v <= hi):
            return "clamp(%r,%r,%r) -> %r" % (x, lo, hi, v)


def n07():
    r = rng()
    cases = [[0], [1, 2], [2, 1], [3, 1, 2], [-1, -5, 4, 0], [5, 5, 1]]
    for _ in range(5000):
        cases.append([r.randint(-50, 50) for _ in range(r.randint(1, 12))])
    for xs in cases:
        try:
            a, b = median(xs), median(sorted(xs))
        except Exception as e:
            return "median(%r) raised %s" % (xs, exc(e))
        if a != b:
            return "median(%r)=%r but median(sorted)=%r" % (xs, a, b)


def n12():
    def ref(n):
        return n >= 2 and all(n % i for i in range(2, n))
    bad = []
    for n in range(0, 1001):
        try:
            g = is_prime(n)
        except Exception as e:
            return "is_prime(%d) raised %s" % (n, exc(e))
        if g != ref(n):
            bad.append((n, g))
    if bad:
        return "is_prime(%d) -> %r (expected %r); %d wrong values in 0..1000" % (bad[0][0], bad[0][1], ref(bad[0][0]), len(bad))


def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            try:
                x, y = gcd(a, b), gcd(b, a)
            except Exception as e:
                return "gcd(%d,%d) raised %s" % (a, b, exc(e))
            if x != y:
                return "gcd(%d,%d)=%r but gcd(%d,%d)=%r" % (a, b, x, b, a, y)


def n17():
    for a in ints(rng()):
        try:
            g = gcd(a, 0)
        except Exception as e:
            return "gcd(%r,0) raised %s" % (a, exc(e))
        if g != a:
            return "gcd(%r,0) -> %r" % (a, g)


def n19():
    for n in sorted(ints(rng()), key=lambda v: (abs(v), v)):
        try:
            v = digits_sum(n)
        except Exception as e:
            return "digits_sum(%r) raised %s" % (n, exc(e))
        if not (isinstance(v, int) and not isinstance(v, bool) and v >= 0):
            return "digits_sum(%r) -> %r" % (n, v)


def n11():
    for x in [0, 1, -1, 5, 1.5, 10**9]:
        try:
            v = percent(x, 0)
        except Exception as e:
            return "percent(%r, 0) raised %s" % (x, exc(e))
        if v != 0.0 or not isinstance(v, float):
            return "percent(%r, 0) -> %r" % (x, v)


CHECKS = {
    "N01": n01,
    "N02": p("clamp(5, 10, 0)", lambda: clamp(5, 10, 0), 0),
    "N03": p("mean([])", lambda: mean([]), 0),
    "N04": p("mean([1, 2])", lambda: mean([1, 2]), 1.5),
    "N05": p("median([3, 1, 2])", lambda: median([3, 1, 2]), 2),
    "N06": p("median([])", lambda: median([]), None),
    "N07": n07,
    "N08": p("round_half(2.5)", lambda: round_half(2.5), 3),
    "N09": p("round_half(3.5)", lambda: round_half(3.5), 4),
    "N10": p("percent(1, 3)", lambda: percent(1, 3), 33.3),
    "N11": n11,
    "N12": n12,
    "N13": p("is_prime(97)", lambda: is_prime(97), True),
    "N14": p("is_prime(2)", lambda: is_prime(2), True),
    "N15": n15,
    "N16": p("gcd(12, 18)", lambda: gcd(12, 18), 6),
    "N17": n17,
    "N18": p("digits_sum(1234)", lambda: digits_sum(1234), 10),
    "N19": n19,
}


def main():
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce}, ensure_ascii=False))


main()
