import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit import numbers as n

def eq(cid, got, exp):
    return True if got == exp else (False, f"{cid} -> {got!r}, expected {exp!r}")

def call(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return ('EXC', repr(e))

@claim('N01')
def n01():
    r = rng('N01')
    cases = [(0,0,0),(-1,-1,-1),(5,0,0),(-5,0,0),(0,-3,3)]
    cases += [(r.randint(-10**6,10**6), *sorted((r.randint(-100,100), r.randint(-100,100)))) for _ in range(3000)]
    for x, lo, hi in cases:
        o = n.clamp(x, lo, hi)
        if not (lo <= o <= hi): return (False, f"clamp({x},{lo},{hi}) -> {o}")
    return True

@claim('N02')
def n02(): return eq('clamp(5,10,0)', call(n.clamp,5,10,0), 0)
@claim('N03')
def n03(): return eq('mean([])', call(n.mean,[]), 0)
@claim('N04')
def n04(): return eq('mean([1,2])', call(n.mean,[1,2]), 1.5)
@claim('N05')
def n05(): return eq('median([3,1,2])', call(n.median,[3,1,2]), 2)
@claim('N06')
def n06():
    o = call(n.median, [])
    return True if o is None else (False, f"median([]) -> {o!r}")

@claim('N07')
def n07():
    r = rng('N07')
    cases = [[0],[-1],[1,2],[2,1],[3,1,2]] + [rand_ints(r, 9, -50, 50) or [0] for _ in range(3000)]
    for xs in cases:
        a = call(n.median, list(xs)); b = call(n.median, sorted(xs))
        if a != b: return (False, f"{xs} -> {a!r} vs sorted {b!r}")
    return True

@claim('N08')
def n08(): return eq('round_half(2.5)', call(n.round_half,2.5), 3)
@claim('N09')
def n09(): return eq('round_half(3.5)', call(n.round_half,3.5), 4)
@claim('N10')
def n10(): return eq('percent(1,3)', call(n.percent,1,3), 33.3)

@claim('N11')
def n11():
    r = rng('N11')
    xs = [0, 1, -1, 0.0, 2.5, -7, 10**9] + [r.choice([r.randint(-1000,1000), r.uniform(-1e3,1e3)]) for _ in range(2000)]
    for x in xs:
        o = call(n.percent, x, 0)
        if not (o == 0.0 and isinstance(o, float)): return (False, f"percent({x!r}, 0) -> {o!r}")
    return True

def ref_prime(k):
    return k >= 2 and all(k % d for d in range(2, k))

@claim('N12')
def n12():
    for k in range(0, 1001):
        o = call(n.is_prime, k)
        if o is not ref_prime(k): return (False, f"is_prime({k}) -> {o!r}, expected {ref_prime(k)}")
    return True

@claim('N13')
def n13(): return eq('is_prime(97)', call(n.is_prime,97), True)
@claim('N14')
def n14(): return eq('is_prime(2)', call(n.is_prime,2), True)

@claim('N15')
def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            x, y = call(n.gcd, a, b), call(n.gcd, b, a)
            if x != y: return (False, f"gcd({a},{b})={x!r} vs gcd({b},{a})={y!r}")
    return True

@claim('N16')
def n16(): return eq('gcd(12,18)', call(n.gcd,12,18), 6)

@claim('N17')
def n17():
    r = rng('N17')
    for a in [0,1,-1,5,-5,10**18,-10**18] + [r.randint(-10**9,10**9) for _ in range(2500)]:
        o = call(n.gcd, a, 0)
        if o != a: return (False, f"gcd({a},0) -> {o!r}")
    return True

@claim('N18')
def n18(): return eq('digits_sum(1234)', call(n.digits_sum,1234), 10)

@claim('N19')
def n19():
    r = rng('N19')
    for k in [0,-1,-5,1,9,10,-10,10**20,-10**20] + [r.randint(-10**9,10**9) for _ in range(2500)]:
        o = call(n.digits_sum, k)
        if not (type(o) is int and o >= 0): return (False, f"digits_sum({k}) -> {o!r}")
    return True

if __name__ == '__main__':
    run(__file__)
