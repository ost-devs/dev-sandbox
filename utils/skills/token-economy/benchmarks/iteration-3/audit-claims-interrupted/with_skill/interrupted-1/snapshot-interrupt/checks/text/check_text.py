import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import *; from kit import text as M
import re

def T01(): return eq(lambda: M.slugify('Café Noir'), 'cafe-noir')
def T02(): return forall('T02', gen_str, lambda s: not M.slugify(s).startswith('-') and not M.slugify(s).endswith('-'))
def T03(): return forall('T03', gen_str, lambda s: re.fullmatch(r'[a-z0-9-]*', M.slugify(s)) is not None)
def T04(): return forall('T04', gen_str, lambda s: M.slugify(M.slugify(s)) == M.slugify(s))
def T05():
    for s in ['', 'a', 'abcdef']:
        for n in range(0, 8):
            if len(M.truncate(s, n)) > n: return f'args={(s,n)!r} -> {M.truncate(s,n)!r}'
    return forall('T05', lambda r: (gen_str(r), gen_int(r, 0, 20)), lambda s, n: len(M.truncate(s, n)) <= n)
def T06(): return eq(lambda: M.truncate('abcdef', 5), 'ab...')
def T07(): return forall('T07', lambda r: (gen_str(r), gen_int(r, 0, 20)), lambda s, n: len(s) > n or M.truncate(s, n) == s)
def T08(): return eq(lambda: M.count_words('a  b\tc\n'), 3)
def T09(): return eq(lambda: M.count_words(''), 0)
def T10(): return eq(lambda: M.title_case('a  b'), 'A  B')
def T11(): return eq(lambda: M.title_case('élan vital'), 'Élan Vital')
def T12():
    for s in ['ß', 'ßa', 'ǆ']:
        if len(M.title_case(s)) != len(s): return f'args={(s,)!r} -> {M.title_case(s)!r}'
    return forall('T12', gen_str, lambda s: len(M.title_case(s)) == len(s))
def T13(): return eq(lambda: M.strip_accents('Ação'), 'Acao')
def T14(): return eq(lambda: M.strip_accents('ø'), 'o')
def T15(): return eq(lambda: M.pad_left('7', 3, '0'), '007')
def T16(): return forall('T16', lambda r: (gen_str(r), gen_int(r, 0, 20)), lambda s, n: len(M.pad_left(s, n)) == max(len(s), n))
def T17(): return eq(lambda: M.is_palindrome(''), True)
def T18(): return eq(lambda: M.is_palindrome('A man, a plan, a canal: Panama'), True)
def T19(): return forall('T19', gen_str, lambda s: M.is_palindrome(s) == M.is_palindrome(s[::-1]))

run('text', {f'T{i:02d}': globals()[f'T{i:02d}'] for i in range(1, 20)})
