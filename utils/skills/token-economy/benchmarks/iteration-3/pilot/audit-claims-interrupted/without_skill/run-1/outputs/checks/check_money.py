#!/usr/bin/env python3
"""Checks for kit/money.py claims M01-M19. SEED fixed for determinism."""
import json, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

SEED = 20240611
N = 1000000


def eq(expr_repr, fn, expected):
    try:
        got = fn()
    except Exception as e:
        got = 'raised ' + repr(e)
    if got == expected:
        return True, None
    return False, f"{expr_repr} -> {got!r}, esperado {expected!r}"


def M01(): return eq("to_cents('12,34')", lambda: to_cents('12,34'), 1234)
def M02(): return eq("to_cents('1.234,5')", lambda: to_cents('1.234,5'), 123450)
def M03(): return eq("to_cents('-1,50')", lambda: to_cents('-1,50'), -150)
def M04(): return eq("to_cents('7')", lambda: to_cents('7'), 700)
def M05(): return eq("format_brl(123456)", lambda: format_brl(123456), 'R$ 1.234,56')
def M06(): return eq("format_brl(5)", lambda: format_brl(5), 'R$ 0,05')
def M07(): return eq("format_brl(-150)", lambda: format_brl(-150), 'R$ -1,50')


def M08():  # exhaustive 0..1_000_000
    for c in range(N + 1):
        s = format_brl(c)[3:]
        try:
            g = to_cents(s)
        except Exception as e:
            g = repr(e)
        if g != c:
            return False, f"c={c}: to_cents(format_brl({c})[3:]) = to_cents({s!r}) -> {g!r}, esperado {c}"
    return True, None


def _totals_ks():
    rnd = random.Random(SEED)
    for t in list(range(0, 60)) + [10**6, 10**9, 2**63]:
        for k in list(range(1, 60)) + [t, t + 1, 1000, 10**5]:
            if 1 <= k <= 10**5:
                yield t, k
    for _ in range(5000):
        yield rnd.randint(0, 10**9), rnd.randint(1, 5000)


def M09():
    for t, k in _totals_ks():
        r = sum(split_bill(t, k))
        if r != t:
            return False, f"split_bill({t},{k}) soma {r}, esperado {t}"
    return True, None


def M10(): return eq("split_bill(900,3)", lambda: split_bill(900, 3), [300, 300, 300])


def M11():
    for t, k in _totals_ks():
        r = sum(installments(t, k))
        if r != t:
            return False, f"installments({t},{k}) soma {r}, esperado {t}"
    return True, None


def M12():
    for t, k in _totals_ks():
        l = installments(t, k)
        if max(l) - min(l) > 1:
            return False, f"installments({t},{k}): max-min = {max(l)-min(l)} > 1"
    return True, None


def M13(): return eq("installments(100,3)", lambda: installments(100, 3), [34, 33, 33])
def M14(): return eq("apply_discount(1000,10)", lambda: apply_discount(1000, 10), 900)


def M15():
    for c in range(N + 1):
        if apply_discount(c, 0) != c:
            return False, f"apply_discount({c},0) -> {apply_discount(c,0)!r}, esperado {c}"
    return True, None


def M16():
    # exhaustive in c for extreme/selected p, seeded sample of c for every p
    rnd = random.Random(SEED)
    for p in (0, 1, 2, 3, 33, 50, 99, 100):
        for c in range(N + 1):
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c},{p}) -> {apply_discount(c,p)!r} > {c}"
    for p in range(101):
        cs = list(range(0, 300)) + [rnd.randint(0, N) for _ in range(3000)] + [N]
        for c in cs:
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c},{p}) -> {apply_discount(c,p)!r} > {c}"
    return True, None


def M17(): return eq("add_tax(100, 0.15)", lambda: add_tax(100, 0.15), 115)


def M18():
    for c in range(N + 1):
        if add_tax(c, 0) != c:
            return False, f"add_tax({c},0) -> {add_tax(c,0)!r}, esperado {c}"
    return True, None


def M19():
    rnd = random.Random(SEED)
    rates = [0, 1, 0.1, 0.15, 0.07, 0.5, 0.25, 0.05, 0.2, 0.3, 0.01, 1e-9, 1e-16, 1e-17, 0.999999, 1 - 1e-16,
             5e-324] + [i / 100 for i in range(101)] + [i / 1000 for i in range(1001)] + [rnd.random() for _ in range(3000)]
    # exhaustive in c for a few rates
    for r in (0, 1, 0.1, 0.15, 0.07, 1e-9, 1e-16):
        for c in range(N + 1):
            if add_tax(c, r) < c:
                return False, f"add_tax({c},{r!r}) -> {add_tax(c,r)!r} < {c}"
    cs = list(range(0, 400)) + [rnd.randint(0, N) for _ in range(300)] + [N]
    for r in rates:
        for c in cs:
            if add_tax(c, r) < c:
                return False, f"add_tax({c},{r!r}) -> {add_tax(c,r)!r} < {c}"
    return True, None


CHECKS = {f"M{i:02d}": globals()[f"M{i:02d}"] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))
