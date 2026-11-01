import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main, rng
from calc.textutil import truncate

ALPHA = ['a', 'b', ' ', 'é', '\t']

def test():
    # n ascending, then string length ascending: first hit is the smallest counterexample
    for n in range(0, 8):
        for length in range(0, 5):
            for tup in itertools.product(ALPHA, repeat=length):
                s = ''.join(tup)
                out = truncate(s, n)
                if len(out) > n:
                    return f"truncate({s!r}, {n}) == {out!r} has len {len(out)} > {n}"
    r = rng()
    for _ in range(20000):
        s = ''.join(chr(r.randint(0, 0x2FF)) for _ in range(r.randint(0, 40)))
        n = r.randint(0, 60)
        out = truncate(s, n)
        if len(out) > n:
            return f"truncate({s!r}, {n}) == {out!r} has len {len(out)} > {n}"
    return None

main("T3", test)
