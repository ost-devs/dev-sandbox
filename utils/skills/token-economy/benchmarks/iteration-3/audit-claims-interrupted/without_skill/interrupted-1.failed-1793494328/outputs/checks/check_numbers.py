import sys, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit import numbers as N
SEED = 12345

def attempt(f, *a):
    try:
        return ("ok", f(*a))
    except Exception as e:
        return ("exc", repr(e))

def eq(id_, f, args, expected):
    r = attempt(f, *args)
    if r[0] == "ok" and r[1] == expected and type(r[1]) is not bool or (r[0]=="ok" and r[1] is expected):
        return None
    return "%s%r -> %r, expected %r" % (f.__name__, args, r[1], expected)

def single(f, args, expected):
    r = attempt(f, *args)
    if r[0] == "ok" and r[1] == expected:
        return None
    return repr((f.__name__, args, "actual", r[1], "expected", expected))

def c01():
    rng = random.Random(SEED)
    cases = [(x, lo, hi) for x in range(-12, 13) for lo in range(-6, 7) for hi in range(lo, 7)]
    cases += [(rng.randint(-10**9, 10**9), *sorted((rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)))) for _ in range(3000)]
    for x, lo, hi in cases:
        r = attempt(N.clamp, x, lo, hi)
        if r[0] != "ok" or not (lo <= r[1] <= hi):
            return repr(((x, lo, hi), "actual", r[1], "expected within", (lo, hi)))
def c02(): return single(N.clamp, (5, 10, 0), 0)
def c03(): return single(N.mean, ([],), 0)
def c04(): return single(N.mean, ([1, 2],), 1.5)
def c05(): return single(N.median, ([3, 1, 2],), 2)
def c06():
    r = attempt(N.median, [])
    return None if r == ("ok", None) else repr(("median([])", "actual", r[1], "expected", None))
def c07():
    rng = random.Random(SEED)
    cases = [[0], [1, 2], [2, 1], [-1, -2, -3, 5]]
    cases += [[rng.randint(-50, 50) for _ in range(rng.randint(1, 12))] for _ in range(3000)]
    for xs in cases:
        a, b = attempt(N.median, xs), attempt(N.median, sorted(xs))
        if a != b:
            return repr((xs, "actual", a, "expected", b))
def c08(): return single(N.round_half, (2.5,), 3)
def c09(): return single(N.round_half, (3.5,), 4)
def c10(): return single(N.percent, (1, 3), 33.3)
def c11():
    for x in [0, 1, -1, 5, 2.5, 0.0, 10**6]:
        r = attempt(N.percent, x, 0)
        if r != ("ok", 0.0):
            return repr(((x, 0), "actual", r[1], "expected", 0.0))
def ref_prime(n):
    return n >= 2 and all(n % i for i in range(2, n))
def c12():
    for n in range(0, 1001):
        r = attempt(N.is_prime, n)
        if r != ("ok", ref_prime(n)):
            return repr((n, "actual", r[1], "expected", ref_prime(n)))
def c13(): return single(N.is_prime, (97,), True)
def c14(): return single(N.is_prime, (2,), True)
def c15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            x, y = attempt(N.gcd, a, b), attempt(N.gcd, b, a)
            if x != y:
                return repr(((a, b), "gcd(a,b)", x[1], "gcd(b,a)", y[1]))
def c16(): return single(N.gcd, (12, 18), 6)
def c17():
    for a in list(range(-200, 201)) + [10**18, -10**18]:
        r = attempt(N.gcd, a, 0)
        if r != ("ok", a):
            return repr(((a, 0), "actual", r[1], "expected", a))
def c18(): return single(N.digits_sum, (1234,), 10)
def c19():
    for n in list(range(-200, 201)) + [10**18, -10**18]:
        r = attempt(N.digits_sum, n)
        if r[0] != "ok" or not isinstance(r[1], int) or isinstance(r[1], bool) or r[1] < 0:
            return repr((n, "actual", r[1], "expected non-negative int"))

CLAIMS = {"N%02d" % i: globals()["c%02d" % i] for i in range(1, 20)}
ids = sys.argv[1:] or sorted(CLAIMS)
for i in ids:
    cx = CLAIMS[i]()
    print(i + ("\tTRUE" if cx is None else "\tFALSE\t" + cx))
