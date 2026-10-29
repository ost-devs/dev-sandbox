from common import *
from kit.money import *

def pairs(cid, tmax=2000, kmax=12):
    return [(t, k) for t in range(0, tmax) for k in range(1, kmax)]

@claim('M01')
def _(): return eq(lambda: to_cents('12,34'), 1234)
@claim('M02')
def _(): return eq(lambda: to_cents('1.234,5'), 123450)
@claim('M03')
def _(): return eq(lambda: to_cents('-1,50'), -150)
@claim('M04')
def _(): return eq(lambda: to_cents('7'), 700)
@claim('M05')
def _(): return eq(lambda: format_brl(123456), 'R$ 1.234,56')
@claim('M06')
def _(): return eq(lambda: format_brl(5), 'R$ 0,05')
@claim('M07')
def _(): return eq(lambda: format_brl(-150), 'R$ -1,50')
@claim('M08')
def _(): return forall(range(0, 1_000_001), lambda c: to_cents(format_brl(c)[3:]) == c)
@claim('M09')
def _(): return forall(pairs('M09'), lambda t, k: sum(split_bill(t, k)) == t)
@claim('M10')
def _(): return eq(lambda: split_bill(900, 3), [300, 300, 300])
@claim('M11')
def _(): return forall(pairs('M11'), lambda t, k: sum(installments(t, k)) == t)
@claim('M12')
def _(): return forall(pairs('M12'), lambda t, k: max(installments(t, k)) - min(installments(t, k)) <= 1)
@claim('M13')
def _(): return eq(lambda: installments(100, 3), [34, 33, 33])
@claim('M14')
def _(): return eq(lambda: apply_discount(1000, 10), 900)
@claim('M15')
def _(): return forall(range(0, 1_000_001), lambda c: apply_discount(c, 0) == c)
@claim('M16')
def _(): return forall(((c, p) for c in range(0, 3000) for p in range(0, 101)), lambda c, p: apply_discount(c, p) <= c)
@claim('M17')
def _(): return eq(lambda: add_tax(100, 0.15), 115)
@claim('M18')
def _(): return forall(range(0, 1_000_001), lambda c: add_tax(c, 0) == c)
@claim('M19')
def _():
    r = rng('M19')
    ins = [(2**53 + 1, 0.0)]  # beyond float precision
    ins += [(r.randint(0, 10**6), r.choice([0, 0.05, 0.15, 1e-9, 0.1, 1, 2.5, r.random()])) for _ in range(N)]
    # put the pedestrian range first so a small counterexample is reported if one exists
    small = [i for i in ins if i[0] <= 10**6]
    return forall(small + [i for i in ins if i[0] > 10**6], lambda c, rt: add_tax(c, rt) >= c)

if __name__ == '__main__': main('money')
