import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 106
v = percent(1, 3)
verdict("M6", v == 33.3, ("percent(1,3)", v))
