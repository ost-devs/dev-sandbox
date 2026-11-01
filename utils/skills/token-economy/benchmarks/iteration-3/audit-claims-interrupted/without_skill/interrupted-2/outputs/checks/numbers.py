import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import numbers as K

CMD = "python3 -I checks/numbers.py"
rng = random.Random(12345)


def run(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return "EXC %s: %s" % (type(e).__name__, e)


def exact(call_repr, f, args, expected):
    r = run(f, *args)
    if (isinstance(r, str) and r.startswith("EXC")) or r != expected or (type(r) is bool) != (type(expected) is bool):
        return "%s -> %r (esperado %r)" % (call_repr, r, expected)
    return None


def first_fail(cases, pred):
    for c in cases:
        try:
            ok, res = pred(*c)
        except Exception as e:
            ok, res = False, "EXC %s: %s" % (type(e).__name__, e)
        if not ok:
            return "entrada %r -> %r" % (c, res)
    return None


def ref_prime(n):
    return n >= 2 and all(n % i for i in range(2, n))

R = {}
ints = [-5, -1, 0, 1, 2, 7, 10, 100]
cases = [(x, lo, hi) for x in ints for lo in ints for hi in ints if lo <= hi]
cases += [(rng.randint(-1000, 1000),) + tuple(sorted((rng.randint(-1000, 1000), rng.randint(-1000, 1000)))) for _ in range(2000)]
R["N01"] = first_fail(cases, lambda x, lo, hi: (lo <= K.clamp(x, lo, hi) <= hi, K.clamp(x, lo, hi)))
R["N02"] = exact("clamp(5, 10, 0)", K.clamp, (5, 10, 0), 0)
R["N03"] = exact("mean([])", K.mean, ([],), 0)
R["N04"] = exact("mean([1, 2])", K.mean, ([1, 2],), 1.5)
R["N05"] = exact("median([3, 1, 2])", K.median, ([3, 1, 2],), 2)
r = run(K.median, [])
R["N06"] = None if r is None else "median([]) -> %r (esperado None)" % (r,)
lists = [[0], [-1], [1, 2], [2, 1], [3, 1, 2], [5, 5, 1], [-3, 4, -3, 0], [1, 2, 3, 4], [4, 3, 2, 1]]
lists += [[rng.randint(-50, 50) for _ in range(rng.randint(1, 12))] for _ in range(2000)]
R["N07"] = first_fail([(l,) for l in lists], lambda xs: (K.median(xs) == K.median(sorted(xs)), K.median(xs)))
R["N08"] = exact("round_half(2.5)", K.round_half, (2.5,), 3)
R["N09"] = exact("round_half(3.5)", K.round_half, (3.5,), 4)
R["N10"] = exact("percent(1, 3)", K.percent, (1, 3), 33.3)
R["N11"] = first_fail([(x,) for x in [0, 1, -1, 5, 2.5, 0.0, 100, -3.7]],
                      lambda x: (K.percent(x, 0) == 0.0 and isinstance(K.percent(x, 0), float), K.percent(x, 0)))
bad = [(n,) for n in range(0, 1001) if run(K.is_prime, n) is not ref_prime(n)]
R["N12"] = ("is_prime(%d) -> %r (correto: %r)" % (bad[0][0], run(K.is_prime, bad[0][0]), ref_prime(bad[0][0]))) if bad else None
R["N13"] = exact("is_prime(97)", K.is_prime, (97,), True)
R["N14"] = exact("is_prime(2)", K.is_prime, (2,), True)
R["N15"] = first_fail([(a, b) for a in range(-50, 51) for b in range(-50, 51)],
                      lambda a, b: (K.gcd(a, b) == K.gcd(b, a), (K.gcd(a, b), K.gcd(b, a))))
R["N16"] = exact("gcd(12, 18)", K.gcd, (12, 18), 6)
R["N17"] = first_fail([(a,) for a in list(range(-100, 101)) + [rng.randint(-10**9, 10**9) for _ in range(500)]],
                      lambda a: (K.gcd(a, 0) == a, K.gcd(a, 0)))
R["N18"] = exact("digits_sum(1234)", K.digits_sum, (1234,), 10)
R["N19"] = first_fail([(n,) for n in [0, 1, 9, 10, 1234, 10**20, -1, -5, -1234] + [rng.randint(-10**6, 10**6) for _ in range(500)]],
                      lambda n: (isinstance(K.digits_sum(n), int) and not isinstance(K.digits_sum(n), bool) and K.digits_sum(n) >= 0, K.digits_sum(n)))

for i in range(1, 20):
    k = "N%02d" % i
    c = R[k]
    print("%s\t%s\t%s\t%s" % (k, "verdadeira" if c is None else "falsa", c or "", CMD))
