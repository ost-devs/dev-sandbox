import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit import text

EDGE = ['', ' ', '-', '--', 'a', 'A b', 'Café Noir', 'ß', 'İ', 'ǆ', 'ŉ', 'ﬁ', '中文', '-a-', '_x_', 'é', 'ø', 'ÀÉ', 'á', ' ', '١٢', '²', 'Ⅷ']

def cases(cid, n=2500):
    r = rng(cid)
    for e in EDGE: yield e
    for _ in range(n): yield rand_str(r, 14)

def prop(cid, pred, fmt):
    for s in cases(cid):
        try:
            if not pred(s): return (False, fmt(s))
        except Exception as e:
            return (False, '%r -> exception %r' % (s, e))
    return True

def eq(v, e): return v == e or (False, '%r != %r' % (v, e))

@claim('T01')
def t01(): return eq(text.slugify('Café Noir'), 'cafe-noir')

@claim('T02')
def t02(): return prop('T02', lambda s: not text.slugify(s).startswith('-') and not text.slugify(s).endswith('-'), lambda s: '%r -> %r' % (s, text.slugify(s)))

@claim('T03')
def t03(): return prop('T03', lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in text.slugify(s)), lambda s: '%r -> %r' % (s, text.slugify(s)))

@claim('T04')
def t04(): return prop('T04', lambda s: text.slugify(text.slugify(s)) == text.slugify(s), lambda s: '%r -> %r' % (s, text.slugify(text.slugify(s))))

@claim('T05')
def t05():
    r = rng('T05')
    pairs = [(s, n) for s in ['', 'a', 'abcdef', 'abc', 'abcd'] for n in range(0, 8)]
    pairs += [(rand_str(r, 14), r.randint(0, 20)) for _ in range(2500)]
    for s, n in pairs:
        try: o = text.truncate(s, n)
        except Exception as e: return (False, '(%r,%d) -> exception %r' % (s, n, e))
        if len(o) > n: return (False, '(%r,%d) -> %r' % (s, n, o))
    return True

@claim('T06')
def t06(): return eq(text.truncate('abcdef', 5), 'ab...')

@claim('T07')
def t07():
    r = rng('T07')
    pairs = [(s, n) for s in ['', 'a', 'abcdef'] for n in range(0, 8)]
    pairs += [(rand_str(r, 14), r.randint(0, 20)) for _ in range(2500)]
    for s, n in pairs:
        if len(s) <= n:
            o = text.truncate(s, n)
            if o != s: return (False, '(%r,%d) -> %r' % (s, n, o))
    return True

@claim('T08')
def t08(): return eq(text.count_words('a  b\tc\n'), 3)

@claim('T09')
def t09(): return eq(text.count_words(''), 0)

@claim('T10')
def t10(): return eq(text.title_case('a  b'), 'A  B')

@claim('T11')
def t11(): return eq(text.title_case('élan vital'), 'Élan Vital')

@claim('T12')
def t12(): return prop('T12', lambda s: len(text.title_case(s)) == len(s), lambda s: '%r -> %r' % (s, text.title_case(s)))

@claim('T13')
def t13(): return eq(text.strip_accents('Ação'), 'Acao')

@claim('T14')
def t14(): return eq(text.strip_accents('ø'), 'o')

@claim('T15')
def t15(): return eq(text.pad_left('7', 3, '0'), '007')

@claim('T16')
def t16():
    r = rng('T16')
    pairs = [(s, n) for s in ['', 'a', 'abc', 'é中'] for n in range(0, 6)]
    pairs += [(rand_str(r, 14), r.randint(0, 20)) for _ in range(2500)]
    for s, n in pairs:
        try: o = text.pad_left(s, n)
        except Exception as e: return (False, '(%r,%d) -> exception %r' % (s, n, e))
        if len(o) != max(len(s), n): return (False, '(%r,%d) -> %r' % (s, n, o))
    return True

@claim('T17')
def t17(): return eq(text.is_palindrome(''), True)

@claim('T18')
def t18(): return eq(text.is_palindrome('A man, a plan, a canal: Panama'), True)

@claim('T19')
def t19(): return prop('T19', lambda s: text.is_palindrome(s) == text.is_palindrome(s[::-1]), lambda s: '%r -> %r vs %r' % (s, text.is_palindrome(s), text.is_palindrome(s[::-1])))

if __name__ == '__main__': run(__file__)
