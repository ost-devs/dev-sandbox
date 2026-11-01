import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import rng, main
from calc.collections_util import flatten


def test():
    got = flatten([[1, [2]], [3]])
    if got != [1, 2, 3]:
        return f"flatten([[1, [2]], [3]]) -> {got}, expected [1, 2, 3]"
    return None


main("C3", test)
