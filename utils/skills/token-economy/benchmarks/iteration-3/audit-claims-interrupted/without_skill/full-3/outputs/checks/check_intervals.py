import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.intervals import overlaps, length, contains, merge, intersect, total_covered

SEED = 12345
N = 3000

def rnd_iv(r, proper=True, lo=-50, hi=50):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if proper and a >= b:
            continue
        return (a, b)

def rnd_list(r):
    return [rnd_iv(r, True, -20, 20) for _ in range(r.randint(1, 8))]

EDGE_IVS = [(0, 1), (-5, -1), (-3, 3), (10**18, 10**18 + 1), (0.5, 1.5), (-10**9, 10**9)]
EDGE_LISTS = [[(0, 1)], [(0, 1), (0, 1)], [(1, 2), (2, 3), (3, 4)], [(0, 10), (2, 3)], [(-5, -1), (-3, 2)], [(2, 3), (0, 1)]]

def res(id_, ok, ce=""):
    return {"id": id_, "verdict": "verdadeira" if ok else "falsa", "counterexample": "" if ok else ce, "note": ""}

def eq(id_, got, exp, desc):
    return res(id_, got == exp, f"{desc}: actual {got!r}, claimed {exp!r}")

def safe(id_, f):
    try:
        return f()
    except Exception as e:
        return res(id_, False, f"exception {type(e).__name__}: {e}")

def I01(): return eq("I01", overlaps((0, 5), (5, 10)), False, "overlaps((0,5),(5,10))")
def I02():
    r = random.Random(SEED)
    cases = [(rnd_iv(r, False), rnd_iv(r, False)) for _ in range(N)] + [(a, b) for a in EDGE_IVS for b in EDGE_IVS] + [((0, 0), (0, 0)), ((5, 0), (0, 5))]
    for a, b in cases:
        if overlaps(a, b) != overlaps(b, a):
            return res("I02", False, f"a={a}, b={b}: {overlaps(a,b)} vs {overlaps(b,a)}")
    return res("I02", True)
def I03(): return eq("I03", merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)], "merge")
def I04(): return eq("I04", merge([(1, 2), (2, 3)]), [(1, 3)], "merge([(1,2),(2,3)])")
def I05():
    r = random.Random(SEED)
    for xs in [rnd_list(r) for _ in range(N)] + EDGE_LISTS:
        m = merge(xs)
        for i in range(len(m) - 1):
            if not (m[i][0] <= m[i + 1][0]) or overlaps(m[i], m[i + 1]):
                return res("I05", False, f"xs={xs}: merge={m}")
    return res("I05", True)
def I06():
    r = random.Random(SEED + 1)
    for xs in [rnd_list(r) for _ in range(N)] + EDGE_LISTS:
        if merge(merge(xs)) != merge(xs):
            return res("I06", False, f"xs={xs}")
    return res("I06", True)
def I07(): return eq("I07", contains((0, 5), 5), False, "contains((0,5),5)")
def I08():
    r = random.Random(SEED + 2)
    for a in [rnd_iv(r) for _ in range(N)] + EDGE_IVS:
        if contains(a, a[0]) is not True:
            return res("I08", False, f"a={a}")
    return res("I08", True)
def I09(): return eq("I09", intersect((0, 5), (3, 8)), (3, 5), "intersect")
def I10(): return eq("I10", intersect((0, 2), (5, 6)), None, "intersect")
def I11(): return eq("I11", intersect((0, 5), (5, 8)), None, "intersect((0,5),(5,8))")
def I12(): return eq("I12", total_covered([(0, 5), (3, 8)]), 8, "total_covered")
def I13():
    r = random.Random(SEED + 3)
    for xs in [rnd_list(r) for _ in range(N)] + EDGE_LISTS:
        if total_covered(xs) > sum(length(i) for i in xs):
            return res("I13", False, f"xs={xs}")
    return res("I13", True)
def I14():
    r = random.Random(SEED + 4)
    cases = [(rnd_iv(r), rnd_iv(r)) for _ in range(N)] + [(a, b) for a in EDGE_IVS for b in EDGE_IVS]
    for a, b in cases:
        if overlaps(a, b):
            i = intersect(a, b)
            if length(i) > min(length(a), length(b)):
                return res("I14", False, f"a={a}, b={b}: {i}")
    return res("I14", True)
def I15(): return eq("I15", merge([]), [], "merge([])")
def I16():
    r = random.Random(SEED + 5)
    for a in [rnd_iv(r) for _ in range(N)] + EDGE_IVS:
        if overlaps(a, a) is not True:
            return res("I16", False, f"a={a}")
    return res("I16", True)
def I17(): return eq("I17", merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)], "merge")
def I18():
    r = random.Random(SEED + 6)
    cases = [(rnd_iv(r), r.randint(-60, 60)) for _ in range(N)] + [((0, 5), 5), ((0, 1), 1)]
    cases.sort(key=lambda c: abs(c[0][1] - c[0][0]) + abs(c[1]))
    for a, x in cases:
        if contains(a, x) and not overlaps(a, (x, x + 1)):
            return res("I18", False, f"a={a}, x={x}: contains=True, overlaps(a,(x,x+1))=False")
    return res("I18", True)
def I19(): return eq("I19", length((3, 1)), 0, "length((3,1))")

if __name__ == "__main__":
    ids = sys.argv[1:] or [f"I{i:02d}" for i in range(1, 20)]
    for i in ids:
        print(json.dumps(safe(i, globals()[i]), ensure_ascii=False))
