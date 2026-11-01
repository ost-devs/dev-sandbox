import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import money as M

def exh(rangeargs, pred):
    for c in range(*rangeargs):
        try:
            if not pred(c): return f'c={c}'
        except Exception as e:
            return f'c={c} raised {type(e).__name__}: {e}'
def m08(): return exh((0,1000001), lambda c: M.to_cents(M.format_brl(c)[3:])==c)
gen_tk = lambda r: (r.choice([0,1,2,5,99,100,101,r.randint(0,10**6),r.randint(0,50)]), r.choice([1,2,3,7,r.randint(1,40),r.randint(1,1000)]))
def m09():
    return forall('M09', gen_tk, lambda t,k: sum(M.split_bill(t,k))==t) 
def m11(): return forall('M11', gen_tk, lambda t,k: sum(M.installments(t,k))==t)
def m12(): return forall('M12', gen_tk, lambda t,k: max(M.installments(t,k))-min(M.installments(t,k))<=1)
def m15(): return exh((0,1000001), lambda c: M.apply_discount(c,0)==c)
def m16():
    for c in list(range(0,3000))+[10**6-i for i in range(50)]:
        for p in range(101):
            if M.apply_discount(c,p)>c: return f'c={c}, p={p} -> {M.apply_discount(c,p)}'
    return forall('M16', lambda r:(r.randint(0,10**6),r.randint(0,100)), lambda c,p: M.apply_discount(c,p)<=c)
def m18(): return exh((0,1000001), lambda c: M.add_tax(c,0)==c)
def m19():
    for c in range(0,100001):
        for r in (0,0.1,0.15,1):
            if M.add_tax(c,r)<c: return f'c={c}, r={r} -> {M.add_tax(c,r)}'
    return forall('M19', lambda r:(r.randint(0,10**6),r.choice([r.random(),r.randint(0,1),round(r.random(),2)])), lambda c,r: M.add_tax(c,r)>=c)
run('money', {
 'M01': lambda: eq(lambda: M.to_cents('12,34'),1234),
 'M02': lambda: eq(lambda: M.to_cents('1.234,5'),123450),
 'M03': lambda: eq(lambda: M.to_cents('-1,50'),-150),
 'M04': lambda: eq(lambda: M.to_cents('7'),700),
 'M05': lambda: eq(lambda: M.format_brl(123456),'R$ 1.234,56'),
 'M06': lambda: eq(lambda: M.format_brl(5),'R$ 0,05'),
 'M07': lambda: eq(lambda: M.format_brl(-150),'R$ -1,50'),
 'M08': m08, 'M09': m09,
 'M10': lambda: eq(lambda: M.split_bill(900,3),[300,300,300]),
 'M11': m11, 'M12': m12,
 'M13': lambda: eq(lambda: M.installments(100,3),[34,33,33]),
 'M14': lambda: eq(lambda: M.apply_discount(1000,10),900),
 'M15': m15, 'M16': m16,
 'M17': lambda: eq(lambda: M.add_tax(100,0.15),115),
 'M18': m18, 'M19': m19})
