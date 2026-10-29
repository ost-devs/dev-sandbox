"""Shared harness. Each check fn returns None (claim held on every input tried)
or a string with a counterexample. Randomness only via rng(), seeded with SEED."""
import sys, os, json, random, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SEED = 20261029
N = 20000  # random samples per universal claim
REGISTRY = {}


def rng(cid):
    return random.Random(f'{SEED}:{cid}')


def claim(cid):
    def deco(f):
        REGISTRY[cid] = f
        return f
    return deco


def forall(inputs, pred):
    """First input where pred(*input) is falsy or raises, as a counterexample string."""
    for args in inputs:
        if not isinstance(args, tuple):
            args = (args,)
        try:
            if not pred(*args):
                return f'input={args!r}: predicate false'
        except Exception as e:
            return f'input={args!r}: raised {type(e).__name__}: {e}'
    return None


def eq(expr_fn, expected):
    """Check a fixed example: expr_fn() == expected."""
    try:
        got = expr_fn()
    except Exception as e:
        return f'raised {type(e).__name__}: {e} (expected {expected!r})'
    ok = (got is expected) if isinstance(expected, bool) or expected is None else got == expected
    return None if ok else f'got {got!r}, expected {expected!r}'


def raises(fn, exc):
    try:
        got = fn()
    except exc:
        return None
    except Exception as e:
        return f'raised {type(e).__name__} instead of {exc.__name__}'
    return f'no exception; returned {got!r}'


def main(module_name):
    ids = sys.argv[1:] or sorted(REGISTRY)
    rc = 0
    for cid in ids:
        try:
            ce = REGISTRY[cid]()
        except Exception:
            ce = 'CHECK ERROR ' + traceback.format_exc(limit=2)
        print(json.dumps({'id': cid, 'holds': ce is None, 'counterexample': ce}, ensure_ascii=False))
        rc |= ce is not None
    return 0
