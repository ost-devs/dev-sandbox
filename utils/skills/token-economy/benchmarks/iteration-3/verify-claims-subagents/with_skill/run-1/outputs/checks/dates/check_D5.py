import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    for i in range(date.min.toordinal(), date.max.toordinal()+1, 1):
        d = date.fromordinal(i)
        if not 1 <= quarter(d) <= 4:
            return f"quarter({d})={quarter(d)}"
run('D5','quarter in 1..4',check)
