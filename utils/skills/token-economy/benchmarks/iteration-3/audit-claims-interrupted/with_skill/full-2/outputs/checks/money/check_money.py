import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.money import *

def eq(a, b):
    if a != b: raise Counter(f"actual={a!r} expected={b!r}")

@claim("M01")
def m01(): eq(to_cents('12,34'), 1234)
@claim("M02")
def m02(): eq(to_cents('1.234,5'), 123450)
@claim("M03")
def m03(): eq(to_cents('-1,50'), -150)
@claim("M04")
def m04(): eq(to_cents('7'), 700)
@claim("M05")
def m05(): eq(format_brl(123456), 'R$ 1.234,56')
@claim("M06")
def m06(): eq(format_brl(5), 'R$ 0,05')
@claim("M07")
def m07(): eq(format_brl(-150), 'R$ -1,50')
@claim("M08")
def m08():
    for c in range(0, 1000001):
        if to_cents(format_brl(c)[3:]) != c:
            raise Counter(f"c={c} format={format_brl(c)!r} back={to_cents(format_brl(c)[3:])}")
@claim("M09")
def m09():
    forall("M09", lambda r: (r.choice([0,1,5,100,r.randint(0,10**6)]), r.choice([1,2,3,7,r.randint(1,50)])),
           lambda t,k: sum(split_bill(t,k)) == t)
@claim("M10")
def m10(): eq(split_bill(900,3), [300,300,300])
@claim("M11")
def m11():
    forall("M11", lambda r: (r.choice([0,1,5,100,r.randint(0,10**6)]), r.choice([1,2,3,7,r.randint(1,50)])),
           lambda t,k: sum(installments(t,k)) == t)
@claim("M12")
def m12():
    forall("M12", lambda r: (r.choice([0,1,5,100,r.randint(0,10**6)]), r.choice([1,2,3,7,r.randint(1,50)])),
           lambda t,k: max(installments(t,k)) - min(installments(t,k)) <= 1)
@claim("M13")
def m13(): eq(installments(100,3), [34,33,33])
@claim("M14")
def m14(): eq(apply_discount(1000,10), 900)
@claim("M15")
def m15():
    for c in range(0, 1000001):
        if apply_discount(c,0) != c: raise Counter(f"c={c} actual={apply_discount(c,0)!r}")
@claim("M16")
def m16():
    for c in range(0, 3001):
        for p in range(101):
            if apply_discount(c,p) > c: raise Counter(f"c={c} p={p} actual={apply_discount(c,p)}")
    forall("M16", lambda r: (r.randint(0,10**6), r.randint(0,100)), lambda c,p: apply_discount(c,p) <= c)
@claim("M17")
def m17(): eq(add_tax(100,0.15), 115)
@claim("M18")
def m18():
    for c in range(0, 1000001):
        if add_tax(c,0) != c: raise Counter(f"c={c} actual={add_tax(c,0)!r}")
@claim("M19")
def m19():
    rates = [i/100 for i in range(101)] + [i/1000 for i in range(1001)] + [0.1,0.15,0.07,0.29]
    for c in range(0, 2001):
        for r_ in rates:
            if add_tax(c,r_) < c: raise Counter(f"c={c} r={r_} actual={add_tax(c,r_)}")
    forall("M19", lambda r: (r.randint(0,10**6), r.random()), lambda c,x: add_tax(c,x) >= c)

if __name__=='__main__': main('money')
