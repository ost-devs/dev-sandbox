from harness import claim, rng, run
from calc import mathutil as m


@claim('M1')
def m1():
    vals = list(range(-12, 13))
    for lo in range(-6, 7):
        for hi in range(lo, 7):
            for x in vals:
                r = m.clamp(x, lo, hi)
                if not lo <= r <= hi:
                    return 'clamp(%r,%r,%r)=%r' % (x, lo, hi, r)
    R = rng()
    for _ in range(20000):
        lo = R.uniform(-1e6, 1e6); hi = lo + R.choice([0, R.uniform(0, 1e6)])
        x = R.uniform(-2e6, 2e6)
        r = m.clamp(x, lo, hi)
        if not lo <= r <= hi:
            return 'clamp(%r,%r,%r)=%r' % (x, lo, hi, r)


@claim('M2')
def m2():
    r = m.mean([])
    return None if r == 0 else 'mean([])=%r' % (r,)


@claim('M3')
def m3():
    r = m.round_half(2.5)
    return None if r == 3 else 'round_half(2.5)=%r' % (r,)


@claim('M4')
def m4():
    for a in range(-60, 61):
        for b in range(-60, 61):
            if m.gcd(a, b) != m.gcd(b, a):
                return 'gcd(%d,%d)!=gcd(%d,%d)' % (a, b, b, a)
    R = rng()
    for _ in range(20000):
        a = R.randint(-10**12, 10**12); b = R.randint(-10**12, 10**12)
        if m.gcd(a, b) != m.gcd(b, a):
            return 'gcd(%d,%d)!=gcd(%d,%d)' % (a, b, b, a)


@claim('M5')
def m5():
    for n in range(0, 1001):
        t = n >= 2 and all(n % d for d in range(2, n))
        r = m.is_prime(n)
        if r != t:
            return 'is_prime(%d)=%r, expected %r' % (n, r, t)


@claim('M6')
def m6():
    r = m.percent(1, 3)
    return None if r == 33.3 else 'percent(1,3)=%r' % (r,)


if __name__ == '__main__':
    run('mathutil')
