from harness import *
from kit.text import *


@claim('T01')
def _(): return eq("slugify('Café Noir')", lambda: slugify('Café Noir'), 'cafe-noir')
@claim('T02')
def _(): return forall(strings('T02'), lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-') or repr(slugify(s)))
@claim('T03')
def _(): return forall(strings('T03'), lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slugify(s)) or repr(slugify(s)))
@claim('T04')
def _(): return forall(strings('T04'), lambda s: slugify(slugify(s)) == slugify(s) or f'{slugify(s)!r} -> {slugify(slugify(s))!r}')
@claim('T05')
def _():
    return forall([(s, n) for s in ('', 'a', 'ab', 'abc', 'abcd', 'abcdef', 'abcdefgh') for n in range(0, 11)],
                  lambda s, n: len(truncate(s, n)) <= n or f'truncate = {truncate(s, n)!r} (len {len(truncate(s, n))})')
@claim('T06')
def _(): return eq("truncate('abcdef', 5)", lambda: truncate('abcdef', 5), 'ab...')
@claim('T07')
def _():
    r = rng('T07')
    return forall([(s, n) for s in strings('T07', 500) for n in (len(s), len(s) + 1, len(s) + r.randint(0, 5))],
                  lambda s, n: truncate(s, n) == s)
@claim('T08')
def _(): return eq("count_words('a  b\\tc\\n')", lambda: count_words('a  b\tc\n'), 3)
@claim('T09')
def _(): return eq("count_words('')", lambda: count_words(''), 0)
@claim('T10')
def _(): return eq("title_case('a  b')", lambda: title_case('a  b'), 'A  B')
@claim('T11')
def _(): return eq("title_case('élan vital')", lambda: title_case('élan vital'), 'Élan Vital')
@claim('T12')
def _(): return forall(strings('T12'), lambda s: len(title_case(s)) == len(s) or f'title_case = {title_case(s)!r}')
@claim('T13')
def _(): return eq("strip_accents('Ação')", lambda: strip_accents('Ação'), 'Acao')
@claim('T14')
def _(): return eq("strip_accents('ø')", lambda: strip_accents('ø'), 'o')
@claim('T15')
def _(): return eq("pad_left('7', 3, '0')", lambda: pad_left('7', 3, '0'), '007')
@claim('T16')
def _():
    return forall([(s, n) for s in strings('T16', 800) for n in range(0, 16)],
                  lambda s, n: len(pad_left(s, n)) == max(len(s), n))
@claim('T17')
def _(): return eq("is_palindrome('')", lambda: is_palindrome(''), True)
@claim('T18')
def _(): return eq("is_palindrome('A man, a plan, a canal: Panama')", lambda: is_palindrome('A man, a plan, a canal: Panama'), True)
@claim('T19')
def _(): return forall(strings('T19', 8000, 8), lambda s: is_palindrome(s) == is_palindrome(s[::-1]))

if __name__ == '__main__':
    sys.exit(main())
