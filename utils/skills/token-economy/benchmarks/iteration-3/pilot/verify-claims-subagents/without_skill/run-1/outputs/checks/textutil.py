import os, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome

SEED = 12345
rng = random.Random(SEED)
ALPHA = list("abcXYZ019 -_\t\n.,!") + ["é", "ß", "İ", "ñ", "日", "—", "…", " ", "٣"]


def rand_str():
    return "".join(rng.choice(ALPHA) for _ in range(rng.randint(0, 8)))


def shrink_str(s, bad):
    # greedy: remove chars while property still fails
    changed = True
    while changed:
        changed = False
        for i in range(len(s)):
            t = s[:i] + s[i + 1:]
            if bad(t):
                s, changed = t, True
                break
    return s


EDGE = ["", " ", "-", "--", "-a-", " a ", "a--b", "İ", "ß", "é", "日本", "\n", "A_B", "…", " x "]
N = 20000
out = []


def run(name, fn):
    try:
        out.append(f"{name}: {fn()}")
    except Exception as e:
        out.append(f"{name}: FALSA | contraexemplo: exceção {type(e).__name__}: {e}")


def t1():
    bad = lambda s: slugify(s).startswith("-") or slugify(s).endswith("-")
    cases = EDGE + [rand_str() for _ in range(N)]
    for s in cases:
        if bad(s):
            m = shrink_str(s, bad)
            return f"FALSA | contraexemplo: slugify({m!r}) = {slugify(m)!r}"
    return f"VERDADEIRA"


def t2():
    r = slugify("Café Noir")
    return "VERDADEIRA" if r == "cafe-noir" else f"FALSA | contraexemplo: slugify('Café Noir') = {r!r}, esperado 'cafe-noir'"


def t3():
    bad = lambda s, n: len(truncate(s, n)) > n
    cases = [(s, n) for s in EDGE for n in range(0, 5)]
    cases += [(rand_str(), rng.randint(0, 10)) for _ in range(N)]
    for s, n in cases:
        if bad(s, n):
            # shrink: smallest n, then shortest s
            for n2 in range(0, n + 1):
                if bad(s, n2):
                    n = n2
                    break
            s = shrink_str(s, lambda t: bad(t, n))
            return f"FALSA | contraexemplo: truncate({s!r}, {n}) = {truncate(s, n)!r} (len {len(truncate(s, n))} > {n})"
    return "VERDADEIRA"


def t4():
    r = count_words("a  b\tc\n")
    return "VERDADEIRA" if r == 3 else f"FALSA | contraexemplo: count_words('a  b\\tc\\n') = {r}"


def t5():
    r = capitalize_words("a  b")
    return "VERDADEIRA" if r == "A  B" else f"FALSA | contraexemplo: capitalize_words('a  b') = {r!r}"


def t6():
    r = is_palindrome("")
    return "VERDADEIRA" if r is True else f"FALSA | contraexemplo: is_palindrome('') = {r!r}"


for name, f in [("T1", t1), ("T2", t2), ("T3", t3), ("T4", t4), ("T5", t5), ("T6", t6)]:
    run(name, f)
print("\n".join(out))
sys.exit(0)
