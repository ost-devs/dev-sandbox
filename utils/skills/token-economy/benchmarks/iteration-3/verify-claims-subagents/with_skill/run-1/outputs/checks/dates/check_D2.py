import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from harness import run, rng
from datetime import date, timedelta
from calc.dates import *
def check():
    d0 = date(1,1,1)
    for i in range(0, 366*400+1):
        d = d0 + timedelta(days=i*1) if False else date.fromordinal(date(1900,1,1).toordinal()+i)
        r = add_months(d,12)
        if (r.year,r.month,r.day) != (d.year+1,d.month,d.day):
            return f"add_months({d},12) -> {r}, expected {d.year+1}-{d.month:02d}-{d.day:02d}"
run('D2','add_months(d,12) same day/month next year',check)
