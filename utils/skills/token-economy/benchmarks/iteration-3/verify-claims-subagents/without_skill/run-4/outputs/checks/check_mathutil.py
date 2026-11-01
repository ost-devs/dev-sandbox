import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calc"))
import mathutil as m

SEED = 12345
rnd = random.Random(SEED)
print("seed", SEED)

def m1():
    vals = [0, -1, 1, 0.0, -0.0, 0.5, -1e308, 1e308, float("inf"), float("-inf"), float("nan"), 10**30, True]
    vals += [rnd.randint(-100, 100) for _ in range(300)] + [rnd.uniform(-100, 100) for _ in range(300)]
    for lo in vals:
        for hi in vals:
            if not (lo <= hi):
                continue
            for x in vals:
                r = m.clamp(x, lo, hi)
                if not (lo <= r <= hi):
                    return False, repr((x, lo, hi, r))
    return True, "none"

def m2():
    try:
        r = m.mean([])
        return (r == 0), f"mean([]) -> {r!r}"
    except Exception as e:
        return False, f"mean([]) raises {e!r}"

def m3():
    r = m.round_half(2.5)
    return r == 3, f"round_half(2.5) -> {r!r}"

def m4():
    cases = [(0, 0), (0, 5), (-4, 6), (12, -18), (-7, -7)]
    cases += [(rnd.randint(-10**6, 10**6), rnd.randint(-10**6, 10**6)) for _ in range(20000)]
    for a, b in cases:
        if m.gcd(a, b) != m.gcd(b, a):
            return False, repr((a, b))
    return True, "none"

def ref_prime(n):
    return n >= 2 and all(n % d for d in range(2, n))

def m5():
    bad = [n for n in range(0, 1001) if m.is_prime(n) != ref_prime(n)]
    if bad:
        return False, f"{bad[0]} (is_prime={m.is_prime(bad[0])!r}, expected={ref_prime(bad[0])!r}); {len(bad)} wrong values, first 10: {bad[:10]}"
    return True, "none"

def m6():
    r = m.percent(1, 3)
    return r == 33.3, f"percent(1, 3) -> {r!r}"

for name, f in [("M1", m1), ("M2", m2), ("M3", m3), ("M4", m4), ("M5", m5), ("M6", m6)]:
    ok, ce = f()
    print(name, "VERDADEIRA" if ok else "FALSA", ce)
sys.exit(0)
