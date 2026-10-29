import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.textutil import *

a=is_palindrome('')
verdict('T6',a is True,f"got {a!r}",method="direct call")
