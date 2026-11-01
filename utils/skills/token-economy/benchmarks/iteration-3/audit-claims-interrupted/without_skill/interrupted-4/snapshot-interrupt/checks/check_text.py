import json, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.text import (slugify, truncate, count_words, title_case, strip_accents,
                      pad_left, is_palindrome)

SEED = 20261101
N = 30000
ALPHA = list("abcXYZ019 -_\t\n.,:!") + list("éÇãøßİıŁñ") + ["́", "̈", "😀", "中", "ﬁ", "²", "Å", " "]


def rnd_str(r, maxlen=12):
    return ''.join(r.choice(ALPHA) for _ in range(r.randint(0, maxlen)))


def strings(tag, extra=()):
    r = random.Random(SEED + hash_tag(tag))
    fixed = ['', ' ', '-', '--', 'a', 'Café Noir', 'ß', 'é', 'ø', 'İ', 'ﬁ', '²', 'a  b', ' a ', '😀', 'é', '́', '中文'] + list(extra)
    yield from fixed
    for _ in range(N):
        yield rnd_str(r)


def hash_tag(t):
    return sum(ord(c) * (i + 1) for i, c in enumerate(t))


def universal(tag, pred, extra=()):
    for s in strings(tag, extra):
        try:
            ok, info = pred(s)
        except Exception as e:
            return False, f"input={s!r} raised {e!r}"
        if not ok:
            return False, f"input={s!r} {info}"
    return True, None


def eq(fn, args, expected):
    try:
        got = fn(*args)
    except Exception as e:
        return False, f"{fn.__name__}{args!r} raised {e!r}, expected {expected!r}"
    if got == expected and type(got) == type(expected):
        return True, None
    return False, f"{fn.__name__}{args!r} -> {got!r}, expected {expected!r}"


def t02(): return universal('T02', lambda s: (not slugify(s).startswith('-') and not slugify(s).endswith('-'), f"-> {slugify(s)!r}"))
def t03(): return universal('T03', lambda s: (all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slugify(s)), f"-> {slugify(s)!r}"))
def t04(): return universal('T04', lambda s: (slugify(slugify(s)) == slugify(s), f"-> {slugify(slugify(s))!r} vs {slugify(s)!r}"))


def t05():
    cases = [('abcdef', 2), ('abcdef', 0), ('abcdef', 1), ('abcdef', 3)]
    for s, n in cases:
        o = truncate(s, n)
        if len(o) > n:
            return False, f"truncate({s!r}, {n}) -> {o!r} (len {len(o)} > {n})"
    r = random.Random(SEED + 5)
    for _ in range(N):
        s = rnd_str(r, 15); n = r.randint(0, 12)
        try:
            o = truncate(s, n)
        except Exception as e:
            return False, f"truncate({s!r}, {n}) raised {e!r}"
        if len(o) > n:
            return False, f"truncate({s!r}, {n}) -> {o!r} (len {len(o)} > {n})"
    return True, None


def t07():
    r = random.Random(SEED + 7)
    for _ in range(N):
        s = rnd_str(r, 15); n = len(s) + r.randint(0, 3)
        if truncate(s, n) != s:
            return False, f"truncate({s!r}, {n}) -> {truncate(s, n)!r}"
    return True, None


def t12(): return universal('T12', lambda s: (len(title_case(s)) == len(s), f"-> {title_case(s)!r} len {len(title_case(s))} vs {len(s)}"))


def t16():
    r = random.Random(SEED + 16)
    for _ in range(N):
        s = rnd_str(r, 10); n = r.randint(0, 14)
        if len(pad_left(s, n)) != max(len(s), n):
            return False, f"pad_left({s!r}, {n}) -> {pad_left(s, n)!r}"
    return True, None


def t19(): return universal('T19', lambda s: (is_palindrome(s) == is_palindrome(s[::-1]), f"-> {is_palindrome(s)} vs reversed {is_palindrome(s[::-1])}"))


CHECKS = {
    'T01': lambda: eq(slugify, ('Café Noir',), 'cafe-noir'),
    'T02': t02, 'T03': t03, 'T04': t04, 'T05': t05,
    'T06': lambda: eq(truncate, ('abcdef', 5), 'ab...'),
    'T07': t07,
    'T08': lambda: eq(count_words, ('a  b\tc\n',), 3),
    'T09': lambda: eq(count_words, ('',), 0),
    'T10': lambda: eq(title_case, ('a  b',), 'A  B'),
    'T11': lambda: eq(title_case, ('élan vital',), 'Élan Vital'),
    'T12': t12,
    'T13': lambda: eq(strip_accents, ('Ação',), 'Acao'),
    'T14': lambda: eq(strip_accents, ('ø',), 'o'),
    'T15': lambda: eq(pad_left, ('7', 3, '0'), '007'),
    'T16': t16,
    'T17': lambda: eq(is_palindrome, ('',), True),
    'T18': lambda: eq(is_palindrome, ('A man, a plan, a canal: Panama',), True),
    'T19': t19,
}


def main():
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": ce,
                          "command": f"python3 checks/check_text.py {i}"}, ensure_ascii=False))


if __name__ == '__main__':
    main()
