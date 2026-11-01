def clamp(x, lo, hi):
    return max(lo, min(x, hi))


def mean(xs):
    return sum(xs) / len(xs)


def round_half(x):
    return round(x)


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5)):
        if n % d == 0:
            return False
    return True


def percent(a, b):
    return round(100 * a / b, 1)
