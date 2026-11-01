import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.textutil import is_palindrome

def test():
    r = is_palindrome('')
    if r is not True:
        return f"is_palindrome('') == {r!r}, expected True"
    return None

main("T6", test)
