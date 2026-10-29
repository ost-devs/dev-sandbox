from common import *
from kit.text import *
import string

def strs(cid, n=N):
    r = rng(cid)
    alpha = string.ascii_letters + string.digits + ' -_.,!\t\n' + 'éÉçãõñüøßıİŁł€—' + '́'
    yield from ['', ' ', '-', '--a--', 'ß', 'ø', 'İ', 'ǆ', 'ﬁ', 'Café Noir', 'á', 'ǅ']
    for _ in range(n):
        yield ''.join(r.choice(alpha) for _ in range(r.randint(0, 12)))

@claim('T01')
def _(): return eq(lambda: slugify('Café Noir'), 'cafe-noir')
@claim('T02')
def _(): return forall(strs('T02'), lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'))
@claim('T03')
def _(): return forall(strs('T03'), lambda s: all(c in string.ascii_lowercase + string.digits + '-' for c in slugify(s)))
@claim('T04')
def _(): return forall(strs('T04'), lambda s: slugify(slugify(s)) == slugify(s))
@claim('T05')
def _():
    r = rng('T05')
    ins = [(s, n) for s in strs('T05', 2000) for n in range(0, 8)]
    return forall(ins, lambda s, n: len(truncate(s, n)) <= n)
@claim('T06')
def _(): return eq(lambda: truncate('abcdef', 5), 'ab...')
@claim('T07')
def _(): return forall(((s, n) for s in strs('T07', 2000) for n in range(0, 15)), lambda s, n: len(s) > n or truncate(s, n) == s)
@claim('T08')
def _(): return eq(lambda: count_words('a  b\tc\n'), 3)
@claim('T09')
def _(): return eq(lambda: count_words(''), 0)
@claim('T10')
def _(): return eq(lambda: title_case('a  b'), 'A  B')
@claim('T11')
def _(): return eq(lambda: title_case('élan vital'), 'Élan Vital')
@claim('T12')
def _(): return forall(strs('T12'), lambda s: len(title_case(s)) == len(s))
@claim('T13')
def _(): return eq(lambda: strip_accents('Ação'), 'Acao')
@claim('T14')
def _(): return eq(lambda: strip_accents('ø'), 'o')
@claim('T15')
def _(): return eq(lambda: pad_left('7', 3, '0'), '007')
@claim('T16')
def _(): return forall(((s, n) for s in strs('T16', 3000) for n in range(0, 15)), lambda s, n: len(pad_left(s, n)) == max(len(s), n))
@claim('T17')
def _(): return eq(lambda: is_palindrome(''), True)
@claim('T18')
def _(): return eq(lambda: is_palindrome('A man, a plan, a canal: Panama'), True)
@claim('T19')
def _(): return forall(strs('T19'), lambda s: is_palindrome(s) == is_palindrome(s[::-1]))

if __name__ == '__main__': main('text')
