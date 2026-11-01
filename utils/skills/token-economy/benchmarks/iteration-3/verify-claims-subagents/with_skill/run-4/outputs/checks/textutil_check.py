import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run, SEED
from calc.textutil import *

ALPHA = "abcXYZ019 -_!é\t\n…ß."

def rstr(rng, mx=8):
    return "".join(rng.choice(ALPHA) for _ in range(rng.randint(0, mx)))

def check_T1(rng):
    cases = ["", "-", "---", " a ", "!a!", "é", "-a-"] + [rstr(rng) for _ in range(3000)]
    for s in cases:
        r = slugify(s)
        if r.startswith("-") or r.endswith("-"):
            return False, repr(s)
    return True, None

def check_T2(rng):
    r = slugify('Café Noir')
    return (r == 'cafe-noir', None if r == 'cafe-noir' else f"slugify('Café Noir') == {r!r}")

def check_T3(rng):
    cases = [("", 0), ("a", 0), ("ab", 1), ("abc", 2)]
    cases += [(rstr(rng, 12), rng.randint(0, 12)) for _ in range(3000)]
    for s, n in cases:
        r = truncate(s, n)
        if len(r) > n:
            return False, f"truncate({s!r}, {n}) == {r!r}"
    return True, None

def check_T4(rng):
    r = count_words('a  b\tc\n')
    return (r == 3, None if r == 3 else repr(r))

def check_T5(rng):
    r = capitalize_words('a  b')
    return (r == 'A  B', None if r == 'A  B' else repr(r))

def check_T6(rng):
    r = is_palindrome('')
    return (r is True, None if r is True else repr(r))

run(globals())
