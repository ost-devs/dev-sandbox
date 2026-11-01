import sys, os, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc.textutil import *

SEED = 12345
rng = random.Random(SEED)
print(f"seed random.Random({SEED})")
ALPHA = ['', ' ', '\t', '\n', '-', '_', 'a', 'Z', '0', '9', '!', '---', ' - ', 'é', 'É', 'ß', 'ñ', '日本', '😀', '…', ' ', 'İ', 'ǅ']
def corpus():
    yield from ALPHA
    for r in (1, 2, 3):
        for t in itertools.product(ALPHA[:14], repeat=r):
            yield ''.join(t)
    for _ in range(3000):
        yield ''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 8)))

def first(pred):
    for s in corpus():
        try:
            if not pred(s): return s
        except Exception as e:
            return (s, repr(e))
    return None

def out(i, ok, ce):
    print(f"{i} {'VERDADEIRA' if ok else 'FALSA'} {'-' if ok else ce}")

ce = first(lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'))
out('T1', ce is None, repr(ce))

r = slugify('Café Noir')
out('T2', r == 'cafe-noir', f"slugify('Café Noir') == {r!r}")

ce = None
for n in range(0, 6):
    for s in corpus():
        if len(truncate(s, n)) > n:
            ce = (s, n, truncate(s, n)); break
    if ce: break
out('T3', ce is None, repr(ce))

r = count_words('a  b\tc\n')
out('T4', r == 3, f"got {r!r}")

r = capitalize_words('a  b')
out('T5', r == 'A  B', f"got {r!r}")

r = is_palindrome('')
out('T6', r is True, f"got {r!r}")
