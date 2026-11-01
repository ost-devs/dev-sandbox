import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    a,b = date(2024,1,2), date(2024,1,1)
    r = days_between(a,b)
    return None if r >= 0 else f"days_between({a},{b}) = {r}, expected >= 0"
run('D3','days_between never negative',check)
