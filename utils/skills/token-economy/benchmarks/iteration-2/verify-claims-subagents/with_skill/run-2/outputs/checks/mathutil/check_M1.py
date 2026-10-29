import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import clamp
r = rng()
cases = [(0,0,0),(5,0,10),(-1,0,10),(11,0,10),(0,0,10),(10,0,10),(5,5,5),(1.5,1,2),(-5,-10,-1),(float('inf'),0,1),(float('-inf'),0,1)]
cases += [(r.randint(-100,100), lo, lo+r.randint(0,50)) for lo in [r.randint(-50,50) for _ in range(5000)]]
search("M1", cases, lambda c: c[1] <= clamp(*c) <= c[2], "edge cases then 5000 seeded random ints")
