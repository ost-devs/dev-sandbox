from harness import claim, example, forall, run, rand_list, rand_int
from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate


@claim('C1')
def _():
    def prop(xs, n):
        xs0 = list(xs)
        out = chunk(list(xs), n)
        return [y for c in out for y in c] == xs0
    return forall(lambda r: (rand_list(r), r.randint(1, 20)), prop, seed=1, n=3000,
                  cases=[([], 1), ([1], 1), ([1, 2, 3], 5), ([1, 2, 3, 4], 2), ([1, 1, 1], 2)])


@claim('C2')
def _():
    def prop(xs):
        exp, seen = [], set()
        for x in xs:
            if x not in seen:
                seen.add(x)
                exp.append(x)
        return dedupe(list(xs)) == exp
    return forall(lambda r: (rand_list(r),), prop, seed=2, n=3000,
                  cases=[([],), ([1, 1],), ([2, 1, 2, 3, 1],)])


@claim('C3')
def _():
    return example(lambda: flatten([[1, [2]], [3]]), [1, 2, 3])


@claim('C4')
def _():
    def prop(xs, n):
        return len(top_n(list(xs), n)) == min(n, len(xs))
    return forall(lambda r: (rand_list(r), r.randint(-20, 20)), prop, seed=4, n=3000,
                  cases=[([], 0), ([1, 2, 3], -1), ([1, 2, 3], 0), ([1, 2, 3], 5), ([], -1), ([1, 1], 1)])


@claim('C5')
def _():
    def prop(a, b):
        a0, b0 = dict(a), dict(b)
        m = merge_dicts(dict(a), dict(b))
        return all(m[k] == a0[k] for k in a0 if k in b0)
    def gen(r):
        mk = lambda: {r.randint(0, 5): r.randint(0, 9) for _ in range(r.randint(0, 5))}
        return (mk(), mk())
    return forall(gen, prop, seed=5, n=3000,
                  cases=[({'k': 1}, {'k': 2}), ({}, {}), ({'a': 1}, {'b': 2})])


@claim('C6')
def _():
    def prop(xs):
        return rotate(list(xs), len(xs)) == xs
    return forall(lambda r: (rand_list(r),), prop, seed=6, n=3000,
                  cases=[([],), ([1],), ([1, 2, 3],), ([1, 1, 2],)])


if __name__ == '__main__':
    run()
