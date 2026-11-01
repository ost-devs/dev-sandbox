import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.textutil import *

def check():
    r = rng('T1')
    al = list('ab -_é!Z09\t') + ['日','…']
    ins = ['', '-', '---', ' a ', 'é', '--a--'] + [''.join(r.choice(al) for _ in range(r.randint(0,12))) for _ in range(2000)]
    for s in ins:
        o = slugify(s)
        if o.startswith('-') or o.endswith('-'):
            return f'{s!r} -> {o!r}'
run('T1','slugify never starts/ends with -',check)
