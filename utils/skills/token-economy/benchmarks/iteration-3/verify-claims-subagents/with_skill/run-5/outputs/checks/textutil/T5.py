import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.textutil import capitalize_words

def test():
    r = capitalize_words('a  b')
    if r != 'A  B':
        return f"capitalize_words('a  b') == {r!r}, expected 'A  B'"
    return None

main("T5", test)
