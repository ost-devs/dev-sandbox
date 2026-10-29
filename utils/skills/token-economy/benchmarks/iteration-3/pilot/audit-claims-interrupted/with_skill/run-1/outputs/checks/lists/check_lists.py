import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import claim, run, rng, rand_str, rand_ints, SEED
from kit import lists as L

N = 2500

def cases(cid, extra=()):
    r = rng(cid)
    out = [[], [0], [1, 1], [-1, 0, 1], [5, 1, 4]] + list(extra)
    for _ in range(N):
        out.append(rand_ints(r, 10))
    return out

def prop(cid, gen_args, pred):
    """gen_args yields arg tuples; pred(args)->bool."""
    for args in gen_args:
        try:
            ok = pred(*args)
        except Exception as e:
            return (False, f"{args!r} -> exception {e!r}")
        if ok is not True:
            return (False, f"{args!r} -> {ok!r}")
    return True

def with_k(cid, lo, hi, extra_ks=()):
    r = rng(cid + 'k')
    for xs in cases(cid):
        for k in list(extra_ks) + [r.randint(lo, hi)]:
            yield (xs, k)

@claim('L01')
def l01(): return L.chunk(list(range(7)), 3) == [[0, 1, 2], [3, 4, 5], [6]]

@claim('L02')
def l02():
    return prop('L02', with_k('L02', 1, 12, (1, 2, 100)), lambda xs, k: L.flatten(L.chunk(xs, k)) == xs or L.flatten(L.chunk(xs, k)))

@claim('L03')
def l03():
    for xs in cases('L03'):
        try:
            res = L.chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return (False, f"chunk({xs!r}, 0) -> {e!r}")
        return (False, f"chunk({xs!r}, 0) -> {res!r}")
    return True

@claim('L04')
def l04(): return L.dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]

def first_occ(xs):
    out = []
    for x in xs:
        if x not in out: out.append(x)
    return out

@claim('L05')
def l05(): return prop('L05', ((xs,) for xs in cases('L05')), lambda xs: L.dedupe(xs) == first_occ(xs) or L.dedupe(xs))

@claim('L06')
def l06(): return prop('L06', ((xs,) for xs in cases('L06')), lambda xs: len(L.dedupe(xs)) == len(set(xs)) or len(L.dedupe(xs)))

@claim('L07')
def l07():
    r = L.flatten([[1, [2]], [3]])
    return r == [1, 2, 3] or (False, f"flatten([[1, [2]], [3]]) -> {r!r}")

@claim('L08')
def l08(): return L.top_n([5, 1, 4], 2) == [5, 4]

@claim('L09')
def l09(): return prop('L09', with_k('L09', 0, 14, (0, 1, 100)), lambda xs, k: len(L.top_n(xs, k)) == min(k, len(xs)) or L.top_n(xs, k))

@claim('L10')
def l10():
    r = L.top_n([3, 2, 1], -1)
    return r == [] or (False, f"top_n([3, 2, 1], -1) -> {r!r}")

@claim('L11')
def l11(): return L.rotate([1, 2, 3], 1) == [2, 3, 1]

@claim('L12')
def l12():
    gen = ((xs, k) for xs, k in with_k('L12', 0, 30, (0, 1, 3, 4)) if xs)
    return prop('L12', gen, lambda xs, k: L.rotate(xs, k) == L.rotate(xs, k % len(xs)) or (L.rotate(xs, k), L.rotate(xs, k % len(xs))))

@claim('L13')
def l13(): return prop('L13', with_k('L13', -30, 30, (-1, 0, 1)), lambda xs, k: len(L.rotate(xs, k)) == len(xs) or L.rotate(xs, k))

@claim('L14')
def l14():
    r = L.interleave([1, 2, 3], [9])
    return r == [1, 9, 2, 3] or (False, f"interleave([1, 2, 3], [9]) -> {r!r}")

@claim('L15')
def l15():
    r = rng('L15b')
    def gen():
        cs = cases('L15')
        for i, a in enumerate(cs):
            yield (a, cs[(i * 7 + 3) % len(cs)])
            yield (a, rand_ints(r, 10))
    return prop('L15', gen(), lambda a, b: len(L.interleave(a, b)) == 2 * min(len(a), len(b)) or L.interleave(a, b))

@claim('L16')
def l16(): return L.frequencies('abca') == {'a': 2, 'b': 1, 'c': 1}

@claim('L17')
def l17(): return prop('L17', ((xs,) for xs in cases('L17')), lambda xs: sum(L.frequencies(xs).values()) == len(xs) or L.frequencies(xs))

@claim('L18')
def l18(): return L.pairwise([1, 2, 3]) == [(1, 2), (2, 3)]

@claim('L19')
def l19(): return prop('L19', ((xs,) for xs in cases('L19')), lambda xs: len(L.pairwise(xs)) == len(xs) - 1 or L.pairwise(xs))

if __name__ == '__main__':
    run(__file__)
