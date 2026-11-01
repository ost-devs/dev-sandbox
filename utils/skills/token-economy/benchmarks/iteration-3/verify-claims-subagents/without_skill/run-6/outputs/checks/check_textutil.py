import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome

SEED = 12345
print("SEED =", SEED)
rng = random.Random(SEED)
ALPHA = list("abcXYZ019 -_.\t\n!") + ["é", "İ", "ß", "—", "…", "日"]

def rand_str(maxlen=8):
    return "".join(rng.choice(ALPHA) for _ in range(rng.randint(0, maxlen)))

def report(cid, cex):
    print(f"{cid}: {'FALSE' if cex is not None else 'TRUE'} | {cex!r}" if cex is not None
          else f"{cid}: TRUE | none found")

# T1
cex = None
fixed = ["", "-", "--a--", " a ", "!!!", "Café", "İ", "ß", "a-", "-a"]
for s in fixed + [rand_str() for _ in range(20000)]:
    r = slugify(s)
    if r.startswith("-") or r.endswith("-"):
        cex = (s, r); break
report("T1", cex)

# T2
r = slugify("Café Noir")
report("T2", None if r == "cafe-noir" else ("Café Noir", r))

# T3
cex = None
cands = [(s, n) for n in range(0, 4) for s in ["", "a", "ab", "abc", "abcd"]]
cands += [(rand_str(10), rng.randint(0, 10)) for _ in range(20000)]
cands.sort(key=lambda c: (len(c[0]) + c[1], c))  # minimal first
for s, n in cands:
    if len(truncate(s, n)) > n:
        cex = (s, n, truncate(s, n)); break
report("T3", cex)

# T4
r = count_words("a  b\tc\n")
report("T4", None if r == 3 else ("a  b\tc\n", r))

# T5
r = capitalize_words("a  b")
report("T5", None if r == "A  B" else ("a  b", r))

# T6
r = is_palindrome("")
report("T6", None if r is True else ("", r))
