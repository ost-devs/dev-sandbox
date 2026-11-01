import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.numbers import *

SEED = 12345


def _eq(expr_fn, expected, label):
    try:
        got = expr_fn()
    except Exception as e:
        return False, "%s levantou %s: %s (esperado %r)" % (label, type(e).__name__, e, expected)
    if got == expected and type(got) is type(expected) or got == expected:
        return True, None
    return False, "%s == %r (esperado %r)" % (label, got, expected)


def check_N01():
    r = random.Random(SEED)
    cases = [(0, 0, 0), (-5, -5, 5), (5, -5, 5), (-6, -5, 5), (6, -5, 5), (3, 3, 3)]
    for _ in range(3000):
        lo = r.randint(-100, 100); hi = lo + r.randint(0, 100)
        cases.append((r.randint(-300, 300), lo, hi))
    for x, lo, hi in cases:
        v = clamp(x, lo, hi)
        if not (lo <= v <= hi):
            return False, "clamp(%r, %r, %r) == %r" % (x, lo, hi, v)
    return True, None


def check_N02(): return _eq(lambda: clamp(5, 10, 0), 0, "clamp(5, 10, 0)")
def check_N03(): return _eq(lambda: mean([]), 0, "mean([])")
def check_N04(): return _eq(lambda: mean([1, 2]), 1.5, "mean([1, 2])")
def check_N05(): return _eq(lambda: median([3, 1, 2]), 2, "median([3, 1, 2])")
def check_N06(): return _eq(lambda: median([]), None, "median([])")


def check_N07():
    r = random.Random(SEED)
    cases = [[0], [1, 2], [2, 1], [-1, -3, 5, 0], [7, 7, 7]]
    for _ in range(3000):
        cases.append([r.randint(-50, 50) for _ in range(r.randint(1, 12))])
    for xs in cases:
        if median(xs) != median(sorted(xs)):
            return False, "median(%r) != median(sorted)" % (xs,)
    return True, None


def check_N08(): return _eq(lambda: round_half(2.5), 3, "round_half(2.5)")
def check_N09(): return _eq(lambda: round_half(3.5), 4, "round_half(3.5)")
def check_N10(): return _eq(lambda: percent(1, 3), 33.3, "percent(1, 3)")


def check_N11():
    for x in [0, 1, -1, 2.5, 100, 10**9]:
        try:
            v = percent(x, 0)
        except Exception as e:
            return False, "percent(%r, 0) levantou %s: %s" % (x, type(e).__name__, e)
        if v != 0.0 or not isinstance(v, float):
            return False, "percent(%r, 0) == %r" % (x, v)
    return True, None


def _ref_prime(n):
    if n < 2:
        return False
    return all(n % i for i in range(2, n))


def check_N12():
    bad = [n for n in range(0, 1001) if is_prime(n) != _ref_prime(n)]
    if bad:
        n = bad[0]
        return False, "is_prime(%d) == %r (correto: %r); todos errados: %r" % (n, is_prime(n), _ref_prime(n), bad[:10])
    return True, None


def check_N13(): return _eq(lambda: is_prime(97), True, "is_prime(97)")
def check_N14(): return _eq(lambda: is_prime(2), True, "is_prime(2)")


def check_N15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            if gcd(a, b) != gcd(b, a):
                return False, "gcd(%d, %d) == %r mas gcd(%d, %d) == %r" % (a, b, gcd(a, b), b, a, gcd(b, a))
    return True, None


def check_N16(): return _eq(lambda: gcd(12, 18), 6, "gcd(12, 18)")


def check_N17():
    r = random.Random(SEED)
    for a in [0, 1, -1, 7, -7, 10**20, -10**20] + [r.randint(-10**6, 10**6) for _ in range(3000)]:
        if gcd(a, 0) != a:
            return False, "gcd(%r, 0) == %r" % (a, gcd(a, 0))
    return True, None


def check_N18(): return _eq(lambda: digits_sum(1234), 10, "digits_sum(1234)")


def check_N19():
    r = random.Random(SEED)
    for n in [0, 1, -1, 9, -9, 10, -10, 1234, -1234, 10**30, -10**30] + [r.randint(-10**9, 10**9) for _ in range(3000)]:
        try:
            v = digits_sum(n)
        except Exception as e:
            return False, "digits_sum(%r) levantou %s: %s" % (n, type(e).__name__, e)
        if not isinstance(v, int) or v < 0:
            return False, "digits_sum(%r) == %r" % (n, v)
    return True, None


def main():
    ids = sys.argv[1:] or ["N%02d" % i for i in range(1, 20)]
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": None if ok else ce,
                          "command": "python3 -I checks/numbers.py " + i}, ensure_ascii=False))


if __name__ == "__main__":
    main()
