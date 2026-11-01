import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import rotate


def test():
    # for every list xs: rotate(xs, len(xs)) == xs
    for L in range(0, 6):
        for xs in itertools.product([0, 1, 2], repeat=L):
            xs = list(xs)
            if rotate(xs, len(xs)) != xs:
                return f"xs={xs} -> {rotate(xs, len(xs))}"
    r = rng()
    for _ in range(3000):
        xs = [r.randint(-5, 5) for _ in range(r.randint(0, 30))]
        if rotate(xs, len(xs)) != xs:
            return f"xs={xs} -> {rotate(xs, len(xs))}"
    return None


main("C6", test)
