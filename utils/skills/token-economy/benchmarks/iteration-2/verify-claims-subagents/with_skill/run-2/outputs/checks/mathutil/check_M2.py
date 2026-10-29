import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search
from calc.mathutil import mean
try:
    a = mean([]); ok = a == 0; ce = f"got {a!r}"
except Exception as e:
    ok = False; ce = f"mean([]) raised {type(e).__name__}: {e}"
verdict("M2", ok, ce, "call mean([])")
