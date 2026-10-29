import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc import mathutil as m

SEED = 20240607
rng = random.Random(SEED)


def ref_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def show(r):
    return "ERRO %s" % r if isinstance(r, Exception) else repr(r)


def call(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return e


def shrink_ints(args, bad):
    """Greedy shrink of a tuple of ints/floats towards small values."""
    args = list(args)
    changed = True
    while changed:
        changed = False
        for i, v in enumerate(args):
            cands = [0, 1, -1, 2, v // 2 if isinstance(v, int) else 0]
            cands += [v - 1, v + 1] if isinstance(v, int) else []
            for c in sorted(set(cands), key=lambda t: (abs(t), t)):
                if abs(c) < abs(v) or (abs(c) == abs(v) and c < v):
                    t = args[:]; t[i] = c
                    if bad(*t):
                        args = t; changed = True; break
    return tuple(args)


def m1():
    def bad(x, lo, hi):
        if not (lo <= hi):
            return False
        r = call(m.clamp, x, lo, hi)
        return isinstance(r, Exception) or not (lo <= r <= hi)
    cases = []
    vals = [0, 1, -1, 5, -5, 0.5, -0.5, 1e308, -1e308, float('inf'), float('-inf'), float('nan')]
    for x in vals:
        for lo in vals:
            for hi in vals:
                cases.append((x, lo, hi))
    for _ in range(20000):
        lo = rng.randint(-100, 100); hi = lo + rng.randint(0, 100)
        cases.append((rng.randint(-300, 300), lo, hi))
        cases.append((rng.uniform(-300, 300), float(lo), float(hi)))
    for c in cases:
        if bad(*c):
            return False, c, call(m.clamp, *c), len(cases)
    return True, None, None, len(cases)


def m4():
    cases = [(a, b) for a in range(-30, 31) for b in range(-30, 31)]
    cases += [(0, 0), (10**20, -7), (-10**20, 3)]
    for _ in range(20000):
        cases.append((rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)))
    bad = lambda a, b: call(m.gcd, a, b) != call(m.gcd, b, a)
    for c in cases:
        if bad(*c):
            c = shrink_ints(c, bad)
            return False, c, (call(m.gcd, *c), call(m.gcd, *c[::-1])), len(cases)
    return True, None, None, len(cases)


def m5():
    for n in range(0, 1001):
        r = call(m.is_prime, n)
        if r != ref_prime(n):
            return False, n, r, ref_prime(n)
    return True, None, None, 1001


out = []
ok, c, r, k = m1()
out.append("M1: VERDADEIRA (%d casos, sem contraexemplo)" % k if ok else
           "M1: FALSA | contraexemplo: clamp%r -> %s" % (c, show(r)))

r = call(m.mean, [])
out.append("M2: VERDADEIRA" if r == 0 and not isinstance(r, Exception) else
           "M2: FALSA | contraexemplo: mean([]) -> %s" % show(r))

r = call(m.round_half, 2.5)
out.append("M3: VERDADEIRA" if r == 3 and not isinstance(r, Exception) else
           "M3: FALSA | contraexemplo: round_half(2.5) -> %s (esperado 3)" % show(r))

ok, c, r, k = m4()
out.append("M4: VERDADEIRA (%d casos, sem contraexemplo)" % k if ok else
           "M4: FALSA | contraexemplo: gcd%r -> %r vs invertido" % (c, r))

ok, n, got, exp = m5()
out.append("M5: VERDADEIRA (exaustivo, %d valores 0..1000 contra referencia independente)" % exp if ok else
           "M5: FALSA | contraexemplo: is_prime(%d) -> %r (esperado %r)" % (n, got, exp))

r = call(m.percent, 1, 3)
out.append("M6: VERDADEIRA" if r == 33.3 and not isinstance(r, Exception) else
           "M6: FALSA | contraexemplo: percent(1, 3) -> %s (esperado 33.3)" % show(r))

print("\n".join(out))
sys.exit(0)
