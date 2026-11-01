import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.numbers import *

SEED = 12345
T = ("verdadeira", "")

def eq(call, expected):
    try:
        r = call()
    except Exception as e:
        return ("falsa", f"raised {e!r}")
    if r == expected and type(r) is not bool or (r == expected and isinstance(expected, bool) and r is expected):
        return T
    return ("falsa", f"got {r!r}, claimed {expected!r}")

def fixed(f, args, expected):
    v, c = eq(lambda: f(*args), expected)
    return (v, f"{f.__name__}{args!r}: {c}" if c else "")

def N01():
    rng = random.Random(SEED)
    cases = [(0, 0, 0), (-5, -3, 3), (5, 0, 0), (10**30, -10**30, 10**30), (-10**30, -1, 1)]
    for _ in range(5000):
        lo = rng.randint(-1000, 1000); hi = lo + rng.randint(0, 1000)
        cases.append((rng.randint(-3000, 3000), lo, hi))
    for x, lo, hi in cases:
        try:
            r = clamp(x, lo, hi)
        except Exception as e:
            return ("falsa", f"clamp{(x,lo,hi)!r} raised {e!r}")
        if not lo <= r <= hi:
            return ("falsa", f"clamp{(x,lo,hi)!r} = {r!r}")
    return T
def N02(): return fixed(clamp, (5, 10, 0), 0)
def N03(): return fixed(mean, ([],), 0)
def N04(): return fixed(mean, ([1, 2],), 1.5)
def N05(): return fixed(median, ([3, 1, 2],), 2)
def N06():
    try:
        r = median([])
    except Exception as e:
        return ("falsa", f"median([]) raised {e!r}, claimed None")
    return T if r is None else ("falsa", f"median([]) = {r!r}")
def N07():
    rng = random.Random(SEED)
    cases = [[0], [-1], [2, 1], [1, 1], [10**30, -10**30, 5]]
    for _ in range(5000):
        cases.append([rng.randint(-100, 100) for _ in range(rng.randint(1, 12))])
    for xs in cases:
        try:
            a, b = median(xs), median(sorted(xs))
        except Exception as e:
            return ("falsa", f"median({xs!r}) raised {e!r}")
        if a != b:
            return ("falsa", f"xs={xs!r}: {a!r} != {b!r}")
    return T
def N08(): return fixed(round_half, (2.5,), 3)
def N09(): return fixed(round_half, (3.5,), 4)
def N10(): return fixed(percent, (1, 3), 33.3)
def N11():
    for x in [0, 1, -1, 2.5, 10**20, 0.0, -3.5]:
        try:
            r = percent(x, 0)
        except Exception as e:
            return ("falsa", f"percent({x!r}, 0) raised {e!r}, claimed 0.0")
        if not (r == 0.0 and isinstance(r, float)):
            return ("falsa", f"percent({x!r}, 0) = {r!r}")
    return T
def N12():
    def ref(n):
        return n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))
    for n in range(0, 1001):
        try:
            r = is_prime(n)
        except Exception as e:
            return ("falsa", f"is_prime({n}) raised {e!r}")
        if r is not ref(n):
            return ("falsa", f"is_prime({n}) = {r!r}, correct {ref(n)!r}")
    return T
def N13(): return fixed(is_prime, (97,), True)
def N14(): return fixed(is_prime, (2,), True)
def N15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            try:
                x, y = gcd(a, b), gcd(b, a)
            except Exception as e:
                return ("falsa", f"gcd({a},{b}) raised {e!r}")
            if x != y:
                return ("falsa", f"gcd({a},{b})={x!r} != gcd({b},{a})={y!r}")
    return T
def N16(): return fixed(gcd, (12, 18), 6)
def N17():
    rng = random.Random(SEED)
    for a in [0, 1, -1, 7, -7, 10**30, -10**30] + [rng.randint(-10**6, 10**6) for _ in range(3000)]:
        try:
            r = gcd(a, 0)
        except Exception as e:
            return ("falsa", f"gcd({a},0) raised {e!r}")
        if r != a:
            return ("falsa", f"gcd({a},0) = {r!r}")
    return T
def N18(): return fixed(digits_sum, (1234,), 10)
def N19():
    rng = random.Random(SEED)
    cases = [0, 1, -1, 9, -9, 10**30, -10**30, -5] + [rng.randint(-10**9, 10**9) for _ in range(3000)]
    for n in cases:
        try:
            r = digits_sum(n)
        except Exception as e:
            return ("falsa", f"digits_sum({n}) raised {e!r}")
        if type(r) is not int or r < 0:
            return ("falsa", f"digits_sum({n}) = {r!r}")
    return T

def main():
    ids = sys.argv[1:] or [f"N{i:02d}" for i in range(1, 20)]
    for i in ids:
        v, c = globals()[i]()
        print(json.dumps({"id": i, "verdict": v, "counterexample": c, "note": ""}, ensure_ascii=False))
main()
