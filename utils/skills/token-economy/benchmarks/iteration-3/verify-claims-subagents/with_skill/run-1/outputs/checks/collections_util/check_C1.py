import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.collections_util import *
def rl(r):
    return [r.choice([0,1,2,3,-1,'a','é',None]) for _ in range(r.randint(0,12))]
def check():
    r = rng('C1')
    cases = [[], [1], [1,2,3]] + [rl(r) for _ in range(2000)]
    for xs in cases:
        for n in range(1, 15):
            if flatten(chunk(xs, n)) != xs:
                return f"chunk({xs},{n})"
run('C1', 'chunk concat roundtrip', check)
