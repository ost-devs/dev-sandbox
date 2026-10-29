import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

o = is_palindrome("")
verdict("T6", o is True, f"is_palindrome('')={o!r}")
