import sys, os
d = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(d, '..', '..')); sys.path.insert(0, os.path.join(d, '..'))
from harness import run, rng
from calc.mathutil import *
def check():
    v = round_half(2.5)
    if v != 3:
        return f"round_half(2.5) -> {v!r}, expected 3"
run('M3', 'round_half(2.5)==3', check)
