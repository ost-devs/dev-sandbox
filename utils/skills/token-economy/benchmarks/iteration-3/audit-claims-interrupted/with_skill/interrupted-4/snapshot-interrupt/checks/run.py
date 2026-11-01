"""Usage: python3 -I checks/run.py <module> [ID]   (run from repo root)
Each checks/<module>.py defines CHECKS = {ID: fn}; fn() returns None if the claim holds,
else a short counterexample string. Prints 'ID<TAB>verdadeira|falsa<TAB>counterexample'."""
import sys, os, importlib
here = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [here, os.path.dirname(here)]
mod = importlib.import_module(sys.argv[1])
ids = sys.argv[2:] or sorted(mod.CHECKS)
bad = 0
for i in ids:
    r = mod.CHECKS[i]()
    bad += r is not None
    print(f"{i}\t{'verdadeira' if r is None else 'falsa'}\t{'' if r is None else r}")
