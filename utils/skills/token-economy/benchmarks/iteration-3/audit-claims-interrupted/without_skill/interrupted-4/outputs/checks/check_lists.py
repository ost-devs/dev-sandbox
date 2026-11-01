import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit.lists import *

SEED = 20261101
N = 20000


def eq(call, expected):
    try:
        got = call()
    except Exception as e:
        return False, f'raised {e!r}, expected {expected!r}'
    return (got == expected), (None if got == expected else f'got {got!r}, expected {expected!r}')


def rand_list(rng, maxlen=12, lo=-5, hi=5):
    return [rng.randint(lo, hi) for _ in range(rng.randint(0, maxlen))]


def search(prop, fixed, gen):
    """prop(*args) -> (ok, detail). Fixed edge cases first, then seeded random cases."""
    rng = random.Random(SEED)
    cases = list(fixed) + [gen(rng) for _ in range(N)]
    for args in cases:
        try:
            ok, detail = prop(*args)
        except Exception as e:
            return False, f'args={args!r}: raised {e!r}'
        if not ok:
            return False, f'args={args!r}: {detail}'
    return True, None


def L01():
    return eq(lambda: chunk(list(range(7)), 3), [[0, 1, 2], [3, 4, 5], [6]])


def L02():
    fixed = [([], 1), ([1], 1), ([1, 2, 3], 5), ([1, 2, 3], 1), ([0, -1], 2)]
    return search(lambda xs, k: (flatten(chunk(xs, k)) == xs, f'flatten(chunk)={flatten(chunk(xs, k))!r}'),
                  fixed, lambda r: (rand_list(r, 20, -10**6, 10**6), r.randint(1, 25)))


def L03():
    for xs in ([1, 2, 3], []):
        try:
            r = chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return False, f'chunk({xs!r}, 0) raised {e!r}, expected ValueError'
        return False, f'chunk({xs!r}, 0) returned {r!r}'
    return True, None


def L04():
    return eq(lambda: dedupe([3, 1, 3, 2, 1]), [3, 1, 2])


def _first_occ(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def L05():
    return search(lambda xs: (dedupe(xs) == _first_occ(xs), f'got {dedupe(xs)!r}, expected {_first_occ(xs)!r}'),
                  [([],), ([1, 1],), ([2, 1, 2],)], lambda r: (rand_list(r, 20),))


def L06():
    return search(lambda xs: (len(dedupe(xs)) == len(set(xs)), f'len(dedupe)={len(dedupe(xs))}, len(set)={len(set(xs))}'),
                  [([],), ([0, 0, 0],), ([1, True],)], lambda r: (rand_list(r, 20),))


def L07():
    return eq(lambda: flatten([[1, [2]], [3]]), [1, 2, 3])


def L08():
    return eq(lambda: top_n([5, 1, 4], 2), [5, 4])


def L09():
    fixed = [([], 0), ([], 3), ([1, 2], 0), ([1, 2], 5), ([3, 1, 2], 3)]
    return search(lambda xs, k: (len(top_n(xs, k)) == min(k, len(xs)), f'len={len(top_n(xs, k))}, expected {min(k, len(xs))}'),
                  fixed, lambda r: (rand_list(r, 15), r.randint(0, 20)))


def L10():
    return eq(lambda: top_n([3, 2, 1], -1), [])


def L11():
    return eq(lambda: rotate([1, 2, 3], 1), [2, 3, 1])


def L12():
    fixed = [([1, 2, 3], 3), ([1, 2, 3], 4), ([1], 1), ([1, 2], 2), ([1, 2, 3], 0), ([1, 2, 3], 1)]
    return search(lambda xs, k: (rotate(xs, k) == rotate(xs, k % len(xs)),
                                 f'rotate(xs,k)={rotate(xs, k)!r}, rotate(xs,k%len(xs))={rotate(xs, k % len(xs))!r}'),
                  fixed, lambda r: (rand_list(r, 10, 0, 9) or [0], r.randint(0, 30)))


def L13():
    fixed = [([], 0), ([], 5), ([], -3), ([1, 2, 3], -1), ([1, 2, 3], 7), ([1, 2, 3], -7)]
    return search(lambda xs, k: (len(rotate(xs, k)) == len(xs), f'len={len(rotate(xs, k))}, expected {len(xs)}'),
                  fixed, lambda r: (rand_list(r, 10), r.randint(-30, 30)))


def L14():
    return eq(lambda: interleave([1, 2, 3], [9]), [1, 9, 2, 3])


def L15():
    fixed = [([], []), ([1], []), ([1, 2, 3], [9])]
    return search(lambda a, b: (len(interleave(a, b)) == 2 * min(len(a), len(b)), f'len={len(interleave(a, b))}, expected {2 * min(len(a), len(b))}'),
                  fixed, lambda r: (rand_list(r, 10), rand_list(r, 10)))


def L16():
    return eq(lambda: frequencies('abca'), {'a': 2, 'b': 1, 'c': 1})


def L17():
    return search(lambda xs: (sum(frequencies(xs).values()) == len(xs), f'sum={sum(frequencies(xs).values())}, len={len(xs)}'),
                  [([],), ([1, 1, 1],), ([1, True, 1.0],)], lambda r: (rand_list(r, 20),))


def L18():
    return eq(lambda: pairwise([1, 2, 3]), [(1, 2), (2, 3)])


def L19():
    fixed = [([],), ([1],), ([1, 2],)]
    return search(lambda xs: (len(pairwise(xs)) == len(xs) - 1, f'len(pairwise)={len(pairwise(xs))}, len(xs)-1={len(xs) - 1}'),
                  fixed, lambda r: (rand_list(r, 10),))


CHECKS = {f'L{i:02d}': globals()[f'L{i:02d}'] for i in range(1, 20)}

if __name__ == '__main__':
    ids = sys.argv[1:] or list(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa', 'counterexample': ce,
                          'command': f'python3 checks/check_lists.py {i}'}, ensure_ascii=False))
