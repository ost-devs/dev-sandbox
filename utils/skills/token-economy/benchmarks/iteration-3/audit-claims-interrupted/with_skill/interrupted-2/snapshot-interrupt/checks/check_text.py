import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from kit import text


S = lambda r: gen_str(r, 14)
U = lambda r: gen_str(r, 10, "aßŉǆİ ÉéAz-9_ \u00e7\u0301ø\u2014")
T = text

@claim("T01")
def t01(): return eq(T.slugify('Café Noir'), 'cafe-noir')
@claim("T02")
def t02(): return forall(lambda r: (U(r) if r.random()<.5 else S(r),), lambda s: not (T.slugify(s).startswith('-') or T.slugify(s).endswith('-')))
@claim("T03")
def t03(): return forall(lambda r: (U(r) if r.random()<.5 else S(r),), lambda s: re.fullmatch(r'[a-z0-9-]*', T.slugify(s)) is not None)
@claim("T04")
def t04(): return forall(lambda r: (U(r) if r.random()<.5 else S(r),), lambda s: T.slugify(T.slugify(s)) == T.slugify(s))
@claim("T05")
def t05(): return forall(lambda r: (S(r), r.randint(0, 12)), lambda s, n: len(T.truncate(s, n)) <= n)
@claim("T06")
def t06(): return eq(T.truncate('abcdef', 5), 'ab...')
@claim("T07")
def t07(): return forall(lambda r: (lambda s: (s, len(s) + r.randint(0, 3)))(S(r)), lambda s, n: T.truncate(s, n) == s)
@claim("T08")
def t08(): return eq(T.count_words('a  b\tc\n'), 3)
@claim("T09")
def t09(): return eq(T.count_words(''), 0)
@claim("T10")
def t10(): return eq(T.title_case('a  b'), 'A  B')
@claim("T11")
def t11(): return eq(T.title_case('élan vital'), 'Élan Vital')
@claim("T12")
def t12(): return forall(lambda r: (U(r),), lambda s: len(T.title_case(s)) == len(s))
@claim("T13")
def t13(): return eq(T.strip_accents('Ação'), 'Acao')
@claim("T14")
def t14(): return eq(T.strip_accents('ø'), 'o')
@claim("T15")
def t15(): return eq(T.pad_left('7', 3, '0'), '007')
@claim("T16")
def t16(): return forall(lambda r: (S(r), r.randint(0, 20)), lambda s, n: len(T.pad_left(s, n)) == max(len(s), n))
@claim("T17")
def t17(): return None if T.is_palindrome('') is True else f"got {T.is_palindrome('')!r}"
@claim("T18")
def t18(): return None if T.is_palindrome('A man, a plan, a canal: Panama') is True else "not True"
@claim("T19")
def t19(): return forall(lambda r: (U(r) if r.random()<.5 else S(r),), lambda s: T.is_palindrome(s) == T.is_palindrome(s[::-1]))

if __name__ == "__main__":
    main("text")
