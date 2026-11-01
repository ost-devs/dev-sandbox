import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import numbers as K

SEED = 12345


def _eq(name, call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f"{name} -> exceção {type(e).__name__}: {e} vs. esperado {expected!r}"
    if got == expected and type(got) is not bool or (isinstance(expected, bool) and got is expected):
        return True, None
    return False, f"{name} -> {got!r} vs. esperado {expected!r}"


def check_N01():
    rng = random.Random(SEED)
    cases = [(x, lo, hi) for lo in range(-4, 5) for hi in range(lo, 5) for x in range(-8, 9)]
    cases += [(rng.randint(-10**9, 10**9), *sorted((rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)))) for _ in range(2000)]
    for x, lo, hi in cases:
        try:
            r = K.clamp(x, lo, hi)
        except Exception as e:
            return False, f"clamp({x},{lo},{hi}) -> exceção {e!r}"
        if not (lo <= r <= hi):
            return False, f"clamp({x},{lo},{hi}) -> {r} vs. esperado dentro de [{lo},{hi}]"
    return True, None


def check_N02(): return _eq("clamp(5, 10, 0)", lambda: K.clamp(5, 10, 0), 0)
def check_N03(): return _eq("mean([])", lambda: K.mean([]), 0)
def check_N04(): return _eq("mean([1, 2])", lambda: K.mean([1, 2]), 1.5)
def check_N05(): return _eq("median([3, 1, 2])", lambda: K.median([3, 1, 2]), 2)


def check_N06():
    try:
        r = K.median([])
    except Exception as e:
        return False, f"median([]) -> exceção {type(e).__name__}: {e} vs. esperado None"
    return (True, None) if r is None else (False, f"median([]) -> {r!r} vs. esperado None")


def check_N07():
    rng = random.Random(SEED)
    cases = [[0], [-1], [1, 2], [2, 1], [3, 1, 2], [5, 5, 1], [-3, 7, 0, 7]]
    cases += [[rng.randint(-20, 20) for _ in range(rng.randint(1, 9))] for _ in range(3000)]
    for xs in cases:
        try:
            a, b = K.median(xs), K.median(sorted(xs))
        except Exception as e:
            return False, f"median({xs}) -> exceção {e!r}"
        if a != b:
            return False, f"xs={xs}: median(xs)={a!r} vs. median(sorted(xs))={b!r}"
    return True, None


def check_N08(): return _eq("round_half(2.5)", lambda: K.round_half(2.5), 3)
def check_N09(): return _eq("round_half(3.5)", lambda: K.round_half(3.5), 4)
def check_N10(): return _eq("percent(1, 3)", lambda: K.percent(1, 3), 33.3)


def check_N11():
    for x in [0, 1, -1, 5, 2.5, -0.5, 10**12, 0.0]:
        try:
            r = K.percent(x, 0)
        except Exception as e:
            return False, f"percent({x!r}, 0) -> exceção {type(e).__name__}: {e} vs. esperado 0.0"
        if r != 0.0 or not isinstance(r, float):
            return False, f"percent({x!r}, 0) -> {r!r} vs. esperado 0.0"
    return True, None


def _ref_prime(n):
    return n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def check_N12():
    for n in range(0, 1001):
        try:
            r = K.is_prime(n)
        except Exception as e:
            return False, f"is_prime({n}) -> exceção {e!r}"
        if r is not _ref_prime(n) and r != _ref_prime(n):
            return False, f"is_prime({n}) -> {r!r} vs. esperado {_ref_prime(n)!r}"
    return True, None


def check_N13(): return _eq("is_prime(97)", lambda: K.is_prime(97), True)
def check_N14(): return _eq("is_prime(2)", lambda: K.is_prime(2), True)


def check_N15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            try:
                x, y = K.gcd(a, b), K.gcd(b, a)
            except Exception as e:
                return False, f"gcd({a},{b}) -> exceção {e!r}"
            if x != y:
                return False, f"gcd({a},{b})={x} vs. gcd({b},{a})={y}"
    return True, None


def check_N16(): return _eq("gcd(12, 18)", lambda: K.gcd(12, 18), 6)


def check_N17():
    for a in list(range(-100, 101)) + [10**18, -10**18]:
        try:
            r = K.gcd(a, 0)
        except Exception as e:
            return False, f"gcd({a}, 0) -> exceção {e!r}"
        if r != a:
            return False, f"gcd({a}, 0) -> {r!r} vs. esperado {a}"
    return True, None


def check_N18(): return _eq("digits_sum(1234)", lambda: K.digits_sum(1234), 10)


def check_N19():
    for n in list(range(-20, 21)) + [10**20, -10**20, -1234]:
        try:
            r = K.digits_sum(n)
        except Exception as e:
            return False, f"digits_sum({n}) -> exceção {type(e).__name__}: {e} vs. esperado int >= 0"
        if not isinstance(r, int) or isinstance(r, bool) or r < 0:
            return False, f"digits_sum({n}) -> {r!r} vs. esperado int >= 0"
    return True, None


IDS = [f"N{i:02d}" for i in range(1, 20)]


def main(argv):
    ids = argv or IDS
    for i in ids:
        try:
            ok, msg = globals()[f"check_{i}"]()
        except Exception as e:
            ok, msg = False, f"exceção no check: {e!r}"
        print(f"{i}\t{'verdadeira' if ok else 'falsa'}\t{(msg or '').replace(chr(10), ' ')}")


if __name__ == "__main__":
    main(sys.argv[1:])
