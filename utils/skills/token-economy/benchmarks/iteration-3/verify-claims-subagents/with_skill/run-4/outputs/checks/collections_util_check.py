import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run, SEED
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate


def _lists(rng):
    yield []
    yield [1]
    for _ in range(300):
        yield [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]


def check_C1(rng):
    for xs in _lists(rng):
        for n in range(1, 15):
            r = chunk(xs, n)
            if [y for c in r for y in c] != xs:
                return False, repr((xs, n))
    return True, None


def check_C2(rng):
    for xs in _lists(rng):
        exp = []
        for x in xs:
            if x not in exp:
                exp.append(x)
        if dedupe(xs) != exp:
            return False, repr(xs)
    return True, None


def check_C3(rng):
    r = flatten([[1, [2]], [3]])
    if r != [1, 2, 3]:
        return False, f"flatten([[1, [2]], [3]]) == {r!r}"
    return True, None


def check_C4(rng):
    for xs in _lists(rng):
        for n in range(-3, 15):
            r = top_n(xs, n)
            if len(r) != min(n, len(xs)):
                return False, f"top_n({xs!r}, {n}) -> {r!r}, len {len(r)} != {min(n, len(xs))}"
    return True, None


def check_C5(rng):
    a, b = {'k': 'a'}, {'k': 'b'}
    r = merge_dicts(a, b)
    if r['k'] != a['k']:
        return False, f"merge_dicts({a!r}, {b!r}) == {r!r}"
    return True, None


def check_C6(rng):
    for xs in _lists(rng):
        if rotate(xs, len(xs)) != xs:
            return False, repr(xs)
    return True, None


if __name__ == "__main__":
    run(globals())
