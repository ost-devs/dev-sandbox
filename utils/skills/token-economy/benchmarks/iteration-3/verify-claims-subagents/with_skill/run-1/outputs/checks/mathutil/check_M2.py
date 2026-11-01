import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def check():
    v = mean([])
    if v != 0:
        return f"mean([]) -> {v!r}, expected 0"
run('M2', 'mean([]) returns 0', check)
