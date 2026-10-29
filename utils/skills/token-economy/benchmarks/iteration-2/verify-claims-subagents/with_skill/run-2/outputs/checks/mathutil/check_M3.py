import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import round_half
a = round_half(2.5)
verdict("M3", a == 3, f"got {a!r}", "call round_half(2.5)")
