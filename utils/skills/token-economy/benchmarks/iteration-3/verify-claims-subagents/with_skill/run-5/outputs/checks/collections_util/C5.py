import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import merge_dicts

# Claim: on a key present in both a and b, merge_dicts(a, b) keeps a's value.


def test():
    # exhaustive over shared key 'k' with values in {1, 2}, plus extra non-shared keys
    for va, vb in itertools.product([1, 2], repeat=2):
        a = {"k": va}
        b = {"k": vb}
        m = merge_dicts(a, b)
        if m["k"] != a["k"]:
            return f"a={a} b={b} -> {m}, expected value from a ({a['k']})"
    r = rng()
    for _ in range(2000):
        a = {k: r.randint(0, 9) for k in "kxy" if r.random() < 0.7}
        b = {k: r.randint(0, 9) for k in "kzw" if r.random() < 0.7}
        if "k" not in a or "k" not in b:
            continue
        m = merge_dicts(a, b)
        if m["k"] != a["k"]:
            return f"a={a} b={b} -> {m}, expected value from a ({a['k']})"
    return None


main("C5", test)
