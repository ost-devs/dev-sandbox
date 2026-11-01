import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import money as m

SEED = 20240611


def _eq(label, got, exp):
    if got == exp:
        return True, None
    return False, f"{label} -> {got!r} vs. esperado {exp!r}"


def _call(label, f, exp):
    try:
        got = f()
    except Exception as e:
        return False, f"{label} -> exceção {type(e).__name__}: {e} vs. esperado {exp!r}"
    return _eq(label, got, exp)


def check_M01(): return _call("to_cents('12,34')", lambda: m.to_cents('12,34'), 1234)
def check_M02(): return _call("to_cents('1.234,5')", lambda: m.to_cents('1.234,5'), 123450)
def check_M03(): return _call("to_cents('-1,50')", lambda: m.to_cents('-1,50'), -150)
def check_M04(): return _call("to_cents('7')", lambda: m.to_cents('7'), 700)
def check_M05(): return _call("format_brl(123456)", lambda: m.format_brl(123456), 'R$ 1.234,56')
def check_M06(): return _call("format_brl(5)", lambda: m.format_brl(5), 'R$ 0,05')
def check_M07(): return _call("format_brl(-150)", lambda: m.format_brl(-150), 'R$ -1,50')


def check_M08():
    for c in range(0, 1_000_001):
        try:
            got = m.to_cents(m.format_brl(c)[3:])
        except Exception as e:
            return False, f"c={c} -> exceção {type(e).__name__}: {e} vs. esperado {c}"
        if got != c:
            return False, f"c={c} -> {got!r} vs. esperado {c}"
    return True, None


def _cases_total_k():
    rng = random.Random(SEED)
    for t in range(0, 40):
        for k in range(1, 12):
            yield t, k
    for _ in range(3000):
        yield rng.randint(0, 10**7), rng.randint(1, 100)


def _sum_check(name, f):
    for t, k in _cases_total_k():
        try:
            r = f(t, k)
        except Exception as e:
            return False, f"{name}({t}, {k}) -> exceção {type(e).__name__}: {e}"
        if sum(r) != t:
            return False, f"{name}({t}, {k}) -> {r!r} com soma {sum(r)} vs. esperado {t}"
    return True, None


def check_M09(): return _sum_check('split_bill', m.split_bill)
def check_M10(): return _call("split_bill(900, 3)", lambda: m.split_bill(900, 3), [300, 300, 300])
def check_M11(): return _sum_check('installments', m.installments)


def check_M12():
    for t, k in _cases_total_k():
        try:
            r = m.installments(t, k)
        except Exception as e:
            return False, f"installments({t}, {k}) -> exceção {type(e).__name__}: {e}"
        if max(r) - min(r) > 1:
            return False, f"installments({t}, {k}) -> {r!r} diferença {max(r)-min(r)} vs. esperado <= 1"
    return True, None


def check_M13(): return _call("installments(100, 3)", lambda: m.installments(100, 3), [34, 33, 33])
def check_M14(): return _call("apply_discount(1000, 10)", lambda: m.apply_discount(1000, 10), 900)


def check_M15():
    for c in range(0, 1_000_001):
        try:
            got = m.apply_discount(c, 0)
        except Exception as e:
            return False, f"apply_discount({c}, 0) -> exceção {type(e).__name__}: {e}"
        if got != c:
            return False, f"apply_discount({c}, 0) -> {got!r} vs. esperado {c}"
    return True, None


def _cs():
    rng = random.Random(SEED)
    for c in range(0, 3001):
        yield c
    for c in (10**6, 10**6 - 1, 999_999, 500_000, 123_456):
        yield c
    for _ in range(20000):
        yield rng.randint(0, 1_000_000)


def check_M16():
    for c in _cs():
        for p in range(0, 101):
            try:
                got = m.apply_discount(c, p)
            except Exception as e:
                return False, f"apply_discount({c}, {p}) -> exceção {type(e).__name__}: {e}"
            if not got <= c:
                return False, f"apply_discount({c}, {p}) -> {got!r} vs. esperado <= {c}"
    return True, None


def check_M17(): return _call("add_tax(100, 0.15)", lambda: m.add_tax(100, 0.15), 115)


def check_M18():
    for c in range(0, 1_000_001):
        try:
            got = m.add_tax(c, 0)
        except Exception as e:
            return False, f"add_tax({c}, 0) -> exceção {type(e).__name__}: {e}"
        if got != c:
            return False, f"add_tax({c}, 0) -> {got!r} vs. esperado {c}"
    return True, None


def check_M19():
    rng = random.Random(SEED)
    rates = [i / 100 for i in range(0, 101)] + [i / 1000 for i in range(0, 1001)]
    rates += [0.0, 1.0, 1e-17, 5e-324, 0.999999999999] + [rng.random() for _ in range(200)]
    for c in _cs():
        for r in rates[:101] if c > 3000 else rates:
            try:
                got = m.add_tax(c, r)
            except Exception as e:
                return False, f"add_tax({c}, {r}) -> exceção {type(e).__name__}: {e}"
            if not got >= c:
                return False, f"add_tax({c}, {r}) -> {got!r} vs. esperado >= {c}"
    return True, None


def main(argv):
    ids = [f"M{i:02d}" for i in range(1, 20)]
    sel = argv or ids
    for i in sel:
        fn = globals().get("check_" + i)
        if fn is None:
            print(f"{i}\tfalsa\tid desconhecido")
            continue
        try:
            ok, ce = fn()
        except Exception as e:
            ok, ce = False, f"exceção inesperada {type(e).__name__}: {e}"
        print(f"{i}\t{'verdadeira' if ok else 'falsa'}\t{'' if ok else ce}")


if __name__ == '__main__':
    main(sys.argv[1:])
