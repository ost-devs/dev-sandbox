import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _lib import claim, rng, rand_str, main
from kit.text import *

EDGE = ["", "-", " a ", "  ", "ß", "İ", "ﬁ", "é", "---", "a--b", "漢字", "😀", "\n", "A-", "-A"]
def inputs(cid):
    r = rng(cid)
    return EDGE + [rand_str(r) for _ in range(3000)]

def eq(cid, expr, got, want):
    if got != want:
        return f"{expr} = {got!r}, expected {want!r}"

@claim("T01")
def t01(): return eq("T01", "slugify('Café Noir')", slugify('Café Noir'), 'cafe-noir')

@claim("T02")
def t02():
    for s in inputs("T02"):
        o = slugify(s)
        if o.startswith("-") or o.endswith("-"): return f"slugify({s!r}) = {o!r}"

@claim("T03")
def t03():
    ok = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    for s in inputs("T03"):
        o = slugify(s)
        if not set(o) <= ok: return f"slugify({s!r}) = {o!r}"

@claim("T04")
def t04():
    for s in inputs("T04"):
        o = slugify(s)
        if slugify(o) != o: return f"slugify({s!r}) = {o!r}, again = {slugify(o)!r}"

@claim("T05")
def t05():
    r = rng("T05")
    for s in inputs("T05"):
        for n in [0, 1, 2, 3, 4, 5, 10, r.randint(0, 20)]:
            o = truncate(s, n)
            if len(o) > n: return f"truncate({s!r}, {n}) = {o!r} (len {len(o)} > {n})"

@claim("T06")
def t06(): return eq("T06", "truncate('abcdef', 5)", truncate('abcdef', 5), 'ab...')

@claim("T07")
def t07():
    for s in inputs("T07"):
        for n in range(len(s), len(s) + 3):
            if truncate(s, n) != s: return f"truncate({s!r}, {n}) = {truncate(s, n)!r}"

@claim("T08")
def t08(): return eq("T08", "count_words('a  b\\tc\\n')", count_words('a  b\tc\n'), 3)

@claim("T09")
def t09(): return eq("T09", "count_words('')", count_words(''), 0)

@claim("T10")
def t10(): return eq("T10", "title_case('a  b')", title_case('a  b'), 'A  B')

@claim("T11")
def t11(): return eq("T11", "title_case('élan vital')", title_case('élan vital'), 'Élan Vital')

@claim("T12")
def t12():
    for s in inputs("T12"):
        o = title_case(s)
        if len(o) != len(s): return f"title_case({s!r}) = {o!r} (len {len(o)} != {len(s)})"

@claim("T13")
def t13(): return eq("T13", "strip_accents('Ação')", strip_accents('Ação'), 'Acao')

@claim("T14")
def t14(): return eq("T14", "strip_accents('ø')", strip_accents('ø'), 'o')

@claim("T15")
def t15(): return eq("T15", "pad_left('7', 3, '0')", pad_left('7', 3, '0'), '007')

@claim("T16")
def t16():
    r = rng("T16")
    for s in inputs("T16"):
        for n in [0, 1, 5, r.randint(0, 20)]:
            o = pad_left(s, n)
            if len(o) != max(len(s), n): return f"pad_left({s!r}, {n}) = {o!r}"

@claim("T17")
def t17(): return eq("T17", "is_palindrome('')", is_palindrome(''), True)

@claim("T18")
def t18(): return eq("T18", "is_palindrome('A man, a plan, a canal: Panama')", is_palindrome('A man, a plan, a canal: Panama'), True)

@claim("T19")
def t19():
    for s in inputs("T19"):
        if is_palindrome(s) != is_palindrome(s[::-1]): return f"is_palindrome({s!r}) != is_palindrome({s[::-1]!r})"

if __name__ == "__main__":
    main()
