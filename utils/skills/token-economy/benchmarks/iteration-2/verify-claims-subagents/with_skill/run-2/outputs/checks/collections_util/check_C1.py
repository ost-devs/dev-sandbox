import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.collections_util import *
import itertools
R = rng()
def lists(maxlen=6, vals=4, k=300):
    for L in range(maxlen+1):
        for t in itertools.product(range(vals), repeat=L):
            if L<=4: yield list(t)
    for _ in range(k):
        yield [R.randint(-5,5) for _ in range(R.randint(0,30))]

cases = [(xs, n) for xs in lists() for n in (1,2,3,5,7,100)]
cases = [([],1),([1],1)] + cases
search("C1", cases, lambda c: [y for p in chunk(c[0], c[1]) for y in p] == c[0], "edge+exhaustive lists len<=4 vals<4 + rng, n in {1,2,3,5,7,100}")
