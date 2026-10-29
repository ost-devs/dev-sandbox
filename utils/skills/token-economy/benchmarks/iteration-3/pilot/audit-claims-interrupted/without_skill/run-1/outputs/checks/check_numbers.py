#!/usr/bin/env python3
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kit import numbers as K

SEED = 20240611
V, F = "verdadeira", "falsa"


def call(f, *a):
    try:
        return ("ok", f(*a))
    except Exception as e:
        return ("exc", f"{type(e).__name__}: {e}")


def eq_check(f, args, expected):
    r = call(f, *args)
    if r[0] == "ok" and r[1] == expected:
        return V, None
    return F, f"{f.__name__}{args!r} -> {r[1]!r} ({'resultado' if r[0]=='ok' else 'excecao'}); esperado {expected!r}"


def n01():
    rng = random.Random(SEED)
    cases = [(0, 0, 0), (-1, 0, 0), (5, 5, 5), (-5, -10, -1), (100, -3, 3), (0, -1, 1)]
    for _ in range(3000):
        lo = rng.randint(-100, 100)
        cases.append((rng.randint(-200, 200), lo, lo + rng.randint(0, 50)))
    for x, lo, hi in cases:
        r = call(K.clamp, x, lo, hi)
        if r[0] != "ok" or not (lo <= r[1] <= hi):
            return F, f"clamp({x}, {lo}, {hi}) -> {r[1]!r}; esperado dentro de [{lo}, {hi}]"
    return V, None


def n02(): return eq_check(K.clamp, (5, 10, 0), 0)
def n03(): return eq_check(K.mean, ([],), 0)
def n04(): return eq_check(K.mean, ([1, 2],), 1.5)
def n05(): return eq_check(K.median, ([3, 1, 2],), 2)


def n06():
    r = call(K.median, [])
    if r == ("ok", None):
        return V, None
    return F, f"median([]) -> {r[1]!r}; esperado None"


def n07():
    rng = random.Random(SEED)
    cases = [[0], [1, 2], [2, 1], [-1], [3, 1, 2], [5, 5], [0, 0, 0, 0]]
    for _ in range(3000):
        cases.append([rng.randint(-20, 20) for _ in range(rng.randint(1, 9))])
    for xs in cases:
        a, b = call(K.median, list(xs)), call(K.median, sorted(xs))
        if a != b:
            return F, f"median({xs!r}) -> {a[1]!r}; median(sorted) -> {b[1]!r}"
    return V, None


def n08(): return eq_check(K.round_half, (2.5,), 3)
def n09(): return eq_check(K.round_half, (3.5,), 4)
def n10(): return eq_check(K.percent, (1, 3), 33.3)


def n11():
    rng = random.Random(SEED)
    xs = [0, 1, -1, 0.0, 2.5, -3.5, 100] + [rng.randint(-1000, 1000) for _ in range(1000)] + [rng.uniform(-1e3, 1e3) for _ in range(1000)]
    for x in xs:
        r = call(K.percent, x, 0)
        if r != ("ok", 0.0):
            return F, f"percent({x!r}, 0) -> {r[1]!r}; esperado 0.0"
    return V, None


def n12():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, n))
    for n in range(0, 1001):
        r = call(K.is_prime, n)
        if r != ("ok", ref(n)):
            return F, f"is_prime({n}) -> {r[1]!r}; esperado {ref(n)!r}"
    return V, None


def n13(): return eq_check(K.is_prime, (97,), True)
def n14(): return eq_check(K.is_prime, (2,), True)


def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            x, y = call(K.gcd, a, b), call(K.gcd, b, a)
            if x != y:
                return F, f"gcd({a}, {b}) -> {x[1]!r}; gcd({b}, {a}) -> {y[1]!r}"
    return V, None


def n16(): return eq_check(K.gcd, (12, 18), 6)


def n17():
    rng = random.Random(SEED)
    xs = [0, 1, -1, 2, -2, 10**30, -10**30] + [rng.randint(-10**6, 10**6) for _ in range(2000)]
    for a in xs:
        r = call(K.gcd, a, 0)
        if r != ("ok", a):
            return F, f"gcd({a}, 0) -> {r[1]!r}; esperado {a!r}"
    return V, None


def n18(): return eq_check(K.digits_sum, (1234,), 10)


def n19():
    rng = random.Random(SEED)
    xs = [0, 1, -1, 9, -9, 10, -10] + [rng.randint(-10**6, 10**6) for _ in range(2000)]
    for n in xs:
        r = call(K.digits_sum, n)
        if r[0] != "ok" or not isinstance(r[1], int) or r[1] < 0:
            return F, f"digits_sum({n}) -> {r[1]!r}; esperado inteiro >= 0"
    return V, None


CHECKS = {f"N{i:02d}": globals()[f"n{i:02d}"] for i in range(1, 20)}

if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        v, c = CHECKS[i]()
        print(json.dumps({"id": i, "verdict": v, "counterexample": c}, ensure_ascii=False))
