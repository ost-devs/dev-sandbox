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

def ref(xs):
    out=[]
    for x in xs:
        if x not in out: out.append(x)
    return out
search("C2", [[],[1,1],[2,1,2]] + list(lists()), lambda xs: dedupe(xs) == ref(xs), "compare to naive first-occurrence reference; exhaustive small + rng")
