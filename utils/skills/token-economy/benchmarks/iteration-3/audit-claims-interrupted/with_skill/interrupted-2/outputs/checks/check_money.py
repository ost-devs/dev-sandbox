import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import money as M

def first(it):
    for x in it:
        if x is not None: return x
    return None

@claim("M01")
def m01(): return eq(M.to_cents('12,34'), 1234)
@claim("M02")
def m02(): return eq(M.to_cents('1.234,5'), 123450)
@claim("M03")
def m03(): return eq(M.to_cents('-1,50'), -150)
@claim("M04")
def m04(): return eq(M.to_cents('7'), 700)
@claim("M05")
def m05(): return eq(M.format_brl(123456), 'R$ 1.234,56')
@claim("M06")
def m06(): return eq(M.format_brl(5), 'R$ 0,05')
@claim("M07")
def m07(): return eq(M.format_brl(-150), 'R$ -1,50')
@claim("M08")
def m08():
    for c in range(0, 1000001):
        g = M.to_cents(M.format_brl(c)[3:])
        if g != c: return f"c={c}: got {g}"
@claim("M09")
def m09():
    for t in list(range(0, 40)) + [100, 900, 1001]:
        for k in range(1, 12):
            s = sum(M.split_bill(t, k))
            if s != t: return f"split_bill({t},{k})={M.split_bill(t,k)} sums to {s}"
@claim("M10")
def m10(): return eq(M.split_bill(900, 3), [300, 300, 300])
@claim("M11")
def m11():
    for t in list(range(0, 40)) + [100, 900, 1001]:
        for k in range(1, 12):
            s = sum(M.installments(t, k))
            if s != t: return f"installments({t},{k}) sums to {s}"
@claim("M12")
def m12():
    for t in list(range(0, 40)) + [100, 900, 1001]:
        for k in range(1, 12):
            l = M.installments(t, k)
            if max(l) - min(l) > 1: return f"installments({t},{k})={l}"
@claim("M13")
def m13(): return eq(M.installments(100, 3), [34, 33, 33])
@claim("M14")
def m14(): return eq(M.apply_discount(1000, 10), 900)
@claim("M15")
def m15():
    for c in range(0, 1000001):
        if M.apply_discount(c, 0) != c: return f"c={c}: got {M.apply_discount(c,0)}"
@claim("M16")
def m16():
    # exhaustive for small c, all p; sampled for large c
    r = rng(16)
    cs = list(range(0, 2001)) + [r.randint(0, 1000000) for _ in range(20000)] + [1000000]
    for c in cs:
        for p in ([r.randint(0, 100)] if c > 2000 else range(0, 101)):
            g = M.apply_discount(c, p)
            if g > c: return f"apply_discount({c},{p})={g}"
@claim("M17")
def m17(): return eq(M.add_tax(100, 0.15), 115)
@claim("M18")
def m18():
    for c in range(0, 1000001):
        if M.add_tax(c, 0) != c: return f"c={c}: got {M.add_tax(c,0)}"
@claim("M19")
def m19():
    # rate r in [0,1]; float rates (also 2-decimal rates) and integer cents
    r = rng(19)
    for c in range(0, 3001):
        for k in range(0, 101):
            rate = k / 100
            g = M.add_tax(c, rate)
            if g < c: return f"add_tax({c},{rate!r})={g}"
    for _ in range(50000):
        c = r.randint(0, 1000000); rate = r.random()
        g = M.add_tax(c, rate)
        if g < c: return f"add_tax({c},{rate!r})={g}"

if __name__ == "__main__":
    main("money")
