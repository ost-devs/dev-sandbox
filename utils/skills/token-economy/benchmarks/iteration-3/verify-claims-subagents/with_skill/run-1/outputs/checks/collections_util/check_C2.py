import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.collections_util import *
def rl(r):
    return [r.choice([0,1,2,3,-1,'a','é',None]) for _ in range(r.randint(0,12))]
def check():
    r = rng('C2')
    for xs in [[], [1,1], [3,1,3,2,1]] + [[r.randint(0,6) for _ in range(r.randint(0,15))] for _ in range(2000)]:
        exp = []
        for x in xs:
            if x not in exp: exp.append(x)
        if dedupe(xs) != exp:
            return f"dedupe({xs}) -> {dedupe(xs)} expected {exp}"
run('C2', 'dedupe order', check)
