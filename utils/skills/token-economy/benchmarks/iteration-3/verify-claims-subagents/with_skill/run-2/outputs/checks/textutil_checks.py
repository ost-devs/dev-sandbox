from harness import claim, rng, run
import itertools
from calc.textutil import slugify, truncate, count_words, capitalize_words, is_palindrome

ALPHA = ['a', 'Z', '0', '-', ' ', '_', '!', 'é', 'ß', '中', '\n', 'İ']


def _strings(maxlen=4):
    yield ''
    for L in range(1, maxlen + 1):
        for t in itertools.product(ALPHA, repeat=L):
            yield ''.join(t)
    r = rng()
    for _ in range(3000):
        yield ''.join(r.choice(ALPHA) for _ in range(r.randint(0, 30)))


@claim('T1')
def t1():
    for s in _strings():
        o = slugify(s)
        if o.startswith('-') or o.endswith('-'):
            return 'slugify(%r) = %r' % (s, o)


@claim('T2')
def t2():
    o = slugify('Café Noir')
    if o != 'cafe-noir':
        return "slugify('Café Noir') = %r" % o


@claim('T3')
def t3():
    r = rng()
    for s in list(_strings(2)):
        for n in range(0, 5):
            o = truncate(s, n)
            if len(o) > n:
                return 'truncate(%r, %d) = %r (len %d)' % (s, n, o, len(o))
    for _ in range(2000):
        s = ''.join(r.choice(ALPHA) for _ in range(r.randint(0, 30)))
        n = r.randint(0, 35)
        o = truncate(s, n)
        if len(o) > n:
            return 'truncate(%r, %d) = %r' % (s, n, o)


@claim('T4')
def t4():
    o = count_words('a  b\tc\n')
    if o != 3:
        return "count_words('a  b\\tc\\n') = %r" % o


@claim('T5')
def t5():
    o = capitalize_words('a  b')
    if o != 'A  B':
        return "capitalize_words('a  b') = %r" % o


@claim('T6')
def t6():
    o = is_palindrome('')
    if o is not True:
        return "is_palindrome('') = %r" % (o,)


if __name__ == '__main__':
    run('textutil')
