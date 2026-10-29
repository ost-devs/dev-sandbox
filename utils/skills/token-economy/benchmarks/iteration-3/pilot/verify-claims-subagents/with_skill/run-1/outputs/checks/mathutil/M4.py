import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from _common import rng, verdict
from calc.mathutil import *

r = rng()
vals = [0,1,-1,2,-2,6,-6,12,-18,7,100,-100]
pairs = [(a,b) for a in vals for b in vals] + [(r.randint(-10**6,10**6), r.randint(-10**6,10**6)) for _ in range(5000)]
for a, b in pairs:
    x, y = gcd(a,b), gcd(b,a)
    if x != y: verdict('M4', False, f'gcd({a},{b})={x} != gcd({b},{a})={y}')
verdict('M4', True)
