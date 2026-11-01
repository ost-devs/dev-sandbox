import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import top_n

# Claim: for every list xs and every integer n, len(top_n(xs, n)) == min(n, len(xs)).
# Test is exhaustive over small int lists and integers n in [-3, 8], plus seeded random.


def test():
    for L in range(0, 5):
        for xs in itertools.product([0, 1, 2], repeat=L):
            xs = list(xs)
            for n in range(-3, 9):
                out = top_n(xs, n)
                expected = min(n, len(xs))
                if len(out) != expected:
                    return f"xs={xs} n={n} -> len {len(out)}, expected min(n, len(xs)) = {expected}"
    r = rng()
    for _ in range(2000):
        xs = [r.randint(-5, 5) for _ in range(r.randint(0, 20))]
        n = r.randint(-5, 25)
        out = top_n(xs, n)
        if len(out) != min(n, len(xs)):
            return f"xs={xs} n={n} -> len {len(out)}, expected min(n, len(xs)) = {min(n, len(xs))}"
    return None


main("C4", test)
