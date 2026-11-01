import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.textutil import count_words

def test():
    r = count_words('a  b\tc\n')
    if r != 3:
        return f"count_words('a  b\\tc\\n') == {r!r}, expected 3"
    return None

main("T4", test)
