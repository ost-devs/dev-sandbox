from harness import *
from kit.money import *


@claim('M01')
def _(): return eq("to_cents('12,34')", lambda: to_cents('12,34'), 1234)
@claim('M02')
def _(): return eq("to_cents('1.234,5')", lambda: to_cents('1.234,5'), 123450)
@claim('M03')
def _(): return eq("to_cents('-1,50')", lambda: to_cents('-1,50'), -150)
@claim('M04')
def _(): return eq("to_cents('7')", lambda: to_cents('7'), 700)
@claim('M05')
def _(): return eq('format_brl(123456)', lambda: format_brl(123456), 'R$ 1.234,56')
@claim('M06')
def _(): return eq('format_brl(5)', lambda: format_brl(5), 'R$ 0,05')
@claim('M07')
def _(): return eq('format_brl(-150)', lambda: format_brl(-150), 'R$ -1,50')
@claim('M08')
def _(): return forall(range(0, 1000001), lambda c: to_cents(format_brl(c)[3:]) == c)
def _totals(cid):
    r = rng(cid)
    return [(t, k) for t in range(0, 61) for k in range(1, 13)] + [(r.randint(0, 10**7), r.randint(1, 50)) for _ in range(3000)]
@claim('M09')
def _(): return forall(_totals('M09'), lambda t, k: sum(split_bill(t, k)) == t or f'split_bill = {split_bill(t, k)}')
@claim('M10')
def _(): return eq('split_bill(900, 3)', lambda: split_bill(900, 3), [300, 300, 300])
@claim('M11')
def _(): return forall(_totals('M11'), lambda t, k: sum(installments(t, k)) == t)
@claim('M12')
def _(): return forall(_totals('M12'), lambda t, k: max(installments(t, k)) - min(installments(t, k)) <= 1)
@claim('M13')
def _(): return eq('installments(100, 3)', lambda: installments(100, 3), [34, 33, 33])
@claim('M14')
def _(): return eq('apply_discount(1000, 10)', lambda: apply_discount(1000, 10), 900)
@claim('M15')
def _(): return forall(range(0, 1000001), lambda c: apply_discount(c, 0) == c)
@claim('M16')
def _():
    r = rng('M16')
    cases = [(c, p) for c in range(0, 1501) for p in range(0, 101)]
    cases += [(r.randint(0, 10**9), r.randint(0, 100)) for _ in range(20000)]
    return forall(cases, lambda c, p: apply_discount(c, p) <= c)
@claim('M17')
def _(): return eq('add_tax(100, 0.15)', lambda: add_tax(100, 0.15), 115)
@claim('M18')
def _(): return forall(range(0, 1000001), lambda c: add_tax(c, 0) == c)
@claim('M19')
def _():
    # taxas finitas (r = inf não tem resultado inteiro e fica fora do domínio razoável)
    r = rng('M19')
    cases = [(c, x / 100) for c in range(0, 401) for x in range(0, 101)]
    cases += [(r.randint(0, 10**9), r.random() * r.choice([0.01, 1, 10, 1000])) for _ in range(20000)]
    return forall(cases, lambda c, rate: add_tax(c, rate) >= c)

if __name__ == '__main__':
    sys.exit(main())
