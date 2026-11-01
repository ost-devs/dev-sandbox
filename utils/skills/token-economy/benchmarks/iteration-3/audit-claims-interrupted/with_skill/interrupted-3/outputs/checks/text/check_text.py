import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from _lib import Checker, rand_strings, rand_ints
from kit.text import (slugify, truncate, count_words, title_case, strip_accents,
                      pad_left, is_palindrome)
import re

c = Checker('text')
S = rand_strings(seed=1001, n=3000)
N = rand_ints(seed=1002, n=100, lo=-5, hi=20)
NN = [n for n in N if n >= 0]


@c.claim('T01')
def _(): return c.eq(slugify('Café Noir'), 'cafe-noir')

@c.claim('T02')
def _(): return c.forall(S, lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'))

@c.claim('T03')
def _(): return c.forall(S, lambda s: re.fullmatch(r'[a-z0-9-]*', slugify(s)) is not None)

@c.claim('T04')
def _(): return c.forall(S, lambda s: slugify(slugify(s)) == slugify(s))

@c.claim('T05')
def _():
    for s in S[:300]:
        for n in NN:
            try:
                if len(truncate(s, n)) > n:
                    return c.fail(f'truncate({s!r}, {n}) = {truncate(s, n)!r} (len {len(truncate(s, n))})')
            except Exception as e:
                return c.fail(f'truncate({s!r}, {n}) raised {e}')
    return c.ok()

@c.claim('T06')
def _(): return c.eq(truncate('abcdef', 5), 'ab...')

@c.claim('T07')
def _():
    for s in S[:300]:
        for n in NN:
            if len(s) <= n and truncate(s, n) != s:
                return c.fail(f'truncate({s!r}, {n})')
    return c.ok()

@c.claim('T08')
def _(): return c.eq(count_words('a  b\tc\n'), 3)

@c.claim('T09')
def _(): return c.eq(count_words(''), 0)

@c.claim('T10')
def _(): return c.eq(title_case('a  b'), 'A  B')

@c.claim('T11')
def _(): return c.eq(title_case('élan vital'), 'Élan Vital')

@c.claim('T12')
def _(): return c.forall(S, lambda s: len(title_case(s)) == len(s))

@c.claim('T13')
def _(): return c.eq(strip_accents('Ação'), 'Acao')

@c.claim('T14')
def _(): return c.eq(strip_accents('ø'), 'o')

@c.claim('T15')
def _(): return c.eq(pad_left('7', 3, '0'), '007')

@c.claim('T16')
def _():
    for s in S[:300]:
        for n in NN:
            if len(pad_left(s, n)) != max(len(s), n):
                return c.fail(f'pad_left({s!r}, {n})')
    return c.ok()

@c.claim('T17')
def _(): return c.eq(is_palindrome(''), True)

@c.claim('T18')
def _(): return c.eq(is_palindrome('A man, a plan, a canal: Panama'), True)

@c.claim('T19')
def _(): return c.forall(S, lambda s: is_palindrome(s) == is_palindrome(s[::-1]))

c.main()
