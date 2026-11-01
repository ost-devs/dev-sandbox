import os, sys, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
rng = random.Random(SEED)
print("seed", SEED)

def first_fail(cases, pred):
    """pred(case) -> True ok; exception counts as counterexample."""
    for c in cases:
        try:
            if not pred(c):
                return "%r -> wrong result" % (c,)
        except Exception as e:
            return "%r -> raises %s: %s" % (c, type(e).__name__, e)
    return None

def report(cid, ce):
    print(cid, "VERDADEIRA" if ce is None else "FALSA", "-" if ce is None else ce)

lists = [[], [1], [1, 1], [1, 2, 3], [None], [[1], [2]], list(range(10))]
lists += [[rng.randint(0, 5) for _ in range(rng.randint(0, 12))] for _ in range(200)]

# C1
cases = [(xs, n) for xs in lists for n in range(1, 15)]
report("C1", first_fail(cases, lambda c: [y for p in chunk(*c) for y in p] == c[0]))

# C2: order of first occurrences
def c2(xs):
    exp, seen = [], []
    for x in xs:
        if x not in seen:
            seen.append(x); exp.append(x)
    return dedupe(xs) == exp
# claim speaks of first occurrences (needs hashable items); unhashable input is noted, not a verdict
c2cases = [xs for xs in lists if all(isinstance(x, (int, type(None))) for x in xs)] + [[3, 1, 3, 2, 1], [1, True, 1.0], ['b', 'a', 'b']]
report("C2", first_fail(c2cases, c2))

# C3
report("C3", first_fail([[[1, [2]], [3]]], lambda x: flatten(x) == [1, 2, 3]))

# C4
cases = [([3, 1, 2], -1)] + [(xs, n) for xs in lists for n in range(-5, 20)]
report("C4", first_fail(cases, lambda c: len(top_n(*c)) == min(c[1], len(c[0]))))

# C5
report("C5", first_fail([({"k": 1}, {"k": 2}), ({"k": "a"}, {"k": "b"})],
                        lambda c: merge_dicts(*c)["k"] == c[0]["k"]))

# C6
report("C6", first_fail(lists, lambda xs: rotate(xs, len(xs)) == xs))
