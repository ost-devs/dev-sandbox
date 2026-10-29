import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

import itertools
edge=['','-','--',' ','---a---','a-','-a','!!!','Café','é','\n','a b ',"-é-"]
alpha='aZ0 -_é!\n'
def cases():
    yield from edge
    for k in range(1,6):
        for t in itertools.product(alpha,repeat=k): yield ''.join(t)
    r=rng()
    for _ in range(2000): yield ''.join(r.choice(alpha+'ß世') for _ in range(r.randint(0,12)))
search('T1',cases(),lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'),'edge cases + exhaustive len<=5 over alphabet + 2000 seeded random')
