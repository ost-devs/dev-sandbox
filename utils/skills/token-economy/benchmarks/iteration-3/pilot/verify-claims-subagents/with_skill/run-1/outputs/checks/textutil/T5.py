import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

o = capitalize_words("a  b")
verdict("T5", o == "A  B", f"capitalize_words('a  b')={o!r}")
