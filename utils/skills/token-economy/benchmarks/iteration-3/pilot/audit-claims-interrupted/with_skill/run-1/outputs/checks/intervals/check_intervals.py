import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_ints, SEED
from kit import intervals as I

N = 2500

def riv(r, valid=True, lo=-20, hi=20):
    a, b = r.randint(lo, hi), r.randint(lo, hi)
    if valid:
        while a == b: b = r.randint(lo, hi)
        a, b = min(a, b), max(a, b)
    return (a, b)

def rlist(r, valid=True, minlen=1):
    return [riv(r, valid) for _ in range(r.randint(minlen, 8))]

def eq(cid, expr, expected):
    got = expr()
    return True if got == expected else (False, f"-> {got!r}, expected {expected!r}")

@claim('I01')
def i01(): return eq('I01', lambda: I.overlaps((0, 5), (5, 10)), False)

@claim('I02')
def i02():
    r = rng('I02')
    cases = [((0,0),(0,0)), ((3,1),(0,5)), ((-1,1),(1,3))] + [(riv(r, r.random()<.7), riv(r, r.random()<.7)) for _ in range(N)]
    for a, b in cases:
        if I.overlaps(a, b) != I.overlaps(b, a): return (False, f"{a},{b} -> {I.overlaps(a,b)} vs {I.overlaps(b,a)}")
    return True

@claim('I03')
def i03(): return eq('I03', lambda: I.merge([(1,3),(2,6),(8,10)]), [(1,6),(8,10)])

@claim('I04')
def i04(): return eq('I04', lambda: I.merge([(1,2),(2,3)]), [(1,3)])

@claim('I05')
def i05():
    r = rng('I05')
    cases = [[(0,1)], [(1,2),(2,3)], [(0,10),(2,3)], [(-5,-1),(-3,4)]] + [rlist(r) for _ in range(N)]
    for xs in cases:
        m = I.merge(xs)
        ok = all(m[i][0] <= m[i+1][0] for i in range(len(m)-1)) and \
             not any(I.overlaps(m[i], m[j]) for i in range(len(m)) for j in range(i+1, len(m)))
        if not ok: return (False, f"{xs} -> {m}")
    return True

@claim('I06')
def i06():
    r = rng('I06')
    cases = [[(0,1)], [(1,2),(2,3)]] + [rlist(r) for _ in range(N)]
    for xs in cases:
        m = I.merge(xs)
        if I.merge(m) != m: return (False, f"{xs} -> {m} -> {I.merge(m)}")
    return True

@claim('I07')
def i07(): return eq('I07', lambda: I.contains((0,5), 5), False)

@claim('I08')
def i08():
    r = rng('I08')
    for a in [(0,1), (-3,-2)] + [riv(r) for _ in range(N)]:
        if I.contains(a, a[0]) is not True: return (False, f"{a} -> {I.contains(a, a[0])}")
    return True

@claim('I09')
def i09(): return eq('I09', lambda: I.intersect((0,5),(3,8)), (3,5))

@claim('I10')
def i10(): return eq('I10', lambda: I.intersect((0,2),(5,6)), None)

@claim('I11')
def i11(): return eq('I11', lambda: I.intersect((0,5),(5,8)), None)

@claim('I12')
def i12(): return eq('I12', lambda: I.total_covered([(0,5),(3,8)]), 8)

@claim('I13')
def i13():
    r = rng('I13')
    cases = [[(0,1)], [(0,5),(0,5)], [(1,2),(2,3)]] + [rlist(r) for _ in range(N)]
    for xs in cases:
        t, s = I.total_covered(xs), sum(I.length(i) for i in xs)
        if not t <= s: return (False, f"{xs} -> {t} > {s}")
    return True

@claim('I14')
def i14():
    r = rng('I14')
    n = 0
    cases = [((0,5),(3,8)), ((0,10),(2,3)), ((0,1),(0,1))] + [(riv(r), riv(r)) for _ in range(N*3)]
    for a, b in cases:
        if not I.overlaps(a, b): continue
        n += 1
        l = I.length(I.intersect(a, b))
        if not l <= min(I.length(a), I.length(b)): return (False, f"{a},{b} -> {I.intersect(a,b)}")
    return True if n >= 2000 else (False, f"only {n} overlapping cases")

@claim('I15')
def i15(): return eq('I15', lambda: I.merge([]), [])

@claim('I16')
def i16():
    r = rng('I16')
    for a in [(0,1)] + [riv(r) for _ in range(N)]:
        if I.overlaps(a, a) is not True: return (False, f"{a} -> {I.overlaps(a,a)}")
    return True

@claim('I17')
def i17(): return eq('I17', lambda: I.merge([(5,7),(1,2)]), [(1,2),(5,7)])

@claim('I18')
def i18():
    r = rng('I18')
    cases = [((0,5),5), ((0,5),0), ((0,5),4), ((-3,-1),-1)] + [(riv(r, r.random()<.8), r.randint(-22,22)) for _ in range(N)]
    for a, x in cases:
        if I.contains(a, x) and not I.overlaps(a, (x, x+1)):
            return (False, f"a={a}, x={x}: contains=True, overlaps(a,{(x,x+1)})=False")
    return True

@claim('I19')
def i19(): return eq('I19', lambda: I.length((3,1)), 0)

if __name__ == '__main__': run(__file__)
