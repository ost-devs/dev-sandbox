import os, sys, random, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.mathutil import clamp, mean, round_half, gcd, is_prime, percent

SEED = 12345
rnd = random.Random(SEED)

def m1():
    vals = [0, -1, 1, -5, 5, 0.0, -0.0, 2.5, -2.5, 1e308, -1e308, float('inf'), float('-inf'), float('nan')]
    vals += [rnd.randint(-100, 100) for _ in range(30)] + [rnd.uniform(-100, 100) for _ in range(30)]
    for lo in vals:
        for hi in vals:
            if not (lo <= hi):
                continue
            for x in vals:
                r = clamp(x, lo, hi)
                if not (lo <= r <= hi):
                    return False, f"clamp({x!r},{lo!r},{hi!r})={r!r}"
    return True, ""

def m2():
    try:
        r = mean([])
    except Exception as e:
        return False, f"mean([]) raises {type(e).__name__}"
    return (r == 0), f"mean([])={r!r}"

def m3():
    r = round_half(2.5)
    return r == 3, f"round_half(2.5)={r!r}"

def m4():
    rng = list(range(-40, 41))
    for a in rng:
        for b in rng:
            if gcd(a, b) != gcd(b, a):
                return False, f"a={a},b={b}"
    for _ in range(2000):
        a, b = rnd.randint(-10**9, 10**9), rnd.randint(-10**9, 10**9)
        if gcd(a, b) != gcd(b, a):
            return False, f"a={a},b={b}"
    return True, ""

def m5():
    bad = []
    for n in range(0, 1001):
        ref = n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))
        if is_prime(n) != ref:
            bad.append(n)
    if bad:
        return False, f"is_prime({bad[0]})={is_prime(bad[0])} (wrong for {len(bad)} values, first: {bad[:8]})"
    return True, ""

def m6():
    r = percent(1, 3)
    return r == 33.3, f"percent(1,3)={r!r}"

for name, f in [("M1", m1), ("M2", m2), ("M3", m3), ("M4", m4), ("M5", m5), ("M6", m6)]:
    ok, info = f()
    print(f"{name} {'TRUE' if ok else 'FALSE'} {info}".rstrip())
sys.exit(0)
