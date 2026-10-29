import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

v = round_half(2.5)
verdict('M3', v == 3, f'round_half(2.5)={v!r}')
