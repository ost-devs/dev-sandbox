def to_cents(s):
    reais, _, cents = s.partition(',')
    return int(reais.replace('.', '')) * 100 + int(cents.ljust(2, '0')[:2])


def format_brl(cents):
    return 'R$ ' + f'{cents // 100:,}'.replace(',', '.') + f',{cents % 100:02d}'


def split_bill(total, n):
    return [total // n] * n


def installments(total, n):
    base, rest = divmod(total, n)
    return [base + 1 if i < rest else base for i in range(n)]


def apply_discount(cents, pct):
    return round(cents * (100 - pct) / 100)


def add_tax(cents, rate):
    return int(cents * (1 + rate))
