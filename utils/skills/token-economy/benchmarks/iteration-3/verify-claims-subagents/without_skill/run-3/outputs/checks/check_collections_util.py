import os, sys, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
rng = random.Random(SEED)

def lists():
    yield []
    for L in range(0, 5):
        for t in itertools.product([0, 1, 2], repeat=L):
            yield list(t)
    for _ in range(300):
        yield [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]

def report(cid, cex):
    print(f"{cid} {'FALSE ' + cex if cex else 'TRUE'}")

def first_cex(gen):
    for c in gen:
        if c: return c
    return None

# C1
def c1():
    for xs in lists():
        for n in range(1, 15):
            r = chunk(xs, n)
            if [y for c in r for y in c] != xs:
                yield f"chunk({xs}, {n}) -> {r}"
report("C1", first_cex(c1()))

# C2 (hashable elements; order of first occurrences)
def c2():
    for xs in lists():
        exp = []
        for x in xs:
            if x not in exp: exp.append(x)
        if dedupe(xs) != exp:
            yield f"dedupe({xs}) -> {dedupe(xs)}"
report("C2", first_cex(c2()))

# C3
r = flatten([[1, [2]], [3]])
report("C3", None if r == [1, 2, 3] else f"flatten([[1, [2]], [3]]) -> {r}")

# C4 (every integer n, including negative)
def c4():
    for xs in lists():
        for n in range(-6, 15):
            r = top_n(xs, n)
            if len(r) != min(n, len(xs)):
                yield f"top_n({xs}, {n}) -> {r} (len {len(r)}, expected {min(n, len(xs))})"
cex = sorted(c4(), key=len)
report("C4", cex[0] if cex else None)

# C5
def c5():
    for a, b in [({'k': 1}, {'k': 2}), ({}, {}), ({'a': 1}, {})]:
        r = merge_dicts(a, b)
        for k in a:
            if k in b and r[k] != a[k]:
                yield f"merge_dicts({a}, {b}) -> {r}"
report("C5", first_cex(c5()))

# C6
def c6():
    for xs in lists():
        if rotate(xs, len(xs)) != xs:
            yield f"rotate({xs}, {len(xs)}) -> {rotate(xs, len(xs))}"
report("C6", first_cex(c6()))
