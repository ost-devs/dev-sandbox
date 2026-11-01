import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.collections_util import *
def rl(r):
    return [r.choice([0,1,2,3,-1,'a','é',None]) for _ in range(r.randint(0,12))]
def check():
    a, b = {'k': 'a'}, {'k': 'b'}
    got = merge_dicts(a, b)
    if got['k'] != 'a':
        return f"merge_dicts({a},{b}) -> {got} expected {{'k': 'a'}}"
run('C5', 'merge keeps a', check)
