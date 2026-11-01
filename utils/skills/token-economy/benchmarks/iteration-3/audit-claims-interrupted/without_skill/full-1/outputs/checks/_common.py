"""Helpers partilhados pelos scripts checks/check_<modulo>.py (só stdlib)."""
import json, os, random, sys

SEED = 20260101  # semente registrada; cada claim usa random.Random(SEED)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def rng():
    return random.Random(SEED)

class Results:
    def __init__(self, module):
        self.module, self.rows = module, []

    def record(self, cid, ok, counterexample=None, note=""):
        """ok=True -> verdadeira; ok=False -> falsa, com counterexample (repr)."""
        self.rows.append({"id": cid, "verdict": "verdadeira" if ok else "falsa",
                          "counterexample": None if ok else repr(counterexample), "note": note})

    def check(self, cid, fn):
        """fn() retorna (ok, counterexample). Exceções viram contraexemplo."""
        try:
            ok, ce = fn()
        except Exception as e:
            ok, ce = False, f"raised {type(e).__name__}: {e}"
        self.record(cid, ok, ce)

    def finish(self):
        print(json.dumps(self.rows, ensure_ascii=False, indent=1))
