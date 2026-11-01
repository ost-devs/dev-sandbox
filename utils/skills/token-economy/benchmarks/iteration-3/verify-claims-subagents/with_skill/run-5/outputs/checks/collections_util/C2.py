import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import dedupe

# Domain: hashable elements (dedupe relies on hashing). Claim has no stated domain.


def ref(xs):
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen


def test():
    alphabet = [0, 1, 2, "a"]
    for L in range(0, 7):
        for xs in itertools.product(alphabet, repeat=L):
            xs = list(xs)
            if dedupe(xs) != ref(xs):
                return f"xs={xs} -> {dedupe(xs)} expected {ref(xs)}"
    r = rng()
    for _ in range(3000):
        xs = [r.randint(0, 9) for _ in range(r.randint(0, 25))]
        if dedupe(xs) != ref(xs):
            return f"xs={xs} -> {dedupe(xs)} expected {ref(xs)}"
    return None


main("C2", test)
