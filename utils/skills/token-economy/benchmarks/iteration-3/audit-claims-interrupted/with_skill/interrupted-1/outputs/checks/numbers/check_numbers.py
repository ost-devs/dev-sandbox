import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import numbers as M

def N01(): return forall('N01', lambda r: (lambda lo: (gen_int(r,-100,100), lo, lo+r.randint(0,30)))(gen_int(r,-100,100)), lambda x,lo,hi: lo <= M.clamp(x,lo,hi) <= hi)
def N02(): return eq(lambda: M.clamp(5,10,0), 0)
def N03(): return eq(lambda: M.mean([]), 0)
def N04(): return eq(lambda: M.mean([1,2]), 1.5)
def N05(): return eq(lambda: M.median([3,1,2]), 2)
def N06(): return eq(lambda: M.median([]), None)
def N07():
    import itertools
    for n in range(1,5):
        for xs in itertools.product(range(-2,3), repeat=n):
            xs=list(xs)
            try:
                if M.median(xs)!=M.median(sorted(xs)): return f'xs={xs}'
            except Exception as e: return f'xs={xs} raised {e}'
    return forall('N07', lambda r: gen_list(r, lambda r: gen_int(r), 9) or [0], lambda xs: M.median(xs)==M.median(sorted(xs)))
def N08(): return eq(lambda: M.round_half(2.5), 3)
def N09(): return eq(lambda: M.round_half(3.5), 4)
def N10(): return eq(lambda: M.percent(1,3), 33.3)
def N11():
    for x in [0,1,-1,2.5]:
        try: got=M.percent(x,0)
        except Exception as e: return f'percent({x}, 0) raised {type(e).__name__}: {e}'
        if not (got==0.0 and type(got) is float): return f'percent({x}, 0) -> {got!r}'
def N12():
    for n in range(0,1001):
        ref = n>=2 and all(n%d for d in range(2,n))
        try: got=M.is_prime(n)
        except Exception as e: return f'is_prime({n}) raised {e}'
        if got!=ref: return f'is_prime({n}) -> {got!r}, expected {ref}'
def N13(): return eq(lambda: M.is_prime(97), True)
def N14(): return eq(lambda: M.is_prime(2), True)
def N15():
    for a in range(-50,51):
        for b in range(-50,51):
            if M.gcd(a,b)!=M.gcd(b,a): return f'a={a}, b={b}: {M.gcd(a,b)} vs {M.gcd(b,a)}'
def N16(): return eq(lambda: M.gcd(12,18), 6)
def N17(): return forall('N17', lambda r: gen_int(r,-1000,1000), lambda a: M.gcd(a,0)==a)
def N18(): return eq(lambda: M.digits_sum(1234), 10)
def N19():
    for n in [0,1,-1,10,-123]:
        try: g=M.digits_sum(n)
        except Exception as e: return f'digits_sum({n}) raised {type(e).__name__}: {e}'
        if type(g) is not int or g<0: return f'digits_sum({n}) -> {g!r}'
run('numbers', {k:v for k,v in globals().items() if k.startswith('N') and k[1:].isdigit()})
