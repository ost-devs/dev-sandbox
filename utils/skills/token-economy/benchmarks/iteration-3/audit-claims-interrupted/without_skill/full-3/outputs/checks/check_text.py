import sys, os, json, random, string
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.text import *

SEED = 1234
EDGE = ['', ' ', '-', '--', 'a', 'A', 'é', 'ø', 'ß', 'İ', 'ǆ', 'ŉ', 'K', '日本語', '😀', 'a b', 'a  b', ' a ', '-a-', 'Café Noir',
        'ǅ', 'ß', 'ﬁ', 'x́', '\t\n', 'a b', 'ı', '١٢٣', '²', 'ª', 'Ⅳ']
ALPHA = string.ascii_letters + string.digits + ' -_.,:\t\n' + 'éÉøßİıǆﬁ日😀́K²Ⅳ١'

def strings(rng, n=3000):
    out = list(EDGE)
    for _ in range(n):
        out.append(''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 12))))
    return out

def res(id, ok, ce=''):
    print(json.dumps({"id": id, "verdict": "verdadeira" if ok else "falsa", "counterexample": "" if ok else ce, "note": ""}, ensure_ascii=False))

def prop(id, pred, gen=None):
    rng = random.Random(SEED)
    cases = strings(rng)
    cases.sort(key=len)
    for s in cases:
        try:
            ok, info = pred(s)
        except Exception as e:
            res(id, False, f"input {s!r}: exception {e!r}"); return
        if not ok:
            res(id, False, f"input {s!r}: {info}"); return
    res(id, True)

def eq(id, f, expected):
    try:
        a = f()
    except Exception as e:
        res(id, False, f"exception {e!r}"); return
    res(id, a == expected, f"actual {a!r} vs claimed {expected!r}")

def T01(): eq('T01', lambda: slugify('Café Noir'), 'cafe-noir')
def T02(): prop('T02', lambda s: (not slugify(s).startswith('-') and not slugify(s).endswith('-'), f"slugify={slugify(s)!r}"))
def T03():
    import re
    prop('T03', lambda s: (re.fullmatch(r'[a-z0-9-]*', slugify(s)) is not None, f"slugify={slugify(s)!r}"))
def T04(): prop('T04', lambda s: (slugify(slugify(s)) == slugify(s), f"{slugify(s)!r} vs {slugify(slugify(s))!r}"))
def T05():
    rng = random.Random(SEED)
    cases = [(s, n) for s in ['', 'a', 'abc', 'abcdef', 'é日😀xyz'] for n in range(0, 8)]
    cases += [(''.join(rng.choice(ALPHA) for _ in range(rng.randint(0, 15))), rng.randint(0, 20)) for _ in range(3000)]
    cases.sort(key=lambda c: (len(c[0]), c[1]))
    for s, n in cases:
        try:
            r = truncate(s, n)
        except Exception as e:
            res('T05', False, f"truncate({s!r}, {n}) raised {e!r}"); return
        if len(r) > n:
            res('T05', False, f"truncate({s!r}, {n}) = {r!r} len {len(r)} > {n}"); return
    res('T05', True)
def T06(): eq('T06', lambda: truncate('abcdef', 5), 'ab...')
def T07():
    rng = random.Random(SEED)
    for s in strings(rng):
        for n in (len(s), len(s) + 1, len(s) + 10):
            if truncate(s, n) != s:
                res('T07', False, f"truncate({s!r},{n})={truncate(s,n)!r}"); return
    res('T07', True)
def T08(): eq('T08', lambda: count_words('a  b\tc\n'), 3)
def T09(): eq('T09', lambda: count_words(''), 0)
def T10(): eq('T10', lambda: title_case('a  b'), 'A  B')
def T11(): eq('T11', lambda: title_case('élan vital'), 'Élan Vital')
def T12(): prop('T12', lambda s: (len(title_case(s)) == len(s), f"title_case={title_case(s)!r} len {len(title_case(s))} vs {len(s)}"))
def T13(): eq('T13', lambda: strip_accents('Ação'), 'Acao')
def T14(): eq('T14', lambda: strip_accents('ø'), 'o')
def T15(): eq('T15', lambda: pad_left('7', 3, '0'), '007')
def T16():
    rng = random.Random(SEED)
    for s in strings(rng):
        for n in (0, 1, 2, 5, 13):
            r = pad_left(s, n)
            if len(r) != max(len(s), n):
                res('T16', False, f"pad_left({s!r},{n})={r!r}"); return
    res('T16', True)
def T17(): eq('T17', lambda: is_palindrome(''), True)
def T18(): eq('T18', lambda: is_palindrome('A man, a plan, a canal: Panama'), True)
def T19(): prop('T19', lambda s: (is_palindrome(s) == is_palindrome(s[::-1]), f"{is_palindrome(s)} vs {is_palindrome(s[::-1])}"))

if __name__ == '__main__':
    ids = sys.argv[1:] or [f'T{i:02d}' for i in range(1, 20)]
    for i in ids:
        globals()[i]()
