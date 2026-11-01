import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import text as T

SEED = 20240601
ALPHA = ['a', 'Z', '0', '9', ' ', '-', '_', '!', '\t', '\n', 'é', 'ø', 'ß', 'İ', 'ç', 'ñ', '漢', 'ǆ', '٣', '\u0301', 'ﬁ', '€']
HAND = ['', ' ', '-', '--', 'a', 'abc', 'Café Noir', '  x  ', '-a-', 'ß', 'ǆ', 'ﬁ', 'İ', 'ø', '漢字', 'A man, a plan', 'é', 'e\u0301', '٣', '\n', 'a--b', '€', 'ŉ', 'ǰ']

def strings(seed_off=0, k=3000):
    r = random.Random(SEED + seed_off)
    out = list(HAND)
    for _ in range(k):
        out.append(''.join(r.choice(ALPHA) for _ in range(r.randint(0, 8))))
    return out

def first_fail(pred, gen):
    best = None
    for x in gen:
        try:
            ok, info = pred(x)
        except Exception as e:
            ok, info = False, 'exceção %s: %s' % (type(e).__name__, e)
        if not ok and (best is None or len(repr(x)) < len(repr(best[0]))):
            best = (x, info)
    return best

def forall(pred, gen):
    b = first_fail(pred, gen)
    if b is None:
        return True, None
    return False, 'entrada %r -> %s' % b

def eq(label, f, expected):
    try:
        got = f()
    except Exception as e:
        return False, '%s -> exceção %s: %s' % (label, type(e).__name__, e)
    if got == expected:
        return True, None
    return False, '%s -> %r vs. esperado %r' % (label, got, expected)

def check_T01(): return eq("slugify('Café Noir')", lambda: T.slugify('Café Noir'), 'cafe-noir')
def check_T02(): return forall(lambda s: (lambda o: (not o.startswith('-') and not o.endswith('-'), 'slugify=%r' % o))(T.slugify(s)), strings())
def check_T03(): return forall(lambda s: (lambda o: (all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in o), 'slugify=%r' % o))(T.slugify(s)), strings())
def check_T04(): return forall(lambda s: (lambda o: (T.slugify(o) == o, 'slugify=%r, segunda=%r' % (o, T.slugify(o))))(T.slugify(s)), strings())

def check_T05():
    # leitura literal: sufixo padrão '...', n inteiro >= 0
    def gen():
        for s in strings(5, 300):
            for n in range(0, 8):
                yield (s, n)
    return forall(lambda p: (lambda o: (len(o) <= p[1], 'truncate=%r (len %d) vs. n=%d' % (o, len(o), p[1])))(T.truncate(*p)), gen())

def check_T06(): return eq("truncate('abcdef', 5)", lambda: T.truncate('abcdef', 5), 'ab...')
def check_T07():
    def gen():
        for s in strings(7, 300):
            for n in range(len(s), len(s) + 4):
                yield (s, n)
    return forall(lambda p: (lambda o: (o == p[0], 'truncate=%r' % o))(T.truncate(*p)), gen())
def check_T08(): return eq("count_words('a  b\\tc\\n')", lambda: T.count_words('a  b\tc\n'), 3)
def check_T09(): return eq("count_words('')", lambda: T.count_words(''), 0)
def check_T10(): return eq("title_case('a  b')", lambda: T.title_case('a  b'), 'A  B')
def check_T11(): return eq("title_case('élan vital')", lambda: T.title_case('élan vital'), 'Élan Vital')
def check_T12(): return forall(lambda s: (lambda o: (len(o) == len(s), 'title_case=%r (len %d) vs. len(s)=%d' % (o, len(o), len(s))))(T.title_case(s)), strings())
def check_T13(): return eq("strip_accents('Ação')", lambda: T.strip_accents('Ação'), 'Acao')
def check_T14(): return eq("strip_accents('ø')", lambda: T.strip_accents('ø'), 'o')
def check_T15(): return eq("pad_left('7', 3, '0')", lambda: T.pad_left('7', 3, '0'), '007')
def check_T16():
    def gen():
        for s in strings(16, 300):
            for n in range(0, 8):
                yield (s, n)
    return forall(lambda p: (lambda o: (len(o) == max(len(p[0]), p[1]), 'pad_left=%r' % o))(T.pad_left(*p)), gen())
def check_T17(): return eq("is_palindrome('')", lambda: T.is_palindrome(''), True)
def check_T18(): return eq("is_palindrome('A man, a plan, a canal: Panama')", lambda: T.is_palindrome('A man, a plan, a canal: Panama'), True)
def check_T19(): return forall(lambda s: (T.is_palindrome(s) == T.is_palindrome(s[::-1]), 'is_palindrome(s)=%r, reverso=%r' % (T.is_palindrome(s), T.is_palindrome(s[::-1]))), strings(19))

def main(argv):
    ids = argv or ['T%02d' % i for i in range(1, 20)]
    for i in ids:
        try:
            ok, info = globals()['check_' + i]()
        except Exception as e:
            ok, info = False, 'exceção %s: %s' % (type(e).__name__, e)
        info = (info or '').replace('\t', '\\t').replace('\n', '\\n')
        print('%s\t%s\t%s' % (i, 'verdadeira' if ok else 'falsa', '' if ok else info))

if __name__ == '__main__':
    main(sys.argv[1:])
