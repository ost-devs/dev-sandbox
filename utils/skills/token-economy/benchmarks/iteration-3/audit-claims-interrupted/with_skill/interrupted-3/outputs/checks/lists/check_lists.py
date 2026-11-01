import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker, rand_lists, rand_ints
from kit.lists import *
c = Checker('lists')
LS = rand_lists(seed=1001, n=1000)
KS = [0, 1, 2, 3, 5, 10, -1, -3]

def pairs(ks):
    return [(xs, k) for xs in LS for k in ks]

@c.claim('L01')
def _(): return c.eq(chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]])
@c.claim('L02')
def _(): return c.forall(pairs([1,2,3,5,10]), lambda p: flatten(chunk(*p)) == p[0])
@c.claim('L03')
def _():
    for xs in LS[:50]:
        try: chunk(xs, 0)
        except ValueError: continue
        except Exception as e: return c.fail(f'chunk({xs!r}, 0) raised {type(e).__name__}')
        return c.fail(f'chunk({xs!r}, 0) did not raise')
    return c.ok()
@c.claim('L04')
def _(): return c.eq(dedupe([3,1,3,2,1]), [3,1,2])
def first_occ(xs):
    out = []
    for x in xs:
        if x not in out: out.append(x)
    return out
@c.claim('L05')
def _(): return c.forall(LS, lambda xs: dedupe(xs) == first_occ(xs))
@c.claim('L06')
def _(): return c.forall(LS, lambda xs: len(dedupe(xs)) == len(set(xs)))
@c.claim('L07')
def _(): return c.eq(flatten([[1,[2]],[3]]), [1,2,3])
@c.claim('L08')
def _(): return c.eq(top_n([5,1,4], 2), [5,4])
@c.claim('L09')
def _(): return c.forall(pairs([0,1,2,3,5,10]), lambda p: len(top_n(*p)) == min(p[1], len(p[0])))
@c.claim('L10')
def _(): return c.eq(top_n([3,2,1], -1), [])
@c.claim('L11')
def _(): return c.eq(rotate([1,2,3], 1), [2,3,1])
@c.claim('L12')
def _(): return c.forall([(xs,k) for xs in LS if xs for k in range(0,12)], lambda p: rotate(*p) == rotate(p[0], p[1] % len(p[0])))
@c.claim('L13')
def _(): return c.forall(pairs(KS), lambda p: len(rotate(*p)) == len(p[0]))
@c.claim('L14')
def _(): return c.eq(interleave([1,2,3],[9]), [1,9,2,3])
@c.claim('L15')
def _(): return c.forall([(a,b) for a in LS[:100] for b in LS[:100]], lambda p: len(interleave(*p)) == 2*min(len(p[0]),len(p[1])))
@c.claim('L16')
def _(): return c.eq(frequencies('abca'), {'a':2,'b':1,'c':1})
@c.claim('L17')
def _(): return c.forall(LS, lambda xs: sum(frequencies(xs).values()) == len(xs))
@c.claim('L18')
def _(): return c.eq(pairwise([1,2,3]), [(1,2),(2,3)])
@c.claim('L19')
def _(): return c.forall(LS, lambda xs: len(pairwise(xs)) == len(xs)-1)
c.main()
