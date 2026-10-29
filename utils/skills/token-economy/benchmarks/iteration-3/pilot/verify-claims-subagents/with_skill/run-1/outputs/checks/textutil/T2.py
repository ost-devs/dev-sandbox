import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

o = slugify("Café Noir")
verdict("T2", o == "cafe-noir", f"slugify('Café Noir')={o!r}")
