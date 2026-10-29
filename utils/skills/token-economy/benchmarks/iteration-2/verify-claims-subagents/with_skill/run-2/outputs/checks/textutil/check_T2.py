import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

a=slugify('Café Noir')
verdict('T2',a=='cafe-noir',f"got {a!r}",method="direct call")
