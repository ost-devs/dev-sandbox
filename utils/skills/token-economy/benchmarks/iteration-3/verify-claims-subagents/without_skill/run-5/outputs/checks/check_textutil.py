import sys, os, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc.textutil import *

SEED = 12345
rng = random.Random(SEED)
ALPHA = list("abAB09 -_.!\t\n") + ['é', 'ß', '日', '…', '😀', ' ']
fixed = ['', ' ', '-', '--', '---a---', '!!!', 'a', 'é', 'Café Noir', ' a ', '日本', '😀', '\t\n', 'a-b', '_a_']
def inputs():
    yield from fixed
    for L in range(0, 3):
        for t in itertools.product(ALPHA, repeat=L):
            yield ''.join(t)
    for _ in range(2000):
        yield ''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 12)))

def out(i, ok, d): print(i, 'TRUE' if ok else 'FALSE', d)

cands = list(inputs())
bad = [s for s in cands if slugify(s).startswith('-') or slugify(s).endswith('-')]
ce = min(bad, key=lambda c: (len(c), repr(c)), default=None)
out('T1', ce is None, f'no counterexample in {len(cands)} inputs' if ce is None else f'slugify({ce!r})={slugify(ce)!r}')

r = slugify('Café Noir')
out('T2', r == 'cafe-noir', f"slugify('Café Noir')={r!r}, expected 'cafe-noir'")

pairs = [(s, n) for s in cands[:600] for n in (0, 1, 2, 3, 5, 10)]
pairs += [(rng.choice(cands), rng.randint(0, 15)) for _ in range(2000)]
bad = [p for p in pairs if len(truncate(*p)) > p[1]]
ce = min(bad, key=lambda p: (len(p[0]), p[1], repr(p)), default=None)
out('T3', ce is None, f'no counterexample in {len(pairs)} pairs' if ce is None else f'truncate{ce!r}={truncate(*ce)!r} len {len(truncate(*ce))} > {ce[1]}')

r = count_words('a  b\tc\n'); out('T4', r == 3, f'got {r!r}')
r = capitalize_words('a  b'); out('T5', r == 'A  B', f'got {r!r}')
r = is_palindrome(''); out('T6', r is True, f'got {r!r}')
sys.exit(0)
