import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import numbers as N

SEED = 20261101


def _try(f, *a):
    try:
        return f(*a), None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def eq(call_repr, f, args, expected):
    out, err = _try(f, *args)
    if err:
        return False, f'{call_repr} raised {err}; expected {expected!r}'
    if out == expected and type(out) is not bool or (out == expected and isinstance(expected, bool)):
        return True, None
    return False, f'{call_repr} -> {out!r}; expected {expected!r}'


def n01():
    rng = random.Random(SEED)
    cases = [(0, 0, 0), (-5, -3, 3), (5, 0, 0), (100, -1, 1), (-100, -1, 1)]
    cases += [(rng.randint(-100, 100), *sorted((rng.randint(-50, 50), rng.randint(-50, 50)))) for _ in range(20000)]
    for x, lo, hi in cases:
        out, err = _try(N.clamp, x, lo, hi)
        if err or not (lo <= out <= hi):
            return False, f'clamp({x},{lo},{hi}) -> {out!r} {err or ""}'
    return True, None


def n07():
    rng = random.Random(SEED)
    cases = [[1], [2, 1], [3, 1, 2], [0, 0], [-1, 5, -3, 2]]
    cases += [[rng.randint(-20, 20) for _ in range(rng.randint(1, 9))] for _ in range(20000)]
    for xs in cases:
        a, ea = _try(N.median, xs)
        b, eb = _try(N.median, sorted(xs))
        if ea or eb or a != b:
            return False, f'median({xs!r}) -> {a!r} {ea or ""}; sorted -> {b!r} {eb or ""}'
    return True, None


def n11():
    for x in [0, 1, -1, 5, 2.5, 1e10, -3.7, 0.0]:
        out, err = _try(N.percent, x, 0)
        if err or out != 0.0 or not isinstance(out, float):
            return False, f'percent({x!r}, 0) -> {out!r} {err or ""}; expected 0.0'
    return True, None


def n12():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, n))
    bad = []
    for n in range(0, 1001):
        out, err = _try(N.is_prime, n)
        if err or out != ref(n):
            bad.append((n, out if not err else err, ref(n)))
    if bad:
        n, o, e = bad[0]
        return False, f'is_prime({n}) -> {o!r}; expected {e!r} ({len(bad)} wrong values in 0..1000, first {[b[0] for b in bad[:5]]})'
    return True, None


def n15():
    for a in range(-50, 51):
        for b in range(-50, 51):
            x, ex = _try(N.gcd, a, b)
            y, ey = _try(N.gcd, b, a)
            if ex or ey or x != y:
                return False, f'gcd({a},{b}) -> {x!r} {ex or ""}; gcd({b},{a}) -> {y!r} {ey or ""}'
    return True, None


def n17():
    for a in range(-1000, 1001):
        out, err = _try(N.gcd, a, 0)
        if err or out != a:
            return False, f'gcd({a}, 0) -> {out!r} {err or ""}; expected {a}'
    return True, None


def n19():
    rng = random.Random(SEED)
    cases = [0, 1, -1, -5, 10, -1234, 10**30, -10**30] + [rng.randint(-10**9, 10**9) for _ in range(20000)]
    for n in cases:
        out, err = _try(N.digits_sum, n)
        if err or not (isinstance(out, int) and not isinstance(out, bool) and out >= 0):
            return False, f'digits_sum({n}) -> {out!r} {err or ""}; expected non-negative int'
    return True, None


def n06():
    out, err = _try(N.median, [])
    if err or out is not None:
        return False, f'median([]) -> {out!r} {err or ""}; expected None'
    return True, None


CHECKS = {
    'N01': n01,
    'N02': lambda: eq('clamp(5, 10, 0)', N.clamp, (5, 10, 0), 0),
    'N03': lambda: eq('mean([])', N.mean, ([],), 0),
    'N04': lambda: eq('mean([1, 2])', N.mean, ([1, 2],), 1.5),
    'N05': lambda: eq('median([3, 1, 2])', N.median, ([3, 1, 2],), 2),
    'N06': n06,
    'N07': n07,
    'N08': lambda: eq('round_half(2.5)', N.round_half, (2.5,), 3),
    'N09': lambda: eq('round_half(3.5)', N.round_half, (3.5,), 4),
    'N10': lambda: eq('percent(1, 3)', N.percent, (1, 3), 33.3),
    'N11': n11,
    'N12': n12,
    'N13': lambda: eq('is_prime(97)', N.is_prime, (97,), True),
    'N14': lambda: eq('is_prime(2)', N.is_prime, (2,), True),
    'N15': n15,
    'N16': lambda: eq('gcd(12, 18)', N.gcd, (12, 18), 6),
    'N17': n17,
    'N18': lambda: eq('digits_sum(1234)', N.digits_sum, (1234,), 10),
    'N19': n19,
}


def main():
    ids = sys.argv[1:] or sorted(CHECKS)
    for i in ids:
        ok, ce = CHECKS[i]()
        print(json.dumps({'id': i, 'verdict': 'verdadeira' if ok else 'falsa',
                          'counterexample': None if ok else ce,
                          'command': f'python3 checks/check_numbers.py {i}'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
