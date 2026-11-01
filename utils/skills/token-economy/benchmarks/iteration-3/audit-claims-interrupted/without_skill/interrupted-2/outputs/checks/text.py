import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.text import *

CMD = 'python3 -I checks/text.py'
rng = random.Random(12345)
EDGE = ['', ' ', '  ', '-', '--', 'a', 'A', 'abc', ' a ', '-a-', 'Café Noir', 'Ação', 'ø', 'ß', 'ǆ', 'ŉ',
        'İ', 'K', 'ﬁ', 'é', 'e\u0301', 'élan vital', 'a  b', 'a\tb\n', '日本語', '😀', 'a😀b', '!!!', 'A man, a plan',
        'A man, a plan, a canal: Panama', 'ab', 'aba', 'abc cba', 'x-y', 'ǅ', 'ΐ', 'ῼ', '١٢٣', '²', '½', 'Σ', 'ΑΣ',
        'hello world', 'a-', '-a', '_', 'ǈ', 'ﬃ', 'ſ']
ALPHA = list('abcXYZ019 -_\t\n,.:!') + ['é', 'ø', 'ß', 'İ', 'K', 'ﬁ', 'ǆ', 'Σ', '日', '😀', '\u0301', 'ŉ', 'ǅ', '²', 'ٳ']
def gen(k=3000):
    out = list(EDGE)
    for _ in range(k):
        out.append(''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 8))))
    return out
S = gen()

def first(f, cases):
    for c in cases:
        try:
            r = f(c)
            if r is not True:
                return r if isinstance(r, str) else repr(c)
        except Exception as e:
            return '%r -> exception %r' % (c, e)
    return None

def eq(expr_f, expected):
    try:
        r = expr_f()
    except Exception as e:
        return 'exception %r' % (e,)
    return None if r == expected else 'got %r, expected %r' % (r, expected)

res = {}
def fnc(i, f, cases):
    res[i] = first(f, cases)
def one(i, expr, f, expected):
    r = eq(f, expected)
    res[i] = None if r is None else '%s: %s' % (expr, r)

def univ(i, pred, cases):
    for c in cases:
        try:
            ok, out = pred(c)
        except Exception as e:
            res[i] = '%r -> exception %r' % (c, e); return
        if not ok:
            res[i] = 'input %r -> result %r' % (c, out); return
    res[i] = None

one('T01', "slugify('Café Noir')", lambda: slugify('Café Noir'), 'cafe-noir')
univ('T02', lambda s: (lambda r: (not r.startswith('-') and not r.endswith('-'), r))(slugify(s)), S)
univ('T03', lambda s: (lambda r: (all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in r), r))(slugify(s)), S)
univ('T04', lambda s: (lambda r: (slugify(r) == r, (r, slugify(r))))(slugify(s)), S)
cases5 = [(s, n) for s in S[:400] for n in range(0, 8)] + [(s, n) for s in S[:200] for n in (10, 50)]
univ('T05', lambda c: (lambda r: (len(r) <= c[1], r))(truncate(*c)), cases5)
one('T06', "truncate('abcdef', 5)", lambda: truncate('abcdef', 5), 'ab...')
cases7 = [(s, n) for s in S for n in (0, 1, 2, 3, 5, 8, 100) if len(s) <= n]
univ('T07', lambda c: (lambda r: (r == c[0], r))(truncate(*c)), cases7)
one('T08', "count_words('a  b\\tc\\n')", lambda: count_words('a  b\tc\n'), 3)
one('T09', "count_words('')", lambda: count_words(''), 0)
one('T10', "title_case('a  b')", lambda: title_case('a  b'), 'A  B')
one('T11', "title_case('élan vital')", lambda: title_case('élan vital'), 'Élan Vital')
univ('T12', lambda s: (lambda r: (len(r) == len(s), r))(title_case(s)), S)
one('T13', "strip_accents('Ação')", lambda: strip_accents('Ação'), 'Acao')
one('T14', "strip_accents('ø')", lambda: strip_accents('ø'), 'o')
one('T15', "pad_left('7', 3, '0')", lambda: pad_left('7', 3, '0'), '007')
cases16 = [(s, n) for s in S[:600] for n in list(range(0, 8)) + [50]]
univ('T16', lambda c: (lambda r: (len(r) == max(len(c[0]), c[1]), r))(pad_left(*c)), cases16)
one('T17', "is_palindrome('')", lambda: is_palindrome(''), True)
one('T18', "is_palindrome('A man, a plan, a canal: Panama')", lambda: is_palindrome('A man, a plan, a canal: Panama'), True)
univ('T19', lambda s: (lambda a, b: (a == b, (a, b)))(is_palindrome(s), is_palindrome(s[::-1])), S)

for i in ['T%02d' % k for k in range(1, 20)]:
    r = res[i]
    print('\t'.join([i, 'verdadeira' if r is None else 'falsa', (r or '').replace('\t', '\\t').replace('\n', '\\n'), CMD]))
