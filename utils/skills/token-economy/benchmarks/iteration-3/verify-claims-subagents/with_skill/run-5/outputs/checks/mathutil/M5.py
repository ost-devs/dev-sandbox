import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import main
from calc.mathutil import is_prime

def ref(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, n))

def test():
    for n in range(0, 1001):
        got, exp = is_prime(n), ref(n)
        if got != exp:
            return f"is_prime({n}) = {got!r}, expected {exp!r}"
    return None

main("M5", test)
