import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.intervals import *

SEED = 12345
V = range(0, 6)
VALID = [(s, e) for s in V for e in V if s < e]
ANY = [(s, e) for s in V for e in V]          # inclui invertidos/vazios
def lists(maxlen):
    for n in range(1, maxlen + 1):
        yield from itertools.product(VALID, repeat=n)
def sampled_lists():
    rng = random.Random(SEED)
    for _ in range(2000):
        n = rng.randint(1, 8)
        out = []
        for _ in range(n):
            s = rng.randint(-20, 20); out.append((s, s + rng.randint(1, 10)))
        yield out
def all_lists():
    yield from (list(x) for x in lists(3))
    yield from sampled_lists()
NOTE_EX = "exaustivo: inteiros 0..5, listas ate 3 intervalos + 2000 listas amostradas com semente %d (ate 8, valores -20..30); nenhum contraexemplo achado" % SEED

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

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

claim('I01')(lambda: eq(lambda: (overlaps((0, 5), (5, 10)), False), "overlaps((0,5),(5,10))"))
claim('I02')(lambda: (forall(lambda c: overlaps(*c) == overlaps(c[1], c[0]), itertools.product(ANY, ANY),
    lambda c: f"overlaps{c[0],c[1]}={overlaps(*c)} vs invertido={overlaps(c[1],c[0])}"),
    "exaustivo: todos pares de (s,e) com s,e em 0..5, incluindo invertidos/vazios; nenhum contraexemplo achado"))
claim('I03')(lambda: eq(lambda: (merge([(1, 3), (2, 6), (8, 10)]), [(1, 6), (8, 10)]), "merge([(1,3),(2,6),(8,10)])"))
claim('I04')(lambda: eq(lambda: (merge([(1, 2), (2, 3)]), [(1, 3)]), "merge([(1,2),(2,3)])"))
def ok5(xs):
    m = merge(xs)
    return all(m[i][0] < m[i][1] for i in range(len(m))) and all(not overlaps(m[i], m[i+1]) and m[i][0] <= m[i+1][0] for i in range(len(m)-1))
claim('I05')(lambda: (forall(ok5, all_lists(), lambda xs: f"merge({xs}) = {merge(xs)}"), NOTE_EX))
claim('I06')(lambda: (forall(lambda xs: merge(merge(xs)) == merge(xs), all_lists(), lambda xs: f"merge({xs}) = {merge(xs)}, dupla = {merge(merge(xs))}"), NOTE_EX))
claim('I07')(lambda: eq(lambda: (contains((0, 5), 5), False), "contains((0,5),5)"))
claim('I08')(lambda: (forall(lambda a: contains(a, a[0]) is True, VALID, lambda a: f"contains({a},{a[0]})={contains(a,a[0])}"),
    "exaustivo: todos intervalos validos em 0..5; nenhum contraexemplo achado"))
claim('I09')(lambda: eq(lambda: (intersect((0, 5), (3, 8)), (3, 5)), "intersect((0,5),(3,8))"))
claim('I10')(lambda: eq(lambda: (intersect((0, 2), (5, 6)), None), "intersect((0,2),(5,6))"))
claim('I11')(lambda: eq(lambda: (intersect((0, 5), (5, 8)), None), "intersect((0,5),(5,8))"))
claim('I12')(lambda: eq(lambda: (total_covered([(0, 5), (3, 8)]), 8), "total_covered([(0,5),(3,8)])"))
claim('I13')(lambda: (forall(lambda xs: total_covered(xs) <= sum(length(i) for i in xs), all_lists(),
    lambda xs: f"total_covered({xs})={total_covered(xs)} > soma={sum(length(i) for i in xs)}"), NOTE_EX))
claim('I14')(lambda: (forall(lambda c: length(intersect(*c)) <= min(length(c[0]), length(c[1])),
    [c for c in itertools.product(VALID, VALID) if overlaps(*c)],
    lambda c: f"intersect{c}={intersect(*c)}"), "exaustivo: pares validos que se sobrepoem em 0..5; nenhum contraexemplo achado"))
def i15():
    try:
        got = merge([])
    except Exception as e:
        return f"merge([]) -> excecao {type(e).__name__}: {e} (esperado [])", "execucao unica"
    return (None if got == [] else f"merge([]) -> {got!r}"), "execucao unica"
claim('I15')(i15)
claim('I16')(lambda: (forall(lambda a: overlaps(a, a) is True, VALID, lambda a: f"overlaps({a},{a})={overlaps(a,a)}"),
    "exaustivo: todos intervalos validos em 0..5; nenhum contraexemplo achado"))
claim('I17')(lambda: eq(lambda: (merge([(5, 7), (1, 2)]), [(1, 2), (5, 7)]), "merge([(5,7),(1,2)])"))
claim('I18')(lambda: (forall(lambda c: (not contains(*c)) or overlaps(c[0], (c[1], c[1] + 1)),
    [(a, x) for a in ANY for x in range(-2, 8)],
    lambda c: f"a={c[0]}, x={c[1]}: contains={contains(*c)}, overlaps(a,(x,x+1))={overlaps(c[0],(c[1],c[1]+1))}"),
    "exaustivo: a com s,e em 0..5 (todos), x em -2..7; nenhum contraexemplo achado"))
claim('I19')(lambda: eq(lambda: (length((3, 1)), 0), "length((3,1))"))

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
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_intervals.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
