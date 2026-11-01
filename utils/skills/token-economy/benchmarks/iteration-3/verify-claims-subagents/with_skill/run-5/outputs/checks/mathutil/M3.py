import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.mathutil import round_half

def test():
    v = round_half(2.5)
    if v != 3:
        return f"round_half(2.5) = {v!r}"
    return None

main("M3", test)
