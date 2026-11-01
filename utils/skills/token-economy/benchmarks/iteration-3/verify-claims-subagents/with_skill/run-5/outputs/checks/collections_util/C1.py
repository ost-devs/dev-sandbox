import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import chunk


def concat(parts):
    out = []
    for p in parts:
        out += p
    return out


def test():
    # for every list xs and n >= 1: concat(chunk(xs, n)) == xs
    for L in range(0, 7):
        xs = list(range(L))
        for n in range(1, 9):
            if concat(chunk(xs, n)) != xs:
                return f"xs={xs} n={n} -> {concat(chunk(xs, n))}"
    r = rng()
    for _ in range(3000):
        xs = [r.randint(-5, 5) for _ in range(r.randint(0, 30))]
        n = r.randint(1, 35)
        if concat(chunk(xs, n)) != xs:
            return f"xs={xs} n={n}"
    return None


main("C1", test)
