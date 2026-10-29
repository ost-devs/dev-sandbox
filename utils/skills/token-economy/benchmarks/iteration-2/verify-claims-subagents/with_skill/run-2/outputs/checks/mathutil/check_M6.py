import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import percent
a = percent(1, 3)
verdict("M6", a == 33.3, f"got {a!r}", "call percent(1, 3)")
