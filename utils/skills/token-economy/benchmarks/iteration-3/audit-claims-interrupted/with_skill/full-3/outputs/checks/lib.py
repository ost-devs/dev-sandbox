"""Shared helpers for claim checks. Deterministic: every random draw uses a seed derived from the claim id."""
import json, os, random, sys, zlib, traceback
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

ALPHABET = list("abcXYZ019 -_.\t\n/\\") + ["é", "ã", "ø", "ß", "İ", "ǅ", "Ω", "日", "😀", "́", "ﬁ"]

def seed_for(cid): return zlib.crc32(cid.encode())

def rand_text(rng, maxlen=12):
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randint(0, maxlen)))

def rand_int(rng, lo=-5, hi=50): return rng.randint(lo, hi)

class Checker:
    """c.fixed(id, fn): fn() returns None/True if the claim holds on that fixed example, else a counterexample string
    (or raises -> the exception is the counterexample).
    c.prop(id, gen, pred, n=3000): gen(rng)->args tuple; pred(*args) True if holds. First failing args = counterexample.
    Verdict 'verdadeira' means: no counterexample found (fixed example holds / n seeded samples passed)."""
    def __init__(self, module):
        self.module, self.results = module, []
    def _rec(self, cid, ok, cex, how):
        self.results.append({"id": cid, "verdict": "verdadeira" if ok else "falsa",
                             "counterexample": None if ok else cex, "how": how})
    def fixed(self, cid, fn):
        try:
            r = fn()
            ok = r is None or r is True
            self._rec(cid, ok, None if ok else str(r), "fixed")
        except Exception as e:
            self._rec(cid, False, f"raises {type(e).__name__}: {e}", "fixed")
    def prop(self, cid, gen, pred, n=3000):
        rng = random.Random(seed_for(cid))
        for _ in range(n):
            args = gen(rng)
            try:
                ok = pred(*args)
            except Exception as e:
                self._rec(cid, False, f"args={args!r} raises {type(e).__name__}: {e}", f"seed={seed_for(cid)} n={n}"); return
            if not ok:
                self._rec(cid, False, f"args={args!r}", f"seed={seed_for(cid)} n={n}"); return
        self._rec(cid, True, None, f"seed={seed_for(cid)} n={n}")
    def finish(self):
        out = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "results.json")
        self.results.sort(key=lambda r: r["id"])
        json.dump(self.results, open(out, "w"), ensure_ascii=False, indent=1)
        for r in self.results: print(r["id"], r["verdict"], r["counterexample"] or "")
