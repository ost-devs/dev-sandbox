import sys, os, json, random, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from lists import *

SEED = 12345

def small_lists(maxlen=5, vals=(0, 1, 2)):
    for n in range(maxlen + 1):
        for t in itertools.product(vals, repeat=n):
            yield list(t)

def rand_lists(rng, n=3000):
    for _ in range(n):
        yield [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]

def all_lists():
    rng = random.Random(SEED)
    yield from small_lists()
    yield from rand_lists(rng)

def ks(lo, hi=9):
    return range(lo, hi)

def example(f, expected):
    try:
        got = f()
    except Exception as e:
        return f"raised {e!r}, expected {expected!r}"
    return None if got == expected else f"got {got!r}, expected {expected!r}"

def prop(pred, gen):
    """gen yields argument tuples; pred(*args) -> (ok, detail). Returns the smallest counterexample."""
    best = None
    for args in gen:
        try:
            ok, detail = pred(*args)
        except Exception as e:
            ok, detail = False, f"raised {e!r}"
        if not ok:
            size = len(repr(args))
            if best is None or size < best[0]:
                best = (size, args, detail)
    if best is None:
        return None
    return f"input {best[1]!r}: {best[2]}"

def ex(label, f, expected):
    r = example(f, expected)
    return r and f"{label}: {r}"

def L01(): return ex("chunk(range(7),3)", lambda: chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]])
def L02():
    return prop(lambda xs, k: (flatten(chunk(xs, k)) == xs, f"got {flatten(chunk(xs,k))!r}, expected {xs!r}"),
                ((xs, k) for xs in all_lists() for k in ks(1, 8)))
def L03():
    for xs in ([], [1], [1, 2, 3]):
        try:
            r = chunk(xs, 0)
            return f"chunk({xs!r},0) returned {r!r}, expected ValueError"
        except ValueError:
            pass
        except Exception as e:
            return f"chunk({xs!r},0) raised {e!r}, expected ValueError"
    return None
def L04(): return ex("dedupe", lambda: dedupe([3,1,3,2,1]), [3,1,2])
def L05():
    def p(xs):
        exp = []
        for x in xs:
            if x not in exp: exp.append(x)
        r = dedupe(xs)
        return r == exp, f"got {r!r}, expected {exp!r}"
    return prop(p, ((xs,) for xs in all_lists()))
def L06():
    return prop(lambda xs: (len(dedupe(xs)) == len(set(xs)), f"len {len(dedupe(xs))} vs {len(set(xs))}"),
                ((xs,) for xs in all_lists()))
def L07(): return ex("flatten", lambda: flatten([[1,[2]],[3]]), [1,2,3])
def L08(): return ex("top_n", lambda: top_n([5,1,4], 2), [5,4])
def L09():
    return prop(lambda xs, k: (len(top_n(xs, k)) == min(k, len(xs)), f"len {len(top_n(xs,k))}, expected {min(k,len(xs))}"),
                ((xs, k) for xs in all_lists() for k in ks(0, 15)))
def L10(): return ex("top_n", lambda: top_n([3,2,1], -1), [])
def L11(): return ex("rotate", lambda: rotate([1,2,3], 1), [2,3,1])
def L12():
    def p(xs, k):
        a, b = rotate(xs, k), rotate(xs, k % len(xs))
        return a == b, f"rotate(xs,k)={a!r}, rotate(xs,k%len)={b!r}"
    return prop(p, ((xs, k) for xs in all_lists() if xs for k in ks(0, 15)))
def L13():
    return prop(lambda xs, k: (len(rotate(xs, k)) == len(xs), f"len {len(rotate(xs,k))}, expected {len(xs)}"),
                ((xs, k) for xs in all_lists() for k in ks(-15, 15)))
def L14(): return ex("interleave", lambda: interleave([1,2,3],[9]), [1,9,2,3])
def L15():
    rng = random.Random(SEED + 1)
    pairs = [(a, b) for a in small_lists(3, (0, 1)) for b in small_lists(3, (0, 1))]
    pairs += [([rng.randint(0, 9) for _ in range(rng.randint(0, 8))],
               [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]) for _ in range(3000)]
    return prop(lambda a, b: (len(interleave(a, b)) == 2 * min(len(a), len(b)),
                              f"len {len(interleave(a,b))}, expected {2*min(len(a),len(b))}"), pairs)
def L16(): return ex("frequencies", lambda: frequencies('abca'), {'a':2,'b':1,'c':1})
def L17():
    return prop(lambda xs: (sum(frequencies(xs).values()) == len(xs), f"sum {sum(frequencies(xs).values())}, expected {len(xs)}"),
                ((xs,) for xs in all_lists()))
def L18(): return ex("pairwise", lambda: pairwise([1,2,3]), [(1,2),(2,3)])
def L19():
    return prop(lambda xs: (len(pairwise(xs)) == len(xs) - 1, f"len {len(pairwise(xs))}, expected {len(xs)-1}"),
                ((xs,) for xs in all_lists()))

CHECKS = {f"L{i:02d}": globals()[f"L{i:02d}"] for i in range(1, 20)}

if __name__ == "__main__":
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ce = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": "verdadeira" if ce is None else "falsa", "counterexample": ce}, ensure_ascii=False))
