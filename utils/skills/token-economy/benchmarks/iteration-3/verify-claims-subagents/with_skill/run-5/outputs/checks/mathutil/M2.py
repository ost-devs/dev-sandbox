import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.mathutil import mean

def test():
    v = mean([])
    if v != 0:
        return f"mean([]) = {v!r}"
    return None

main("M2", test)
