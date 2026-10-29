from common import *
from kit.lists import *

def lists(cid, n=N, lo=0, hi=8, v=5):
    r = rng(cid)
    return [[r.randint(0, v) for _ in range(r.randint(lo, hi))] for _ in range(n)]

@claim('L01')
def _(): return eq(lambda: chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]])
@claim('L02')
def _(): return forall(((xs, k) for xs in lists('L02', 3000) for k in range(1, 10)), lambda xs, k: flatten(chunk(xs, k)) == xs)
@claim('L03')
def _(): return raises(lambda: chunk([1, 2, 3], 0), ValueError) or raises(lambda: chunk([], 0), ValueError)
@claim('L04')
def _(): return eq(lambda: dedupe([3, 1, 3, 2, 1]), [3, 1, 2])
@claim('L05')
def _():
    def ref(xs):
        out = []
        for x in xs:
            if x not in out: out.append(x)
        return out
    return forall(lists('L05'), lambda xs: dedupe(xs) == ref(xs))
@claim('L06')
def _(): return forall(lists('L06'), lambda xs: len(dedupe(xs)) == len(set(xs)))
@claim('L07')
def _(): return eq(lambda: flatten([[1, [2]], [3]]), [1, 2, 3])
@claim('L08')
def _(): return eq(lambda: top_n([5, 1, 4], 2), [5, 4])
@claim('L09')
def _(): return forall(((xs, k) for xs in lists('L09', 3000) for k in range(0, 12)), lambda xs, k: len(top_n(xs, k)) == min(k, len(xs)))
@claim('L10')
def _(): return eq(lambda: top_n([3, 2, 1], -1), [])
@claim('L11')
def _(): return eq(lambda: rotate([1, 2, 3], 1), [2, 3, 1])
@claim('L12')
def _(): return forall(((xs, k) for xs in lists('L12', 3000, lo=1) for k in range(0, 20)), lambda xs, k: rotate(xs, k) == rotate(xs, k % len(xs)))
@claim('L13')
def _(): return forall(((xs, k) for xs in lists('L13', 3000) for k in range(-20, 20)), lambda xs, k: len(rotate(xs, k)) == len(xs))
@claim('L14')
def _(): return eq(lambda: interleave([1, 2, 3], [9]), [1, 9, 2, 3])
@claim('L15')
def _(): return forall(zip(lists('L15a'), lists('L15b')), lambda a, b: len(interleave(a, b)) == 2 * min(len(a), len(b)))
@claim('L16')
def _(): return eq(lambda: frequencies('abca'), {'a': 2, 'b': 1, 'c': 1})
@claim('L17')
def _(): return forall(lists('L17'), lambda xs: sum(frequencies(xs).values()) == len(xs))
@claim('L18')
def _(): return eq(lambda: pairwise([1, 2, 3]), [(1, 2), (2, 3)])
@claim('L19')
def _(): return forall(lists('L19'), lambda xs: len(pairwise(xs)) == len(xs) - 1)

if __name__ == '__main__': main('lists')
