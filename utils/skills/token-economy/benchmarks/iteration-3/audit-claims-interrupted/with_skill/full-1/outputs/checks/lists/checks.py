import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, rand_str, main
from kit.lists import *

def rl(r, lo=-5, hi=5, maxn=10):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxn))]

def lists_(cid):
    r = rng(cid)
    return [[], [0], [1, 1], [3, 1, 3, 2, 1], [-1, 0, 1]] + [rl(r) for _ in range(3000)]

def eq(cid, expr_fn, expected):
    got = expr_fn()
    return None if got == expected else f"got {got!r}, expected {expected!r}"

@claim("L01")
def l01(): return eq("L01", lambda: chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]])

@claim("L02")
def l02():
    r = rng("L02")
    for xs in lists_("L02"):
        for k in [1, 2, 3, 5, 100, r.randint(1, 12)]:
            try: out = flatten(chunk(xs, k))
            except Exception as e: return f"chunk({xs!r},{k}) raised {e!r}"
            if out != xs: return f"xs={xs!r}, k={k}: got {out!r}"

@claim("L03")
def l03():
    for xs in [[], [1], [1, 2, 3]]:
        try: out = chunk(xs, 0)
        except ValueError: continue
        except Exception as e: return f"chunk({xs!r},0) raised {type(e).__name__}"
        return f"chunk({xs!r},0) = {out!r}, no ValueError"

@claim("L04")
def l04(): return eq("L04", lambda: dedupe([3,1,3,2,1]), [3,1,2])

@claim("L05")
def l05():
    for xs in lists_("L05"):
        exp = [x for i, x in enumerate(xs) if x not in xs[:i]]
        if dedupe(xs) != exp: return f"dedupe({xs!r}) = {dedupe(xs)!r}, expected {exp!r}"

@claim("L06")
def l06():
    for xs in lists_("L06"):
        if len(dedupe(xs)) != len(set(xs)): return f"dedupe({xs!r}) = {dedupe(xs)!r}"

@claim("L07")
def l07(): return eq("L07", lambda: flatten([[1,[2]],[3]]), [1,2,3])

@claim("L08")
def l08(): return eq("L08", lambda: top_n([5,1,4], 2), [5,4])

@claim("L09")
def l09():
    r = rng("L09")
    for xs in lists_("L09"):
        for k in [0, 1, 2, 5, 50, r.randint(0, 15)]:
            if len(top_n(xs, k)) != min(k, len(xs)): return f"top_n({xs!r},{k}) = {top_n(xs,k)!r}"

@claim("L10")
def l10(): return eq("L10", lambda: top_n([3,2,1], -1), [])

@claim("L11")
def l11(): return eq("L11", lambda: rotate([1,2,3], 1), [2,3,1])

@claim("L12")
def l12():
    r = rng("L12")
    for xs in lists_("L12"):
        if not xs: continue
        for k in [0, 1, len(xs), len(xs)+1, 2*len(xs)+1, r.randint(0, 30)]:
            a, b = rotate(xs, k), rotate(xs, k % len(xs))
            if a != b: return f"xs={xs!r}, k={k}: rotate(xs,k)={a!r}, rotate(xs,k%len)={b!r}"

@claim("L13")
def l13():
    r = rng("L13")
    for xs in lists_("L13"):
        for k in [-100, -3, -1, 0, 1, 3, 100, r.randint(-20, 20)]:
            if len(rotate(xs, k)) != len(xs): return f"rotate({xs!r},{k}) = {rotate(xs,k)!r}"

@claim("L14")
def l14(): return eq("L14", lambda: interleave([1,2,3],[9]), [1,9,2,3])

@claim("L15")
def l15():
    r = rng("L15")
    for _ in range(3000):
        a, b = rl(r), rl(r)
        if len(interleave(a, b)) != 2*min(len(a), len(b)): return f"a={a!r}, b={b!r}: {interleave(a,b)!r}"
    if len(interleave([], [])) != 0: return "empty"

@claim("L16")
def l16(): return eq("L16", lambda: frequencies('abca'), {'a':2,'b':1,'c':1})

@claim("L17")
def l17():
    for xs in lists_("L17"):
        if sum(frequencies(xs).values()) != len(xs): return f"xs={xs!r}"

@claim("L18")
def l18(): return eq("L18", lambda: pairwise([1,2,3]), [(1,2),(2,3)])

@claim("L19")
def l19():
    for xs in lists_("L19"):
        if len(pairwise(xs)) != len(xs)-1: return f"pairwise({xs!r}) = {pairwise(xs)!r}, len {len(pairwise(xs))} != {len(xs)-1}"

if __name__ == "__main__":
    main()
