from common import *
from kit.intervals import *

def ivs(cid, n=N, v=8):
    r = rng(cid)
    out = []
    for _ in range(n):
        a = r.randint(-v, v); out.append((a, a + r.randint(0, v)))
    return out
def lists(cid, n=5000):
    r = rng(cid); iv = ivs(cid + 'x', n * 5)
    return [tuple([iv[i * 5 + j] for j in range(r.randint(1, 5))]) for i in range(n)]
def strict(cid, n=N): return [i for i in ivs(cid, n) if i[0] < i[1]]
def ok_merge(m):
    return all(m[i][0] <= m[i][1] for i in range(len(m))) and all(m[i][1] < m[i + 1][0] for i in range(len(m) - 1))

@claim('I01')
def _(): return eq(lambda: overlaps((0, 5), (5, 10)), False)
@claim('I02')
def _(): return forall(zip(ivs('I02a'), ivs('I02b')), lambda a, b: overlaps(a, b) == overlaps(b, a))
@claim('I03')
def _(): return eq(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@claim('I04')
def _(): return eq(lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
@claim('I05')
def _(): return forall([(x,) for x in lists('I05')], lambda xs: ok_merge(merge(list(xs))))
@claim('I06')
def _(): return forall([(x,) for x in lists('I06')], lambda xs: merge(merge(list(xs))) == merge(list(xs)))
@claim('I07')
def _(): return eq(lambda: contains((0, 5), 5), False)
@claim('I08')
def _(): return forall([(x,) for x in strict('I08')], lambda a: contains(a, a[0]) is True)
@claim('I09')
def _(): return eq(lambda: intersect((0, 5), (3, 8)), (3, 5))
@claim('I10')
def _(): return eq(lambda: intersect((0, 2), (5, 6)), None)
@claim('I11')
def _(): return eq(lambda: intersect((0, 5), (5, 8)), None)
@claim('I12')
def _(): return eq(lambda: total_covered([(0, 5), (3, 8)]), 8)
@claim('I13')
def _():
    r = rng('I13'); s = strict('I13', 20000)
    ins = [tuple(s[i * 4 + j] for j in range(r.randint(1, 4))) for i in range(len(s) // 4)]
    return forall([(x,) for x in ins], lambda xs: total_covered(list(xs)) <= sum(length(i) for i in xs))
@claim('I14')
def _(): return forall([(a, b) for a, b in zip(ivs('I14a'), ivs('I14b')) if overlaps(a, b)], lambda a, b: length(intersect(a, b)) <= min(length(a), length(b)))
@claim('I15')
def _(): return eq(lambda: merge([]), [])
@claim('I16')
def _(): return forall([(x,) for x in strict('I16')], lambda a: overlaps(a, a) is True)
@claim('I17')
def _(): return eq(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@claim('I18')
def _(): return forall(((a, x) for a in ivs('I18', 3000) for x in range(-17, 18)), lambda a, x: (not contains(a, x)) or overlaps(a, (x, x + 1)))
@claim('I19')
def _(): return eq(lambda: length((3, 1)), 0)

if __name__ == '__main__': main('intervals')
