import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.intervals import *

def iv(r, strict=True):
    a = rand_int(r, -10, 10); b = rand_int(r, -10, 10)
    if strict:
        while a == b: b = rand_int(r, -10, 10)
        return (min(a, b), max(a, b))
    return (a, b)
def ivs(r):
    return [iv(r) for _ in range(r.randint(1, 8))]

def eq(f, exp):
    got = f()
    return True if got == exp else (False, 'got %r' % (got,))

@exact
def I01(): return eq(lambda: overlaps((0, 5), (5, 10)), False)
@prop
def I02(r):
    a, b = iv(r, r.random() < .5), iv(r, r.random() < .5)
    if overlaps(a, b) != overlaps(b, a): return 'a=%r b=%r' % (a, b)
@exact
def I03(): return eq(lambda: merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)])
@exact
def I04(): return eq(lambda: merge([(1, 2), (2, 3)]), [(1, 3)])
@prop
def I05(r):
    xs = ivs(r); m = merge(xs)
    for i in range(len(m) - 1):
        if not (m[i][0] <= m[i+1][0]) or overlaps(m[i], m[i+1]):
            return 'xs=%r merge=%r' % (xs, m)
@prop
def I06(r):
    xs = ivs(r); m = merge(xs)
    if merge(m) != m: return 'xs=%r merge=%r merge2=%r' % (xs, m, merge(m))
@exact
def I07(): return eq(lambda: contains((0, 5), 5), False)
@prop
def I08(r):
    a = iv(r)
    if contains(a, a[0]) is not True: return 'a=%r' % (a,)
@exact
def I09(): return eq(lambda: intersect((0, 5), (3, 8)), (3, 5))
@exact
def I10(): return eq(lambda: intersect((0, 2), (5, 6)), None)
@exact
def I11(): return eq(lambda: intersect((0, 5), (5, 8)), None)
@exact
def I12(): return eq(lambda: total_covered([(0, 5), (3, 8)]), 8)
@prop
def I13(r):
    xs = ivs(r); t = total_covered(xs); s = sum(length(i) for i in xs)
    if t > s: return 'xs=%r total=%r sum=%r' % (xs, t, s)
@prop
def I14(r):
    a, b = iv(r), iv(r)
    if overlaps(a, b):
        i = intersect(a, b)
        if length(i) > min(length(a), length(b)): return 'a=%r b=%r intersect=%r' % (a, b, i)
@exact
def I15(): return eq(lambda: merge([]), [])
@prop
def I16(r):
    a = iv(r)
    if overlaps(a, a) is not True: return 'a=%r' % (a,)
@exact
def I17(): return eq(lambda: merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)])
@prop
def I18(r):
    a = iv(r); x = rand_int(r, -12, 12)
    if contains(a, x) and not overlaps(a, (x, x + 1)):
        return 'a=%r x=%r contains=True overlaps(a,(x,x+1))=False' % (a, x)
@exact
def I19(): return eq(lambda: length((3, 1)), 0)

run({k: v for k, v in globals().items() if k[:1] == 'I' and k[1:].isdigit()})
