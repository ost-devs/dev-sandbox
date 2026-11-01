import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import Results, rng
from kit.money import *

R = Results("money")
N = 1_000_000

def eq(expr_fn):
    def f():
        got = expr_fn()
        return got[0] == got[1], got[0]
    return f

R.check("M01", eq(lambda: (to_cents('12,34'), 1234)))
R.check("M02", eq(lambda: (to_cents('1.234,5'), 123450)))
R.check("M03", eq(lambda: (to_cents('-1,50'), -150)))
R.check("M04", eq(lambda: (to_cents('7'), 700)))
R.check("M05", eq(lambda: (format_brl(123456), 'R$ 1.234,56')))
R.check("M06", eq(lambda: (format_brl(5), 'R$ 0,05')))
R.check("M07", eq(lambda: (format_brl(-150), 'R$ -1,50')))

def m08():
    for c in range(0, N + 1):
        if to_cents(format_brl(c)[3:]) != c:
            return False, c
    return True, None
R.check("M08", m08)

def totals_ks():
    r = rng()
    for t in range(0, 60):
        for k in range(1, 15):
            yield t, k
    for _ in range(3000):
        yield r.randint(0, 10**9), r.randint(1, 1000)

def m09():
    best = None
    for t, k in totals_ks():
        if sum(split_bill(t, k)) != t:
            if best is None or (t + k) < (best[0] + best[1]):
                best = (t, k)
    return (best is None), (None if best is None else {"total": best[0], "k": best[1], "got": split_bill(*best)})
R.check("M09", m09)
R.check("M10", eq(lambda: (split_bill(900, 3), [300, 300, 300])))

def m11():
    for t, k in totals_ks():
        if sum(installments(t, k)) != t:
            return False, (t, k)
    return True, None
R.check("M11", m11)

def m12():
    for t, k in totals_ks():
        l = installments(t, k)
        if max(l) - min(l) > 1:
            return False, (t, k, l)
    return True, None
R.check("M12", m12)
R.check("M13", eq(lambda: (installments(100, 3), [34, 33, 33])))
R.check("M14", eq(lambda: (apply_discount(1000, 10), 900)))

def m15():
    for c in range(0, N + 1):
        if apply_discount(c, 0) != c:
            return False, c
    return True, None
R.check("M15", m15)

def m16():
    for p in range(0, 101):
        for c in list(range(0, 400)) + list(range(400, N + 1, 997)) + [N - 1, N]:
            if apply_discount(c, p) > c:
                return False, (c, p)
    r = rng()
    for _ in range(300000):
        c, p = r.randint(0, N), r.randint(0, 100)
        if apply_discount(c, p) > c:
            return False, (c, p)
    for p in (0, 1, 50, 99, 100):
        for c in range(0, N + 1):
            if apply_discount(c, p) > c:
                return False, (c, p)
    return True, None
R.check("M16", m16)
R.check("M17", eq(lambda: (add_tax(100, 0.15), 115)))

def m18():
    for c in range(0, N + 1):
        if add_tax(c, 0) != c:
            return False, c
    return True, None
R.check("M18", m18)

def m19():
    rates = [i / 100 for i in range(0, 101)] + [1e-17, 1e-9, 0.1, 0.07, 0.15, 1/3, 0.999999999]
    r = rng()
    rates += [r.random() for _ in range(50)]
    for rt in rates:
        for c in list(range(0, 500)) + [r.randint(0, N) for _ in range(2000)] + [N]:
            if add_tax(c, rt) < c:
                return False, (c, rt)
    for rt in (0, 0.15, 0.07, 1, 0.3333333333):
        for c in range(0, N + 1):
            if add_tax(c, rt) < c:
                return False, (c, rt)
    return True, None
R.check("M19", m19)
R.finish()
