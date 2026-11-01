import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.textutil import slugify

def test():
    r = slugify('Café Noir')
    if r != 'cafe-noir':
        return f"slugify('Café Noir') == {r!r}, expected 'cafe-noir'"
    return None

main("T2", test)
