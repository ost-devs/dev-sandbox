import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

a=capitalize_words('a  b')
verdict('T5',a=='A  B',f"got {a!r}",method="direct call")
