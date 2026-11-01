import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker
from kit.money import *

c = Checker('money')
R = range(0, 1000001)
def pairs():
    r = random.Random(1909)
    out = [(t, k) for t in (0, 1, 2, 5, 10, 100, 899, 900) for k in (1, 2, 3, 7)]
    return out + [(r.randint(0, 10**6), r.randint(1, 50)) for _ in range(2000)]

@c.claim('M01')
def _(): return c.eq(to_cents('12,34'), 1234)
@c.claim('M02')
def _(): return c.eq(to_cents('1.234,5'), 123450)
@c.claim('M03')
def _(): return c.eq(to_cents('-1,50'), -150)
@c.claim('M04')
def _(): return c.eq(to_cents('7'), 700)
@c.claim('M05')
def _(): return c.eq(format_brl(123456), 'R$ 1.234,56')
@c.claim('M06')
def _(): return c.eq(format_brl(5), 'R$ 0,05')
@c.claim('M07')
def _(): return c.eq(format_brl(-150), 'R$ -1,50')
@c.claim('M08')
def _(): return c.forall(R, lambda x: to_cents(format_brl(x)[3:]) == x)
@c.claim('M09')
def _(): return c.forall(pairs(), lambda p: sum(split_bill(*p)) == p[0])
@c.claim('M10')
def _(): return c.eq(split_bill(900, 3), [300, 300, 300])
@c.claim('M11')
def _(): return c.forall(pairs(), lambda p: sum(installments(*p)) == p[0])
@c.claim('M12')
def _(): return c.forall(pairs(), lambda p: max(installments(*p)) - min(installments(*p)) <= 1)
@c.claim('M13')
def _(): return c.eq(installments(100, 3), [34, 33, 33])
@c.claim('M14')
def _(): return c.eq(apply_discount(1000, 10), 900)
@c.claim('M15')
def _(): return c.forall(R, lambda x: apply_discount(x, 0) == x)
@c.claim('M16')
def _():
    ps = list(range(0, 101))
    cs = list(range(0, 300)) + [random.Random(1916).randint(0, 10**6) for _ in range(3000)] + [10**6, 999999]
    return c.forall([(x, p) for x in cs for p in ps], lambda a: apply_discount(*a) <= a[0])
@c.claim('M17')
def _(): return c.eq(add_tax(100, 0.15), 115)
@c.claim('M18')
def _(): return c.forall(R, lambda x: add_tax(x, 0) == x)
@c.claim('M19')
def _():
    rs = [0, 1, 0.1, 0.15, 0.5, 0.99, 1e-9] + [random.Random(1919).random() for _ in range(5)]
    cs = list(range(0, 2000)) + [random.Random(1920).randint(0, 10**6) for _ in range(3000)] + [10**6]
    return c.forall([(x, r) for x in cs for r in rs], lambda a: add_tax(*a) >= a[0])

c.main()
