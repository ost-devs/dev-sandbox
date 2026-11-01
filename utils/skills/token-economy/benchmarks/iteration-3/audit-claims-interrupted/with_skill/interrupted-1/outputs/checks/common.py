"""Shared helpers for claim checks. Deterministic: all randomness comes from SEED."""
import json, os, random, string, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

SEED = 20261101
N = 3000  # default samples per property

def rng(tag=''):
    """Fresh Random per claim, seeded by SEED + tag, so claims are independent and reproducible."""
    return random.Random(f'{SEED}:{tag}')

ALPHABET = string.ascii_letters + string.digits + ' \t\n-_.,:/\\' + 'éÉãçøßñİıΩ中😀́ '

def gen_str(r, maxlen=12, alphabet=ALPHABET):
    return ''.join(r.choice(alphabet) for _ in range(r.randint(0, maxlen)))

def gen_int(r, lo=-50, hi=50):
    return r.randint(lo, hi)

def gen_list(r, elem, maxlen=8):
    return [elem(r) for _ in range(r.randint(0, maxlen))]

def forall(tag, gen, pred, n=N):
    """gen(r)->args tuple; pred(*args)->truthy. Returns None if holds for n samples (plus
    exceptions count as failures), else a counterexample string 'args -> result/exception'."""
    r = rng(tag)
    for _ in range(n):
        a = gen(r)
        a = a if isinstance(a, tuple) else (a,)
        try:
            if not pred(*a):
                return f'args={a!r}'
        except Exception as e:
            return f'args={a!r} raised {type(e).__name__}: {e}'
    return None

def eq(expr_fn, expected):
    """Fixed-input check: returns None if expr_fn() == expected (and type-equal for bool/None), else counterexample."""
    try:
        got = expr_fn()
    except Exception as e:
        return f'raised {type(e).__name__}: {e}'
    if got == expected and type(got) == type(expected):
        return None
    return f'got {got!r}, claim says {expected!r}'

def run(module, checks):
    """checks: dict id -> zero-arg fn returning None (holds) or counterexample string (fails).
    Usage: python3 checks/<module>/check_<module>.py [ID ...]. Exit 0 always; prints verdicts, writes results.json."""
    ids = sys.argv[1:] or list(checks)
    out = {}
    for i in ids:
        try:
            ce = checks[i]()
        except Exception as e:
            ce = f'check raised {type(e).__name__}: {e}'
        out[i] = {'verdict': 'verdadeira' if ce is None else 'falsa', 'counterexample': ce}
        print(f'{i}\t{out[i]["verdict"]}\t{ce or ""}')
    if not sys.argv[1:]:
        with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'results.json'), 'w') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
