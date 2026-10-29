import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

v = percent(1, 3)
verdict('M6', v == 33.3, f'percent(1,3)={v!r}')
