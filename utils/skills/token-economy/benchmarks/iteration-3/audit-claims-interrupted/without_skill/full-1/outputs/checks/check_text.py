import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import Results, rng
from kit.text import *

R = Results("text")
ALPHA = list("aAbZ09 -_.,:!\t\n") + ["é", "Ç", "ø", "ß", "İ", "K", "ñ", "日", "́", "ŉ", "ﬁ", "²", "😀", ""]
def strings(maxlen=3):
    for L in range(maxlen + 1):
        for t in itertools.product(ALPHA, repeat=L):
            yield "".join(t)
def rand_strings(k=3000):
    r = rng()
    for _ in range(k):
        yield "".join(r.choice(ALPHA) for _ in range(r.randint(0, 12)))
def allstr():
    yield from strings(3)
    yield from rand_strings()

def forall(pred):
    def fn():
        for s in allstr():
            if not pred(s):
                return False, s
        return True, None
    return fn
def eq(cid, got, exp):
    R.check(cid, lambda: (got() == exp, got()))

eq("T01", lambda: slugify("Café Noir"), "cafe-noir")
R.check("T02", forall(lambda s: not slugify(s).startswith("-") and not slugify(s).endswith("-")))
R.check("T03", forall(lambda s: all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slugify(s))))
R.check("T04", forall(lambda s: slugify(slugify(s)) == slugify(s)))

def t05():
    r = rng()
    for s in list(strings(2)) + ["abcdef", "abcdefghij"]:
        for n in range(0, 15):
            if len(truncate(s, n)) > n:
                return False, (s, n)
    return True, None
R.check("T05", t05)
eq("T06", lambda: truncate("abcdef", 5), "ab...")
def t07():
    for s in allstr():
        for n in range(len(s), len(s) + 3):
            if truncate(s, n) != s:
                return False, (s, n)
    return True, None
R.check("T07", t07)
eq("T08", lambda: count_words("a  b\tc\n"), 3)
eq("T09", lambda: count_words(""), 0)
eq("T10", lambda: title_case("a  b"), "A  B")
eq("T11", lambda: title_case("élan vital"), "Élan Vital")
R.check("T12", forall(lambda s: len(title_case(s)) == len(s)))
eq("T13", lambda: strip_accents("Ação"), "Acao")
eq("T14", lambda: strip_accents("ø"), "o")
eq("T15", lambda: pad_left("7", 3, "0"), "007")
def t16():
    for s in allstr():
        for n in range(0, 6):
            if len(pad_left(s, n)) != max(len(s), n):
                return False, (s, n)
    return True, None
R.check("T16", t16)
eq("T17", lambda: is_palindrome(""), True)
eq("T18", lambda: is_palindrome("A man, a plan, a canal: Panama"), True)
R.check("T19", forall(lambda s: is_palindrome(s) == is_palindrome(s[::-1])))
R.finish()
