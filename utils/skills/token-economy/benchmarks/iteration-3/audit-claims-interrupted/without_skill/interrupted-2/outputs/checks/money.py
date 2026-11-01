import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

CMD = 'python3 -I checks/money.py'
RNG = random.Random(12345)
out = {}

def run(f):
    try:
        return f()
    except Exception as e:
        return ('EXC', repr(e))

def eq(i, expr, f, expected):
    r = run(f)
    out[i] = None if r == expected and not (isinstance(r, tuple) and r[:1] == ('EXC',)) else f'{expr} -> {r!r}, esperado {expected!r}'

eq('M01', "to_cents('12,34')", lambda: to_cents('12,34'), 1234)
eq('M02', "to_cents('1.234,5')", lambda: to_cents('1.234,5'), 123450)
eq('M03', "to_cents('-1,50')", lambda: to_cents('-1,50'), -150)
eq('M04', "to_cents('7')", lambda: to_cents('7'), 700)
eq('M05', "format_brl(123456)", lambda: format_brl(123456), 'R$ 1.234,56')
eq('M06', "format_brl(5)", lambda: format_brl(5), 'R$ 0,05')
eq('M07', "format_brl(-150)", lambda: format_brl(-150), 'R$ -1,50')

def first_bad(cases, pred):
    for a in cases:
        try:
            if not pred(*a):
                return a
        except Exception as e:
            return a + (('EXC', repr(e)),)
    return None

def report(i, expr, cases, pred, show):
    for a in cases:
        try:
            ok, res = pred(*a)
        except Exception as e:
            out[i] = f'{expr} com {a!r} -> excecao {e!r}'
            return
        if not ok:
            out[i] = f'{expr} com {a!r} -> {res!r}'
            return
    out[i] = None

# M08 full domain
def m08():
    for c in range(0, 1000001):
        try:
            r = to_cents(format_brl(c)[3:])
        except Exception as e:
            return f'to_cents(format_brl({c})[3:]) -> excecao {e!r}'
        if r != c:
            return f'to_cents(format_brl({c})[3:]) -> {r!r} (format_brl={format_brl(c)!r})'
    return None
out['M08'] = m08()

tc = [(t, k) for t in [0, 1, 5, 100, 899, 900, 1000, 999999] for k in [1, 2, 3, 7, 10]]
tc += [(RNG.randint(0, 10**7), RNG.randint(1, 50)) for _ in range(2000)]
report('M09', 'sum(split_bill(total,k))==total', tc, lambda t, k: (sum(split_bill(t, k)) == t, split_bill(t, k)), 0)
eq('M10', 'split_bill(900, 3)', lambda: split_bill(900, 3), [300, 300, 300])
report('M11', 'sum(installments(total,k))==total', tc, lambda t, k: (sum(installments(t, k)) == t, installments(t, k)), 0)
report('M12', 'max-min<=1', tc, lambda t, k: (max(installments(t, k)) - min(installments(t, k)) <= 1, installments(t, k)), 0)
eq('M13', 'installments(100, 3)', lambda: installments(100, 3), [34, 33, 33])
eq('M14', 'apply_discount(1000, 10)', lambda: apply_discount(1000, 10), 900)

def m15():
    for c in range(1000001):
        r = apply_discount(c, 0)
        if r != c:
            return f'apply_discount({c}, 0) -> {r!r}'
out['M15'] = run(m15) if not isinstance(run(m15), tuple) else f'excecao {run(m15)}'

def m16():
    for c in range(1000001):
        for p in range(101):
            r = apply_discount(c, p)
            if not r <= c:
                return f'apply_discount({c}, {p}) -> {r!r}'
    return None
out['M16'] = run(m16)

eq('M17', 'add_tax(100, 0.15)', lambda: add_tax(100, 0.15), 115)

def m18():
    for c in range(1000001):
        r = add_tax(c, 0)
        if r != c:
            return f'add_tax({c}, 0) -> {r!r}'
out['M18'] = run(m18)

def m19():
    rates = [i / 100 for i in range(101)] + [0.15, 0.07, 0.1, 0.29, 0.57, 1]
    for r in rates:
        for c in range(1000001) if False else []:
            pass
    # full sweep over c for hand-picked and random rates
    rates2 = sorted(set(rates + [RNG.random() for _ in range(5)]))
    for r in rates2:
        for c in range(1000001):
            v = add_tax(c, r)
            if not v >= c:
                return f'add_tax({c}, {r!r}) -> {v!r}'
    return None
out['M19'] = run(m19)

for k in out:
    v = out[k]
    if isinstance(v, tuple):
        out[k] = f'excecao {v[1]}'
for i in sorted(out):
    v = out[i]
    print(f"{i}\t{'verdadeira' if v is None else 'falsa'}\t{v or ''}\t{CMD}")
