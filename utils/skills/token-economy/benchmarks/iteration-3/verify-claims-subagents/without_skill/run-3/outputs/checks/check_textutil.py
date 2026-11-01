import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome

rng = random.Random(12345)
alphabet = list("abcXYZ019 -_.!?\t\n") + ["é", "İ", "ß", "—", "日", "…", " ", "Σ"]
def rand_strs(k=3000):
    yield from ["", " ", "-", "---", "!!!", "é", "İ", "ß", "日本", "-a-", "a-", "Café Noir"]
    for _ in range(k):
        yield "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
strs = list(rand_strs())

def report(cid, cex):
    print(f"{cid} FALSE {cex!r}" if cex is not None else f"{cid} TRUE")

def first(gen):
    for x in gen:
        return x
    return None

report("T1", first((s, slugify(s)) for s in strs if (lambda r: r.startswith('-') or r.endswith('-'))(slugify(s))))
r = slugify('Café Noir')
report("T2", None if r == 'cafe-noir' else ("slugify('Café Noir')", r))
report("T3", first(((s, n), truncate(s, n)) for s in strs for n in range(0, 6) if len(truncate(s, n)) > n))
r = count_words('a  b\tc\n')
report("T4", None if r == 3 else ("count_words", r))
r = capitalize_words('a  b')
report("T5", None if r == 'A  B' else ("capitalize_words('a  b')", r))
report("T6", None if is_palindrome('') is True else ("is_palindrome('')", is_palindrome('')))
