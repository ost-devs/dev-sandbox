import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.money import *

SEED = 20240607
N = 20000
MAXC = 1_000_000

def eq(f, code):
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", "execucao unica"
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), "execucao unica"

def first(cases, pred, show):
    for c in cases:
        try:
            if not pred(c):
                return show(c)
        except Exception as e:
            return show(c) + f" -> excecao {type(e).__name__}: {e}"
    return None

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

claim('M01')(lambda: eq(lambda: (to_cents('12,34'), 1234), "to_cents('12,34')"))
claim('M02')(lambda: eq(lambda: (to_cents('1.234,5'), 123450), "to_cents('1.234,5')"))
claim('M03')(lambda: eq(lambda: (to_cents('-1,50'), -150), "to_cents('-1,50')"))
claim('M04')(lambda: eq(lambda: (to_cents('7'), 700), "to_cents('7')"))
claim('M05')(lambda: eq(lambda: (format_brl(123456), 'R$ 1.234,56'), "format_brl(123456)"))
claim('M06')(lambda: eq(lambda: (format_brl(5), 'R$ 0,05'), "format_brl(5)"))
claim('M07')(lambda: eq(lambda: (format_brl(-150), 'R$ -1,50'), "format_brl(-150)"))

def m08():
    r = first(range(0, MAXC + 1), lambda c: to_cents(format_brl(c)[3:]) == c,
              lambda c: f"c={c}: format_brl={format_brl(c)!r}, to_cents(...)={to_cents(format_brl(c)[3:])!r}")
    return r, "exaustivo c=0..1000000"
claim('M08')(m08)

def sample_tk(rng):
    cases = [(t, k) for t in list(range(0, 60)) + [99, 100, 101, 999, 1000, 10**6] for k in range(1, 15)]
    cases += [(rng.randint(0, 10**7), rng.randint(1, 500)) for _ in range(N)]
    return cases

def m09():
    cs = sample_tk(random.Random(SEED))
    r = first(cs, lambda c: sum(split_bill(*c)) == c[0],
              lambda c: f"split_bill({c[0]}, {c[1]}) = {split_bill(*c)} (soma {sum(split_bill(*c))})")
    return r, f"exaustivo total<60 x k<15 + bordas + {N} amostras semente {SEED}"
claim('M09')(m09)
claim('M10')(lambda: eq(lambda: (split_bill(900, 3), [300, 300, 300]), "split_bill(900, 3)"))

def m11():
    cs = sample_tk(random.Random(SEED))
    r = first(cs, lambda c: sum(installments(*c)) == c[0],
              lambda c: f"installments({c[0]}, {c[1]}) = {installments(*c)} (soma {sum(installments(*c))})")
    return r, f"exaustivo total<60 x k<15 + bordas + {N} amostras semente {SEED}; nenhum contraexemplo achado"
claim('M11')(m11)

def m12():
    cs = sample_tk(random.Random(SEED + 1))
    r = first(cs, lambda c: max(installments(*c)) - min(installments(*c)) <= 1,
              lambda c: f"installments({c[0]}, {c[1]}) = {installments(*c)}")
    return r, f"exaustivo total<60 x k<15 + bordas + {N} amostras semente {SEED+1}; nenhum contraexemplo achado"
claim('M12')(m12)
claim('M13')(lambda: eq(lambda: (installments(100, 3), [34, 33, 33]), "installments(100, 3)"))
claim('M14')(lambda: eq(lambda: (apply_discount(1000, 10), 900), "apply_discount(1000, 10)"))

def m15():
    r = first(range(0, MAXC + 1), lambda c: apply_discount(c, 0) == c,
              lambda c: f"apply_discount({c}, 0) = {apply_discount(c, 0)}")
    return r, "exaustivo c=0..1000000"
claim('M15')(m15)

def m16():
    rng = random.Random(SEED + 2)
    cs = [(c, p) for c in range(0, 3001) for p in range(0, 101)]
    cs += [(c, p) for p in range(0, 101) for c in (MAXC, MAXC - 1, 999_999, 500_000, 123_456)]
    cs += [(c, p) for p in (0, 1, 5, 10, 33, 50, 99, 100) for c in range(0, MAXC + 1, 1)]
    cs += [(rng.randint(0, MAXC), rng.randint(0, 100)) for _ in range(N)]
    r = first(cs, lambda c: apply_discount(*c) <= c[0],
              lambda c: f"apply_discount({c[0]}, {c[1]}) = {apply_discount(*c)}")
    return r, f"exaustivo c<=3000 x p=0..100; todos c=0..1e6 para p em {{0,1,5,10,33,50,99,100}}; bordas; {N} amostras semente {SEED+2}; nenhum contraexemplo achado"
claim('M16')(m16)
claim('M17')(lambda: eq(lambda: (add_tax(100, 0.15), 115), "add_tax(100, 0.15)"))

def m18():
    r = first(range(0, MAXC + 1), lambda c: add_tax(c, 0) == c,
              lambda c: f"add_tax({c}, 0) = {add_tax(c, 0)}")
    return r, "exaustivo c=0..1000000 (taxa inteira 0)"
claim('M18')(m18)

def m19():
    rng = random.Random(SEED + 3)
    rates = [0, 1, 0.0, 1.0, 0.5, 0.15, 0.1, 0.01, 1e-9, 1e-16, 2**-53, 2**-52, 0.999999999999] + [k / 100 for k in range(101)] + [k / 1000 for k in range(1001)]
    cs = [(c, r) for c in list(range(0, 2001)) + [MAXC, MAXC - 1, 999_999, 500_000] for r in rates]
    cs += [(rng.randint(0, MAXC), rng.random()) for _ in range(N)]
    r = first(cs, lambda c: add_tax(*c) >= c[0],
              lambda c: f"add_tax({c[0]}, {c[1]!r}) = {add_tax(*c)}")
    return r, f"c<=2000 e bordas x taxas {{k/100,k/1000,bordas}} + {N} amostras (c, r aleatorio em [0,1)) semente {SEED+3}; nenhum contraexemplo achado"
claim('M19')(m19)

def main():
    ids = sys.argv[1:] or sorted(R)
    res = []
    for i in ids:
        try:
            ce, note = R[i]()
        except Exception as e:
            ce, note = f"excecao {type(e).__name__}: {e}", "erro na checagem"
        if ce: note = note.replace("; nenhum contraexemplo achado", "; contraexemplo encontrado")
        line = {"id": i, "verdict": "falsa" if ce else "verdadeira", "counterexample": ce, "note": note}
        res.append(line)
        print(json.dumps(line, ensure_ascii=False))
    if not sys.argv[1:]:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_money.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
