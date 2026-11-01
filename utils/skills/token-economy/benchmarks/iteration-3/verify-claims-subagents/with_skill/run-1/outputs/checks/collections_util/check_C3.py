import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.collections_util import *
def rl(r):
    return [r.choice([0,1,2,3,-1,'a','é',None]) for _ in range(r.randint(0,12))]
def check():
    got = flatten([[1, [2]], [3]])
    if got != [1, 2, 3]:
        return f"flatten([[1, [2]], [3]]) -> {got} expected [1, 2, 3]"
run('C3', 'flatten', check)
