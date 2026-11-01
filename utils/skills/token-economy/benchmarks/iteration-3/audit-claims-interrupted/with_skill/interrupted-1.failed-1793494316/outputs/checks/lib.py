"""Shared helpers for claim checks. Deterministic: all randomness from SEED."""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEED = 20261101
N = 2000  # random cases per property claim

def rng(claim_id):
    return random.Random(f"{SEED}:{claim_id}")

# Alphabet deliberately includes accents, non-Latin, punctuation, whitespace, symbols, empty.
_ALPHA = list("abcXYZ019 -_.,:!\t\n") + list("éÉçãõøØßİıñüΣσ") + ["中", "٣", "²", " ", "́", "😀", "ǆ"]
def rand_str(r, maxlen=12):
    return "".join(r.choice(_ALPHA) for _ in range(r.randint(0, maxlen)))
def rand_int(r, lo=-50, hi=50):
    return r.randint(lo, hi)
def rand_ints(r, maxlen=8, lo=-20, hi=20):
    return [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]

def find_counterexample(claim_id, gen, pred, n=N):
    """gen(r)->args tuple; pred(*args)->bool. Returns first failing args (repr) or None.
    An exception raised by pred counts as failure."""
    r = rng(claim_id)
    for _ in range(n):
        args = gen(r)
        try:
            ok = pred(*args)
        except Exception as e:
            return f"{args!r} -> raised {type(e).__name__}: {e}"
        if not ok:
            return repr(args)
    return None

def expect(fn, expected):
    """Example claim. Returns None if fn()==expected (type-strict via repr of value+type), else description."""
    try:
        got = fn()
    except Exception as e:
        return f"raised {type(e).__name__}: {e}"
    if got == expected and type(got) is type(expected):
        return None
    return f"got {got!r}, expected {expected!r}"

class Runner:
    """Each module's run.py registers claims: R.claim('T01', fn) where fn returns None (true) or a
    counterexample string (false). `python3 -I checks/<mod>/run.py [ID...]` prints one line per claim
    `ID TRUE|FALSE <counterexample>` and writes checks/<mod>/results.json (when run for all)."""
    def __init__(self, mod): self.mod, self.cl = mod, {}
    def claim(self, cid, fn): self.cl[cid] = fn
    def main(self):
        ids = sys.argv[1:] or sorted(self.cl)
        out = {}
        for cid in ids:
            try: ce = self.cl[cid]()
            except Exception as e: ce = f"check crashed: {type(e).__name__}: {e}"
            out[cid] = {"verdict": "verdadeira" if ce is None else "falsa", "counterexample": ce}
            print(cid, "TRUE" if ce is None else "FALSE", ce or "")
        if not sys.argv[1:]:
            with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "results.json"), "w") as f:
                json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
