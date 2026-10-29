from harness import *
from kit.lists import *


def rand_lists(cid, n=3000, maxlen=9, lo=-5, hi=5):
    r = rng(cid)
    return [[r.randint(lo, hi) for _ in range(r.randint(0, maxlen))] for _ in range(n)]


@claim('L01')
def _(): return eq('chunk(range(7), 3)', lambda: chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]])
@claim('L02')
def _(): return forall([(xs, k) for xs in rand_lists('L02', 600) for k in range(1, 12)], lambda xs, k: flatten(chunk(xs, k)) == xs)
@claim('L03')
def _(): return raises('chunk([1,2,3], 0)', lambda: chunk([1, 2, 3], 0), ValueError) or raises('chunk([], 0)', lambda: chunk([], 0), ValueError)
@claim('L04')
def _(): return eq('dedupe([3,1,3,2,1])', lambda: dedupe([3, 1, 3, 2, 1]), [3, 1, 2])
@claim('L05')
def _():
    def ref(xs):
        seen, out = set(), []
        for x in xs:
            if x not in seen:
                seen.add(x); out.append(x)
        return out
    return forall(rand_lists('L05'), lambda xs: dedupe(xs) == ref(xs))
@claim('L06')
def _(): return forall(rand_lists('L06'), lambda xs: len(dedupe(xs)) == len(set(xs)))
@claim('L07')
def _(): return eq('flatten([[1,[2]],[3]])', lambda: flatten([[1, [2]], [3]]), [1, 2, 3])
@claim('L08')
def _(): return eq('top_n([5,1,4], 2)', lambda: top_n([5, 1, 4], 2), [5, 4])
@claim('L09')
def _(): return forall([(xs, k) for xs in rand_lists('L09', 600) for k in range(0, 13)], lambda xs, k: len(top_n(xs, k)) == min(k, len(xs)))
@claim('L10')
def _(): return eq('top_n([3,2,1], -1)', lambda: top_n([3, 2, 1], -1), [])
@claim('L11')
def _(): return eq('rotate([1,2,3], 1)', lambda: rotate([1, 2, 3], 1), [2, 3, 1])
@claim('L12')
def _():
    return forall([(xs, k) for xs in rand_lists('L12', 300) if xs for k in range(0, 15)],
                  lambda xs, k: rotate(xs, k) == rotate(xs, k % len(xs)) or f'rotate(xs,k)={rotate(xs, k)}, rotate(xs,{k % len(xs)})={rotate(xs, k % len(xs))}')
@claim('L13')
def _(): return forall([(xs, k) for xs in rand_lists('L13', 500) for k in range(-15, 16)], lambda xs, k: len(rotate(xs, k)) == len(xs))
@claim('L14')
def _(): return eq('interleave([1,2,3],[9])', lambda: interleave([1, 2, 3], [9]), [1, 9, 2, 3])
@claim('L15')
def _():
    ls = rand_lists('L15', 150)
    return forall([(a, b) for a in ls for b in ls[:20]], lambda a, b: len(interleave(a, b)) == 2 * min(len(a), len(b)))
@claim('L16')
def _(): return eq("frequencies('abca')", lambda: frequencies('abca'), {'a': 2, 'b': 1, 'c': 1})
@claim('L17')
def _(): return forall(rand_lists('L17'), lambda xs: sum(frequencies(xs).values()) == len(xs))
@claim('L18')
def _(): return eq('pairwise([1,2,3])', lambda: pairwise([1, 2, 3]), [(1, 2), (2, 3)])
@claim('L19')
def _(): return forall([[], [1], [1, 2]] + rand_lists('L19', 500), lambda xs: len(pairwise(xs)) == len(xs) - 1 or f'len(pairwise)={len(pairwise(xs))}, len(xs)-1={len(xs)-1}')

if __name__ == '__main__':
    sys.exit(main())
