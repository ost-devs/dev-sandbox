def clamp(x, lo, hi):
    return max(lo, min(x, hi))


def mean(xs):
    return sum(xs) / len(xs) if xs else 0


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def round_half(x):
    return round(x)


def percent(part, total, digits=1):
    return round(100 * part / total, digits)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5)):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def digits_sum(n):
    return sum(int(c) for c in str(n))
