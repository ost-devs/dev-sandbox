import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.money import *

def eq(actual, expected):
    return True if actual == expected else (False, 'got %r, expected %r' % (actual, expected))

@exact
def M01(): return eq(to_cents('12,34'), 1234)
@exact
def M02(): return eq(to_cents('1.234,5'), 123450)
@exact
def M03(): return eq(to_cents('-1,50'), -150)
@exact
def M04(): return eq(to_cents('7'), 700)
@exact
def M05(): return eq(format_brl(123456), 'R$ 1.234,56')
@exact
def M06(): return eq(format_brl(5), 'R$ 0,05')
@exact
def M07(): return eq(format_brl(-150), 'R$ -1,50')
@exact
def M08():
    for c in range(0, 1000001):
        s = format_brl(c)
        if to_cents(s[3:]) != c:
            return False, 'c=%r format_brl=%r to_cents=%r' % (c, s, to_cents(s[3:]))
    return True

def gen_total_k(r):
    return r.choice([r.randint(0, 20), r.randint(0, 10**6), r.randint(0, 10**9)]), r.choice([r.randint(1, 10), r.randint(1, 1000)])

@prop
def M09(r):
    t, k = gen_total_k(r)
    out = split_bill(t, k)
    if sum(out) != t: return 'total=%r k=%r -> %r sum=%r' % (t, k, out, sum(out))
@exact
def M10(): return eq(split_bill(900, 3), [300, 300, 300])
@prop
def M11(r):
    t, k = gen_total_k(r)
    out = installments(t, k)
    if sum(out) != t: return 'total=%r k=%r -> %r' % (t, k, out)
@prop
def M12(r):
    t, k = gen_total_k(r)
    out = installments(t, k)
    if max(out) - min(out) > 1: return 'total=%r k=%r -> %r' % (t, k, out)
@exact
def M13(): return eq(installments(100, 3), [34, 33, 33])
@exact
def M14(): return eq(apply_discount(1000, 10), 900)
@exact
def M15():
    for c in range(0, 1000001):
        if apply_discount(c, 0) != c: return False, 'c=%r -> %r' % (c, apply_discount(c, 0))
    return True
@prop
def M16(r):
    c = r.choice([r.randint(0, 100), r.randint(0, 10**6), 10**6]); p = r.choice([r.randint(0, 100), 0, 100, 1, 99])
    v = apply_discount(c, p)
    if v > c: return 'c=%r p=%r -> %r' % (c, p, v)
@exact
def M17(): return eq(add_tax(100, 0.15), 115)
@exact
def M18():
    for c in range(0, 1000001):
        if add_tax(c, 0) != c: return False, 'c=%r -> %r' % (c, add_tax(c, 0))
    return True
@prop
def M19(r):
    c = r.choice([r.randint(0, 100), r.randint(0, 10**6), 10**6])
    rate = r.choice([r.random(), r.randint(0, 100) / 100, r.random() * 1e-12, 0.0, 1.0, r.randint(0, 20) / 20])
    v = add_tax(c, rate)
    if v < c: return 'c=%r rate=%r -> %r' % (c, rate, v)

run({k: v for k, v in globals().items() if len(k) == 3 and k[0] == 'M' and k[1:].isdigit()})
