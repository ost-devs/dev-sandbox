import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.mathutil import percent

def test():
    v = percent(1, 3)
    if v != 33.3:
        return f"percent(1, 3) = {v!r}"
    return None

main("M6", test)
