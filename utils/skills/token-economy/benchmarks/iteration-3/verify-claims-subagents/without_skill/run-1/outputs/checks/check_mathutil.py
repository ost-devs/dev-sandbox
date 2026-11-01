import os, sys, random, itertools
sys.path.insert(0, os.getcwd())
from calc import mathutil as m

SEED = 12345
rng = random.Random(SEED)
out = {}

def verdict(i, ce):
    out[i] = "VERDADEIRA" if ce is None else "FALSA contraexemplo=%r" % (ce,)

# M1
edge = [0, -1, 1, -5, 5, 2.5, -2.5, 0.0, -0.0, 1e308, -1e308, float("inf"), float("-inf"), float("nan")]
edge += [rng.randint(-100, 100) for _ in range(30)] + [rng.uniform(-100, 100) for _ in range(30)]
ce = None
for lo, hi, x in itertools.product(edge, edge, edge):
    if lo != lo or hi != hi or not lo <= hi:
        continue
    try:
        r = m.clamp(x, lo, hi)
        ok = lo <= r <= hi
    except Exception as e:
        ok, r = False, repr(e)
    if not ok:
        ce = (x, lo, hi); break
verdict("M1", ce)

# M2
try:
    r = m.mean([])
    ce = None if (r == 0 and not isinstance(r, bool)) else ("mean([])", r)
except Exception as e:
    ce = ("mean([])", type(e).__name__ + ": " + str(e))
verdict("M2", ce)

# M3
r = m.round_half(2.5)
verdict("M3", None if r == 3 else ("round_half(2.5)", r))

# M4
vals = [0, 1, -1, 2, -2, 6, -6, 12, -18, 7, 100, -100] + [rng.randint(-1000, 1000) for _ in range(50)]
ce = None
for a, b in itertools.product(vals, vals):
    try:
        if m.gcd(a, b) != m.gcd(b, a):
            ce = (a, b); break
    except Exception as e:
        ce = (a, b, repr(e)); break
verdict("M4", ce)

# M5 (oracle: trial division by all d with d*d <= n, independent of module)
def oracle(n):
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True
bad = [n for n in range(0, 1001) if m.is_prime(n) != oracle(n)]
verdict("M5", None if not bad else (bad[0], "is_prime=%r esperado=%r (total divergencias=%d)" % (m.is_prime(bad[0]), oracle(bad[0]), len(bad))))

# M6
r = m.percent(1, 3)
verdict("M6", None if r == 33.3 else ("percent(1, 3)", r))

for i in ["M1", "M2", "M3", "M4", "M5", "M6"]:
    print(i, out[i])
