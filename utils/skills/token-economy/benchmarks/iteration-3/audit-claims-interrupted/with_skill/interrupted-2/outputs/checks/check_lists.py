import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import lists as L

I = lambda r: (gen_ints(r),)

@claim("L01")
def l01(): return eq(L.chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]])
@claim("L02")
def l02(): return forall(lambda r: (gen_ints(r), r.randint(1, 10)), lambda xs, k: L.flatten(L.chunk(xs, k)) == xs)
@claim("L03")
def l03():
    for xs in ([], [1, 2]):
        try: L.chunk(xs, 0)
        except ValueError: continue
        except Exception as e: return f"xs={xs} raised {type(e).__name__}"
        return f"xs={xs} did not raise"
@claim("L04")
def l04(): return eq(L.dedupe([3, 1, 3, 2, 1]), [3, 1, 2])
@claim("L05")
def l05(): return forall(lambda r: (gen_ints(r, 10, -5, 5),), lambda xs: L.dedupe(xs) == [x for i, x in enumerate(xs) if x not in xs[:i]])
@claim("L06")
def l06(): return forall(I, lambda xs: len(L.dedupe(xs)) == len(set(xs)))
@claim("L07")
def l07(): return eq(L.flatten([[1, [2]], [3]]), [1, 2, 3])
@claim("L08")
def l08(): return eq(L.top_n([5, 1, 4], 2), [5, 4])
@claim("L09")
def l09(): return forall(lambda r: (gen_ints(r), r.randint(0, 12)), lambda xs, k: len(L.top_n(xs, k)) == min(k, len(xs)))
@claim("L10")
def l10(): return eq(L.top_n([3, 2, 1], -1), [])
@claim("L11")
def l11(): return eq(L.rotate([1, 2, 3], 1), [2, 3, 1])
@claim("L12")
def l12(): return forall(lambda r: (gen_ints(r, 8)  or [r.randint(0, 5)], r.randint(0, 30)), lambda xs, k: L.rotate(xs, k) == L.rotate(xs, k % len(xs)))
@claim("L13")
def l13(): return forall(lambda r: (gen_ints(r), r.randint(-30, 30)), lambda xs, k: len(L.rotate(xs, k)) == len(xs))
@claim("L14")
def l14(): return eq(L.interleave([1, 2, 3], [9]), [1, 9, 2, 3])
@claim("L15")
def l15(): return forall(lambda r: (gen_ints(r), gen_ints(r)), lambda a, b: len(L.interleave(a, b)) == 2 * min(len(a), len(b)))
@claim("L16")
def l16(): return eq(L.frequencies('abca'), {'a': 2, 'b': 1, 'c': 1})
@claim("L17")
def l17(): return forall(I, lambda xs: sum(L.frequencies(xs).values()) == len(xs))
@claim("L18")
def l18(): return eq(L.pairwise([1, 2, 3]), [(1, 2), (2, 3)])
@claim("L19")
def l19(): return forall(I, lambda xs: len(L.pairwise(xs)) == len(xs) - 1)

if __name__ == "__main__":
    main("lists")
