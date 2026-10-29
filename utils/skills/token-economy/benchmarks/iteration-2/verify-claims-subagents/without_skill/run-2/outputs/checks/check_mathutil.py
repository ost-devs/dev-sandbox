"""Deterministic verification of claims M1-M6 about calc/mathutil.py (stdlib only)."""
import math
import os
import random
import sys

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKDIR)

from calc import mathutil  # noqa: E402

SEED = 20261029
N_RANDOM = 20000


def report(cid, failure):
    if failure is None:
        print(f"{cid} | TRUE")
    else:
        print(f"{cid} | FALSE | counterexample: {failure}")


def call(fn, *args):
    """Return (ok, value_or_exception_text)."""
    try:
        return True, fn(*args)
    except Exception as e:  # noqa: BLE001
        return False, f"raises {type(e).__name__}: {e}"


# ---------------- M1: clamp within [lo, hi] for lo <= hi ----------------
def check_m1():
    rng = random.Random(SEED)
    inf = math.inf
    vals = [0, 1, -1, 2, -2, 5, -5, 10, 0.5, -0.5, 1e-300, -1e-300,
            1e308, -1e308, inf, -inf, 0.0, -0.0, True, False]
    cases = []
    for lo in vals:
        for hi in vals:
            if lo <= hi:
                for x in vals + [math.nan]:
                    cases.append((x, lo, hi))
    for _ in range(N_RANDOM):
        a, b = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
        lo, hi = min(a, b), max(a, b)
        cases.append((rng.randint(-2000, 2000), lo, hi))
        a, b = rng.uniform(-1e6, 1e6), rng.uniform(-1e6, 1e6)
        lo, hi = min(a, b), max(a, b)
        cases.append((rng.uniform(-2e6, 2e6), lo, hi))
        lo = rng.randint(-50, 50)
        cases.append((rng.randint(-100, 100), lo, lo))  # equal bounds
    fails = []
    for x, lo, hi in cases:
        ok, r = call(mathutil.clamp, x, lo, hi)
        if not ok:
            fails.append((abs(x) if x == x else 0, f"clamp({x!r}, {lo!r}, {hi!r}) -> {r} vs expected value in [{lo!r}, {hi!r}]"))
        elif not (lo <= r <= hi):
            fails.append((0, f"clamp({x!r}, {lo!r}, {hi!r}) -> {r!r} vs expected value in [{lo!r}, {hi!r}]"))
    return min(fails)[1] if fails else None


# ---------------- M2: mean([]) == 0 ----------------
def check_m2():
    ok, r = call(mathutil.mean, [])
    if not ok:
        return f"mean([]) -> {r} vs expected 0"
    if not (r == 0 and not isinstance(r, bool)):
        return f"mean([]) -> {r!r} vs expected 0"
    return None


# ---------------- M3: round_half(2.5) == 3 ----------------
def check_m3():
    ok, r = call(mathutil.round_half, 2.5)
    if not ok:
        return f"round_half(2.5) -> {r} vs expected 3"
    if r != 3:
        return f"round_half(2.5) -> {r!r} vs expected 3"
    return None


# ---------------- M4: gcd symmetric ----------------
def check_m4():
    rng = random.Random(SEED + 4)
    edge = [0, 1, -1, 2, -2, 3, -3, 6, -6, 12, -18, 17, -17, 97,
            2**31 - 1, -(2**31), 2**63, -(2**63), 10**30, -(10**30), 2**100 * 3]
    pairs = [(a, b) for a in edge for b in edge]
    pairs += [(a, b) for a in range(-60, 61) for b in range(-60, 61)]
    for _ in range(N_RANDOM):
        pairs.append((rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)))
        pairs.append((rng.randint(-10**40, 10**40), rng.randint(-10**40, 10**40)))
        k = rng.randint(1, 10**6)
        pairs.append((k * rng.randint(-1000, 1000), k * rng.randint(-1000, 1000)))
    fails = []
    for a, b in pairs:
        ok1, r1 = call(mathutil.gcd, a, b)
        ok2, r2 = call(mathutil.gcd, b, a)
        if not (ok1 and ok2) or r1 != r2:
            fails.append((abs(a) + abs(b), f"gcd({a}, {b}) -> {r1} vs gcd({b}, {a}) -> {r2} (expected equal)"))
    return min(fails)[1] if fails else None


# ---------------- M5: is_prime correct for 0..1000 ----------------
def ref_is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def check_m5():
    for n in range(0, 1001):
        exp = ref_is_prime(n)
        ok, r = call(mathutil.is_prime, n)
        if not ok:
            return f"is_prime({n}) -> {r} vs expected {exp}"
        if r is not exp and r != exp:
            return f"is_prime({n}) -> {r!r} vs expected {exp}"
    return None


# ---------------- M6: percent(1, 3) == 33.3 ----------------
def check_m6():
    ok, r = call(mathutil.percent, 1, 3)
    if not ok:
        return f"percent(1, 3) -> {r} vs expected 33.3"
    if r != 33.3:
        return f"percent(1, 3) -> {r!r} vs expected 33.3"
    return None


def main():
    for cid, fn in [("M1", check_m1), ("M2", check_m2), ("M3", check_m3),
                    ("M4", check_m4), ("M5", check_m5), ("M6", check_m6)]:
        try:
            report(cid, fn())
        except Exception as e:  # noqa: BLE001
            report(cid, f"checker crashed: {type(e).__name__}: {e}")
    sys.exit(0)


if __name__ == "__main__":
    main()
