import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.lists import *

def eq(actual, expected):
    if actual != expected:
        raise Counter(f"actual={actual!r} expected={expected!r}")

def gl(r): return (rand_list(r),)
def gl_k(r): return (rand_list(r), r.randint(-3, 12))

@claim("L01")
def _(): eq(chunk(list(range(7)), 3), [[0,1,2],[3,4,5],[6]])

@claim("L02")
def _(): forall("L02", lambda r: (rand_list(r), r.randint(1, 12)), lambda xs, k: flatten(chunk(xs, k)) == xs)

@claim("L03")
def _():
    for xs in ([], [1,2,3]):
        try: chunk(xs, 0)
        except ValueError: continue
        raise Counter(f"chunk({xs},0) did not raise ValueError")

@claim("L04")
def _(): eq(dedupe([3,1,3,2,1]), [3,1,2])

@claim("L05")
def _():
    def ref(xs):
        out = []
        for x in xs:
            if x not in out: out.append(x)
        return out
    forall("L05", gl, lambda xs: dedupe(xs) == ref(xs))

@claim("L06")
def _(): forall("L06", gl, lambda xs: len(dedupe(xs)) == len(set(xs)))

@claim("L07")
def _(): eq(flatten([[1,[2]],[3]]), [1,2,3])

@claim("L08")
def _(): eq(top_n([5,1,4], 2), [5,4])

@claim("L09")
def _(): forall("L09", lambda r: (rand_list(r), r.randint(0, 12)), lambda xs, k: len(top_n(xs, k)) == min(k, len(xs)))

@claim("L10")
def _(): eq(top_n([3,2,1], -1), [])

@claim("L11")
def _(): eq(rotate([1,2,3], 1), [2,3,1])

@claim("L12")
def _(): forall("L12", lambda r: (rand_list(r, minlen=1), r.randint(0, 20)), lambda xs, k: rotate(xs, k) == rotate(xs, k % len(xs)))

@claim("L13")
def _(): forall("L13", lambda r: (rand_list(r), r.randint(-25, 25)), lambda xs, k: len(rotate(xs, k)) == len(xs))

@claim("L14")
def _(): eq(interleave([1,2,3],[9]), [1,9,2,3])

@claim("L15")
def _(): forall("L15", lambda r: (rand_list(r), rand_list(r)), lambda a, b: len(interleave(a, b)) == 2*min(len(a), len(b)))

@claim("L16")
def _(): eq(frequencies('abca'), {'a':2,'b':1,'c':1})

@claim("L17")
def _(): forall("L17", gl, lambda xs: sum(frequencies(xs).values()) == len(xs))

@claim("L18")
def _(): eq(pairwise([1,2,3]), [(1,2),(2,3)])

@claim("L19")
def _(): forall("L19", gl, lambda xs: len(pairwise(xs)) == len(xs)-1)

if __name__=='__main__': main('lists')
