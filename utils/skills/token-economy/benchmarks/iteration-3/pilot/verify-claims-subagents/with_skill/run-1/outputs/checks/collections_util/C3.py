import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _common import rng, verdict
from calc.collections_util import *
r = rng()

try:
    o=flatten([[1,[2]],[3]])
    bad=None if o==[1,2,3] else f"flatten([[1,[2]],[3]])={o}"
except Exception as e:
    bad=f"raised {e!r}"
verdict('C3', bad is None, bad)
