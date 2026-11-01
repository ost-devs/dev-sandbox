from lib import strings, ints, first_fail, eq, rng
from kit.money import *

R = range(0, 1000001)


def sample_c(tag, n=20000):
    r = rng(tag)
    yield from [0, 1, 5, 99, 100, 1000, 999999, 1000000]
    for _ in range(n):
        yield r.randint(0, 1000000)


def tk():
    for t in ints('m9', lo=0, hi=1000):
        for k in range(1, 12):
            yield (t, k)
    r = rng('m9b')
    for _ in range(3000):
        yield (r.randint(0, 10**9), r.randint(1, 50))


def rates():
    r = rng('m19')
    yield from [0, 1, 0.15, 0.5, 1e-9, 1e-16]
    for _ in range(300):
        yield r.random()


CHECKS = {
    'M01': lambda: eq(lambda: to_cents('12,34'), 1234, "to_cents('12,34')"),
    'M02': lambda: eq(lambda: to_cents('1.234,5'), 123450, "to_cents('1.234,5')"),
    'M03': lambda: eq(lambda: to_cents('-1,50'), -150, "to_cents('-1,50')"),
    'M04': lambda: eq(lambda: to_cents('7'), 700, "to_cents('7')"),
    'M05': lambda: eq(lambda: format_brl(123456), 'R$ 1.234,56', 'format_brl(123456)'),
    'M06': lambda: eq(lambda: format_brl(5), 'R$ 0,05', 'format_brl(5)'),
    'M07': lambda: eq(lambda: format_brl(-150), 'R$ -1,50', 'format_brl(-150)'),
    'M08': lambda: first_fail(R, lambda c: to_cents(format_brl(c)[3:]) == c),
    'M09': lambda: first_fail(tk(), lambda p: sum(split_bill(*p)) == p[0]),
    'M10': lambda: eq(lambda: split_bill(900, 3), [300, 300, 300], 'split_bill(900,3)'),
    'M11': lambda: first_fail(tk(), lambda p: sum(installments(*p)) == p[0]),
    'M12': lambda: first_fail(tk(), lambda p: max(installments(*p)) - min(installments(*p)) <= 1),
    'M13': lambda: eq(lambda: installments(100, 3), [34, 33, 33], 'installments(100,3)'),
    'M14': lambda: eq(lambda: apply_discount(1000, 10), 900, 'apply_discount(1000,10)'),
    'M15': lambda: first_fail(R, lambda c: apply_discount(c, 0) == c),
    'M16': lambda: first_fail(((c, p) for c in sample_c('m16', 3000) for p in range(101)), lambda a: apply_discount(*a) <= a[0]),
    'M17': lambda: eq(lambda: add_tax(100, 0.15), 115, 'add_tax(100,0.15)'),
    'M18': lambda: first_fail(R, lambda c: add_tax(c, 0) == c),
    'M19': lambda: first_fail(((c, r) for c in sample_c('m19c', 2000) for r in rates()), lambda a: add_tax(*a) >= a[0]),
}
