import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    return None if is_leap(1900) is False else f"is_leap(1900)={is_leap(1900)}"
run('D4','is_leap(1900) False',check)
