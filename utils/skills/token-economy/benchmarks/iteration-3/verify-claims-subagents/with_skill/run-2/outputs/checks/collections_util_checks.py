from harness import claim, rng, run
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate


def lists():
    r = rng()
    out = [[], [0], [1, 1], ['é', '漢', 'é'], [-1, -2, 0]]
    for _ in range(300):
        out.append([r.randint(-5, 5) for _ in range(r.randint(0, 20))])
    return out


@claim('C1')
def c1():
    for xs in lists():
        for n in range(1, len(xs) + 3):
            c = chunk(xs, n)
            if [y for p in c for y in p] != xs:
                return 'chunk(%r,%d)=%r' % (xs, n, c)


@claim('C2')
def c2():
    for xs in lists():
        exp = [x for i, x in enumerate(xs) if x not in xs[:i]]
        if dedupe(xs) != exp:
            return 'dedupe(%r)=%r' % (xs, dedupe(xs))


@claim('C3')
def c3():
    r = flatten([[1, [2]], [3]])
    if r != [1, 2, 3]:
        return 'flatten([[1, [2]], [3]])=%r' % (r,)


@claim('C4')
def c4():
    for xs in lists():
        for n in range(-len(xs) - 2, len(xs) + 3):
            r = top_n(xs, n)
            if len(r) != min(n, len(xs)):
                return 'top_n(%r,%d)=%r (len %d, expected %d)' % (xs, n, r, len(r), min(n, len(xs)))


@claim('C5')
def c5():
    a, b = {'k': 1}, {'k': 2}
    r = merge_dicts(a, b)
    if r['k'] != a['k']:
        return "merge_dicts(%r,%r)=%r" % (a, b, r)


@claim('C6')
def c6():
    for xs in lists():
        if rotate(xs, len(xs)) != xs:
            return 'rotate(%r,%d)=%r' % (xs, len(xs), rotate(xs, len(xs)))


if __name__ == '__main__':
    run('collections_util')
