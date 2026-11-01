"""Shared helpers for claim checks. Deterministic: all randomness derives from SEED + claim id."""
import json, os, random, sys, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SEED = 20261101
_CLAIMS = {}


class Counter(Exception):
    """Raised when a claim is falsified; message = the counterexample."""


def claim(cid):
    """Register a check. Return normally => claim holds. Raise Counter/AssertionError/any
    exception => claim false (message/exception is recorded as the counterexample)."""
    def deco(fn):
        _CLAIMS[cid] = fn
        return fn
    return deco


def rng(cid):
    return random.Random(f"{SEED}:{cid}")


def rand_str(r, maxlen=12):
    pools = ["abcxyzABCXYZ019", " -_.,!\t\n", "éàçãõüñøßœÆłİı", "日本語😀 ́", "abcdefghijklmnopqrstuvwxyz"]
    pool = "".join(r.sample(pools, r.randint(1, 3)))
    return "".join(r.choice(pool) for _ in range(r.randint(0, maxlen)))


def rand_list(r, lo=-20, hi=20, maxlen=8, minlen=0):
    return [r.randint(lo, hi) for _ in range(r.randint(minlen, maxlen))]


def forall(cid, gen, pred, n=3000):
    """gen(r) -> tuple of args; pred(*args) -> truthy if claim holds. Raises Counter on first failure
    (exceptions from pred count as failures). Fixed seed => same result every run."""
    r = rng(cid)
    for _ in range(n):
        args = gen(r)
        try:
            ok = pred(*args)
        except Exception as e:
            raise Counter(f"args={args!r} raised {type(e).__name__}: {e}")
        if not ok:
            raise Counter(f"args={args!r}")


def main(module, only=None):
    out = []
    for cid, fn in sorted(_CLAIMS.items()):
        try:
            fn()
            out.append({"id": cid, "verdict": "verdadeira", "counterexample": ""})
        except Counter as e:
            out.append({"id": cid, "verdict": "falsa", "counterexample": str(e)})
        except AssertionError as e:
            out.append({"id": cid, "verdict": "falsa", "counterexample": f"assertion failed: {e}"})
        except Exception as e:
            out.append({"id": cid, "verdict": "falsa",
                        "counterexample": f"{type(e).__name__}: {e}"})
    path = os.path.join(ROOT, "checks", module, "results.json")
    with open(path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for o in out:
        print(o["id"], o["verdict"], o["counterexample"][:150])
