"""Deterministic checks for claims T1-T6 about calc/textutil.py (stdlib only)."""
import os
import random
import sys

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKDIR)

from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome  # noqa: E402

SEED = 20261029
N_RANDOM = 20000
rng = random.Random(SEED)

# Alphabet mixing ASCII, separators, punctuation, and unicode (incl. chars whose
# lower() expands or maps into ASCII, e.g. 'İ' -> 'i̇', 'K' (Kelvin) -> 'k').
ALPHABET = (
    list("abcxyzABCXYZ0189")
    + list("-_ .,!?'\"/\\\t\n\r")
    + ["é", "É", "ß", "İ", "K", "ﬁ", "Σ", "ς", "中", "😀", "́", " ", " ", "　", "…", "–"]
)


def rand_str(max_len=12):
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randint(0, max_len)))


def report(cid, cex):
    if cex is None:
        print(f"{cid} | TRUE")
    else:
        print(f"{cid} | FALSE | counterexample: {cex}")


# ---------- T1: slugify never starts/ends with '-' ----------
def check_t1():
    curated = ["", "-", "--", "a", "-a-", "  a  ", "!a!", "a-", "-a", "---a---b---",
               "é", "éa", "aé", "Café", "İ", "K", "ﬁ", "😀a😀", "á", " a ",
               "Hello, World!", "___", "a_b", "1-2", "..1..", "\t\n"]
    rand = [rand_str() for _ in range(N_RANDOM)] + [rand_str(60) for _ in range(2000)]
    for s in curated + rand:
        r = slugify(s)
        if r.startswith("-") or r.endswith("-"):
            return f"slugify({s!r}) -> {r!r} vs expected no leading/trailing '-'"
    return None


# ---------- T2 ----------
def check_t2():
    r = slugify("Café Noir")
    return None if r == "cafe-noir" else f"slugify('Café Noir') -> {r!r} vs expected 'cafe-noir'"


# ---------- T3: len(truncate(s, n)) <= n for all s, n >= 0 ----------
def check_t3():
    curated = []
    for s in ["", "a", "ab", "abc", "hello", "é", "😀😀", "…"]:
        for n in range(0, 7):
            curated.append((s, n))
    curated.sort(key=lambda p: (len(p[0]) + p[1], p[1], p[0]))  # smallest first
    rand = []
    for _ in range(N_RANDOM):
        s = rand_str(20)
        n = rng.choice([0, 1, 2, len(s), max(len(s) - 1, 0), len(s) + 1, rng.randint(0, 25)])
        rand.append((s, n))
    for s, n in curated + rand:
        r = truncate(s, n)
        if len(r) > n:
            return f"truncate({s!r}, {n}) -> {r!r} (len {len(r)}) vs expected len <= {n}"
    return None


# ---------- T4 ----------
def check_t4():
    r = count_words("a  b\tc\n")
    return None if r == 3 else f"count_words('a  b\\tc\\n') -> {r!r} vs expected 3"


# ---------- T5 ----------
def check_t5():
    r = capitalize_words("a  b")
    return None if r == "A  B" else f"capitalize_words('a  b') -> {r!r} vs expected 'A  B'"


# ---------- T6 ----------
def check_t6():
    r = is_palindrome("")
    return None if r is True else f"is_palindrome('') -> {r!r} vs expected True"


report("T1", check_t1())
report("T2", check_t2())
report("T3", check_t3())
report("T4", check_t4())
report("T5", check_t5())
report("T6", check_t6())
sys.exit(0)
