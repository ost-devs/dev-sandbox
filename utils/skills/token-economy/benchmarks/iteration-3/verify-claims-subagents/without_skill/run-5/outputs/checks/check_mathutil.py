import sys, os, random, math, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc import mathutil as m
SEED = 12345
rng = random.Random(SEED)

def out(i, ok, d): print(i, 'TRUE' if ok else 'FALSE', d)

# M1
vals = [-10, -1, 0, 1, 10, 0.5, -0.5, 1e308, -1e308, float('inf'), float('-inf')]
cx = None
for lo, hi in itertools.product(vals, vals):
    if lo <= hi:
        for x in vals:
            try: r = m.clamp(x, lo, hi)
            except Exception as e: cx = (x, lo, hi, repr(e)); break
            if not (lo <= r <= hi): cx = (x, lo, hi, r); break
        if cx: break
if not cx:
    for _ in range(20000):
        lo = rng.randint(-100, 100); hi = lo + rng.randint(0, 100)
        x = rng.choice([rng.randint(-300, 300), rng.uniform(-300, 300)])
        if not (lo <= m.clamp(x, lo, hi) <= hi): cx = (x, lo, hi); break
out('M1', cx is None, f'counterexample clamp{cx[:3]!r}' if cx else 'no violation in grid+20000 seeded random (seed=%d)' % SEED)

# M2
try: r = m.mean([]); out('M2', r == 0 and not isinstance(r, bool), f'mean([]) = {r!r}')
except Exception as e: out('M2', False, f'mean([]) raises {e!r}')

# M3
r = m.round_half(2.5); out('M3', r == 3, f'round_half(2.5) = {r!r}')

# M4
cx = None
rng2 = [-12, -5, -1, 0, 1, 2, 5, 12, 18, 10**12]
pairs = list(itertools.product(rng2, rng2)) + [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(20000)]
for a, b in pairs:
    if m.gcd(a, b) != m.gcd(b, a): cx = (a, b, m.gcd(a, b), m.gcd(b, a)); break
out('M4', cx is None, f'gcd{cx[:2]!r}={cx[2]} but reversed={cx[3]}' if cx else f'symmetric on {len(pairs)} pairs')

# M5 exhaustive vs independent reference (trial division / sieve)
sieve = [True]*1001; sieve[0] = sieve[1] = False
for i in range(2, 1001):
    if sieve[i]:
        for j in range(i*i, 1001, i): sieve[j] = False
bad = [n for n in range(0, 1001) if m.is_prime(n) != sieve[n]]
out('M5', not bad, f'minimal counterexample is_prime({bad[0]}) = {m.is_prime(bad[0])!r}, expected {sieve[bad[0]]}; all wrong n: {bad}' if bad else 'all 1001 correct')

# M6
r = m.percent(1, 3); out('M6', r == 33.3, f'percent(1, 3) = {r!r}')
