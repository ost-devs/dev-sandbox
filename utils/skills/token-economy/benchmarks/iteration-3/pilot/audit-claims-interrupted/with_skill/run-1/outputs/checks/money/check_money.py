import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit import money as m

def eq(expr_s, got, want):
    return True if got == want else (False, f"{expr_s} -> {got!r} (esperado {want!r})")

@claim('M01')
def m01(): return eq("to_cents('12,34')", m.to_cents('12,34'), 1234)
@claim('M02')
def m02(): return eq("to_cents('1.234,5')", m.to_cents('1.234,5'), 123450)
@claim('M03')
def m03(): return eq("to_cents('-1,50')", m.to_cents('-1,50'), -150)
@claim('M04')
def m04(): return eq("to_cents('7')", m.to_cents('7'), 700)
@claim('M05')
def m05(): return eq("format_brl(123456)", m.format_brl(123456), 'R$ 1.234,56')
@claim('M06')
def m06(): return eq("format_brl(5)", m.format_brl(5), 'R$ 0,05')
@claim('M07')
def m07(): return eq("format_brl(-150)", m.format_brl(-150), 'R$ -1,50')

@claim('M08')
def m08():
    for c in range(0, 1000001):
        o = m.to_cents(m.format_brl(c)[3:])
        if o != c: return (False, f"c={c} -> {o}")
    return True

@claim('M09')
def m09():
    r = rng('M09')
    cases = [(0,1),(1,2),(0,5),(5,3),(10**9,7)] + [(r.randint(0,10**6), r.randint(1,50)) for _ in range(2000)]
    for t, k in cases:
        s = sum(m.split_bill(t, k))
        if s != t: return (False, f"split_bill({t},{k}) sum={s}")
    return True

@claim('M10')
def m10(): return eq("split_bill(900,3)", m.split_bill(900, 3), [300]*3)

def _cases(cid):
    r = rng(cid)
    return [(0,1),(0,7),(1,2),(100,3),(5,10)] + [(r.randint(0,10**6), r.randint(1,60)) for _ in range(2500)]

@claim('M11')
def m11():
    for t, k in _cases('M11'):
        o = m.installments(t, k)
        if sum(o) != t: return (False, f"installments({t},{k}) -> sum {sum(o)}")
    return True

@claim('M12')
def m12():
    for t, k in _cases('M12'):
        o = m.installments(t, k)
        if max(o) - min(o) > 1: return (False, f"installments({t},{k}) -> {o}")
    return True

@claim('M13')
def m13(): return eq("installments(100,3)", m.installments(100, 3), [34,33,33])
@claim('M14')
def m14(): return eq("apply_discount(1000,10)", m.apply_discount(1000, 10), 900)

@claim('M15')
def m15():
    for c in range(0, 1000001):
        o = m.apply_discount(c, 0)
        if o != c: return (False, f"apply_discount({c},0) -> {o}")
    return True

@claim('M16')
def m16():
    r = rng('M16')
    cs = [0,1,2,999999,1000000] + [r.randint(0,10**6) for _ in range(3000)]
    for c in cs:
        ps = range(101) if c in (0,1,2,999999,1000000) or r.random()<0.1 else [0,1,50,99,100,r.randint(0,100),r.randint(0,100)]
        for p in ps:
            o = m.apply_discount(c, p)
            if o > c: return (False, f"apply_discount({c},{p}) -> {o}")
    return True

@claim('M17')
def m17(): return eq("add_tax(100,0.15)", m.add_tax(100, 0.15), 115)

@claim('M18')
def m18():
    for c in range(0, 1000001):
        o = m.add_tax(c, 0)
        if o != c: return (False, f"add_tax({c},0) -> {o}")
    return True

@claim('M19')
def m19():
    r = rng('M19')
    rs = [0, 0.0, 1, 1.0, 0.5, 0.15, 1e-12, 0.1, 0.07, 0.3, 0.9999999]
    for _ in range(3000):
        c = r.randint(0, 10**6); rate = r.choice(rs + [r.random(), round(r.random(), 2)])
        o = m.add_tax(c, rate)
        if o < c: return (False, f"add_tax({c},{rate}) -> {o}")
    for c in range(0, 1000001, 7):
        for rate in (0.01, 0.1, 0.15, 1):
            o = m.add_tax(c, rate)
            if o < c: return (False, f"add_tax({c},{rate}) -> {o}")
    return True

if __name__ == '__main__':
    run(__file__)
