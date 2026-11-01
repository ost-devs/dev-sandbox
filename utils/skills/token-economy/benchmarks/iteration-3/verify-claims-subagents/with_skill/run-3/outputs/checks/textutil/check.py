import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from common import rng, report
from calc.textutil import *

ALPHA = ['a', 'Z', '0', '-', ' ', '_', 'é', '\t', '…', '!']

def cands(cid, maxlen=3, extra=300):
    for L in range(maxlen + 1):
        for t in itertools.product(ALPHA, repeat=L):
            yield ''.join(t)
    r = rng(cid)
    for _ in range(extra):
        yield ''.join(r.choice(ALPHA) for _ in range(r.randint(4, 12)))

def smallest(bad):
    return min(bad, key=lambda x: (len(repr(x)), repr(x))) if bad else None

# T1
bad = [s for s in cands('T1') if slugify(s).startswith('-') or slugify(s).endswith('-')]
c = smallest(bad)
report('T1', c is None, f"s={c!r} -> {slugify(c)!r}" if c is not None else '')

# T2
v = slugify('Café Noir')
report('T2', v == 'cafe-noir', f"slugify('Café Noir')={v!r}" if v != 'cafe-noir' else '')

# T3
bad = []
r = rng('T3')
ss = list(cands('T3', 2, 100))
for s in ss:
    for n in list(range(0, 6)) + [r.randint(0, 20) for _ in range(3)]:
        if len(truncate(s, n)) > n:
            bad.append((s, n))
c = smallest([(s, n) for s, n in bad]) if bad else None
if c:
    c = min(bad, key=lambda p: (len(p[0]) + p[1], len(p[0]), p[1], repr(p[0])))
report('T3', c is None, f"s={c[0]!r}, n={c[1]} -> {truncate(*c)!r} (len {len(truncate(*c))})" if c else '')

# T4
v = count_words('a  b\tc\n')
report('T4', v == 3, f"got {v}" if v != 3 else '')

# T5
v = capitalize_words('a  b')
report('T5', v == 'A  B', f"got {v!r}" if v != 'A  B' else '')

# T6
v = is_palindrome('')
report('T6', v is True, f"got {v!r}" if v is not True else '')
