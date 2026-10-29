import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import gcd
r = rng()
cases = [(0,0),(0,5),(5,0),(-4,6),(6,-4),(-4,-6),(1,1),(12,18),(7,13)]
cases += [(a,b) for a in range(-60,61) for b in range(-60,61)]
cases += [(r.randint(-10**9,10**9), r.randint(-10**9,10**9)) for _ in range(5000)]
search("M4", cases, lambda c: gcd(c[0],c[1]) == gcd(c[1],c[0]), "edge cases, exhaustive -60..60 pairs, 5000 seeded random")
