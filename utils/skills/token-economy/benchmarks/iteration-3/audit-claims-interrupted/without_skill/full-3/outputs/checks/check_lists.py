import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.lists import *

SEED = 12345
N = 3000

def rlist(r, lo=-10**9, hi=10**9, maxlen=12):
    return [r.choice([r.randint(-5, 5), r.randint(lo, hi), 0]) for _ in range(r.randint(0, maxlen))]

def int_lists():
    r = random.Random(SEED)
    out = [[], [0], [-1], [1, 1], [3, 1, 3, 2, 1], [-5, 5, -5], [10**18, -10**18, 10**18], list(range(20))]
    out += [rlist(r) for _ in range(N)]
    return out

def eq(claim_id, ok, ce=""):
    return {"id": claim_id, "verdict": "verdadeira" if ok else "falsa", "counterexample": "" if ok else ce, "note": ""}

def fixed(cid, expr_fn, claimed):
    try:
        got = expr_fn()
    except Exception as e:
        return eq(cid, False, f"raised {e!r}")
    return eq(cid, got == claimed, f"actual {got!r} vs claimed {claimed!r}")

def prop(cid, cases, pred):
    best = None
    for c in cases:
        try:
            ok, info = pred(*c)
        except Exception as e:
            ok, info = False, f"raised {e!r}"
        if not ok:
            if best is None or len(repr(c)) < len(repr(best[0])):
                best = (c, info)
    if best:
        return eq(cid, False, f"input {best[0]!r}: {best[1]}")
    return eq(cid, True)

def L01(): return fixed("L01", lambda: chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]])
def L02():
    r = random.Random(SEED + 2)
    cases = [(xs, k) for xs in int_lists() for k in (1, r.randint(1, 8), len(xs) + 1, 10**6)]
    return prop("L02", cases, lambda xs, k: (flatten(chunk(xs, k)) == xs, f"got {flatten(chunk(xs, k))!r}"))
def L03():
    for xs in ([], [1], [1, 2, 3]):
        try:
            got = chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return eq("L03", False, f"chunk({xs!r}, 0) raised {e!r}")
        return eq("L03", False, f"chunk({xs!r}, 0) returned {got!r}")
    return eq("L03", True)
def L04(): return fixed("L04", lambda: dedupe([3,1,3,2,1]), [3,1,2])
def L05():
    def ref(xs):
        seen, o = set(), []
        for x in xs:
            if x not in seen: seen.add(x); o.append(x)
        return o
    return prop("L05", [(x,) for x in int_lists()], lambda xs: (dedupe(xs) == ref(xs), f"got {dedupe(xs)!r}"))
def L06(): return prop("L06", [(x,) for x in int_lists()], lambda xs: (len(dedupe(xs)) == len(set(xs)), f"got len {len(dedupe(xs))}"))
def L07(): return fixed("L07", lambda: flatten([[1,[2]],[3]]), [1,2,3])
def L08(): return fixed("L08", lambda: top_n([5,1,4], 2), [5,4])
def L09():
    cases = [(xs, k) for xs in int_lists() for k in (0, 1, 3, len(xs), len(xs)+1, 10**6)]
    return prop("L09", cases, lambda xs, k: (len(top_n(xs, k)) == min(k, len(xs)), f"got {top_n(xs, k)!r}"))
def L10(): return fixed("L10", lambda: top_n([3,2,1], -1), [])
def L11(): return fixed("L11", lambda: rotate([1,2,3], 1), [2,3,1])
def L12():
    cases = [(xs, k) for xs in int_lists() if xs for k in (0, 1, 2, len(xs), len(xs)+1, 2*len(xs)+1, 10**6)]
    return prop("L12", cases, lambda xs, k: (rotate(xs, k) == rotate(xs, k % len(xs)), f"{rotate(xs,k)!r} vs {rotate(xs, k % len(xs))!r}"))
def L13():
    cases = [(xs, k) for xs in int_lists() for k in (-10**6, -len(xs)-1, -1, 0, 1, len(xs), len(xs)+1, 10**6)]
    return prop("L13", cases, lambda xs, k: (len(rotate(xs, k)) == len(xs), f"got {rotate(xs,k)!r}"))
def L14(): return fixed("L14", lambda: interleave([1,2,3],[9]), [1,9,2,3])
def L15():
    L = int_lists(); r = random.Random(SEED + 15)
    cases = [(a, r.choice(L)) for a in L] + [([], []), ([], [1]), ([1], [])]
    return prop("L15", cases, lambda a, b: (len(interleave(a, b)) == 2*min(len(a), len(b)), f"got {interleave(a,b)!r}"))
def L16(): return fixed("L16", lambda: frequencies('abca'), {'a':2,'b':1,'c':1})
def L17(): return prop("L17", [(x,) for x in int_lists()], lambda xs: (sum(frequencies(xs).values()) == len(xs), f"got {frequencies(xs)!r}"))
def L18(): return fixed("L18", lambda: pairwise([1,2,3]), [(1,2),(2,3)])
def L19():
    cases = [(x,) for x in int_lists()] + [(["é"],), (["日本", "x"],)]
    return prop("L19", cases, lambda xs: (len(pairwise(xs)) == len(xs)-1, f"len {len(pairwise(xs))} vs {len(xs)-1}"))

def main():
    ids = sys.argv[1:] or [f"L{i:02d}" for i in range(1, 20)]
    for i in ids:
        print(json.dumps(globals()[i](), ensure_ascii=False))

if __name__ == "__main__":
    main()
