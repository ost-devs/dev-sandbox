import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, main
from kit.numbers import *

def ex(expr_fn, expected, label):
    try:
        out = expr_fn()
    except Exception as e:
        return f"{label} raised {type(e).__name__}: {e}"
    if out != expected or (type(out) is bool) != (type(expected) is bool):
        return f"{label} = {out!r}, expected {expected!r}"

@claim("N01")
def n01():
    r = rng("N01")
    cases = [(0,0,0),(-5,-5,5),(5,-5,5),(-9,-5,5),(9,-5,5)]
    cases += [(r.randint(-100,100), *sorted([r.randint(-100,100), r.randint(-100,100)])) for _ in range(3000)]
    for x, lo, hi in cases:
        try: o = clamp(x, lo, hi)
        except Exception as e: return f"clamp({x},{lo},{hi}) raised {e}"
        if not lo <= o <= hi: return f"clamp({x},{lo},{hi}) = {o}"
@claim("N02")
def n02(): return ex(lambda: clamp(5,10,0), 0, "clamp(5,10,0)")
@claim("N03")
def n03(): return ex(lambda: mean([]), 0, "mean([])")
@claim("N04")
def n04(): return ex(lambda: mean([1,2]), 1.5, "mean([1,2])")
@claim("N05")
def n05(): return ex(lambda: median([3,1,2]), 2, "median([3,1,2])")
@claim("N06")
def n06():
    try: o = median([])
    except Exception as e: return f"median([]) raised {type(e).__name__}: {e}"
    if o is not None: return f"median([]) = {o!r}"
@claim("N07")
def n07():
    r = rng("N07")
    cases = [[0],[-1],[1,2],[2,1],[5,5,5]] + [[r.randint(-20,20) for _ in range(r.randint(1,9))] for _ in range(3000)]
    for xs in cases:
        a, b = median(xs), median(sorted(xs))
        if a != b: return f"median({xs}) = {a} vs sorted {b}"
@claim("N08")
def n08(): return ex(lambda: round_half(2.5), 3, "round_half(2.5)")
@claim("N09")
def n09(): return ex(lambda: round_half(3.5), 4, "round_half(3.5)")
@claim("N10")
def n10(): return ex(lambda: percent(1,3), 33.3, "percent(1,3)")
@claim("N11")
def n11():
    r = rng("N11")
    for x in [0, 1, -1, 0.5, 10**9] + [r.randint(-100,100) for _ in range(50)]:
        try: o = percent(x, 0)
        except Exception as e: return f"percent({x}, 0) raised {type(e).__name__}: {e}"
        if o != 0.0 or not isinstance(o, float): return f"percent({x}, 0) = {o!r}"
@claim("N12")
def n12():
    bad = []
    for n in range(1001):
        t = n >= 2 and all(n % d for d in range(2, n))
        if is_prime(n) is not t: bad.append(f"is_prime({n}) = {is_prime(n)}, expected {t}")
    if bad: return "; ".join(bad[:3])
@claim("N13")
def n13(): return ex(lambda: is_prime(97), True, "is_prime(97)")
@claim("N14")
def n14(): return ex(lambda: is_prime(2), True, "is_prime(2)")
@claim("N15")
def n15():
    for a in range(-50,51):
        for b in range(-50,51):
            if gcd(a,b) != gcd(b,a): return f"gcd({a},{b}) = {gcd(a,b)} but gcd({b},{a}) = {gcd(b,a)}"
@claim("N16")
def n16(): return ex(lambda: gcd(12,18), 6, "gcd(12,18)")
@claim("N17")
def n17():
    r = rng("N17")
    for a in [0,1,-1,-7,10**30,-10**30] + [r.randint(-10**6,10**6) for _ in range(3000)]:
        if gcd(a,0) != a: return f"gcd({a},0) = {gcd(a,0)}"
@claim("N18")
def n18(): return ex(lambda: digits_sum(1234), 10, "digits_sum(1234)")
@claim("N19")
def n19():
    r = rng("N19")
    for n in [0,1,-1,-1234,10**30,-10**30] + [r.randint(-10**9,10**9) for _ in range(3000)]:
        try: o = digits_sum(n)
        except Exception as e: return f"digits_sum({n}) raised {type(e).__name__}: {e}"
        if type(o) is not int or o < 0: return f"digits_sum({n}) = {o!r}"

if __name__ == "__main__":
    main()
