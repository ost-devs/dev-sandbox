import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.textutil import *
r = rng()

import string
edge = ["", "-", "---", "!!!", " ", "-a-", "a-", "-a", "É", "İ", "日本語", "aé-", "ß", "K", "--x--", "  x  "]
alpha = string.printable + "éÉİß日本-Kİ "
rand = ["".join(r.choice(alpha) for _ in range(r.randint(0, 12))) for _ in range(5000)]
for s in edge + rand:
    o = slugify(s)
    if o.startswith("-") or o.endswith("-"):
        verdict("T1", False, f"slugify({s!r})={o!r}")
verdict("T1", True)
