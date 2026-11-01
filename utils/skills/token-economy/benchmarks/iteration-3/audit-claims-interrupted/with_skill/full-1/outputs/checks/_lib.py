"""Shared helpers for claim checks. Deterministic: all randomness from rng(id) with fixed SEED."""
import json, os, random, string, sys, zlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SEED = 20261101
_CLAIMS = {}

def rng(cid):
    """Per-claim reproducible Random (SEED + crc of id)."""
    return random.Random(SEED + zlib.crc32(cid.encode()))

# Alphabet mixing ASCII, accents, symbols, whitespace, non-Latin, emoji.
ALPHABET = string.ascii_letters + string.digits + " -_.,/\t\n" + "éèçãõñüøßİıÅ" + "漢字😀 '\"" 
def rand_str(r, maxlen=12, alphabet=ALPHABET):
    return "".join(r.choice(alphabet) for _ in range(r.randint(0, maxlen)))

def claim(cid):
    """Register fn(): must return None if the claim holds on all tested inputs,
    or a short string describing a concrete counterexample (inputs + actual output) if it fails.
    An exception raised by kit code on in-scope input counts as a counterexample: catch and report it."""
    def deco(fn):
        _CLAIMS[cid] = fn
        return fn
    return deco

def main():
    """Call at bottom of checks.py. Usage: python3 checks/<mod>/checks.py [ID ...]
    Prints 'ID<TAB>verdadeira|falsa<TAB>counterexample' per claim; exit 0 always."""
    ids = sys.argv[1:] or sorted(_CLAIMS)
    for cid in ids:
        try:
            ce = _CLAIMS[cid]()
        except Exception as e:  # check itself crashed on unexpected error
            ce = f"exception {type(e).__name__}: {e}"
        print(f"{cid}\t{'verdadeira' if ce is None else 'falsa'}\t{'' if ce is None else ce}")
