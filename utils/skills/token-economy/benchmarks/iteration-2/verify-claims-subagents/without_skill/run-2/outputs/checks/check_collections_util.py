"""Executable checks for claims C1-C6 about calc/collections_util.py (stdlib only)."""
import copy
import os
import random
import sys

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKDIR)

from calc.collections_util import chunk, dedupe, flatten, top_n, merge_dicts, rotate  # noqa: E402

SEED = 20261029
RANDOM_CASES = 3000


class Fail(Exception):
    pass


def call(fn, *args):
    """Call fn, converting exceptions into a claim failure description."""
    try:
        return fn(*args)
    except Exception as e:  # exception => claim fails
        raise Fail(f"raised {type(e).__name__}: {e}")


def rand_lists(rng, hashable=True):
    out = []
    for _ in range(RANDOM_CASES):
        length = rng.randint(0, 12)
        pool = rng.randint(1, 6)  # small pool => many duplicates
        kind = rng.randint(0, 2)
        if kind == 0 or not hashable:
            xs = [rng.randint(-pool, pool) for _ in range(length)]
        elif kind == 1:
            xs = [rng.choice("abcdef"[:pool]) for _ in range(length)]
        else:
            xs = [rng.choice([0, 1, 1.0, True, False, None, (1, 2), "x"]) for _ in range(length)]
        if not hashable and xs and rng.random() < 0.5:
            xs = [[v] for v in xs]
        out.append(xs)
    return out


def by_size(case):
    return (len(repr(case)), repr(case))


def report(cid, fn):
    try:
        fails = fn()
    except Fail as f:
        print(f"{cid} | FALSE | counterexample: {f}")
        return
    if not fails:
        print(f"{cid} | TRUE")
    else:
        print(f"{cid} | FALSE | counterexample: {min(fails, key=lambda s: (len(s), s))}")


# ---------------- C1 ----------------
def c1():
    rng = random.Random(SEED + 1)
    fixed = [[], [1], [1, 2, 3], [1, 2, 3, 4], [1, 1, 1], [[1], [2]], list("hello")]
    cases = [(xs, n) for xs in fixed for n in range(1, 8)]
    cases += [(xs, rng.randint(1, 15)) for xs in rand_lists(rng, hashable=False)]
    fails = []
    for xs, n in cases:
        snap = copy.deepcopy(xs)
        try:
            parts = chunk(xs, n)
        except Exception as e:
            fails.append(f"chunk({snap!r}, {n}) -> raised {type(e).__name__}: {e} vs expected chunks concatenating to {snap!r}")
            continue
        joined = [y for p in parts for y in p]
        if joined != snap:
            fails.append(f"chunk({snap!r}, {n}) -> concat {joined!r} vs expected {snap!r}")
        elif xs != snap:
            fails.append(f"chunk({snap!r}, {n}) mutated input to {xs!r}")
    return fails


# ---------------- C2 ----------------
def ref_dedupe(xs):
    out = []
    for x in xs:
        if not any(x == y for y in out):
            out.append(x)
    return out


def c2():
    rng = random.Random(SEED + 2)
    fixed = [[], [1], [1, 1], [3, 1, 3, 2, 1], ["b", "a", "b"], [1, True, 1.0, 0, False], [None, None, (1,), (1,)]]
    fails = []
    for xs in fixed + rand_lists(rng):
        snap = list(xs)
        try:
            got = dedupe(xs)
        except Exception as e:
            fails.append(f"dedupe({snap!r}) -> raised {type(e).__name__}: {e}")
            continue
        exp = ref_dedupe(snap)
        # compare element identity/type too (first occurrence must be kept, e.g. 1 vs True)
        if got != exp or [type(v) for v in got] != [type(v) for v in exp]:
            fails.append(f"dedupe({snap!r}) -> {got!r} vs expected {exp!r}")
        elif xs != snap:
            fails.append(f"dedupe({snap!r}) mutated input to {xs!r}")
    return fails


# ---------------- C3 ----------------
def c3():
    xs = [[1, [2]], [3]]
    snap = copy.deepcopy(xs)
    got = call(flatten, xs)
    exp = [1, 2, 3]
    if got != exp:
        return [f"flatten({snap!r}) -> {got!r} vs expected {exp!r}"]
    return []


# ---------------- C4 ----------------
def c4():
    rng = random.Random(SEED + 4)
    fixed_lists = [[], [1], [1, 2], [2, 1, 2], [5, 5, 5], [3, 1, 2, 4]]
    cases = [(xs, n) for xs in fixed_lists for n in range(-6, 8)]
    cases += [(xs, rng.randint(-15, 15)) for xs in rand_lists(rng) if all(isinstance(v, int) for v in xs)]
    fails = []
    for xs, n in cases:
        snap = list(xs)
        try:
            got = top_n(xs, n)
        except Exception as e:
            fails.append(f"top_n({snap!r}, {n}) -> raised {type(e).__name__}: {e}")
            continue
        claimed = min(n, len(snap))
        # A list cannot have a negative length; the only sensible reading of a
        # negative min(n, len) is "0 items". Any other count is a mismatch.
        exp_len = max(claimed, 0)
        if len(got) != exp_len:
            fails.append(
                f"top_n({snap!r}, {n}) -> {got!r} ({len(got)} items) vs expected "
                f"min({n}, {len(snap)}) = {claimed} items (i.e. {exp_len})"
            )
        elif xs != snap:
            fails.append(f"top_n({snap!r}, {n}) mutated input to {xs!r}")
    return fails


# ---------------- C5 ----------------
def c5():
    fails = []
    for a, b, k in [({"k": 1}, {"k": 2}, "k"), ({"x": 0, "y": 1}, {"y": 9}, "y")]:
        sa, sb = dict(a), dict(b)
        got = call(merge_dicts, a, b)
        if got.get(k) != sa[k]:
            fails.append(f"merge_dicts({sa!r}, {sb!r})[{k!r}] -> {got.get(k)!r} vs expected {sa[k]!r}")
    return fails


# ---------------- C6 ----------------
def c6():
    rng = random.Random(SEED + 6)
    fixed = [[], [1], [1, 2], [1, 2, 3], [1, 1, 2], [[1], [2]], [None]]
    fails = []
    for xs in fixed + rand_lists(rng, hashable=False):
        snap = copy.deepcopy(xs)
        try:
            got = rotate(xs, len(xs))
        except Exception as e:
            fails.append(f"rotate({snap!r}, {len(snap)}) -> raised {type(e).__name__}: {e}")
            continue
        if got != snap:
            fails.append(f"rotate({snap!r}, {len(snap)}) -> {got!r} vs expected {snap!r}")
        elif xs != snap:
            fails.append(f"rotate({snap!r}, {len(snap)}) mutated input to {xs!r}")
    return fails


if __name__ == "__main__":
    for cid, fn in [("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4), ("C5", c5), ("C6", c6)]:
        report(cid, fn)
    sys.exit(0)
