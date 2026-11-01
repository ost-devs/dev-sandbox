import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.textutil import *
SEED = 12345
r = rng(SEED)
got = count_words("a  b\tc\n")
verdict("T4", got == 3, got)
