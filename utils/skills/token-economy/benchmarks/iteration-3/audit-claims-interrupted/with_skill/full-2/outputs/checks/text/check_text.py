import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.text import *
import re

S = lambda r: (rand_str(r),)
SN = lambda r: (rand_str(r), r.randint(0, 15))

def eq(a, b):
    assert a == b, f"got {a!r}, expected {b!r}"

@claim("T01")
def t01(): eq(slugify('Café Noir'), 'cafe-noir')
@claim("T02")
def t02(): forall("T02", S, lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'))
@claim("T03")
def t03(): forall("T03", S, lambda s: re.fullmatch(r'[a-z0-9-]*', slugify(s)) is not None)
@claim("T04")
def t04(): forall("T04", S, lambda s: slugify(slugify(s)) == slugify(s))
@claim("T05")
def t05():
    def pred(s, n):
        return len(truncate(s, n)) <= n
    forall("T05", SN, pred)
@claim("T06")
def t06(): eq(truncate('abcdef', 5), 'ab...')
@claim("T07")
def t07(): forall("T07", lambda r: (rand_str(r), r.randint(0, 15)), lambda s, n: len(s) > n or truncate(s, n) == s)
@claim("T08")
def t08(): eq(count_words('a  b\tc\n'), 3)
@claim("T09")
def t09(): eq(count_words(''), 0)
@claim("T10")
def t10(): eq(title_case('a  b'), 'A  B')
@claim("T11")
def t11(): eq(title_case('élan vital'), 'Élan Vital')
@claim("T12")
def t12(): forall("T12", S, lambda s: len(title_case(s)) == len(s))
@claim("T13")
def t13(): eq(strip_accents('Ação'), 'Acao')
@claim("T14")
def t14(): eq(strip_accents('ø'), 'o')
@claim("T15")
def t15(): eq(pad_left('7', 3, '0'), '007')
@claim("T16")
def t16(): forall("T16", SN, lambda s, n: len(pad_left(s, n)) == max(len(s), n))
@claim("T17")
def t17(): assert is_palindrome('') is True
@claim("T18")
def t18(): assert is_palindrome('A man, a plan, a canal: Panama') is True
@claim("T19")
def t19(): forall("T19", S, lambda s: is_palindrome(s) == is_palindrome(s[::-1]))

if __name__=='__main__': main('text')
