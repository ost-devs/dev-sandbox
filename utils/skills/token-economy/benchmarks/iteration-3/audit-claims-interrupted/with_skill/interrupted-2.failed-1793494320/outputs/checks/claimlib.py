"""Shared helper for claim checks. Seed is fixed: every run is identical.

Usage in checks/<module>/check_<module>.py:
    sys.path.insert(0, <repo root>); sys.path.insert(0, <checks dir>)
    from claimlib import *
    @claim("T01")
    def t01():
        return expect(slugify('Café Noir'), 'cafe-noir')   # None = holds
    @claim("T02")
    def t02():
        for s in strings(rng("T02")):          # property claim
            if bad(s): return f"s={s!r} -> {slugify(s)!r}"
    main("text")
A check returns None when the claim holds, or a short counterexample string
when it fails (an exception raised by kit counts as a failure; it's reported).
"""
import json, os, random, sys, traceback

SEED = 20261101
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CLAIMS = {}

def rng(claim_id):
    return random.Random(f"{SEED}:{claim_id}")

def claim(cid):
    def deco(f):
        _CLAIMS[cid] = f
        return f
    return deco

def expect(got, want):
    return None if got == want and type(got) is type(want) else f"got {got!r}, expected {want!r}"

# Alphabet mixes ASCII, spaces/tabs/newlines, punctuation, accents, non-Latin, symbols.
ALPHABET = list("abcXYZ019 -_.,:!\t\n") + list("éèçãõøßÅñİıΩж中€😀") + ["́", " "]

def strings(r, n=2000, maxlen=12):
    """Edge cases first, then n random strings."""
    yield from ["", " ", "-", "--", "a", "A-", " -a- ", "é", "ø", "ß", "İ", "́", "á"]
    for _ in range(n):
        yield "".join(r.choice(ALPHABET) for _ in range(r.randint(0, maxlen)))

def ints(r, n=2000, lo=-50, hi=50):
    yield from [0, 1, -1, lo, hi]
    for _ in range(n):
        yield r.randint(lo, hi)

def int_lists(r, n=2000, maxlen=8, lo=-20, hi=20):
    yield from [[], [0], [1, 1], [1, 2], [2, 1]]
    for _ in range(n):
        yield [r.randint(lo, hi) for _ in range(r.randint(0, maxlen))]

def main(module):
    out, bad = [], 0
    for cid, f in sorted(_CLAIMS.items()):
        try:
            cex = f()
            verdict = "verdadeira" if cex is None else "falsa"
        except Exception:
            cex = "raised " + traceback.format_exc().strip().splitlines()[-1]
            verdict = "falsa"
        out.append({"id": cid, "verdict": verdict, "counterexample": cex})
    os.makedirs(os.path.join(ROOT, "checks", module), exist_ok=True)
    with open(os.path.join(ROOT, "checks", module, "results.json"), "w") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    for o in out:
        print(o["id"], o["verdict"], o["counterexample"] or "")
