import os, sys, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome

rng = random.Random(12345)
ALPHA = list('abzAZ09 -_\t\n.') + ['é', 'É', 'ß', 'İ', '日', ' ', '—', '…', '', 'é']

def strings():
    yield from ['', ' ', '-', '--', '-a-', 'a', 'Café Noir', 'İ', '日本', ' ', ' a ', '!!!', 'ab', '…']
    for L in range(1, 4):
        for t in itertools.product(ALPHA[:12], repeat=L):
            yield ''.join(t)
    for _ in range(3000):
        yield ''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 12)))

def first(pred):
    for s in strings():
        try:
            if not pred(s):
                return s
        except Exception as e:
            return (s, repr(e))
    return None

def report(i, cex):
    print(f"{i} {'TRUE' if cex is None else 'FALSE'} {'-' if cex is None else repr(cex)}")

report('T1', first(lambda s: not (slugify(s).startswith('-') or slugify(s).endswith('-'))))
report('T2', None if slugify('Café Noir') == 'cafe-noir' else ('Café Noir', slugify('Café Noir')))
cex = None
for s in strings():
    for n in range(0, 8):
        try:
            if len(truncate(s, n)) > n:
                cex = (s, n, truncate(s, n)); break
        except Exception as e:
            cex = (s, n, repr(e)); break
    if cex: break
report('T3', cex)
report('T4', None if count_words('a  b\tc\n') == 3 else count_words('a  b\tc\n'))
report('T5', None if capitalize_words('a  b') == 'A  B' else capitalize_words('a  b'))
report('T6', None if is_palindrome('') is True else is_palindrome(''))
