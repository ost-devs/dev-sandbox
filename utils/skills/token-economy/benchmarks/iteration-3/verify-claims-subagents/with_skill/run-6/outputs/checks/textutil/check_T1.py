import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import rng, verdict
from calc.textutil import *
SEED = 12345
r = rng(SEED)
edge = ["", " ", "---", "!!!", "-a-", "Café", "日本語", "İ", "ß", "a - b", "éé", "\n"]
alpha = "abcXYZ019 -_!é日İ\t"
rand = ["".join(r.choice(alpha) for _ in range(r.randint(0, 12))) for _ in range(20000)]
bad = next((s for s in edge + rand if slugify(s).startswith("-") or slugify(s).endswith("-")), None)
verdict("T1", bad is None, bad)
