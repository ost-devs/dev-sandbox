import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

SEED = 12345

def eq(expr_str, f, expected):
    try:
        got = f()
    except Exception as e:
        return False, f"{expr_str} raised {e!r}; claimed {expected!r}"
    if got == expected and type(got) == type(expected):
        return True, ""
    return False, f"{expr_str} -> {got!r}; claimed {expected!r}"

def M01(): return eq("to_cents('12,34')", lambda: to_cents('12,34'), 1234)
def M02(): return eq("to_cents('1.234,5')", lambda: to_cents('1.234,5'), 123450)
def M03(): return eq("to_cents('-1,50')", lambda: to_cents('-1,50'), -150)
def M04(): return eq("to_cents('7')", lambda: to_cents('7'), 700)
def M05(): return eq("format_brl(123456)", lambda: format_brl(123456), 'R$ 1.234,56')
def M06(): return eq("format_brl(5)", lambda: format_brl(5), 'R$ 0,05')
def M07(): return eq("format_brl(-150)", lambda: format_brl(-150), 'R$ -1,50')

def M08():
    for c in range(0, 1000001):
        try:
            got = to_cents(format_brl(c)[3:])
        except Exception as e:
            return False, f"c={c}: raised {e!r}"
        if got != c:
            return False, f"c={c}: to_cents(format_brl(c)[3:]) -> {got!r}; claimed {c}"
    return True, ""

def _cases(rng):
    totals = [0, 1, 2, 3, 10, 99, 100, 101, 10**6, 10**12, 2**63]
    totals += [rng.randrange(0, 10**6) for _ in range(2500)]
    ks = [1, 2, 3, 7, 10, 100]
    for t in totals:
        for k in ks + [rng.randrange(1, 50)]:
            yield t, k
    for t in range(0, 40):
        for k in range(1, 15):
            yield t, k

def _sum_prop(fn, name):
    rng = random.Random(SEED)
    best = None
    for t, k in _cases(rng):
        try:
            r = fn(t, k)
            s = sum(r)
        except Exception as e:
            return False, f"{name}({t}, {k}) raised {e!r}"
        if s != t:
            if best is None or (t, k) < best[0]:
                best = ((t, k), r, s)
    if best:
        (t, k), r, s = best
        return False, f"{name}({t}, {k}) -> {r!r}, sum={s}; claimed sum == {t}"
    return True, ""

def M09(): return _sum_prop(split_bill, "split_bill")
def M10(): return eq("split_bill(900, 3)", lambda: split_bill(900, 3), [300, 300, 300])
def M11(): return _sum_prop(installments, "installments")

def M12():
    rng = random.Random(SEED)
    for t, k in _cases(rng):
        try:
            r = installments(t, k)
        except Exception as e:
            return False, f"installments({t}, {k}) raised {e!r}"
        if max(r) - min(r) > 1:
            return False, f"installments({t}, {k}) -> {r!r}; max-min > 1"
    return True, ""

def M13(): return eq("installments(100, 3)", lambda: installments(100, 3), [34, 33, 33])
def M14(): return eq("apply_discount(1000, 10)", lambda: apply_discount(1000, 10), 900)

def M15():
    for c in range(0, 1000001):
        if apply_discount(c, 0) != c:
            return False, f"apply_discount({c}, 0) -> {apply_discount(c,0)!r}; claimed {c}"
    return True, ""

def M16():
    rng = random.Random(SEED)
    for c in range(0, 3000):
        for p in range(0, 101):
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c}, {p}) -> {apply_discount(c,p)!r} > {c}"
    for p in range(0, 101):
        for c in [10**6, 10**6 - 1, 500000, 999999]:
            if apply_discount(c, p) > c:
                return False, f"apply_discount({c}, {p}) > {c}"
    for _ in range(300000):
        c = rng.randrange(0, 1000001); p = rng.randrange(0, 101)
        if apply_discount(c, p) > c:
            return False, f"apply_discount({c}, {p}) -> {apply_discount(c,p)!r} > {c}"
    return True, ""

def M17(): return eq("add_tax(100, 0.15)", lambda: add_tax(100, 0.15), 115)

def M18():
    for c in range(0, 1000001):
        if add_tax(c, 0) != c:
            return False, f"add_tax({c}, 0) -> {add_tax(c,0)!r}; claimed {c}"
    return True, ""

def M19():
    rng = random.Random(SEED)
    rates = [0, 1, 0.5, 0.15, 5e-324, 1e-16, 1e-9, 0.07, 0.1, 0.2, 0.9999999999999999]
    rates += [rng.random() for _ in range(300)]
    for c in list(range(0, 2000)) + [10**6, 10**6 - 1] + [rng.randrange(0, 1000001) for _ in range(5000)]:
        for r in rates:
            try:
                v = add_tax(c, r)
            except Exception as e:
                return False, f"add_tax({c}, {r!r}) raised {e!r}"
            if v < c:
                return False, f"add_tax({c}, {r!r}) -> {v!r} < {c}"
    return True, ""

ALL = [f"M{i:02d}" for i in range(1, 20)]

def main():
    ids = sys.argv[1:] or ALL
    for i in ids:
        ok, ce = globals()[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": ce, "note": ""}, ensure_ascii=False))

if __name__ == '__main__':
    main()
