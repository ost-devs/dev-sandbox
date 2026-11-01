"""Shared helper. Each check script: define test() returning None if the claim
holds, or a string with a concrete counterexample if it fails; then call main(ID, test).
Randomness: use rng() (fixed SEED) only."""
import json, os, random, sys
SEED = 20261101
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)  # makes `import calc` work from anywhere

def rng():
    return random.Random(SEED)

def main(claim_id, test):
    try:
        cex = test()
    except Exception as e:  # an exception on a valid input is a counterexample
        cex = f"raised {type(e).__name__}: {e}"
    out = {"id": claim_id, "verdict": "verdadeira" if cex is None else "falsa",
           "counterexample": cex, "seed": SEED}
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(0 if cex is None else 1)
