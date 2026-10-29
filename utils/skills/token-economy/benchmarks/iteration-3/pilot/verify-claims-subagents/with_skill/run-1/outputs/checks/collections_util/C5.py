import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

bad=None
cases=[({'k':1},{'k':2}),({},{}),({'a':1},{}),({'a':None},{'a':5})]
for _ in range(300):
    cases.append(({r.randint(0,6):r.randint(0,99) for _ in range(5)},{r.randint(0,6):r.randint(100,199) for _ in range(5)}))
for a,b in cases:
    try:
        o=merge_dicts(a,b)
        for k in a:
            if k in b and o[k]!=a[k]: bad=f"merge_dicts({a},{b})[{k!r}]={o[k]}, expected {a[k]}"; break
    except Exception as e:
        bad=f"raised {e!r}"
    if bad: break
verdict('C5', bad is None, bad)
