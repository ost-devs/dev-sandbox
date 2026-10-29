import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

try: v = mean([])
except Exception as e: verdict('M2', False, f'mean([]) raised {e!r}')
verdict('M2', v == 0 and not isinstance(v, bool), None if v == 0 else f'mean([])={v!r}')
