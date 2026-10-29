import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

a=count_words('a  b\tc\n')
verdict('T4',a==3,f"got {a}",method="direct call")
