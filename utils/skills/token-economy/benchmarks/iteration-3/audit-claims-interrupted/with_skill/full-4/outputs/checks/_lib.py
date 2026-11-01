"""Shared helpers for claim checks. Each module script: checks/<module>.py (run from repo root)."""
import json, os, random, string, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SEED = 20261101  # recorded seed; every generator below derives from it
N = 5000         # default number of random cases

def rng(claim_id):
    return random.Random(f"{SEED}:{claim_id}")

# Alphabet mixes ASCII, punctuation, whitespace, accents, non-Latin, symbols, to hit edge cases.
ALPHABET = (string.ascii_letters + string.digits + " -_.,:/\\\t\n" +
            "éÉãçñüøßıİǅﬁ½²ΣЖ中😀́")

def rand_str(r, maxlen=12, alphabet=ALPHABET):
    return ''.join(r.choice(alphabet) for _ in range(r.randint(0, maxlen)))

def rand_int(r, lo=-20, hi=20):
    return r.randint(lo, hi)

def rand_list(r, gen, maxlen=8):
    return [gen(r) for _ in range(r.randint(0, maxlen))]

def exact(f):
    """Decorator: claim about fixed inputs. f() returns (ok, detail). Exceptions = false."""
    f.kind = 'exact'; return f

def prop(f):
    """Decorator: property claim. f(r) draws inputs from r and returns None/True if holds,
    or False/str describing the counterexample (str preferred, include inputs via repr)."""
    f.kind = 'prop'; return f

def run(claims):
    """claims: dict id -> function. Prints one JSON line per claim:
    {"id","verdict":"verdadeira|falsa","counterexample":str|null,"cases":int}
    Exit 0 always. Optional argv: ids to run."""
    ids = sys.argv[1:] or sorted(claims)
    for cid in ids:
        f = claims[cid]; cex = None; cases = 1
        try:
            if f.kind == 'exact':
                res = f()
                if res is not True and not (isinstance(res, tuple) and res[0]):
                    cex = res[1] if isinstance(res, tuple) else 'returned %r' % (res,)
            else:
                r = rng(cid); cases = 0
                for _ in range(N):
                    cases += 1
                    res = f(r)
                    if res is not None and res is not True:
                        cex = res if isinstance(res, str) else 'failed'; break
        except Exception as e:
            cex = 'exception %s: %s' % (type(e).__name__, e)
        print(json.dumps({"id": cid, "verdict": "falsa" if cex else "verdadeira",
                          "counterexample": cex, "cases": cases}, ensure_ascii=False))
