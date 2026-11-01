import os, sys, random, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc import mathutil as m

rng = random.Random(12345)
res = {}

# M1
def m1():
    vals = [0, -1, 1, 5, -5, 2.5, -0.0, 1e308, -1e308, float('inf'), float('-inf')]
    vals += [rng.randint(-100, 100) for _ in range(200)] + [rng.uniform(-100, 100) for _ in range(200)]
    for lo in vals:
        for hi in vals:
            if lo <= hi:
                for x in vals[:40] + [lo, hi]:
                    try:
                        r = m.clamp(x, lo, hi)
                    except Exception as e:
                        return ((x, lo, hi), 'raised %r' % e)
                    if not (lo <= r <= hi):
                        return ((x, lo, hi), r)
    return None
res['M1'] = m1()

def m2():
    try:
        r = m.mean([])
    except Exception as e:
        return 'raises %s' % type(e).__name__
    return None if r == 0 else r
res['M2'] = m2()

def m3():
    r = m.round_half(2.5)
    return None if r == 3 else 'round_half(2.5)=%r' % r
res['M3'] = m3()

def m4():
    pairs = [(a, b) for a in range(-30, 31) for b in range(-30, 31)]
    pairs += [(rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)) for _ in range(5000)]
    for a, b in pairs:
        try:
            x, y = m.gcd(a, b), m.gcd(b, a)
        except Exception as e:
            return ((a, b), 'raised %r' % e)
        if x != y:
            return ((a, b), x, y)
    return None
res['M4'] = m4()

def ref_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))
def m5():
    bad = [(n, m.is_prime(n)) for n in range(0, 1001) if m.is_prime(n) != ref_prime(n)]
    return None if not bad else 'n=%d got %r (first of %d wrong: %s)' % (bad[0][0], bad[0][1], len(bad), [b[0] for b in bad][:8])
res['M5'] = m5()

def m6():
    r = m.percent(1, 3)
    return None if r == 33.3 else 'percent(1,3)=%r' % r
res['M6'] = m6()

lines = []
for k in ['M1','M2','M3','M4','M5','M6']:
    v = res[k]
    lines.append('%s %s %s' % (k, 'TRUE' if v is None else 'FALSE', '-' if v is None else repr(v)))
out = '\n'.join(lines)
print(out)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mathutil.out'), 'w') as f:
    f.write(out + '\n')
