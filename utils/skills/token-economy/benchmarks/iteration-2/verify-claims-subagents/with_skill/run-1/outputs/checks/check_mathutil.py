from harness import claim, example, forall, run, rand_int
from calc.mathutil import clamp, mean, round_half, gcd, is_prime, percent

@claim('M1')
def _():
    def gen(r):
        lo = rand_int(r); hi = lo + r.randint(0, 500)
        return (rand_int(r, -2000, 2000), lo, hi)
    cases = [(5, 0, 0), (-1, 0, 0), (0, -3, -3), (1.5, 1, 2), (float('inf'), 0, 1), (float('-inf'), 0, 1), (0.5, 0.5, 0.5), (float('nan'), 0, 1)]
    return forall(gen, lambda x, lo, hi: lo <= clamp(x, lo, hi) <= hi, seed=1, n=3000, cases=cases)

@claim('M2')
def _():
    return example(lambda: mean([]), 0)

@claim('M3')
def _():
    return example(lambda: round_half(2.5), 3)

@claim('M4')
def _():
    cases = [(0, 0), (0, 5), (5, 0), (-4, 6), (6, -4), (-4, -6), (1, 0)]
    return forall(lambda r: (rand_int(r), rand_int(r)), lambda a, b: gcd(a, b) == gcd(b, a), seed=4, n=3000, cases=cases)

@claim('M5')
def _():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, n))
    bad = []
    for n in range(0, 1001):
        try:
            got = is_prime(n)
        except Exception as e:
            got = f'raised {type(e).__name__}'
        if got is not ref(n):
            bad.append(n)
    if bad:
        return False, f'{len(bad)} wrong of 1001; first: {bad[:8]}'
    return True, 'all 0..1000 correct'

@claim('M6')
def _():
    return example(lambda: percent(1, 3), 33.3)

if __name__ == '__main__':
    run()
