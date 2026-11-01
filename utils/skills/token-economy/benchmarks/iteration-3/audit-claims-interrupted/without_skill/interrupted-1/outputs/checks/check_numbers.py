import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kit.numbers import *

SEED = 12345
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_numbers.json")
CHECKS = {}

def claim(i):
    def d(f):
        CHECKS[i] = f
        return f
    return d

def call(f, *a):
    try:
        return ("ok", f(*a))
    except Exception as e:
        return ("exc", f"{type(e).__name__}: {e}")

def fmt(name, args, r):
    s = ", ".join(map(repr, args))
    return f"{name}({s}) -> " + (repr(r[1]) if r[0] == "ok" else "raised " + r[1])

def eq_case(name, f, args, expected, note):
    r = call(f, *args)
    if r[0] == "ok" and r[1] == expected and type(r[1]) is not bool or (r[0] == "ok" and r[1] is expected):
        return True, None, note
    return False, fmt(name, args, r) + f"; esperado {expected!r}", note

@claim("N01")
def _():
    rng = random.Random(SEED)
    cases = [(x, lo, hi) for lo in range(-8, 9) for hi in range(lo, 9) for x in range(-12, 13)]
    cases += [(rng.randint(-10**9, 10**9), *sorted((rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)))) for _ in range(2000)]
    for x, lo, hi in cases:
        r = call(clamp, x, lo, hi)
        if r[0] != "ok" or not (lo <= r[1] <= hi):
            return False, fmt("clamp", (x, lo, hi), r), "falsa"
    return True, None, f"exaustivo lo,hi,x em [-12,12] + 2000 casos semente {SEED}; nenhum contraexemplo"

@claim("N02")
def _(): return eq_case("clamp", clamp, (5, 10, 0), 0, "caso unico")
@claim("N03")
def _(): return eq_case("mean", mean, ([],), 0, "caso unico")
@claim("N04")
def _(): return eq_case("mean", mean, ([1, 2],), 1.5, "caso unico")
@claim("N05")
def _(): return eq_case("median", median, ([3, 1, 2],), 2, "caso unico")
@claim("N06")
def _():
    r = call(median, [])
    if r == ("ok", None): return True, None, "caso unico"
    return False, fmt("median", ([],), r), "esperado None"

@claim("N07")
def _():
    import itertools
    rng = random.Random(SEED)
    cases = [list(t) for n in range(1, 6) for t in itertools.product(range(-2, 3), repeat=n)]
    cases += [[rng.randint(-100, 100) for _ in range(rng.randint(1, 12))] for _ in range(3000)]
    cases += [[0], [-1], [10**18, -10**18]]
    for xs in cases:
        a, b = call(median, xs), call(median, sorted(xs))
        if a != b:
            return False, f"median({xs}) -> {a}; median(sorted)={b}", "falsa"
    return True, None, f"exaustivo listas ate 5 elems em [-2,2] + 3000 aleatorias semente {SEED}; nenhum contraexemplo"

@claim("N08")
def _(): return eq_case("round_half", round_half, (2.5,), 3, "caso unico")
@claim("N09")
def _(): return eq_case("round_half", round_half, (3.5,), 4, "caso unico")
@claim("N10")
def _(): return eq_case("percent", percent, (1, 3), 33.3, "caso unico")

@claim("N11")
def _():
    rng = random.Random(SEED)
    xs = [0, 1, -1, 0.0, 1.5, -2.5, 10**9, float("inf"), float("nan")] + [rng.randint(-1000, 1000) for _ in range(50)]
    for x in xs:
        r = call(percent, x, 0)
        if not (r[0] == "ok" and r[1] == 0.0 and isinstance(r[1], float)):
            return False, fmt("percent", (x, 0), r), "falsa"
    return True, None, "bordas + 50 aleatorios"

@claim("N12")
def _():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, n))
    for n in range(0, 1001):
        r = call(is_prime, n)
        if r != ("ok", ref(n)):
            return False, fmt("is_prime", (n,), r) + f"; correto {ref(n)}", "falsa"
    return True, None, "exaustivo 0..1000 contra divisao por tentativa"

@claim("N13")
def _(): return eq_case("is_prime", is_prime, (97,), True, "caso unico")
@claim("N14")
def _(): return eq_case("is_prime", is_prime, (2,), True, "caso unico")

@claim("N15")
def _():
    pairs = sorted(((a, b) for a in range(-50, 51) for b in range(-50, 51)), key=lambda p: (abs(p[0]) + abs(p[1]), p))
    for a, b in pairs:
        if True:
            x, y = call(gcd, a, b), call(gcd, b, a)
            if x != y:
                return False, f"gcd({a},{b})={x}; gcd({b},{a})={y}", "falsa"
    return True, None, "exaustivo 101x101 pares em [-50,50]"

@claim("N16")
def _(): return eq_case("gcd", gcd, (12, 18), 6, "caso unico")

@claim("N17")
def _():
    rng = random.Random(SEED)
    xs = list(range(-1000, 1001)) + [rng.randint(-10**18, 10**18) for _ in range(1000)]
    for a in xs:
        r = call(gcd, a, 0)
        if r != ("ok", a):
            return False, fmt("gcd", (a, 0), r), "falsa"
    return True, None, f"exaustivo -1000..1000 + 1000 grandes semente {SEED}; nenhum contraexemplo"

@claim("N18")
def _(): return eq_case("digits_sum", digits_sum, (1234,), 10, "caso unico")

@claim("N19")
def _():
    rng = random.Random(SEED)
    xs = list(range(-1000, 1001)) + [rng.randint(-10**30, 10**30) for _ in range(1000)]
    xs.sort(key=lambda v: (abs(v), v))
    for n in xs:
        r = call(digits_sum, n)
        if not (r[0] == "ok" and type(r[1]) is int and r[1] >= 0):
            return False, fmt("digits_sum", (n,), r), "falsa"
    return True, None, "exaustivo -1000..1000 + 1000 grandes"

def main():
    ids = sys.argv[1:] or sorted(CHECKS)
    res = []
    for i in ids:
        ok, ce, note = CHECKS[i]()
        if not ok:
            note = "contraexemplo encontrado; " + note if note not in ("falsa",) else "contraexemplo encontrado"
            if ce and note.startswith("contraexemplo encontrado; "):
                pass
        line = {"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce, "note": note}
        res.append(line)
        print(json.dumps(line, ensure_ascii=False))
    with open(OUT, "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

main()
