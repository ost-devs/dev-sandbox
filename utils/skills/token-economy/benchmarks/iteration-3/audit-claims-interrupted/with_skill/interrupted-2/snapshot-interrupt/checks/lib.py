"""Shared helpers for claim checks. Run from repo root: python3 checks/check_<module>.py [ID ...]

Each check is a function decorated with @claim("T01"). It returns None if the claim holds,
or a string describing a counterexample (inputs and actual output) if it is false.
An exception raised by kit code counts as a counterexample. Random inputs come from
rng(seed) with a fixed seed (SEED by default), so every run gives the same result.
"""
import json, os, random, sys, string

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SEED = 20261101
N = 3000  # default number of generated cases

_CLAIMS = {}

def claim(cid):
    def deco(f):
        _CLAIMS[cid] = f
        return f
    return deco

def rng(salt=0):
    return random.Random(SEED + salt)

# --- generators (all take a random.Random) ---
_SPECIAL = " \t\n-_.,:'\"éÉãçøñüß–—1234567890ABCxyz"
def gen_str(r, maxlen=12, alphabet=None):
    a = alphabet or (string.ascii_letters + string.digits + _SPECIAL)
    return "".join(r.choice(a) for _ in range(r.randint(0, maxlen)))

def gen_int(r, lo=-20, hi=20):
    return r.randint(lo, hi)

def gen_ints(r, maxlen=8, lo=-20, hi=20):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]

def forall(gen, pred, n=N, salt=0):
    """gen(r) -> args tuple; pred(*args) -> True if holds. Returns counterexample string or None."""
    r = rng(salt)
    for _ in range(n):
        args = gen(r)
        try:
            ok = pred(*args)
        except Exception as e:
            return f"args={args!r} raised {type(e).__name__}: {e}"
        if not ok:
            return f"args={args!r}"
    return None

def eq(actual, expected, label=""):
    """For fixed examples: return None if equal else counterexample string."""
    return None if actual == expected else f"{label} got {actual!r}, expected {expected!r}"

def main(module):
    ids = sys.argv[1:] or sorted(_CLAIMS)
    out = {}
    for cid in ids:
        try:
            cex = _CLAIMS[cid]()
        except Exception as e:
            cex = f"raised {type(e).__name__}: {e}"
        out[cid] = {"verdict": "verdadeira" if cex is None else "falsa", "counterexample": cex}
        print(f"{cid}\t{out[cid]['verdict']}\t{cex or ''}")
    if not sys.argv[1:]:
        with open(os.path.join(ROOT, "checks", "results", f"{module}.json"), "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
