import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, rand_str, main
from kit.money import *

def eq(expr_str, got, want):
    if got != want:
        return f"{expr_str} = {got!r}, expected {want!r}"

def ex(cid, s, want):
    def f():
        try:
            return eq(s, eval(s), want)
        except Exception as e:
            return f"{s} raised {type(e).__name__}: {e}"
    claim(cid)(f)

ex("M01", "to_cents('12,34')", 1234)
ex("M02", "to_cents('1.234,5')", 123450)
ex("M03", "to_cents('-1,50')", -150)
ex("M04", "to_cents('7')", 700)
ex("M05", "format_brl(123456)", 'R$ 1.234,56')
ex("M06", "format_brl(5)", 'R$ 0,05')
ex("M07", "format_brl(-150)", 'R$ -1,50')
ex("M10", "split_bill(900, 3)", [300, 300, 300])
ex("M13", "installments(100, 3)", [34, 33, 33])
ex("M14", "apply_discount(1000, 10)", 900)
ex("M17", "add_tax(100, 0.15)", 115)

@claim("M08")
def m08():
    for c in range(0, 1000001):
        try:
            o = to_cents(format_brl(c)[3:])
        except Exception as e:
            return f"to_cents(format_brl({c})[3:]) raised {e}"
        if o != c:
            return f"to_cents(format_brl({c})[3:]) = {o}"

def pairs(cid):
    r = rng(cid)
    ts = [0, 1, 2, 99, 100, 101, 10**9]
    ks = [1, 2, 3, 7, 10, 1000]
    for t in ts:
        for k in ks:
            yield t, k
    for _ in range(3000):
        yield r.randint(0, 10**6), r.randint(1, 50)

@claim("M09")
def m09():
    for t, k in pairs("M09"):
        o = split_bill(t, k)
        if sum(o) != t:
            return f"split_bill({t}, {k}) = {o[:5]}... sum={sum(o)}"

@claim("M11")
def m11():
    for t, k in pairs("M11"):
        o = installments(t, k)
        if sum(o) != t:
            return f"installments({t}, {k}) sum={sum(o)}"

@claim("M12")
def m12():
    for t, k in pairs("M12"):
        o = installments(t, k)
        if max(o) - min(o) > 1:
            return f"installments({t}, {k}) = {o}"

@claim("M15")
def m15():
    for c in range(0, 1000001):
        if apply_discount(c, 0) != c:
            return f"apply_discount({c}, 0) = {apply_discount(c, 0)}"

@claim("M16")
def m16():
    r = rng("M16")
    cs = list(range(0, 300)) + [10**6 - i for i in range(300)] + [r.randint(0, 10**6) for _ in range(3000)]
    for c in cs:
        for p in range(0, 101):
            o = apply_discount(c, p)
            if o > c:
                return f"apply_discount({c}, {p}) = {o}"

@claim("M18")
def m18():
    for c in range(0, 1000001):
        if add_tax(c, 0) != c:
            return f"add_tax({c}, 0) = {add_tax(c, 0)}"

@claim("M19")
def m19():
    r = rng("M19")
    rates = [0, 1, 0.5, 0.1, 0.15, 0.07, 0.3, 1e-9, 1e-17, 0.999999] + [r.random() for _ in range(300)]
    cs = list(range(0, 2000)) + [10**6 - i for i in range(1000)] + [r.randint(0, 10**6) for _ in range(2000)]
    for c in cs:
        for x in rates:
            o = add_tax(c, x)
            if o < c:
                return f"add_tax({c}, {x}) = {o}"

if __name__ == "__main__":
    main()
