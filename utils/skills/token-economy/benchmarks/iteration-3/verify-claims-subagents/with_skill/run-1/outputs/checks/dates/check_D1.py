import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    r = add_months(date(2024,1,31),1)
    return None if r == date(2024,2,29) else f"got {r}"
run('D1','add_months(2024-01-31,1)==2024-02-29',check)
