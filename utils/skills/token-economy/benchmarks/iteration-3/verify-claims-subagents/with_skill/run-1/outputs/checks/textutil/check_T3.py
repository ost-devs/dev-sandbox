import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.textutil import *

def check():
    r = rng('T3')
    for n in range(0,6):
        for L in range(0,8):
            s='x'*L
            o=truncate(s,n)
            if len(o)>n: return f'truncate({s!r}, {n}) -> {o!r} (len {len(o)}) > {n}'
    for _ in range(2000):
        s=''.join(r.choice('ab é日') for _ in range(r.randint(0,10))); n=r.randint(0,12)
        o=truncate(s,n)
        if len(o)>n: return f'truncate({s!r}, {n}) -> {o!r}'
run('T3','truncate len <= n',check)
