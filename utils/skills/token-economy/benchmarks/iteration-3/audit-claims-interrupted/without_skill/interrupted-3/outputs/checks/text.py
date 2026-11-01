import sys, os, json, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kit.text import (slugify, truncate, count_words, title_case,
                      strip_accents, pad_left, is_palindrome)

SEED = 20240611
N = 4000
ALPHABET = list("abcXYZ019 -_,.:\t\n") + ["é", "É", "ç", "ã", "ø", "ß", "İ", "ǆ", "ﬁ", "日", "本", "😀", "́", "٣", "²", " "]
EDGE_S = ["", " ", "  ", "-", "---", "a", "A", "é", "ß", "ø", "İ", "ﬁ", "日本", "😀", " a ", "a--b", "-a-", "Café Noir",
          "́", "á", "²", "٣", "ǆ", "A man, a plan", "ab", "aba", "abc", "\t\n", "ǅ"]
EDGE_N = [0, 1, 2, 3, 4, 5, 10]

def rnd_strings():
    r = random.Random(SEED)
    yield from EDGE_S
    for _ in range(N):
        yield "".join(r.choice(ALPHABET) for _ in range(r.randint(0, 12)))

def rnd_pairs():
    r = random.Random(SEED + 1)
    for s in EDGE_S:
        for n in EDGE_N:
            yield s, n
    for s in rnd_strings():
        yield s, r.randint(0, 15)

def pt(f, expected, got_fn=None):
    got = f()
    return None if got == expected else "obtido %r, esperado %r" % (got, expected)

def universal(pairs, pred, fmt):
    for args in pairs:
        try:
            ok, out = pred(*args) if isinstance(args, tuple) else pred(args)
        except Exception as e:
            return "entrada %r -> exceção %s: %s" % (args, type(e).__name__, e)
        if not ok:
            return "entrada %r -> saída %r" % (args, out)
    return None

def U1(pred):
    return lambda: universal(rnd_strings(), pred, None)
def U2(pred):
    return lambda: universal(rnd_pairs(), pred, None)

def pointwise(label, f, expected):
    def run():
        try:
            got = f()
        except Exception as e:
            return "%s -> exceção %s: %s" % (label, type(e).__name__, e)
        return None if got == expected else "%s -> %r (esperado %r)" % (label, got, expected)
    return run

def minimal(pairs_or_strs):
    return pairs_or_strs

CHECKS = {
 "T01": pointwise("slugify('Café Noir')", lambda: slugify('Café Noir'), 'cafe-noir'),
 "T02": U1(lambda s: (lambda o: (not o.startswith('-') and not o.endswith('-'), o))(slugify(s))),
 "T03": U1(lambda s: (lambda o: (all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in o), o))(slugify(s))),
 "T04": U1(lambda s: (lambda o: (slugify(o) == o, "slugify(slugify)=%r, slugify=%r" % (slugify(o), o)))(slugify(s))),
 "T05": U2(lambda s, n: (lambda o: (len(o) <= n, o))(truncate(s, n))),
 "T06": pointwise("truncate('abcdef', 5)", lambda: truncate('abcdef', 5), 'ab...'),
 "T07": U2(lambda s, n: (True, None) if len(s) > n else (truncate(s, n) == s, truncate(s, n))),
 "T08": pointwise("count_words('a  b\\tc\\n')", lambda: count_words('a  b\tc\n'), 3),
 "T09": pointwise("count_words('')", lambda: count_words(''), 0),
 "T10": pointwise("title_case('a  b')", lambda: title_case('a  b'), 'A  B'),
 "T11": pointwise("title_case('élan vital')", lambda: title_case('élan vital'), 'Élan Vital'),
 "T12": U1(lambda s: (lambda o: (len(o) == len(s), o))(title_case(s))),
 "T13": pointwise("strip_accents('Ação')", lambda: strip_accents('Ação'), 'Acao'),
 "T14": pointwise("strip_accents('ø')", lambda: strip_accents('ø'), 'o'),
 "T15": pointwise("pad_left('7', 3, '0')", lambda: pad_left('7', 3, '0'), '007'),
 "T16": U2(lambda s, n: (lambda o: (len(o) == max(len(s), n), o))(pad_left(s, n))),
 "T17": pointwise("is_palindrome('')", lambda: is_palindrome(''), True),
 "T18": pointwise("is_palindrome('A man, a plan, a canal: Panama')", lambda: is_palindrome('A man, a plan, a canal: Panama'), True),
 "T19": U1(lambda s: (is_palindrome(s) == is_palindrome(s[::-1]), "%r vs %r" % (is_palindrome(s), is_palindrome(s[::-1])))),
}

def shrink_report(cx):
    return cx

def main():
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        if i not in CHECKS:
            print(json.dumps({"id": i, "verdict": "falsa", "counterexample": "id desconhecido"}))
            continue
        cx = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if cx is None else "falsa", "counterexample": cx}, ensure_ascii=False))

main()
