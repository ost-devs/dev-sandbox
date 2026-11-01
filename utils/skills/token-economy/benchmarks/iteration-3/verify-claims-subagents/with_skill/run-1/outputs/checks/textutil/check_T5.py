import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.textutil import *

def check():
    o = capitalize_words('a  b')
    if o != 'A  B': return f'got {o!r}'
run('T5','capitalize_words',check)
