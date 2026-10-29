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

cases = [([],0),([],-1),([1],-1),([1,2,3],-1),([1,2,3],0),([1,2,3],5)] + [(xs,n) for xs in lists() for n in range(-3,8)]
search("C4", cases, lambda c: len(top_n(c[0], c[1])) == min(c[1], len(c[0])), "edge cases incl negatives, then exhaustive small lists x n in -3..7 + rng")
