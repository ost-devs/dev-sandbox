import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import numbers as M


def exhaustive(pred, items):
    for a in items:
        try:
            ok = pred(*a)
        except Exception as e:
            return f"args={a!r} raised {type(e).__name__}: {e}"
        if not ok:
            return f"args={a!r}"
    return None

def call(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"raised {type(e).__name__}: {e}"

@claim("N01")
def n01(): return forall(lambda r: (lambda lo: (r.randint(-50, 50), lo, lo + r.randint(0, 30)))(r.randint(-30, 30)), lambda x, lo, hi: lo <= M.clamp(x, lo, hi) <= hi)
@claim("N02")
def n02(): return eq(call(M.clamp, 5, 10, 0), 0)
@claim("N03")
def n03(): return eq(call(M.mean, []), 0)
@claim("N04")
def n04(): return eq(call(M.mean, [1, 2]), 1.5)
@claim("N05")
def n05(): return eq(call(M.median, [3, 1, 2]), 2)
@claim("N06")
def n06(): return eq(call(M.median, []), None)
@claim("N07")
def n07(): return forall(lambda r: (gen_ints(r, 9) or [0],), lambda xs: M.median(xs) == M.median(sorted(xs)))
@claim("N08")
def n08(): return eq(call(M.round_half, 2.5), 3)
@claim("N09")
def n09(): return eq(call(M.round_half, 3.5), 4)
@claim("N10")
def n10(): return eq(call(M.percent, 1, 3), 33.3)
@claim("N11")
def n11(): return forall(lambda r: (r.choice([0, 1, -3, 2.5, 100, 0.0]),), lambda x: M.percent(x, 0) == 0.0)
def _ref_prime(n): return n >= 2 and all(n % i for i in range(2, n))
@claim("N12")
def n12(): return exhaustive(lambda n: M.is_prime(n) == _ref_prime(n), [(n,) for n in range(1001)])
@claim("N13")
def n13(): return eq(call(M.is_prime, 97), True)
@claim("N14")
def n14(): return eq(call(M.is_prime, 2), True)
@claim("N15")
def n15(): return exhaustive(lambda a, b: M.gcd(a, b) == M.gcd(b, a), [(a, b) for a in range(-50, 51) for b in range(-50, 51)])
@claim("N16")
def n16(): return eq(call(M.gcd, 12, 18), 6)
@claim("N17")
def n17(): return exhaustive(lambda a: M.gcd(a, 0) == a, [(a,) for a in range(-100, 101)])
@claim("N18")
def n18(): return eq(call(M.digits_sum, 1234), 10)
@claim("N19")
def n19(): return exhaustive(lambda n: isinstance(M.digits_sum(n), int) and M.digits_sum(n) >= 0, [(n,) for n in range(-20, 21)])

if __name__ == "__main__":
    main("numbers")
