def chunk(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def dedupe(xs):
    return list(dict.fromkeys(xs))


def flatten(xs):
    return [y for x in xs for y in x]


def top_n(xs, n):
    return sorted(xs, reverse=True)[:n]


def merge_dicts(a, b):
    return {**a, **b}


def rotate(xs, k):
    return xs[k:] + xs[:k]
