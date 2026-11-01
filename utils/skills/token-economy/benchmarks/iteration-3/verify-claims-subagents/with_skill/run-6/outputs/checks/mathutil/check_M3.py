import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 103
v = round_half(2.5)
verdict("M3", v == 3, ("round_half(2.5)", v))
