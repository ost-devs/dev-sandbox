import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.text import *

SEED = 12345
N = 3000
EDGE = ['', ' ', '  ', '-', '--', ' a ', 'a  b', 'a\tb\n', 'Café Noir', 'Ação', 'élan vital', 'ø', 'ß', 'straße',
        'ŉ', 'İ', 'K', 'ǆ', '日本語', '😀', '---a---', 'A man, a plan, a canal: Panama', 'abc', 'abcdef', '́',
        'é', '١٢٣', 'x-y', 'Z9', '_', 'ﬁ', '½', 'Ω']
ALPHA = list("abcXYZ019 -_\t\n,.:é ø ß İ K日😀́ﬁ½")

def samples():
    rng = random.Random(SEED)
    out = list(EDGE)
    for _ in range(N):
        out.append(''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 8))))
    for _ in range(500):
        out.append(''.join(chr(rng.randint(0, 0x2FFF)) for _ in range(rng.randint(0, 6))))
    return out

def fmt(**kw):
    return kw

def forall(pred, cases, show):
    for c in cases:
        try:
            if not pred(c):
                return show(c)
        except Exception as e:
            return show(c) + f" -> excecao {type(e).__name__}: {e}"
    return None

def eq_case(f, expected):
    got = f()
    return None if got == expected else f"obtido {got!r}, esperado {expected!r}"

R = {}
def claim(i):
    def d(f):
        R[i] = f
        return f
    return d

NOTE_INF = f"bordas manuais + {N}+500 amostras com semente {SEED}; nenhum contraexemplo achado"
S = None
def S_():
    global S
    if S is None: S = samples()
    return S

def inf(pred, show):
    return forall(pred, S_(), show), NOTE_INF

def eq(f, code):
    r = eq_case(f, None) if False else None
    try:
        got, exp = f()
    except Exception as e:
        return f"{code} -> excecao {type(e).__name__}: {e}", "execucao unica"
    return (None if got == exp else f"{code} -> {got!r} (esperado {exp!r})"), "execucao unica"

claim('T01')(lambda: eq(lambda: (slugify('Café Noir'), 'cafe-noir'), "slugify('Café Noir')"))
claim('T02')(lambda: inf(lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'), lambda s: f"slugify({s!r}) = {slugify(s)!r}"))
claim('T03')(lambda: inf(lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slugify(s)), lambda s: f"slugify({s!r}) = {slugify(s)!r}"))
claim('T04')(lambda: inf(lambda s: slugify(slugify(s)) == slugify(s), lambda s: f"slugify({s!r}) = {slugify(s)!r}, slugify dupla = {slugify(slugify(s))!r}"))

def t05():
    cases = [(s, n) for s in S_()[:600] for n in range(0, 12)]
    r = forall(lambda c: len(truncate(*c)) <= c[1], cases, lambda c: f"truncate({c[0]!r}, {c[1]}) = {truncate(*c)!r} (len {len(truncate(*c))})")
    return r, f"{len(cases)} casos (600 strings x n=0..11), semente {SEED}"
claim('T05')(t05)
claim('T06')(lambda: eq(lambda: (truncate('abcdef', 5), 'ab...'), "truncate('abcdef', 5)"))
def t07():
    cases = [(s, n) for s in S_()[:600] for n in range(0, 12) if len(s) <= n]
    r = forall(lambda c: truncate(*c) == c[0], cases, lambda c: f"truncate({c[0]!r}, {c[1]}) = {truncate(*c)!r}")
    return r, f"{len(cases)} casos com len(s)<=n, semente {SEED}"
claim('T07')(t07)
claim('T08')(lambda: eq(lambda: (count_words('a  b\tc\n'), 3), "count_words('a  b\\tc\\n')"))
claim('T09')(lambda: eq(lambda: (count_words(''), 0), "count_words('')"))
claim('T10')(lambda: eq(lambda: (title_case('a  b'), 'A  B'), "title_case('a  b')"))
claim('T11')(lambda: eq(lambda: (title_case('élan vital'), 'Élan Vital'), "title_case('élan vital')"))
claim('T12')(lambda: inf(lambda s: len(title_case(s)) == len(s), lambda s: f"title_case({s!r}) = {title_case(s)!r} (len {len(title_case(s))} != {len(s)})"))
claim('T13')(lambda: eq(lambda: (strip_accents('Ação'), 'Acao'), "strip_accents('Ação')"))
claim('T14')(lambda: eq(lambda: (strip_accents('ø'), 'o'), "strip_accents('ø')"))
claim('T15')(lambda: eq(lambda: (pad_left('7', 3, '0'), '007'), "pad_left('7', 3, '0')"))
def t16():
    cases = [(s, n) for s in S_()[:600] for n in range(0, 12)]
    r = forall(lambda c: len(pad_left(*c)) == max(len(c[0]), c[1]), cases, lambda c: f"pad_left({c[0]!r}, {c[1]}) = {pad_left(*c)!r}")
    return r, f"{len(cases)} casos (600 strings x n=0..11), semente {SEED}; nenhum contraexemplo achado"
claim('T16')(t16)
claim('T17')(lambda: eq(lambda: (is_palindrome(''), True), "is_palindrome('')"))
claim('T18')(lambda: eq(lambda: (is_palindrome('A man, a plan, a canal: Panama'), True), "is_palindrome('A man, a plan, a canal: Panama')"))
claim('T19')(lambda: inf(lambda s: is_palindrome(s) == is_palindrome(s[::-1]), lambda s: f"is_palindrome({s!r}) = {is_palindrome(s)}, invertida = {is_palindrome(s[::-1])}"))

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
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_text.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
main()
