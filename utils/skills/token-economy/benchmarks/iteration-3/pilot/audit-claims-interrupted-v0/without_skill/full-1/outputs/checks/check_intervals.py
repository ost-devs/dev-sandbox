from harness import *
from kit.intervals import *


def rand_iv(r, lo=0, hi=20):
    s = r.randint(lo, hi - 1)
    return (s, r.randint(s + 1, hi))


def rand_ivs(cid, n=4000):
    r = rng(cid)
    return [[rand_iv(r) for _ in range(r.randint(1, 7))] for _ in range(n)]


ALL_IV = [(s, e) for s in range(0, 7) for e in range(s + 1, 8)]


@claim('I01')
def _(): return eq('overlaps((0,5),(5,10))', lambda: overlaps((0, 5), (5, 10)), False)
@claim('I02')
def _(): return forall([(a, b) for a in ALL_IV for b in ALL_IV], lambda a, b: overlaps(a, b) == overlaps(b, a))
@claim('I03')
def _(): return eq('merge([(1,3),(2,6),(8,10)])', lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@claim('I04')
def _(): return eq('merge([(1,2),(2,3)])', lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
@claim('I05')
def _():
    def prop(xs):
        m = merge(xs)
        return all(m[i][0] <= m[i + 1][0] and not overlaps(m[i], m[i + 1]) for i in range(len(m) - 1)) or f'merge = {m}'
    return forall(rand_ivs('I05'), prop)
@claim('I06')
def _(): return forall(rand_ivs('I06'), lambda xs: merge(merge(xs)) == merge(xs))
@claim('I07')
def _(): return eq('contains((0,5), 5)', lambda: contains((0, 5), 5), False)
@claim('I08')
def _(): return forall([(a,) for a in ALL_IV], lambda a: contains(a, a[0]) is True)
@claim('I09')
def _(): return eq('intersect((0,5),(3,8))', lambda: intersect((0, 5), (3, 8)), (3, 5))
@claim('I10')
def _(): return eq('intersect((0,2),(5,6))', lambda: intersect((0, 2), (5, 6)), None)
@claim('I11')
def _(): return eq('intersect((0,5),(5,8))', lambda: intersect((0, 5), (5, 8)), None)
@claim('I12')
def _(): return eq('total_covered([(0,5),(3,8)])', lambda: total_covered([(0, 5), (3, 8)]), 8)
@claim('I13')
def _(): return forall(rand_ivs('I13'), lambda xs: total_covered(xs) <= sum(length(i) for i in xs))
@claim('I14')
def _(): return forall([(a, b) for a in ALL_IV for b in ALL_IV if overlaps(a, b)],
                       lambda a, b: length(intersect(a, b)) <= min(length(a), length(b)))
@claim('I15')
def _(): return eq('merge([])', lambda: merge([]), [])
@claim('I16')
def _(): return forall([(a,) for a in ALL_IV], lambda a: overlaps(a, a) is True)
@claim('I17')
def _(): return eq('merge([(5,7),(1,2)])', lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@claim('I18')
def _(): return forall([(a, x) for a in ALL_IV for x in range(-2, 10) if contains(a, x)],
                       lambda a, x: overlaps(a, (x, x + 1)) or f'contains={contains(a, x)}, overlaps(a,({x},{x+1}))=False')
@claim('I19')
def _(): return eq('length((3,1))', lambda: length((3, 1)), 0)

if __name__ == '__main__':
    sys.exit(main())
