import os, sys, random, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit.lists import chunk, dedupe, flatten, top_n, rotate, interleave, frequencies, pairwise

SEED = 20240607


def _lists(rng, maxlen=8, n=300):
    """Small exhaustive-ish + random int lists, incl. empty, negatives, zero, duplicates."""
    out = [[]]
    for L in range(1, 5):
        out += [list(t) for t in itertools.product([-1, 0, 2], repeat=L)]
    for _ in range(n):
        out.append([rng.randint(-5, 5) for _ in range(rng.randint(0, maxlen))])
    out.append([10**20, -10**20, 10**20])
    return out


def _eq(name, got, exp):
    return got == exp, f"{name} -> {got!r} vs. esperado {exp!r}"


def _single(f, name):
    try:
        ok, msg = f()
    except Exception as e:
        return False, f"{name} -> exceção {type(e).__name__}: {e}"
    return (True, None) if ok else (False, msg)


def check_L01():
    return _single(lambda: _eq("chunk(list(range(7)), 3)", chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]]), "chunk")

def check_L02():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            for k in range(1, 10):
                r = flatten(chunk(xs, k))
                if r != xs:
                    return False, f"xs={xs}, k={k} -> {r} vs. esperado {xs}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L03():
    for xs in ([], [1, 2, 3]):
        try:
            r = chunk(xs, 0)
        except ValueError:
            continue
        except Exception as e:
            return False, f"chunk({xs}, 0) -> {type(e).__name__}: {e} vs. esperado ValueError"
        return False, f"chunk({xs}, 0) -> {r!r} vs. esperado ValueError"
    return True, None

def check_L04():
    return _single(lambda: _eq("dedupe([3,1,3,2,1])", dedupe([3,1,3,2,1]), [3,1,2]), "dedupe")

def check_L05():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            exp = [x for i, x in enumerate(xs) if x not in xs[:i]]
            r = dedupe(xs)
            if r != exp:
                return False, f"dedupe({xs}) -> {r} vs. esperado {exp}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L06():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            if len(dedupe(xs)) != len(set(xs)):
                return False, f"dedupe({xs}) -> len {len(dedupe(xs))} vs. esperado {len(set(xs))}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L07():
    return _single(lambda: _eq("flatten([[1,[2]],[3]])", flatten([[1,[2]],[3]]), [1,2,3]), "flatten")

def check_L08():
    return _single(lambda: _eq("top_n([5,1,4], 2)", top_n([5,1,4], 2), [5,4]), "top_n")

def check_L09():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            for k in range(0, 12):
                r = top_n(xs, k)
                if len(r) != min(k, len(xs)):
                    return False, f"top_n({xs}, {k}) -> len {len(r)} vs. esperado {min(k, len(xs))}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L10():
    return _single(lambda: _eq("top_n([3,2,1], -1)", top_n([3,2,1], -1), []), "top_n")

def check_L11():
    return _single(lambda: _eq("rotate([1,2,3], 1)", rotate([1,2,3], 1), [2,3,1]), "rotate")

def check_L12():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            if not xs:
                continue
            for k in range(0, 12):
                a, b = rotate(xs, k), rotate(xs, k % len(xs))
                if a != b:
                    return False, f"xs={xs}, k={k} -> rotate(xs,k)={a} vs. rotate(xs,k%len)={b}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L13():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            for k in range(-12, 13):
                r = rotate(xs, k)
                if len(r) != len(xs):
                    return False, f"rotate({xs}, {k}) -> len {len(r)} vs. esperado {len(xs)}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L14():
    return _single(lambda: _eq("interleave([1,2,3],[9])", interleave([1,2,3],[9]), [1,9,2,3]), "interleave")

def check_L15():
    rng = random.Random(SEED)
    ls = _lists(rng, n=60)
    try:
        for a in ls:
            for b in ls:
                r = interleave(a, b)
                if len(r) != 2 * min(len(a), len(b)):
                    return False, f"interleave({a}, {b}) -> len {len(r)} vs. esperado {2*min(len(a),len(b))}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L16():
    return _single(lambda: _eq("frequencies('abca')", frequencies('abca'), {'a':2,'b':1,'c':1}), "frequencies")

def check_L17():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            if sum(frequencies(xs).values()) != len(xs):
                return False, f"frequencies({xs}) -> soma {sum(frequencies(xs).values())} vs. esperado {len(xs)}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None

def check_L18():
    return _single(lambda: _eq("pairwise([1,2,3])", pairwise([1,2,3]), [(1,2),(2,3)]), "pairwise")

def check_L19():
    rng = random.Random(SEED)
    try:
        for xs in _lists(rng):
            if len(pairwise(xs)) != len(xs) - 1:
                return False, f"pairwise({xs}) -> len {len(pairwise(xs))} vs. esperado {len(xs)-1}"
    except Exception as e:
        return False, f"exceção {type(e).__name__}: {e}"
    return True, None


def main(argv):
    ids = argv or [f"L{i:02d}" for i in range(1, 20)]
    for i in ids:
        ok, msg = globals()[f"check_{i}"]()
        print(f"{i}\t{'verdadeira' if ok else 'falsa'}\t{'' if ok else msg.replace(chr(9), ' ').replace(chr(10), ' ')}")

if __name__ == "__main__":
    main(sys.argv[1:])
