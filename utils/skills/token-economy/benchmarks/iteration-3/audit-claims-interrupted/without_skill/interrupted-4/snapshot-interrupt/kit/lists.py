def chunk(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def dedupe(xs):
    return list(dict.fromkeys(xs))


def flatten(xs):
    return [y for x in xs for y in x]


def top_n(xs, n):
    return sorted(xs, reverse=True)[:n]


def rotate(xs, k):
    return xs[k:] + xs[:k]


def interleave(a, b):
    return [x for pair in zip(a, b) for x in pair]


def frequencies(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


def pairwise(xs):
    return list(zip(xs, xs[1:]))
