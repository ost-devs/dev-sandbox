#!/usr/bin/env python3
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.text import *

SEED = 12345
N = 3000
ALPHA = list("abcXYZ019 -_\t\n.,:é Ç ñßøİﬁ́ 日本!") + ['Ação', 'ǅ']
EDGE = ['', ' ', '-', '--', 'a', 'A', ' a ', 'é', 'ß', 'ø', 'İ', 'ﬁ', 'ǅ', '日本', '-a-', 'a--b', '́',
        'Café Noir', 'a  b', '\t', '\n', 'ǆ', 'ŉ', 'ǰ', '٣', '²', 'ａ']

def strings():
    r = random.Random(SEED)
    for e in EDGE:
        yield e
    for _ in range(N):
        yield ''.join(r.choice(ALPHA) for _ in range(r.randint(0, 8)))

def forall(pred, gen):
    """return None if holds, else repr of first (minimal-length) counterexample string"""
    best = None
    for s in gen:
        if not pred(s):
            if best is None or len(s) < len(best[0]):
                best = (s,)
    return best

def res(ok, ce=None):
    return (ok, None if ok else ce)

def eq(expr_str, got, exp):
    return res(got == exp and type(got) == type(exp), f"{expr_str} -> {got!r}, esperado {exp!r}")

def cx_slug(prop, name):
    b = forall(prop, strings())
    if b is None: return res(True)
    return res(False, f"s={b[0]!r}: {name}")

def T01(): return eq("slugify('Café Noir')", slugify('Café Noir'), 'cafe-noir')
def T02():
    b = forall(lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'), strings())
    return res(b is None, b and f"s={b[0]!r} -> {slugify(b[0])!r}")
def T03():
    ok = lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slugify(s))
    b = forall(ok, strings())
    return res(b is None, b and f"s={b[0]!r} -> {slugify(b[0])!r}")
def T04():
    b = forall(lambda s: slugify(slugify(s)) == slugify(s), strings())
    return res(b is None, b and f"s={b[0]!r}: slugify(slugify(s))={slugify(slugify(b[0]))!r} vs {slugify(b[0])!r}")
def T05():
    best = None
    for n in range(0, 12):
        for L in range(0, 12):
            s = 'a' * L
            t = truncate(s, n)
            if len(t) > n and (best is None or (n, L) < best[0]):
                best = ((n, L), s, t)
    if best is None:
        r = random.Random(SEED)
        for _ in range(N):
            s = ''.join(r.choice('abé ') for _ in range(r.randint(0, 20))); n = r.randint(0, 25)
            if len(truncate(s, n)) > n: best = (None, s, truncate(s, n), n); break
    if best is None: return res(True)
    (nl, s, t) = best[:3]
    n = nl[0] if nl else best[3]
    return res(False, f"truncate({s!r}, {n}) = {t!r} (len {len(t)}) > {n}")
def T06(): return eq("truncate('abcdef',5)", truncate('abcdef', 5), 'ab...')
def T07():
    r = random.Random(SEED)
    for s in list(strings()):
        for n in range(len(s), len(s) + 4):
            if truncate(s, n) != s: return res(False, f"truncate({s!r},{n}) = {truncate(s,n)!r}")
    return res(True)
def T08(): return eq("count_words('a  b\\tc\\n')", count_words('a  b\tc\n'), 3)
def T09(): return eq("count_words('')", count_words(''), 0)
def T10(): return eq("title_case('a  b')", title_case('a  b'), 'A  B')
def T11(): return eq("title_case('élan vital')", title_case('élan vital'), 'Élan Vital')
def T12():
    b = forall(lambda s: len(title_case(s)) == len(s), strings())
    return res(b is None, b and f"s={b[0]!r} -> {title_case(b[0])!r} (len {len(title_case(b[0]))} vs {len(b[0])})")
def T13(): return eq("strip_accents('Ação')", strip_accents('Ação'), 'Acao')
def T14(): return eq("strip_accents('ø')", strip_accents('ø'), 'o')
def T15(): return eq("pad_left('7',3,'0')", pad_left('7', 3, '0'), '007')
def T16():
    for s in strings():
        for n in range(0, 12):
            if len(pad_left(s, n)) != max(len(s), n):
                return res(False, f"pad_left({s!r},{n}) = {pad_left(s,n)!r}")
    return res(True)
def T17(): return eq("is_palindrome('')", is_palindrome(''), True)
def T18(): return eq("is_palindrome('A man, a plan, a canal: Panama')", is_palindrome('A man, a plan, a canal: Panama'), True)
def T19():
    b = forall(lambda s: is_palindrome(s) == is_palindrome(s[::-1]), strings())
    return res(b is None, b and f"s={b[0]!r}")

CHECKS = {f"T{i:02d}": globals()[f"T{i:02d}"] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce}, ensure_ascii=False))
