"""Verifica C1-C6 de calc/collections_util.py. Execute da raiz: python3 checks/check_collections_util.py"""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
rng = random.Random(SEED)


def lists():
    """Listas deterministicas: vazia, pequenas com duplicatas, aleatorias (semente fixa)."""
    yield []
    for L in range(1, 5):
        for t in itertools.product([0, 1, 2], repeat=L):
            yield list(t)
    for _ in range(200):
        yield [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]


def unhashable_lists():
    yield [[1]]
    yield [[1], [1]]
    yield [{"a": 1}, 2]


def first(pred_gen):
    for r in pred_gen:
        if r is not None:
            return r
    return None


def report(cid, ce):
    print(f"{cid} VERDADEIRA" if ce is None else f"{cid} FALSA contraexemplo={ce!r}")


def safe(f, *a):
    try:
        return ("ok", f(*a))
    except Exception as e:
        return ("exc", type(e).__name__)


# C1
def c1():
    for xs in lists():
        for n in range(1, len(xs) + 4):
            r = safe(chunk, xs, n)
            if r[0] == "exc" or [y for c in r[1] for y in c] != xs:
                yield (xs, n, r)
report("C1", first(c1()))


# C2: ordem da primeira ocorrencia (itens hasheaveis; a afirmacao fala de ordem,
# nao de aceitar nao hasheaveis, que lancam TypeError - ressalva no report)
def c2():
    for xs in list(lists()):
        exp = []
        for x in xs:
            if x not in exp:
                exp.append(x)
        r = safe(dedupe, xs)
        if r != ("ok", exp):
            yield (xs, r)
report("C2", first(c2()))

# C3
r = safe(flatten, [[1, [2]], [3]])
report("C3", None if r == ("ok", [1, 2, 3]) else ([[1, [2]], [3]], r))


# C4
def c4():
    for xs in lists():
        for n in range(-len(xs) - 2, len(xs) + 4):
            r = safe(top_n, xs, n)
            if r[0] == "exc" or len(r[1]) != min(n, len(xs)):
                yield (xs, n, r)
report("C4", first(c4()))


# C5
def c5():
    for a, b in [({"k": 1}, {"k": 2}), ({}, {"k": 2}), ({"k": 1}, {})]:
        if "k" in a and "k" in b:
            r = safe(merge_dicts, a, b)
            if r[0] == "exc" or r[1]["k"] != a["k"]:
                yield (a, b, r)
report("C5", first(c5()))


# C6
def c6():
    for xs in lists():
        r = safe(rotate, xs, len(xs))
        if r != ("ok", xs):
            yield (xs, r)
report("C6", first(c6()))
