import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import *
from kit.text import *
import re

def _eq(got, exp):
    return True if got == exp else (False, 'got %r, expected %r' % (got, exp))

@exact
def T01(): return _eq(slugify('Café Noir'), 'cafe-noir')

@prop
def T02(r):
    s = rand_str(r, 20); o = slugify(s)
    if o.startswith('-') or o.endswith('-'): return 's=%r -> %r' % (s, o)

@prop
def T03(r):
    s = rand_str(r, 20); o = slugify(s)
    if not re.fullmatch(r'[a-z0-9-]*', o): return 's=%r -> %r' % (s, o)

@prop
def T04(r):
    s = rand_str(r, 20); a = slugify(s); b = slugify(a)
    if a != b: return 's=%r -> %r -> %r' % (s, a, b)

@prop
def T05(r):
    s = rand_str(r, 20); n = rand_int(r, 0, 25); o = truncate(s, n)
    if len(o) > n: return 's=%r n=%d -> %r (len %d)' % (s, n, o, len(o))

@exact
def T06(): return _eq(truncate('abcdef', 5), 'ab...')

@prop
def T07(r):
    s = rand_str(r, 20); n = rand_int(r, len(s), len(s) + 5); o = truncate(s, n)
    if o != s: return 's=%r n=%d -> %r' % (s, n, o)

@exact
def T08(): return _eq(count_words('a  b\tc\n'), 3)

@exact
def T09(): return _eq(count_words(''), 0)

@exact
def T10(): return _eq(title_case('a  b'), 'A  B')

@exact
def T11(): return _eq(title_case('élan vital'), 'Élan Vital')

@prop
def T12(r):
    s = rand_str(r, 20); o = title_case(s)
    if len(o) != len(s): return 's=%r -> %r (len %d vs %d)' % (s, o, len(o), len(s))

@exact
def T13(): return _eq(strip_accents('Ação'), 'Acao')

@exact
def T14(): return _eq(strip_accents('ø'), 'o')

@exact
def T15(): return _eq(pad_left('7', 3, '0'), '007')

@prop
def T16(r):
    s = rand_str(r, 20); n = rand_int(r, 0, 25); o = pad_left(s, n)
    if len(o) != max(len(s), n): return 's=%r n=%d -> %r' % (s, n, o)

@exact
def T17(): return _eq(is_palindrome(''), True)

@exact
def T18(): return _eq(is_palindrome('A man, a plan, a canal: Panama'), True)

@prop
def T19(r):
    s = rand_str(r, 12)
    if is_palindrome(s) != is_palindrome(s[::-1]):
        return 's=%r: %r vs reversed %r' % (s, is_palindrome(s), is_palindrome(s[::-1]))

run({k: v for k, v in list(globals().items()) if re.fullmatch(r'T\d\d', k)})
