# Claims about kit/

| id | module | claim |
|---|---|---|
| T01 | text | `slugify('Café Noir') == 'cafe-noir'`. |
| T02 | text | `slugify(s)` never starts or ends with `-`, for any string `s`. |
| T03 | text | `slugify(s)` contains only `a-z`, `0-9` and `-`, for any string `s`. |
| T04 | text | `slugify(slugify(s)) == slugify(s)` for any string `s`. |
| T05 | text | `len(truncate(s, n)) <= n` for every string `s` and every integer `n >= 0`. |
| T06 | text | `truncate('abcdef', 5) == 'ab...'`. |
| T07 | text | `truncate(s, n) == s` whenever `len(s) <= n`. |
| T08 | text | `count_words('a  b\tc\n') == 3`. |
| T09 | text | `count_words('') == 0`. |
| T10 | text | `title_case('a  b') == 'A  B'` (the double space is kept). |
| T11 | text | `title_case('élan vital') == 'Élan Vital'`. |
| T12 | text | `len(title_case(s)) == len(s)` for any string `s`. |
| T13 | text | `strip_accents('Ação') == 'Acao'`. |
| T14 | text | `strip_accents('ø') == 'o'`. |
| T15 | text | `pad_left('7', 3, '0') == '007'`. |
| T16 | text | `len(pad_left(s, n)) == max(len(s), n)` for any string `s` and integer `n >= 0`. |
| T17 | text | `is_palindrome('')` is `True`. |
| T18 | text | `is_palindrome('A man, a plan, a canal: Panama')` is `True`. |
| T19 | text | `is_palindrome(s) == is_palindrome(s[::-1])` for any string `s`. |
| N01 | numbers | For integers `lo <= hi`, `clamp(x, lo, hi)` is always within `[lo, hi]`. |
| N02 | numbers | `clamp(5, 10, 0) == 0`. |
| N03 | numbers | `mean([]) == 0`. |
| N04 | numbers | `mean([1, 2]) == 1.5`. |
| N05 | numbers | `median([3, 1, 2]) == 2`. |
| N06 | numbers | `median([])` returns `None`. |
| N07 | numbers | `median(xs) == median(sorted(xs))` for every non-empty list of integers `xs`. |
| N08 | numbers | `round_half(2.5) == 3`. |
| N09 | numbers | `round_half(3.5) == 4`. |
| N10 | numbers | `percent(1, 3) == 33.3`. |
| N11 | numbers | `percent(x, 0)` returns `0.0` for any number `x`. |
| N12 | numbers | `is_prime(n)` is correct for every `n` from 0 to 1000. |
| N13 | numbers | `is_prime(97)` is `True`. |
| N14 | numbers | `is_prime(2)` is `True`. |
| N15 | numbers | `gcd(a, b) == gcd(b, a)` for all integers `a`, `b` in `[-50, 50]`. |
| N16 | numbers | `gcd(12, 18) == 6`. |
| N17 | numbers | `gcd(a, 0) == a` for every integer `a`. |
| N18 | numbers | `digits_sum(1234) == 10`. |
| N19 | numbers | `digits_sum(n)` returns a non-negative integer for every integer `n`. |
| D01 | dates | `add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)`. |
| D02 | dates | For every date `x` from 2000 to 2030, `add_months(x, 12)` has the same day and month as `x`, one year later. |
| D03 | dates | `add_months(add_months(x, 1), -1) == x` for every date `x` from 2000 to 2030. |
| D04 | dates | `days_between(a, b)` is never negative. |
| D05 | dates | `days_between(a, b) == -days_between(b, a)` for all dates `a`, `b`. |
| D06 | dates | `is_leap(1900)` is `False`. |
| D07 | dates | `is_leap(2000)` is `True`. |
| D08 | dates | `is_leap(y) == calendar.isleap(y)` for every year `y` from 1 to 9999. |
| D09 | dates | `weekday_name(date(2024, 1, 1)) == 'Monday'`. |
| D10 | dates | `quarter(date(2024, 4, 1)) == 2`. |
| D11 | dates | `quarter(x)` is always one of 1, 2, 3, 4. |
| D12 | dates | `end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)`. |
| D13 | dates | `end_of_month(x) >= x` for every date `x` from 2000 to 2030. |
| D14 | dates | `iso_week(date(2021, 1, 1)) == 1`. |
| D15 | dates | `parse_br('31/12/2024') == date(2024, 12, 31)`. |
| D16 | dates | `parse_br('1/2/2024')` raises `ValueError` (day and month need two digits). |
| D17 | dates | `add_days(x, k) - x == timedelta(days=k)` for every date `x` from 2000 to 2030 and integer `k` from -1000 to 1000. |
| D18 | dates | `add_months(x, k).day <= x.day` for every date `x` from 2000 to 2030 and integer `k` from -30 to 30. |
| D19 | dates | `weekday_name(add_days(x, 7)) == weekday_name(x)` for every date `x` from 2000 to 2030. |
| L01 | lists | `chunk(list(range(7)), 3) == [[0, 1, 2], [3, 4, 5], [6]]`. |
| L02 | lists | `flatten(chunk(xs, k)) == xs` for every list of integers `xs` and integer `k >= 1`. |
| L03 | lists | `chunk(xs, 0)` raises `ValueError`. |
| L04 | lists | `dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]`. |
| L05 | lists | For every list of integers, `dedupe` keeps the order of first occurrences. |
| L06 | lists | `len(dedupe(xs)) == len(set(xs))` for every list of integers `xs`. |
| L07 | lists | `flatten([[1, [2]], [3]]) == [1, 2, 3]`. |
| L08 | lists | `top_n([5, 1, 4], 2) == [5, 4]`. |
| L09 | lists | `len(top_n(xs, k)) == min(k, len(xs))` for every list of integers and integer `k >= 0`. |
| L10 | lists | `top_n([3, 2, 1], -1) == []`. |
| L11 | lists | `rotate([1, 2, 3], 1) == [2, 3, 1]`. |
| L12 | lists | `rotate(xs, k) == rotate(xs, k % len(xs))` for every non-empty list `xs` and integer `k >= 0`. |
| L13 | lists | `len(rotate(xs, k)) == len(xs)` for every list `xs` and integer `k`. |
| L14 | lists | `interleave([1, 2, 3], [9]) == [1, 9, 2, 3]`. |
| L15 | lists | `len(interleave(a, b)) == 2 * min(len(a), len(b))` for all lists `a`, `b`. |
| L16 | lists | `frequencies('abca') == {'a': 2, 'b': 1, 'c': 1}`. |
| L17 | lists | `sum(frequencies(xs).values()) == len(xs)` for every list of integers `xs`. |
| L18 | lists | `pairwise([1, 2, 3]) == [(1, 2), (2, 3)]`. |
| L19 | lists | `len(pairwise(xs)) == len(xs) - 1` for every list `xs`. |
| M01 | money | `to_cents('12,34') == 1234`. |
| M02 | money | `to_cents('1.234,5') == 123450`. |
| M03 | money | `to_cents('-1,50') == -150`. |
| M04 | money | `to_cents('7') == 700`. |
| M05 | money | `format_brl(123456) == 'R$ 1.234,56'`. |
| M06 | money | `format_brl(5) == 'R$ 0,05'`. |
| M07 | money | `format_brl(-150) == 'R$ -1,50'`. |
| M08 | money | `to_cents(format_brl(c)[3:]) == c` for every integer `c` from 0 to 1,000,000. |
| M09 | money | `sum(split_bill(total, k)) == total` for every integer `total >= 0` and `k >= 1`. |
| M10 | money | `split_bill(900, 3) == [300, 300, 300]`. |
| M11 | money | `sum(installments(total, k)) == total` for every integer `total >= 0` and `k >= 1`. |
| M12 | money | In `installments(total, k)`, the largest and smallest installment differ by at most 1. |
| M13 | money | `installments(100, 3) == [34, 33, 33]`. |
| M14 | money | `apply_discount(1000, 10) == 900`. |
| M15 | money | `apply_discount(c, 0) == c` for every integer `c` from 0 to 1,000,000. |
| M16 | money | `apply_discount(c, p) <= c` for every integer `c` from 0 to 1,000,000 and every integer `p` from 0 to 100. |
| M17 | money | `add_tax(100, 0.15) == 115`. |
| M18 | money | `add_tax(c, 0) == c` for every integer `c` from 0 to 1,000,000. |
| M19 | money | `add_tax(c, r) >= c` for every integer `c` from 0 to 1,000,000 and every rate `r` from 0 to 1. |
| I01 | intervals | `overlaps((0, 5), (5, 10))` is `False`. |
| I02 | intervals | `overlaps(a, b) == overlaps(b, a)` for all intervals `a`, `b`. |
| I03 | intervals | `merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]`. |
| I04 | intervals | `merge([(1, 2), (2, 3)]) == [(1, 3)]`. |
| I05 | intervals | For every non-empty list of intervals with start < end, `merge` returns intervals sorted by start with no two overlapping. |
| I06 | intervals | `merge(merge(xs)) == merge(xs)` for every non-empty list of intervals with start < end. |
| I07 | intervals | `contains((0, 5), 5)` is `False` (intervals are half-open, the end is excluded). |
| I08 | intervals | `contains(a, a[0])` is `True` for every interval with start < end. |
| I09 | intervals | `intersect((0, 5), (3, 8)) == (3, 5)`. |
| I10 | intervals | `intersect((0, 2), (5, 6))` is `None`. |
| I11 | intervals | `intersect((0, 5), (5, 8))` is `None`. |
| I12 | intervals | `total_covered([(0, 5), (3, 8)]) == 8`. |
| I13 | intervals | `total_covered(xs) <= sum(length(i) for i in xs)` for every non-empty list of intervals with start < end. |
| I14 | intervals | For intervals with start < end that overlap, `length(intersect(a, b)) <= min(length(a), length(b))`. |
| I15 | intervals | `merge([]) == []`. |
| I16 | intervals | `overlaps(a, a)` is `True` for every interval with start < end. |
| I17 | intervals | `merge([(5, 7), (1, 2)]) == [(1, 2), (5, 7)]`. |
| I18 | intervals | For integer intervals, `contains(a, x)` implies `overlaps(a, (x, x + 1))`. |
| I19 | intervals | `length((3, 1))` returns `0` for an inverted interval. |
| P01 | paths | `join('a', 'b', 'c.txt') == 'a/b/c.txt'`. |
| P02 | paths | `join('/usr', 'bin') == '/usr/bin'`. |
| P03 | paths | `join('a/', '/b') == 'a/b'`. |
| P04 | paths | `ext('foto.tar.gz') == 'gz'`. |
| P05 | paths | `ext('dir.d/arquivo') == ''`. |
| P06 | paths | `ext('.bashrc') == ''`. |
| P07 | paths | `stem('relatorio.pdf') == 'relatorio'`. |
| P08 | paths | `normalize('a/./b/../c') == 'a/c'`. |
| P09 | paths | `normalize('/a/../..') == '/'`. |
| P10 | paths | `normalize('../x') == '../x'`. |
| P11 | paths | `normalize(normalize(x)) == normalize(x)` for every path string `x`. |
| P12 | paths | `is_hidden('.env')` is `True`. |
| P13 | paths | `is_hidden('config/.git/HEAD')` is `False`. |
| P14 | paths | `depth('/a/b/c') == 3`. |
| P15 | paths | `depth('a//b/') == 2`. |
| P16 | paths | `parent('a/b/c') == 'a/b'`. |
| P17 | paths | `parent('/a') == '/'`. |
| P18 | paths | `depth(join(*parts)) == len(parts)` for every non-empty list of names made of letters and digits. |
| P19 | paths | `stem(x) + '.' + ext(x) == x` for every string `x` that contains a dot. |
| R01 | records | `parse_kv('a=1;b=2') == {'a': '1', 'b': '2'}`. |
| R02 | records | `parse_kv('a=1;;b=2') == {'a': '1', 'b': '2'}`. |
| R03 | records | `parse_kv('url=x=y') == {'url': 'x=y'}`. |
| R04 | records | `parse_kv('a=1;flag') == {'a': '1', 'flag': ''}`. |
| R05 | records | `parse_kv(to_kv(d)) == d` for every dict whose keys and values are non-empty strings of letters and digits. |
| R06 | records | `parse_kv(to_kv(d)) == d` for every dict of strings to strings. |
| R07 | records | `pick({'a': 1, 'b': 2}, ['a', 'c']) == {'a': 1}`. |
| R08 | records | `len(pick(d, keys)) <= len(d)` for every dict `d` and list `keys`. |
| R09 | records | `rename({'a': 1}, {'a': 'b'}) == {'b': 1}`. |
| R10 | records | `len(rename(d, mapping)) == len(d)` for every dict `d` and dict `mapping`. |
| R11 | records | `group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't')` returns `{'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}`. |
| R12 | records | `sum(len(g) for g in group_by(rows, key).values()) == len(rows)` whenever every row has `key`. |
| R13 | records | `sort_by` is stable: rows with equal keys keep their relative order. |
| R14 | records | `sort_by(rows, 'n')` puts rows that have no key `'n'` at the end. |
| R15 | records | `deep_get({'a': {'b': {'c': 1}}}, 'a.b.c') == 1`. |
| R16 | records | `deep_get({'a': {'b': 0}}, 'a.b', 5) == 0`. |
| R17 | records | `deep_get({'a': [1, 2]}, 'a.0') == 1`. |
| R18 | records | `deep_get(d, 'x') == d.get('x')` for every dict `d`. |
| R19 | records | `to_kv({}) == ''`. |
