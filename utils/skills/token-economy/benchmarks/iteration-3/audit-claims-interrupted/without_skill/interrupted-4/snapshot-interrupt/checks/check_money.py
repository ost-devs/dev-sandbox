import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

SEED = 20261101


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def fixed(expr, fn, expected):
    ok, ce = eq(fn, expected)
    return ok, (None if ok else f'{expr}: {ce}')


def M01(): return fixed("to_cents('12,34')", lambda: to_cents('12,34'), 1234)
def M02(): return fixed("to_cents('1.234,5')", lambda: to_cents('1.234,5'), 123450)
def M03(): return fixed("to_cents('-1,50')", lambda: to_cents('-1,50'), -150)
def M04(): return fixed("to_cents('7')", lambda: to_cents('7'), 700)
def M05(): return fixed("format_brl(123456)", lambda: format_brl(123456), 'R$ 1.234,56')
def M06(): return fixed("format_brl(5)", lambda: format_brl(5), 'R$ 0,05')
def M07(): return fixed("format_brl(-150)", lambda: format_brl(-150), 'R$ -1,50')


def M08():
    for c in range(0, 1000001):
        try:
            g = to_cents(format_brl(c)[3:])
        except Exception as e:
            return False, f'c={c!r}: raised {e!r}'
        if g != c:
            return False, f'c={c!r}: got {g!r}, expected {c!r}'
    return True, None


def _cases(rng):
    fx = [(0, 1), (1, 1), (0, 5), (1, 2), (100, 3), (10, 3), (5, 7), (999, 10), (1, 100)]
    for _ in range(20000):
        fx.append((rng.randint(0, 10**7), rng.randint(1, 50)))
    return fx


def M09():
    for t, k in _cases(random.Random(SEED)):
        try:
            r = split_bill(t, k)
        except Exception as e:
            return False, f'split_bill({t!r}, {k!r}) raised {e!r}'
        if sum(r) != t:
            return False, f'split_bill({t}, {k}) = {r!r}, sum {sum(r)} != {t}'
    return True, None


def M10(): return fixed("split_bill(900, 3)", lambda: split_bill(900, 3), [300, 300, 300])


def M11():
    for t, k in _cases(random.Random(SEED)):
        try:
            r = installments(t, k)
        except Exception as e:
            return False, f'installments({t!r}, {k!r}) raised {e!r}'
        if sum(r) != t:
            return False, f'installments({t}, {k}) = {r!r}, sum {sum(r)} != {t}'
    return True, None


def M12():
    for t, k in _cases(random.Random(SEED)):
        try:
            r = installments(t, k)
        except Exception as e:
            return False, f'installments({t!r}, {k!r}) raised {e!r}'
        if max(r) - min(r) > 1:
            return False, f'installments({t}, {k}) = {r!r}, spread {max(r)-min(r)}'
    return True, None


def M13(): return fixed("installments(100, 3)", lambda: installments(100, 3), [34, 33, 33])
def M14(): return fixed("apply_discount(1000, 10)", lambda: apply_discount(1000, 10), 900)
def M17(): return fixed("add_tax(100, 0.15)", lambda: add_tax(100, 0.15), 115)


def M15():
    for c in range(0, 1000001):
        try:
            g = apply_discount(c, 0)
        except Exception as e:
            return False, f'c={c!r}: raised {e!r}'
        if g != c:
            return False, f'apply_discount({c}, 0) = {g!r}, expected {c}'
    return True, None


def M16():
    rng = random.Random(SEED)
    cs = [(c, p) for c in range(0, 1000001, 997) for p in range(101)]
    cs += [(rng.randint(0, 1000000), rng.randint(0, 100)) for _ in range(200000)]
    cs += [(c, p) for c in (0, 1, 999999, 1000000) for p in range(101)]
    for c, p in cs:
        try:
            g = apply_discount(c, p)
        except Exception as e:
            return False, f'apply_discount({c}, {p}) raised {e!r}'
        if not g <= c:
            return False, f'apply_discount({c}, {p}) = {g!r} > {c}'
    return True, None


def M18():
    for c in range(0, 1000001):
        for r in (0, 0.0):
            try:
                g = add_tax(c, r)
            except Exception as e:
                return False, f'add_tax({c}, {r!r}) raised {e!r}'
            if g != c:
                return False, f'add_tax({c}, {r!r}) = {g!r}, expected {c}'
    return True, None


def M19():
    rng = random.Random(SEED)
    rs = [0, 1, 0.0, 1.0, 0.5, 0.15, 1e-9, 1e-12, 1e-16, 0.1, 0.07, 0.99]
    cs = [(c, r) for c in range(0, 1000001, 991) for r in rs]
    cs += [(rng.randint(0, 1000000), rng.random()) for _ in range(200000)]
    cs += [(rng.randint(0, 1000000), rng.choice(rs)) for _ in range(100000)]
    for c, r in cs:
        try:
            g = add_tax(c, r)
        except Exception as e:
            return False, f'add_tax({c}, {r!r}) raised {e!r}'
        if not g >= c:
            return False, f'add_tax({c}, {r!r}) = {g!r} < {c}'
    return True, None


CHECKS = {f'M{i:02d}': globals()[f'M{i:02d}'] for i in range(1, 20)}


def main():
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": None if ok else ce,
                          "command": f"python3 checks/check_money.py {i}"}, ensure_ascii=False))


main()
