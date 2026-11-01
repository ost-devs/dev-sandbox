import json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.text import (slugify, truncate, count_words, title_case, strip_accents,
                      pad_left, is_palindrome)

SEED = 12345
ALPHA = list("abcXYZ019 -_\t\n.,:!?ÀéçãõøßİKﬁǅ́​€😀ñ") + ["", " "]


def samples(count=3000):
    r = random.Random(SEED)
    out = ["", " ", "-", "--", " a ", "ß", "ßa", "İ", "Café Noir", "ǆ", "ﬁ", "ø", "K"]
    for _ in range(count):
        out.append("".join(r.choice(ALPHA) for _ in range(r.randint(0, 12))))
    return out


def first_fail(pred, inputs):
    for x in inputs:
        try:
            if not pred(x):
                return x
        except Exception as e:
            return (x, repr(e))
    return None


def prop(pred, inputs, fmt):
    bad = first_fail(pred, inputs)
    if bad is None:
        return True, None
    return False, fmt(bad)


def eq(expr_val, expected):
    return (True, None) if expr_val == expected else (False, f"got {expr_val!r}, expected {expected!r}")


def check_T01(): return eq(slugify('Café Noir'), 'cafe-noir')
def check_T02(): return prop(lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'), samples(), lambda s: f"slugify({s!r})={slugify(s)!r}")
def check_T03(): return prop(lambda s: all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slugify(s)), samples(), lambda s: f"slugify({s!r})={slugify(s)!r}")
def check_T04(): return prop(lambda s: slugify(slugify(s)) == slugify(s), samples(), lambda s: f"s={s!r}")


def check_T05():
    r = random.Random(SEED)
    cases = [(s, n) for s in ["abcdef", "", "a"] for n in range(0, 8)]
    cases += [("".join(r.choice(ALPHA) for _ in range(r.randint(0, 12))), r.randint(0, 15)) for _ in range(3000)]
    bad = first_fail(lambda c: len(truncate(*c)) <= c[1], cases)
    if bad is None:
        return True, None
    s, n = bad
    return False, f"truncate({s!r}, {n})={truncate(s, n)!r} has len {len(truncate(s, n))} > {n}"


def check_T06(): return eq(truncate('abcdef', 5), 'ab...')


def check_T07():
    r = random.Random(SEED)
    cases = [(s, len(s) + r.randint(0, 3)) for s in samples()]
    return prop(lambda c: truncate(*c) == c[0], cases, lambda c: f"s={c[0]!r}, n={c[1]}")


def check_T08(): return eq(count_words('a  b\tc\n'), 3)
def check_T09(): return eq(count_words(''), 0)
def check_T10(): return eq(title_case('a  b'), 'A  B')
def check_T11(): return eq(title_case('élan vital'), 'Élan Vital')
def check_T12(): return prop(lambda s: len(title_case(s)) == len(s), samples(), lambda s: f"title_case({s!r})={title_case(s)!r}")
def check_T13(): return eq(strip_accents('Ação'), 'Acao')
def check_T14(): return eq(strip_accents('ø'), 'o')
def check_T15(): return eq(pad_left('7', 3, '0'), '007')


def check_T16():
    r = random.Random(SEED)
    cases = [(s, r.randint(0, 15)) for s in samples()]
    cases += [("", 0), ("abc", 0), ("abc", 3)]
    bad = first_fail(lambda c: len(pad_left(*c)) == max(len(c[0]), c[1]), cases)
    return (True, None) if bad is None else (False, f"pad_left({bad[0]!r}, {bad[1]})")


def check_T17(): return eq(is_palindrome(''), True)
def check_T18(): return eq(is_palindrome('A man, a plan, a canal: Panama'), True)
def check_T19(): return prop(lambda s: is_palindrome(s) == is_palindrome(s[::-1]), samples(), lambda s: f"s={s!r}")


def main():
    ids = sys.argv[1:] or sorted(k[6:] for k in globals() if k.startswith("check_"))
    for i in ids:
        ok, ce = globals()["check_" + i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ok else "falsa", "counterexample": ce,
                          "command": f"python3 -I checks/text.py {i}"}, ensure_ascii=True))


main()
