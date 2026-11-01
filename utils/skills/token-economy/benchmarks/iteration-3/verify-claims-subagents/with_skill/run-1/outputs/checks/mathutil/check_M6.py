import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def check():
    v = percent(1, 3)
    if v != 33.3:
        return f"percent(1,3) -> {v!r}"
run('M6', 'percent(1,3)==33.3', check)
