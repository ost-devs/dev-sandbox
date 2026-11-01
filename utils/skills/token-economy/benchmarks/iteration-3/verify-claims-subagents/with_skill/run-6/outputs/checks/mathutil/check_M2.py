import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.mathutil import *
SEED = 102
try:
    ok = mean([]) == 0; ce = None if ok else ("mean([])", mean([]))
except Exception as e:
    ok = False; ce = ("mean([])", repr(e))
verdict("M2", ok, ce)
