import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.lists import *

SEED = 4242
rng = random.Random(SEED)

# Listas de inteiros: todas com len<=4 sobre {0,1,2} + amostras semeadas
LISTS = [list(t) for n in range(0, 5) for t in itertools.product(range(3), repeat=n)]
for _ in range(1500):
    LISTS.append([rng.randint(-5, 5) for _ in range(rng.randint(0, 12))])
KS = list(range(-3, 15))

def forall(pred, cases, show):
    for c in cases:
        try:
            if not pred(c):
                return show(c)
        except Exception as e:
            return show(c) + f" -> excecao {type(e).__name__}: {e}"
    return None

def eq(f, code):
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", "execucao unica"
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), "execucao unica"

NOTE = f"exaustivo em listas len<=4 sobre {{0,1,2}} + 1500 listas semeadas (semente {SEED}) x k; nenhum contraexemplo achado"
def inf(pred, show, cases):
    return forall(pred, cases, show), NOTE

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

claim('L01')(lambda: eq(lambda: (chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]]), "chunk(list(range(7)), 3)"))
claim('L02')(lambda: inf(lambda c: flatten(chunk(c[0], c[1])) == c[0],
    lambda c: f"xs={c[0]}, k={c[1]} -> {flatten(chunk(*c))}", [(x, k) for x in LISTS for k in range(1, 15)]))

def l03():
    for xs in ([], [1], [1, 2, 3]):
        try:
            r = chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return f"chunk({xs}, 0) -> excecao {type(e).__name__}: {e} (esperado ValueError)", "execucao em 3 listas"
        return f"chunk({xs}, 0) -> {r!r} (nao levantou)", "execucao em 3 listas"
    return None, "chunk(xs,0) com xs=[],[1],[1,2,3] levanta ValueError"
claim('L03')(l03)

claim('L04')(lambda: eq(lambda: (dedupe([3,1,3,2,1]), [3,1,2]), "dedupe([3,1,3,2,1])"))
def first_occ(xs):
    out = []
    for x in xs:
        if x not in out: out.append(x)
    return out
claim('L05')(lambda: inf(lambda x: dedupe(x) == first_occ(x), lambda x: f"dedupe({x}) = {dedupe(x)}", LISTS))
claim('L06')(lambda: inf(lambda x: len(dedupe(x)) == len(set(x)), lambda x: f"dedupe({x}) = {dedupe(x)}", LISTS))
claim('L07')(lambda: eq(lambda: (flatten([[1,[2]],[3]]), [1,2,3]), "flatten([[1, [2]], [3]])"))
claim('L08')(lambda: eq(lambda: (top_n([5,1,4], 2), [5,4]), "top_n([5, 1, 4], 2)"))
claim('L09')(lambda: inf(lambda c: len(top_n(*c)) == min(c[1], len(c[0])),
    lambda c: f"top_n({c[0]}, {c[1]}) = {top_n(*c)}", [(x, k) for x in LISTS for k in range(0, 15)]))
claim('L10')(lambda: eq(lambda: (top_n([3,2,1], -1), []), "top_n([3, 2, 1], -1)"))
claim('L11')(lambda: eq(lambda: (rotate([1,2,3], 1), [2,3,1]), "rotate([1, 2, 3], 1)"))
claim('L12')(lambda: inf(lambda c: rotate(c[0], c[1]) == rotate(c[0], c[1] % len(c[0])),
    lambda c: f"rotate({c[0]}, {c[1]}) = {rotate(*c)} vs rotate({c[0]}, {c[1] % len(c[0])}) = {rotate(c[0], c[1] % len(c[0]))}",
    sorted(([x, k] for x in LISTS if x for k in range(0, 15)), key=lambda c: (len(c[0]), c[1], max(map(abs, c[0])), c[0]))))
claim('L13')(lambda: inf(lambda c: len(rotate(*c)) == len(c[0]),
    lambda c: f"rotate({c[0]}, {c[1]}) = {rotate(*c)}", [(x, k) for x in LISTS for k in range(-15, 16)]))
claim('L14')(lambda: eq(lambda: (interleave([1,2,3],[9]), [1,9,2,3]), "interleave([1, 2, 3], [9])"))
claim('L15')(lambda: inf(lambda c: len(interleave(*c)) == 2*min(len(c[0]), len(c[1])),
    lambda c: f"interleave({c[0]}, {c[1]}) = {interleave(*c)}", [(a, b) for a in LISTS[:120] for b in LISTS[:120]]))
claim('L16')(lambda: eq(lambda: (frequencies('abca'), {'a':2,'b':1,'c':1}), "frequencies('abca')"))
claim('L17')(lambda: inf(lambda x: sum(frequencies(x).values()) == len(x), lambda x: f"frequencies({x}) = {frequencies(x)}", LISTS))
claim('L18')(lambda: eq(lambda: (pairwise([1,2,3]), [(1,2),(2,3)]), "pairwise([1, 2, 3])"))
claim('L19')(lambda: inf(lambda x: len(pairwise(x)) == len(x) - 1, lambda x: f"pairwise({x}) = {pairwise(x)} (len {len(pairwise(x))}, esperado {len(x)-1})",
    sorted(LISTS, key=len)))

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
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_lists.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
