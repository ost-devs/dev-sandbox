import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.textutil import *

def check():
    o = slugify('Café Noir')
    if o != 'cafe-noir': return f"slugify('Café Noir') -> {o!r}, expected 'cafe-noir'"
run('T2','slugify Café Noir',check)
