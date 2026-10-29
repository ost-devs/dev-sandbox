import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

o = count_words("a  b\tc\n")
verdict("T4", o == 3, f"count_words={o}")
