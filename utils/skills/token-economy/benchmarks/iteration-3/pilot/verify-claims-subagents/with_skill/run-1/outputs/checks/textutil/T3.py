import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

import string
edge = [("", 0), ("a", 0), ("abc", 0), ("abc", 1), ("abc", 2), ("abc", 3), ("", 5), ("日本語", 0), ("日本語", 1)]
alpha = string.ascii_letters + "é日 "
rand = [("".join(r.choice(alpha) for _ in range(r.randint(0, 15))), r.randint(0, 15)) for _ in range(5000)]
for s, n in edge + rand:
    o = truncate(s, n)
    if len(o) > n:
        verdict("T3", False, f"truncate({s!r}, {n})={o!r} len {len(o)} > {n}")
verdict("T3", True)
