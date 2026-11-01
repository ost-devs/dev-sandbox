import sys, os, random, itertools
sys.path.insert(0, os.getcwd())
from calc.textutil import *

SEED = 12345
rng = random.Random(SEED)
ALPHA = list("aZ09 -_.,!?\t\n") + ["é", "ñ", "–", "日", "…", "'"]
fixed = ["", " ", "-", "--", "!", "a", "-a-", "a-", " a ", "Café Noir", "Hello, World!", "é", "日本", "...x...", "a b"]
cands = list(fixed)
for L in range(1, 4):
    cands += ["".join(p) for p in itertools.product(ALPHA, repeat=L)]
cands += ["".join(rng.choice(ALPHA) for _ in range(rng.randint(0, 12))) for _ in range(2000)]

def first(pred):
    for x in cands:
        try:
            if not pred(x):
                return x
        except Exception as e:
            return (x, repr(e))
    return None

def report(i, ok, ce=None):
    print(f"{i} VERDADEIRA" if ok else f"{i} FALSA contraexemplo={ce!r}")

ce = first(lambda s: not (slugify(s).startswith('-') or slugify(s).endswith('-')))
report("T1", ce is None, ce)

report("T2", slugify('Café Noir') == 'cafe-noir', ('Café Noir', slugify('Café Noir')))

ce = None
for n in range(0, 8):
    for s in cands:
        try:
            if len(truncate(s, n)) > n:
                ce = (s, n, truncate(s, n)); break
        except Exception as e:
            ce = (s, n, repr(e)); break
    if ce: break
report("T3", ce is None, ce)

report("T4", count_words('a  b\tc\n') == 3, count_words('a  b\tc\n'))
report("T5", capitalize_words('a  b') == 'A  B', capitalize_words('a  b'))
report("T6", is_palindrome('') is True, is_palindrome(''))
