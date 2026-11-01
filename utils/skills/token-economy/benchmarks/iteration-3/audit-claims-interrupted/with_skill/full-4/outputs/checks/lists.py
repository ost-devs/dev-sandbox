import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.lists import *

def ints(r, m=8): return rand_list(r, rand_int, m)

@exact
def L01(): v = chunk(list(range(7)), 3); return v == [[0,1,2],[3,4,5],[6]] or (False, repr(v))
@prop
def L02(r):
    xs = ints(r); k = rand_int(r, 1, 10)
    v = flatten(chunk(xs, k))
    return None if v == xs else f"xs={xs!r} k={k} got {v!r}"
@exact
def L03():
    for xs in ([1, 2, 3], []):
        try: chunk(xs, 0)
        except ValueError: continue
        return (False, f"no ValueError for {xs!r}")
    return True
@exact
def L04(): v = dedupe([3,1,3,2,1]); return v == [3,1,2] or (False, repr(v))
@prop
def L05(r):
    xs = ints(r, 12); exp = []
    for x in xs:
        if x not in exp: exp.append(x)
    v = dedupe(xs)
    return None if v == exp else f"xs={xs!r} got {v!r}"
@prop
def L06(r):
    xs = ints(r, 12); v = dedupe(xs)
    return None if len(v) == len(set(xs)) else f"xs={xs!r} got {v!r}"
@exact
def L07(): v = flatten([[1,[2]],[3]]); return v == [1,2,3] or (False, f"got {v!r}")
@exact
def L08(): v = top_n([5,1,4], 2); return v == [5,4] or (False, repr(v))
@prop
def L09(r):
    xs = ints(r); k = rand_int(r, 0, 12); v = top_n(xs, k)
    return None if len(v) == min(k, len(xs)) else f"xs={xs!r} k={k} got {v!r}"
@exact
def L10(): v = top_n([3,2,1], -1); return v == [] or (False, f"got {v!r}")
@exact
def L11(): v = rotate([1,2,3], 1); return v == [2,3,1] or (False, repr(v))
@prop
def L12(r):
    xs = ints(r); 
    if not xs: return None
    k = rand_int(r, 0, 20)
    a, b = rotate(xs, k), rotate(xs, k % len(xs))
    return None if a == b else f"xs={xs!r} k={k}: rotate(xs,k)={a!r} rotate(xs,k%len)={b!r}"
@prop
def L13(r):
    xs = ints(r); k = rand_int(r, -25, 25); v = rotate(xs, k)
    return None if len(v) == len(xs) else f"xs={xs!r} k={k} got {v!r}"
@exact
def L14(): v = interleave([1,2,3],[9]); return v == [1,9,2,3] or (False, f"got {v!r}")
@prop
def L15(r):
    a, b = ints(r), ints(r); v = interleave(a, b)
    return None if len(v) == 2*min(len(a), len(b)) else f"a={a!r} b={b!r} got {v!r}"
@exact
def L16(): v = frequencies('abca'); return v == {'a':2,'b':1,'c':1} or (False, repr(v))
@prop
def L17(r):
    xs = ints(r, 12); v = frequencies(xs)
    return None if sum(v.values()) == len(xs) else f"xs={xs!r} got {v!r}"
@exact
def L18(): v = pairwise([1,2,3]); return v == [(1,2),(2,3)] or (False, repr(v))
@prop
def L19(r):
    xs = ints(r); v = pairwise(xs)
    return None if len(v) == len(xs)-1 else f"xs={xs!r} len(pairwise)={len(v)} expected {len(xs)-1}"

run({k: v for k, v in globals().items() if len(k) == 3 and k[0] == 'L' and k[1:].isdigit()})
