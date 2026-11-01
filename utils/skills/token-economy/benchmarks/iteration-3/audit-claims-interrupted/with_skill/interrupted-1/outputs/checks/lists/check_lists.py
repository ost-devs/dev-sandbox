import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import lists as M

def ints(r): return gen_list(r, gen_int, 10)
def small(r): return gen_list(r, lambda r: gen_int(r,0,4), 10)

def L03():
    for xs in ([], [1,2]):
        try: M.chunk(xs,0)
        except ValueError: continue
        except Exception as e: return f'chunk({xs},0) raised {type(e).__name__}'
        return f'chunk({xs},0) did not raise'
def L05():
    def p(xs):
        exp=[x for i,x in enumerate(xs) if x not in xs[:i]]
        return M.dedupe(xs)==exp
    return forall('L05', small, p)
def L13():
    r1=forall('L13', lambda r:(ints(r), gen_int(r,-20,20)), lambda xs,k: len(M.rotate(xs,k))==len(xs))
    return r1
def L19():
    return forall('L19', lambda r: gen_list(r,gen_int,6), lambda xs: len(M.pairwise(xs))==len(xs)-1)

C={
'L01': lambda: eq(lambda: M.chunk(list(range(7)),3), [[0,1,2],[3,4,5],[6]]),
'L02': lambda: forall('L02', lambda r:(ints(r), gen_int(r,1,12)), lambda xs,k: M.flatten(M.chunk(xs,k))==xs),
'L03': L03,
'L04': lambda: eq(lambda: M.dedupe([3,1,3,2,1]), [3,1,2]),
'L05': L05,
'L06': lambda: forall('L06', ints, lambda xs: len(M.dedupe(xs))==len(set(xs))),
'L07': lambda: eq(lambda: M.flatten([[1,[2]],[3]]), [1,2,3]),
'L08': lambda: eq(lambda: M.top_n([5,1,4],2), [5,4]),
'L09': lambda: forall('L09', lambda r:(ints(r), gen_int(r,0,12)), lambda xs,k: len(M.top_n(xs,k))==min(k,len(xs))),
'L10': lambda: eq(lambda: M.top_n([3,2,1],-1), []),
'L11': lambda: eq(lambda: M.rotate([1,2,3],1), [2,3,1]),
'L12': lambda: next((f'args={a!r} -> {M.rotate(*a)} vs {M.rotate(a[0],a[1]%len(a[0]))}' for a in [([1,2],2),([1,2],3)] if M.rotate(*a)!=M.rotate(a[0],a[1]%len(a[0]))),None) or ( forall('L12', lambda r:([gen_int(r) for _ in range(r.randint(1,8))], gen_int(r,0,40)), lambda xs,k: M.rotate(xs,k)==M.rotate(xs,k%len(xs)))),
'L13': L13,
'L14': lambda: eq(lambda: M.interleave([1,2,3],[9]), [1,9,2,3]),
'L15': lambda: forall('L15', lambda r:(ints(r),ints(r)), lambda a,b: len(M.interleave(a,b))==2*min(len(a),len(b))),
'L16': lambda: eq(lambda: M.frequencies('abca'), {'a':2,'b':1,'c':1}),
'L17': lambda: forall('L17', ints, lambda xs: sum(M.frequencies(xs).values())==len(xs)),
'L18': lambda: eq(lambda: M.pairwise([1,2,3]), [(1,2),(2,3)]),
'L19': L19,
}
run('lists', C)
