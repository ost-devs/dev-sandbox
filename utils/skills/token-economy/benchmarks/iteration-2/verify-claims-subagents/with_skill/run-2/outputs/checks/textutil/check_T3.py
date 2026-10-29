import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

r=rng()
def cases():
    for s in ['','a','ab','abc','hello world']:
        for n in range(0,8): yield (s,n)
    for _ in range(2000): yield (''.join(r.choice('abc é') for _ in range(r.randint(0,15))), r.randint(0,15))
search('T3',cases(),lambda c: len(truncate(*c))<=c[1],'edge (s,n) grid n=0..7 + 2000 seeded random')
