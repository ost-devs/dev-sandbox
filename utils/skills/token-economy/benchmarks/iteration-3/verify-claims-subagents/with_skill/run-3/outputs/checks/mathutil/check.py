import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from common import rng, report, ROOT
from calc.mathutil import clamp, mean, round_half, gcd, is_prime, percent

# M1
r = rng('M1'); bad = None
cases = [(x, lo, hi) for lo in range(-6, 7) for hi in range(lo, 7) for x in range(-8, 9)]
cases += [(r.uniform(-1e6, 1e6), 0, 0) for _ in range(50)]
for _ in range(5000):
    lo = r.randint(-1000, 1000); hi = lo + r.randint(0, 1000); cases.append((r.randint(-3000, 3000), lo, hi))
cases += [(float('inf'), -1, 1), (float('-inf'), -1, 1)]
for x, lo, hi in cases:
    if not (lo <= clamp(x, lo, hi) <= hi):
        c = (x, lo, hi)
        if bad is None or sum(map(abs, c)) < sum(map(abs, bad)): bad = c
report('M1', bad is None, '' if bad is None else f"clamp{bad}={clamp(*bad)}")

# M2
try:
    v = mean([]); ok = (v == 0); ce = f"mean([])={v!r}"
except Exception as e:
    ok = False; ce = f"mean([]) raises {type(e).__name__}: {e}"
report('M2', ok, '' if ok else ce)

# M3
v = round_half(2.5)
report('M3', v == 3, '' if v == 3 else f"round_half(2.5)={v!r}")

# M4
r = rng('M4'); bad = None
pairs = [(a, b) for a in range(-60, 61) for b in range(-60, 61)]
pairs += [(r.randint(-10**9, 10**9), r.randint(-10**9, 10**9)) for _ in range(5000)]
pairs += [(0, 0), (0, -5), (2**64, 3)]
for a, b in pairs:
    if gcd(a, b) != gcd(b, a):
        if bad is None or abs(a) + abs(b) < abs(bad[0]) + abs(bad[1]): bad = (a, b)
report('M4', bad is None, '' if bad is None else f"gcd{bad}={gcd(*bad)} vs gcd{bad[::-1]}={gcd(*bad[::-1])}")

# M5
def ref(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))
bads = [n for n in range(0, 1001) if is_prime(n) != ref(n)]
report('M5', not bads, '' if not bads else f"smallest is_prime({bads[0]})={is_prime(bads[0])}, expected {ref(bads[0])} ({len(bads)} wrong in 0..1000)")

# M6
v = percent(1, 3)
report('M6', v == 33.3, '' if v == 33.3 else f"percent(1,3)={v!r}")
