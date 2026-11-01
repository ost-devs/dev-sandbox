import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.money import to_cents, format_brl, split_bill, installments, apply_discount, add_tax

SEED = 20240607
N = 5000


def point(expr, expected):
    def f():
        got = eval(expr)
        return None if got == expected else f"{expr} = {got!r}, esperado {expected!r}"
    return f


def universal(cases, pred, desc):
    """cases: iterable de tuplas; pred(*args) -> (ok, obtido). Retorna o primeiro contraexemplo."""
    def f():
        for a in cases():
            try:
                ok, got = pred(*a)
            except Exception as e:
                return f"{desc} com entrada {a!r}: exceção {type(e).__name__}: {e}"
            if not ok:
                return f"{desc} com entrada {a!r}: obtido {got!r}"
        return None
    return f


def cents_cases():
    yield from [(0,), (1,), (99,), (100,), (999,), (1000,), (1000000,)]
    r = random.Random(SEED)
    for _ in range(N):
        yield (r.randint(0, 1000000),)


def m08():
    for c in range(0, 1000001):
        try:
            got = to_cents(format_brl(c)[3:])
        except Exception as e:
            return f"c={c}: exceção {type(e).__name__}: {e}"
        if got != c:
            return f"c={c}: format_brl={format_brl(c)!r}, to_cents(...)={got!r}"
    return None


def tk_cases(seed_off):
    def g():
        yield from [(0, 1), (1, 2), (0, 2), (1, 1), (100, 3), (10, 3), (5, 10)]
        r = random.Random(SEED + seed_off)
        for _ in range(N):
            yield (r.randint(0, 10**6), r.randint(1, 50))
    return g


def m12(t, k):
    l = installments(t, k)
    return max(l) - min(l) <= 1, l


def disc_cases():
    yield from [(0, 0), (1, 100), (1000000, 100), (1, 50), (5, 10), (3, 99)]
    r = random.Random(SEED + 3)
    for _ in range(N):
        yield (r.randint(0, 1000000), r.randint(0, 100))


def tax_cases():
    yield from [(0, 0.0), (1, 0.0), (1000000, 1.0), (1, 1e-12), (1000000, 1e-16), (100, 0.15)]
    r = random.Random(SEED + 4)
    for _ in range(N):
        yield (r.randint(0, 1000000), r.random() if r.random() < .8 else r.choice([0.0, 1.0, 0.1, 0.07, 0.15]))


def z(c):
    return (c,)


CLAIMS = {
    "M01": point("to_cents('12,34')", 1234),
    "M02": point("to_cents('1.234,5')", 123450),
    "M03": point("to_cents('-1,50')", -150),
    "M04": point("to_cents('7')", 700),
    "M05": point("format_brl(123456)", 'R$ 1.234,56'),
    "M06": point("format_brl(5)", 'R$ 0,05'),
    "M07": point("format_brl(-150)", 'R$ -1,50'),
    "M08": m08,
    "M09": universal(tk_cases(1), lambda t, k: (sum(split_bill(t, k)) == t, split_bill(t, k)), "sum(split_bill(total,k)) != total"),
    "M10": point("split_bill(900, 3)", [300, 300, 300]),
    "M11": universal(tk_cases(2), lambda t, k: (sum(installments(t, k)) == t, installments(t, k)), "sum(installments(total,k)) != total"),
    "M12": universal(tk_cases(5), m12, "max-min > 1"),
    "M13": point("installments(100, 3)", [34, 33, 33]),
    "M14": point("apply_discount(1000, 10)", 900),
    "M15": universal(cents_cases, lambda c: (apply_discount(c, 0) == c, apply_discount(c, 0)), "apply_discount(c,0) != c"),
    "M16": universal(disc_cases, lambda c, p: (apply_discount(c, p) <= c, apply_discount(c, p)), "apply_discount(c,p) > c"),
    "M17": point("add_tax(100, 0.15)", 115),
    "M18": universal(cents_cases, lambda c: (add_tax(c, 0) == c, add_tax(c, 0)), "add_tax(c,0) != c"),
    "M19": universal(tax_cases, lambda c, r: (add_tax(c, r) >= c, add_tax(c, r)), "add_tax(c,r) < c"),
}


def main():
    ids = sys.argv[1:] or list(CLAIMS)
    for i in ids:
        try:
            ce = CLAIMS[i]()
        except Exception as e:
            ce = f"exceção inesperada {type(e).__name__}: {e}"
        print(json.dumps({"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce}, ensure_ascii=False))


main()
