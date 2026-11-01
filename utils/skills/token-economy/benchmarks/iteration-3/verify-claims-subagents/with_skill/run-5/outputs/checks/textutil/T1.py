import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main, rng
from calc.textutil import slugify

ALPHA = ['-', 'a', 'Z', '1', ' ', '\t', '_', '.', 'é', 'İ', 'ß', '€', ' ']

def test():
    # exhaustive over short strings, shortest first (smallest counterexample first)
    for length in range(0, 4):
        for tup in itertools.product(ALPHA, repeat=length):
            s = ''.join(tup)
            r = slugify(s)
            if r.startswith('-') or r.endswith('-'):
                return f"slugify({s!r}) == {r!r}"
    r = rng()
    chars = ALPHA + [chr(c) for c in range(0x20, 0x250)]
    for _ in range(20000):
        s = ''.join(r.choice(chars) for _ in range(r.randint(0, 12)))
        out = slugify(s)
        if out.startswith('-') or out.endswith('-'):
            return f"slugify({s!r}) == {out!r}"
    return None

main("T1", test)
