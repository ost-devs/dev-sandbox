import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    r = parse_iso('2026-02-30')
    return None if r == date(2026,3,2) else f"got {r}"
run('D6',"parse_iso('2026-02-30')==2026-03-02",check)
