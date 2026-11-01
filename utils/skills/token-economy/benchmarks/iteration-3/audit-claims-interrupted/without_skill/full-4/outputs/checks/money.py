import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

SEED = 12345
N = 3000

def eq(expr_str, got, want):
    return (True, None) if got == want else (False, f"{expr_str} = {got!r}, esperado {want!r}")

def check_M01(): return eq("to_cents('12,34')", to_cents('12,34'), 1234)
def check_M02(): return eq("to_cents('1.234,5')", to_cents('1.234,5'), 123450)
def check_M03(): return eq("to_cents('-1,50')", to_cents('-1,50'), -150)
def check_M04(): return eq("to_cents('7')", to_cents('7'), 700)
def check_M05(): return eq("format_brl(123456)", format_brl(123456), 'R$ 1.234,56')
def check_M06(): return eq("format_brl(5)", format_brl(5), 'R$ 0,05')
def check_M07(): return eq("format_brl(-150)", format_brl(-150), 'R$ -1,50')

def check_M08():
    for c in range(0, 1000001):
        if to_cents(format_brl(c)[3:]) != c:
            return False, f"c={c}: format_brl={format_brl(c)!r}, to_cents={to_cents(format_brl(c)[3:])}"
    return True, None

def check_M09():
    rng = random.Random(SEED)
    cases = [(0, 1), (1, 1), (0, 5), (1, 2), (1000, 3), (100, 3)]
    cases += [(rng.randint(0, 10**6), rng.randint(1, 50)) for _ in range(N)]
    for t, k in cases:
        s = sum(split_bill(t, k))
        if s != t:
            return False, f"split_bill({t}, {k}) = {split_bill(t, k)} soma {s} != {t}"
    return True, None

def _inst_cases():
    rng = random.Random(SEED)
    cases = [(0, 1), (1, 1), (0, 5), (1, 7), (100, 3), (1000, 3)]
    cases += [(rng.randint(0, 10**6), rng.randint(1, 60)) for _ in range(N)]
    cases += [(t, k) for t in range(0, 40) for k in range(1, 40)]
    return cases

def check_M10(): return eq("split_bill(900, 3)", split_bill(900, 3), [300, 300, 300])

def check_M11():
    for t, k in _inst_cases():
        r = installments(t, k)
        if sum(r) != t or len(r) != k:
            return False, f"installments({t}, {k}) = {r}"
    return True, None

def check_M12():
    for t, k in _inst_cases():
        r = installments(t, k)
        if max(r) - min(r) > 1:
            return False, f"installments({t}, {k}) = {r}"
    return True, None

def check_M13(): return eq("installments(100, 3)", installments(100, 3), [34, 33, 33])
def check_M14(): return eq("apply_discount(1000, 10)", apply_discount(1000, 10), 900)

def check_M15():
    for c in range(0, 1000001):
        if apply_discount(c, 0) != c:
            return False, f"apply_discount({c}, 0) = {apply_discount(c, 0)}"
    return True, None

def check_M16():
    rng = random.Random(SEED)
    for c in range(0, 1000001, 997):
        for p in range(0, 101):
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c}, {p}) = {apply_discount(c, p)} > {c}"
    for c in list(range(0, 300)) + [10**6, 10**6 - 1]:
        for p in range(0, 101):
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c}, {p}) = {apply_discount(c, p)} > {c}"
    for _ in range(N * 10):
        c, p = rng.randint(0, 10**6), rng.randint(0, 100)
        if apply_discount(c, p) > c:
            return False, f"apply_discount({c}, {p}) = {apply_discount(c, p)} > {c}"
    return True, None

def check_M17(): return eq("add_tax(100, 0.15)", add_tax(100, 0.15), 115)

def check_M18():
    for c in range(0, 1000001):
        if add_tax(c, 0) != c:
            return False, f"add_tax({c}, 0) = {add_tax(c, 0)}"
    return True, None

def check_M19():
    rng = random.Random(SEED)
    rates = [0, 1, 0.5, 0.15, 1e-17, 1e-9, 0.999999999]
    for c in list(range(0, 300)) + [10**6, 10**6 - 1]:
        for r in rates + [i / 100 for i in range(101)]:
            if add_tax(c, r) < c:
                return False, f"add_tax({c}, {r}) = {add_tax(c, r)} < {c}"
    for _ in range(N * 10):
        c, r = rng.randint(0, 10**6), rng.random()
        if add_tax(c, r) < c:
            return False, f"add_tax({c}, {r!r}) = {add_tax(c, r)} < {c}"
    return True, None

def main():
    ids = sys.argv[1:] or sorted(k[6:] for k in globals() if k.startswith("check_"))
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce,
                          "command": f"python3 -I checks/money.py {i}"}, ensure_ascii=False))

main()
