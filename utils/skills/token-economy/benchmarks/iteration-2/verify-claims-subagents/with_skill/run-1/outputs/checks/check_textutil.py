from harness import claim, example, forall, run, rand_text, rand_int
from calc.textutil import *

@claim('T1')
def _():
    return forall(lambda r: (rand_text(r),), lambda s: not slugify(s).startswith('-') and not slugify(s).endswith('-'),
                  seed=1, n=5000, cases=[('',), ('-',), ('  a  ',), ('!!!',), ('é',), ('-a-',), ('Café',)])

@claim('T2')
def _():
    return example(lambda: slugify('Café Noir'), 'cafe-noir')

@claim('T3')
def _():
    return forall(lambda r: (rand_text(r), r.randint(0, 25)), lambda s, n: len(truncate(s, n)) <= n,
                  seed=3, n=5000, cases=[('', 0), ('a', 0), ('ab', 0), ('abc', 1), ('abc', 2), ('abc', 3)])

@claim('T4')
def _():
    return example(lambda: count_words('a  b\tc\n'), 3)

@claim('T5')
def _():
    return example(lambda: capitalize_words('a  b'), 'A  B')

@claim('T6')
def _():
    return example(lambda: is_palindrome(''), True)

if __name__ == '__main__':
    run()
