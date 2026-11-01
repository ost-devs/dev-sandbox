import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from harness import run, rng
from calc.collections_util import *
def rl(r):
    return [r.choice([0,1,2,3,-1,'a','é',None]) for _ in range(r.randint(0,12))]
def check():
    r = rng('C4')
    cases = [([], 0), ([1,2], -1), ([1,2,3], -1), ([1], 0)] + [(rl(r), r.randint(-5, 20)) for _ in range(2000)]
    for xs, n in cases:
        try: xs2 = [x for x in xs if isinstance(x, int)]
        except Exception: pass
        xs2 = [x for x in xs if isinstance(x, int)]
        got = top_n(xs2, n)
        if len(got) != min(n, len(xs2)):
            return f"top_n({xs2},{n}) -> {got} (len {len(got)}) expected len {min(n, len(xs2))}"
run('C4', 'top_n length', check)
