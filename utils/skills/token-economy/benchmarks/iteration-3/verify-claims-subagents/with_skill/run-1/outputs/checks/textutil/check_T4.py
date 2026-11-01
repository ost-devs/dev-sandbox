import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.textutil import *

def check():
    o = count_words('a  b\tc\n')
    if o != 3: return f'got {o}'
run('T4','count_words',check)
