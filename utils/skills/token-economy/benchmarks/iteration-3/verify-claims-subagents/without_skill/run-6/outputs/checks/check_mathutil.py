import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.mathutil import clamp, mean, round_half, gcd, is_prime, percent

SEED = 12345
print("seed", SEED)
rng = random.Random(SEED)

def out(i, ok, ce):
    print(f"{i}: {'TRUE' if ok else 'FALSE'} | {ce}")

# M1
fixed = [-5, -1, 0, 1, 5, -2.5, 0.0, 2.5, 1e9, -1e9]
ce = None
for lo in fixed:
    for hi in fixed:
        if lo <= hi:
            for x in fixed:
                if not (lo <= clamp(x, lo, hi) <= hi):
                    ce = ce or (x, lo, hi)
for _ in range(20000):
    lo = rng.uniform(-100, 100); hi = lo + rng.choice([0, rng.uniform(0, 100)])
    x = rng.uniform(-300, 300)
    if not (lo <= clamp(x, lo, hi) <= hi):
        ce = ce or (x, lo, hi)
out("M1", ce is None, f"clamp{ce!r}" if ce else "none found")

# M2
try:
    r = mean([]); ok = (r == 0); ce = f"mean([]) -> {r!r}"
except Exception as e:
    ok = False; ce = f"mean([]) raises {type(e).__name__}: {e}"
out("M2", ok, ce)

# M3
r = round_half(2.5)
out("M3", r == 3, f"round_half(2.5) -> {r!r}")

# M4
ce = None
vals = [0, 1, -1, 2, -2, 6, -6, 12, 18, -18, 97, 0]
pairs = [(a, b) for a in vals for b in vals] + [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(20000)]
for a, b in pairs:
    if gcd(a, b) != gcd(b, a):
        ce = (a, b); break
out("M4", ce is None, f"gcd{ce!r}" if ce else "none found")

# M5
def ref(n):
    if n < 2: return False
    return all(n % d for d in range(2, n))
bad = [n for n in range(0, 1001) if is_prime(n) != ref(n)]
out("M5", not bad, f"is_prime({bad[0]!r}) -> {is_prime(bad[0])!r}, expected {ref(bad[0])!r}; {len(bad)} wrong, first 5: {bad[:5]}" if bad else "none found")

# M6
r = percent(1, 3)
out("M6", r == 33.3, f"percent(1, 3) -> {r!r}")
