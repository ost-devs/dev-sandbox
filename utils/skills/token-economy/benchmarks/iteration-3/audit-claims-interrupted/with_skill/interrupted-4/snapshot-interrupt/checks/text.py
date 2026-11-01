from lib import strings, ints, first_fail, eq
from kit.text import *
import re


def pairs(tag):
    ns = list(ints(tag + 'n', n=60, lo=0, hi=15))
    ns = [n for n in ns if n >= 0]
    for s in strings(tag, n=300):
        for n in ns[:8]:
            yield (s, n)
    for s in ['abcdef', 'ab', '', 'x' * 10]:
        for n in range(0, 12):
            yield (s, n)


CHECKS = {
    'T01': lambda: eq(lambda: slugify('Café Noir'), 'cafe-noir', "slugify('Café Noir')"),
    'T02': lambda: first_fail(strings('t2'), lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-')),
    'T03': lambda: first_fail(strings('t3'), lambda s: re.fullmatch(r'[a-z0-9-]*', slugify(s)) is not None),
    'T04': lambda: first_fail(strings('t4'), lambda s: slugify(slugify(s)) == slugify(s)),
    'T05': lambda: first_fail(pairs('t5'), lambda p: len(truncate(*p)) <= p[1]),
    'T06': lambda: eq(lambda: truncate('abcdef', 5), 'ab...', "truncate('abcdef',5)"),
    'T07': lambda: first_fail(((s, n) for s, n in pairs('t7') if len(s) <= n), lambda p: truncate(*p) == p[0]),
    'T08': lambda: eq(lambda: count_words('a  b\tc\n'), 3, 'count_words'),
    'T09': lambda: eq(lambda: count_words(''), 0, "count_words('')"),
    'T10': lambda: eq(lambda: title_case('a  b'), 'A  B', "title_case('a  b')"),
    'T11': lambda: eq(lambda: title_case('élan vital'), 'Élan Vital', "title_case('élan vital')"),
    'T12': lambda: first_fail(strings('t12'), lambda s: len(title_case(s)) == len(s)),
    'T13': lambda: eq(lambda: strip_accents('Ação'), 'Acao', "strip_accents('Ação')"),
    'T14': lambda: eq(lambda: strip_accents('ø'), 'o', "strip_accents('ø')"),
    'T15': lambda: eq(lambda: pad_left('7', 3, '0'), '007', "pad_left('7',3,'0')"),
    'T16': lambda: first_fail(((s, n) for s in strings('t16', n=300) for n in range(0, 8)),
                              lambda p: len(pad_left(*p)) == max(len(p[0]), p[1])),
    'T17': lambda: eq(lambda: is_palindrome(''), True, "is_palindrome('')"),
    'T18': lambda: eq(lambda: is_palindrome('A man, a plan, a canal: Panama'), True, 'panama'),
    'T19': lambda: first_fail(strings('t19'), lambda s: is_palindrome(s) == is_palindrome(s[::-1])),
}
