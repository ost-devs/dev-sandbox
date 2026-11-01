import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.numbers import *

def eq(actual, expected):
    if actual != expected or (type(actual) is bool) != (type(expected) is bool):
        raise Counter(f"actual={actual!r} expected={expected!r}")

@claim("N01")
def n01():
    def gen(r):
        lo = r.randint(-30, 30); hi = lo + r.randint(0, 30)
        return (r.randint(-100, 100), lo, hi)
    forall("N01", gen, lambda x, lo, hi: lo <= clamp(x, lo, hi) <= hi)

@claim("N02")
def n02(): eq(clamp(5, 10, 0), 0)

@claim("N03")
def n03(): eq(mean([]), 0)

@claim("N04")
def n04(): eq(mean([1, 2]), 1.5)

@claim("N05")
def n05(): eq(median([3, 1, 2]), 2)

@claim("N06")
def n06():
    eq(median([]), None)

@claim("N07")
def n07():
    forall("N07", lambda r: (rand_list(r, minlen=1),), lambda xs: median(xs) == median(sorted(xs)))

@claim("N08")
def n08(): eq(round_half(2.5), 3)

@claim("N09")
def n09(): eq(round_half(3.5), 4)

@claim("N10")
def n10(): eq(percent(1, 3), 33.3)

@claim("N11")
def n11():
    for x in [0, 1, -1, 5, 2.5, 100, -3.7]:
        eq(percent(x, 0), 0.0)

def ref_prime(n):
    return n > 1 and all(n % d for d in range(2, n))

@claim("N12")
def n12():
    bad = [n for n in range(0, 1001) if is_prime(n) != ref_prime(n)]
    if bad: raise Counter(f"wrong for n={bad[:8]} (count {len(bad)}); e.g. is_prime({bad[0]})={is_prime(bad[0])}")

@claim("N13")
def n13(): eq(is_prime(97), True)

@claim("N14")
def n14(): eq(is_prime(2), True)

@claim("N15")
def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            if gcd(a, b) != gcd(b, a):
                raise Counter(f"a={a} b={b}: gcd(a,b)={gcd(a,b)} gcd(b,a)={gcd(b,a)}")

@claim("N16")
def n16(): eq(gcd(12, 18), 6)

@claim("N17")
def n17():
    forall("N17", lambda r: (r.choice([0, 1, -1, r.randint(-10**6, 10**6)]),), lambda a: gcd(a, 0) == a)

@claim("N18")
def n18(): eq(digits_sum(1234), 10)

@claim("N19")
def n19():
    def pred(n):
        v = digits_sum(n)
        return isinstance(v, int) and v >= 0
    forall("N19", lambda r: (r.choice([0, -1, r.randint(-10**9, 10**9)]),), pred)

if __name__=='__main__': main('numbers')
