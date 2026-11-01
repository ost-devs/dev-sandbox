import os, sys, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate

SEED = 12345
print("SEED =", SEED)
rng = random.Random(SEED)

def rand_list(maxlen=8):
    return [rng.randint(-5, 5) for _ in range(rng.randint(0, maxlen))]

fixed_lists = [[], [1], [1, 2], [1, 2, 3], [3, 1, 2, 2], list(range(10))]
rand_lists = [rand_list() for _ in range(300)]
all_lists = fixed_lists + rand_lists
ns = [-3, -1, 0, 1, 2, 3, 5, 100]

def first_cex(pred, cases):
    # cases: iterable of arg tuples; pred returns True if claim holds; exceptions = failure
    for args in cases:
        try:
            ok = pred(*args)
        except Exception as e:
            return f"{args!r} raised {type(e).__name__}: {e}"
        if not ok:
            return repr(args)
    return None

def report(cid, cex):
    print(f"{cid}: {'TRUE' if cex is None else 'FALSE'} | {cex if cex else 'none found'}")

def c1(xs, n):
    return [y for c in chunk(xs, n) for y in c] == xs
report("C1", first_cex(c1, [(xs, n) for xs in all_lists for n in ns if n >= 1]))

def c2(xs):
    exp, seen = [], set()
    for x in xs:
        if x not in seen:
            seen.add(x); exp.append(x)
    return dedupe(xs) == exp
report("C2", first_cex(c2, [(xs,) for xs in all_lists]))

report("C3", first_cex(lambda: flatten([[1, [2]], [3]]) == [1, 2, 3], [()]))

def c4(xs, n):
    return len(top_n(xs, n)) == min(n, len(xs))
report("C4", first_cex(c4, sorted(((xs, n) for xs in all_lists for n in ns),
                                  key=lambda t: (len(t[0]), abs(t[1]), t[1]))))

dict_cases = [({}, {}), ({"k": 1}, {"k": 2}), ({"k": 1, "a": 0}, {"k": 2, "b": 3})]
for _ in range(200):
    a = {rng.randint(0, 4): rng.randint(0, 9) for _ in range(rng.randint(0, 4))}
    b = {rng.randint(0, 4): rng.randint(0, 9) for _ in range(rng.randint(0, 4))}
    dict_cases.append((a, b))
def c5(a, b):
    m = merge_dicts(a, b)
    return all(m[k] == a[k] for k in a if k in b)
report("C5", first_cex(c5, dict_cases))

report("C6", first_cex(lambda xs: rotate(xs, len(xs)) == xs, [(xs,) for xs in all_lists]))
