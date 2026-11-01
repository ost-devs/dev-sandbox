import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.text import *

SEED = 12345
ALPHA = list("abcXYZ019 -_\t\n.,:!") + ["é", "ø", "ß", "İ", "ǆ", "ﬁ", "Ç", "日本", "😀", "́", "ŉ", "ΐ", "-", "--"]

def samples(rng, k=3000, maxlen=8):
    out = ["", " ", "-", "--", "a", "-a-", "ß", "İ", "ø", "é", "́", "ﬁ", "ǆ", "Café Noir", "日本", "😀", "A-", "a b"]
    for _ in range(k):
        out.append("".join(rng.choice(ALPHA) for _ in range(rng.randint(0, maxlen))))
    return out

def fmt(**kw): return ", ".join(f"{k}={v!r}" for k, v in kw.items())

def eq(expr_desc, got, exp):
    if got == exp: return True, ""
    return False, f"{expr_desc} -> {got!r}, esperado {exp!r}"

def forall(pred, inputs):
    for x in inputs:
        try:
            ok, msg = pred(x)
        except Exception as e:
            return False, f"entrada {x!r}: exceção {type(e).__name__}: {e}"
        if not ok: return False, f"entrada {x!r}: {msg}"
    return True, ""

def rs(): return random.Random(SEED)
S = None
def lazy_samples(): return samples(rs())

def T05(inp):
    s, n = inp
    r = truncate(s, n)
    return len(r) <= n, f"truncate({s!r}, {n}) = {r!r} (len {len(r)}) > {n}"
def t05_inputs():
    r = rs(); out = []
    for s in ["", "a", "abcdef", "abcdefghij"]:
        for n in range(0, 12): out.append((s, n))
    for _ in range(500): out.append(("".join(r.choice("abc") for _ in range(r.randint(0, 12))), r.randint(0, 12)))
    return sorted(set(out), key=lambda t: (t[1], len(t[0]), t[0]))

def T07(inp):
    s, n = inp; return truncate(s, n) == s, f"truncate({s!r},{n}) = {truncate(s,n)!r}"
def t07_inputs():
    out = [(s, n) for s in samples(rs(), 300) for n in range(len(s), len(s) + 3)]
    return out

def T16(inp):
    s, n = inp; r = pad_left(s, n); return len(r) == max(len(s), n), f"pad_left({s!r},{n}) = {r!r}"
def t16_inputs():
    return [(s, n) for s in samples(rs(), 300) for n in (0, 1, 3, 10)]

def mk(f):
    return lambda: f

claims = {}
def reg(i, method, fn): claims[i] = (method, fn)

reg("T01", "caso literal", lambda: eq("slugify('Café Noir')", slugify('Café Noir'), 'cafe-noir'))
SM = "amostra 3000 seed 12345 (alfabeto com unicode/símbolos) + bordas"
reg("T02", SM, lambda: forall(lambda s: (lambda r: (not r.startswith('-') and not r.endswith('-'), f"slugify={r!r}"))(slugify(s)), lazy_samples()))
reg("T03", SM, lambda: forall(lambda s: (lambda r: (all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in r), f"slugify={r!r}"))(slugify(s)), lazy_samples()))
reg("T04", SM, lambda: forall(lambda s: (lambda r: (slugify(r) == r, f"slugify(slugify)={slugify(r)!r} vs {r!r}"))(slugify(s)), lazy_samples()))
reg("T05", "s em {'', a, abcdef, abcdefghij} x n 0..11 + 500 aleatórios seed 12345; len(truncate)<=n", lambda: forall(T05, t05_inputs()))
reg("T06", "caso literal", lambda: eq("truncate('abcdef',5)", truncate('abcdef', 5), 'ab...'))
reg("T07", "amostra 300 seed 12345 x n in len..len+2 (sufixo padrão)", lambda: forall(T07, t07_inputs()))
reg("T08", "caso literal", lambda: eq("count_words('a  b\\tc\\n')", count_words('a  b\tc\n'), 3))
reg("T09", "caso literal", lambda: eq("count_words('')", count_words(''), 0))
reg("T10", "caso literal", lambda: eq("title_case('a  b')", title_case('a  b'), 'A  B'))
reg("T11", "caso literal", lambda: eq("title_case('élan vital')", title_case('élan vital'), 'Élan Vital'))
reg("T12", SM, lambda: forall(lambda s: (lambda r: (len(r) == len(s), f"title_case={r!r} len {len(r)} vs {len(s)}"))(title_case(s)), lazy_samples()))
reg("T13", "caso literal", lambda: eq("strip_accents('Ação')", strip_accents('Ação'), 'Acao'))
reg("T14", "caso literal", lambda: eq("strip_accents('ø')", strip_accents('ø'), 'o'))
reg("T15", "caso literal", lambda: eq("pad_left('7',3,'0')", pad_left('7', 3, '0'), '007'))
reg("T16", "amostra 300 seed 12345 x n in {0,1,3,10}, ch padrão ' '", lambda: forall(T16, t16_inputs()))
reg("T17", "caso literal", lambda: eq("is_palindrome('')", is_palindrome(''), True))
reg("T18", "caso literal", lambda: eq("is_palindrome(...)", is_palindrome('A man, a plan, a canal: Panama'), True))
reg("T19", SM, lambda: forall(lambda s: (is_palindrome(s) == is_palindrome(s[::-1]), f"{is_palindrome(s)} vs {is_palindrome(s[::-1])}"), lazy_samples()))

def run(i):
    method, fn = claims[i]
    try:
        ok, cex = fn()
    except Exception as e:
        ok, cex = False, f"exceção inesperada {type(e).__name__}: {e}"
    return {"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": "" if ok else cex, "method": method}

if __name__ == "__main__":
    ids = sys.argv[1:] or list(claims)
    for i in ids:
        print(json.dumps(run(i), ensure_ascii=False))
