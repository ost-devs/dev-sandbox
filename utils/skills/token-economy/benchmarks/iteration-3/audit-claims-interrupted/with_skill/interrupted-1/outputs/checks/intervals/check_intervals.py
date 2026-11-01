import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import intervals as M

def iv(r, lo=-20, hi=20):
    a = r.randint(lo, hi); b = r.randint(lo, hi)
    while a == b: b = r.randint(lo, hi)
    return (min(a, b), max(a, b))
def anyiv(r):
    return (r.randint(-20, 20), r.randint(-20, 20))
def ivs(r):
    return [iv(r) for _ in range(r.randint(1, 8))]

def I02():
    return forall('I02', lambda r: (anyiv(r), anyiv(r)), lambda a, b: M.overlaps(a, b) == M.overlaps(b, a))
def I05(): 
    def p(xs):
        m = M.merge(xs)
        return all(m[i][0] <= m[i+1][0] and not M.overlaps(m[i], m[i+1]) and m[i][1] < m[i+1][0] for i in range(len(m)-1))
    return forall('I05', lambda r: (ivs(r),), p)
def I06(): return forall('I06', lambda r: (ivs(r),), lambda xs: M.merge(M.merge(xs)) == M.merge(xs))
def I08(): return forall('I08', lambda r: (iv(r),), lambda a: M.contains(a, a[0]) is True)
def I13(): return forall('I13', lambda r: (ivs(r),), lambda xs: M.total_covered(xs) <= sum(M.length(i) for i in xs))
def I14():
    def g(r):
        while True:
            a, b = iv(r), iv(r)
            if M.overlaps(a, b): return (a, b)
    return forall('I14', g, lambda a, b: M.length(M.intersect(a, b)) <= min(M.length(a), M.length(b)))
def I16(): return forall('I16', lambda r: (iv(r),), lambda a: M.overlaps(a, a) is True)
def I18():
    return forall('I18', lambda r: (iv(r), r.randint(-25, 25)), lambda a, x: (not M.contains(a, x)) or M.overlaps(a, (x, x+1)))

run('intervals', {
 'I01': lambda: eq(lambda: M.overlaps((0,5),(5,10)), False),
 'I02': I02,
 'I03': lambda: eq(lambda: M.merge([(1,3),(2,6),(8,10)]), [(1,6),(8,10)]),
 'I04': lambda: eq(lambda: M.merge([(1,2),(2,3)]), [(1,3)]),
 'I05': I05, 'I06': I06,
 'I07': lambda: eq(lambda: M.contains((0,5),5), False),
 'I08': I08,
 'I09': lambda: eq(lambda: M.intersect((0,5),(3,8)), (3,5)),
 'I10': lambda: eq(lambda: M.intersect((0,2),(5,6)), None),
 'I11': lambda: eq(lambda: M.intersect((0,5),(5,8)), None),
 'I12': lambda: eq(lambda: M.total_covered([(0,5),(3,8)]), 8),
 'I13': I13, 'I14': I14,
 'I15': lambda: eq(lambda: M.merge([]), []),
 'I16': I16,
 'I17': lambda: eq(lambda: M.merge([(5,7),(1,2)]), [(1,2),(5,7)]),
 'I18': I18,
 'I19': lambda: eq(lambda: M.length((3,1)), 0),
})
