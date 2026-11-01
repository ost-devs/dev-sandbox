import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.numbers import *

def eq(got, want):
    return True if got == want else (False, 'got %r, expected %r' % (got, want))

@prop
def N01(r):
    lo = rand_int(r, -50, 50); hi = lo + r.randint(0, 50); x = rand_int(r, -150, 150)
    v = clamp(x, lo, hi)
    return None if lo <= v <= hi else 'clamp(%r,%r,%r)=%r' % (x, lo, hi, v)

@exact
def N02(): return eq(clamp(5, 10, 0), 0)
@exact
def N03(): return eq(mean([]), 0)
@exact
def N04(): return eq(mean([1, 2]), 1.5)
@exact
def N05(): return eq(median([3, 1, 2]), 2)
@exact
def N06(): return eq(median([]), None)

@prop
def N07(r):
    xs = rand_list(r, lambda r: rand_int(r, -100, 100), 10) or [rand_int(r)]
    a, b = median(xs), median(sorted(xs))
    return None if a == b else 'xs=%r: %r vs %r' % (xs, a, b)

@exact
def N08(): return eq(round_half(2.5), 3)
@exact
def N09(): return eq(round_half(3.5), 4)
@exact
def N10(): return eq(percent(1, 3), 33.3)

@prop
def N11(r):
    x = r.choice([rand_int(r, -1000, 1000), r.uniform(-1e3, 1e3), 0])
    v = percent(x, 0)
    return None if v == 0.0 and isinstance(v, float) else 'percent(%r,0)=%r' % (x, v)

@exact
def N12():
    ref = lambda n: n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))
    bad = [(n, is_prime(n)) for n in range(1001) if is_prime(n) != ref(n)]
    return True if not bad else (False, 'wrong (n, is_prime(n)) e.g. %r; %d total' % (bad[:5], len(bad)))

@exact
def N13(): return eq(is_prime(97), True)
@exact
def N14(): return eq(is_prime(2), True)

@exact
def N15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            if gcd(a, b) != gcd(b, a):
                return False, 'gcd(%d,%d)=%r but gcd(%d,%d)=%r' % (a, b, gcd(a, b), b, a, gcd(b, a))
    return True

@exact
def N16(): return eq(gcd(12, 18), 6)

@prop
def N17(r):
    a = rand_int(r, -10**6, 10**6)
    v = gcd(a, 0)
    return None if v == a else 'gcd(%r,0)=%r' % (a, v)

@exact
def N18(): return eq(digits_sum(1234), 10)

@prop
def N19(r):
    n = r.choice([rand_int(r, -10**6, 10**6), rand_int(r, -20, 20)])
    v = digits_sum(n)
    return None if isinstance(v, int) and v >= 0 else 'digits_sum(%r)=%r' % (n, v)

run({k: v for k, v in globals().items() if len(k) == 3 and k[0] == 'N' and k[1:].isdigit()})
