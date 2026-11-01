# Relatório de verificação de claims.md

152 afirmações: 113 verdadeiras, 39 falsas. Rodar tudo: `sh checks/run_all.sh` (cwd = raiz; regenera este relatório).
Cada comando imprime `id<TAB>veredito<TAB>contraexemplo` e é determinístico (entradas fixas ou sementes literais no script).

| id | afirmação | veredito | contraexemplo | comando |
|---|---|---|---|---|
| D01 | `add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D02 | For every date `x` from 2000 to 2030, `add_months(x, 12)` has the same day and month as `x`, one year later. | falsa | `input datetime.date(2000, 2, 29)` | `python3 -I checks/dates/check_dates.py` |
| D03 | `add_months(add_months(x, 1), -1) == x` for every date `x` from 2000 to 2030. | falsa | `input datetime.date(2000, 1, 30)` | `python3 -I checks/dates/check_dates.py` |
| D04 | `days_between(a, b)` is never negative. | falsa | `input (datetime.date(2024, 1, 2), datetime.date(2024, 1, 1))` | `python3 -I checks/dates/check_dates.py` |
| D05 | `days_between(a, b) == -days_between(b, a)` for all dates `a`, `b`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D06 | `is_leap(1900)` is `False`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D07 | `is_leap(2000)` is `True`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D08 | `is_leap(y) == calendar.isleap(y)` for every year `y` from 1 to 9999. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D09 | `weekday_name(date(2024, 1, 1)) == 'Monday'`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D10 | `quarter(date(2024, 4, 1)) == 2`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D11 | `quarter(x)` is always one of 1, 2, 3, 4. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D12 | `end_of_month(date(2023, 2, 10)) == date(2023, 2, 28)`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D13 | `end_of_month(x) >= x` for every date `x` from 2000 to 2030. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D14 | `iso_week(date(2021, 1, 1)) == 1`. | falsa | `got 53, expected 1` | `python3 -I checks/dates/check_dates.py` |
| D15 | `parse_br('31/12/2024') == date(2024, 12, 31)`. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D16 | `parse_br('1/2/2024')` raises `ValueError` (day and month need two digits). | falsa | `parse_br('1/2/2024') returned datetime.date(2024, 2, 1), no ValueError` | `python3 -I checks/dates/check_dates.py` |
| D17 | `add_days(x, k) - x == timedelta(days=k)` for every date `x` from 2000 to 2030 and integer `k` from -1000 to 1000. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D18 | `add_months(x, k).day <= x.day` for every date `x` from 2000 to 2030 and integer `k` from -30 to 30. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| D19 | `weekday_name(add_days(x, 7)) == weekday_name(x)` for every date `x` from 2000 to 2030. | verdadeira |  | `python3 -I checks/dates/check_dates.py` |
| I01 | `overlaps((0, 5), (5, 10))` is `False`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I02 | `overlaps(a, b) == overlaps(b, a)` for all intervals `a`, `b`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I03 | `merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I04 | `merge([(1, 2), (2, 3)]) == [(1, 3)]`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I05 | For every non-empty list of intervals with start < end, `merge` returns intervals sorted by start with no two overlapping. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I06 | `merge(merge(xs)) == merge(xs)` for every non-empty list of intervals with start < end. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I07 | `contains((0, 5), 5)` is `False` (intervals are half-open, the end is excluded). | falsa | `got True, expected False` | `python3 -I checks/intervals/check_intervals.py` |
| I08 | `contains(a, a[0])` is `True` for every interval with start < end. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I09 | `intersect((0, 5), (3, 8)) == (3, 5)`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I10 | `intersect((0, 2), (5, 6))` is `None`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I11 | `intersect((0, 5), (5, 8))` is `None`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I12 | `total_covered([(0, 5), (3, 8)]) == 8`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I13 | `total_covered(xs) <= sum(length(i) for i in xs)` for every non-empty list of intervals with start < end. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I14 | For intervals with start < end that overlap, `length(intersect(a, b)) <= min(length(a), length(b))`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I15 | `merge([]) == []`. | falsa | `raised IndexError: list index out of range` | `python3 -I checks/intervals/check_intervals.py` |
| I16 | `overlaps(a, a)` is `True` for every interval with start < end. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I17 | `merge([(5, 7), (1, 2)]) == [(1, 2), (5, 7)]`. | verdadeira |  | `python3 -I checks/intervals/check_intervals.py` |
| I18 | For integer intervals, `contains(a, x)` implies `overlaps(a, (x, x + 1))`. | falsa | `input ((0, 5), 5)` | `python3 -I checks/intervals/check_intervals.py` |
| I19 | `length((3, 1))` returns `0` for an inverted interval. | falsa | `got -2, expected 0` | `python3 -I checks/intervals/check_intervals.py` |
| L01 | `chunk(list(range(7)), 3) == [[0, 1, 2], [3, 4, 5], [6]]`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L02 | `flatten(chunk(xs, k)) == xs` for every list of integers `xs` and integer `k >= 1`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L03 | `chunk(xs, 0)` raises `ValueError`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L04 | `dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L05 | For every list of integers, `dedupe` keeps the order of first occurrences. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L06 | `len(dedupe(xs)) == len(set(xs))` for every list of integers `xs`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L07 | `flatten([[1, [2]], [3]]) == [1, 2, 3]`. | falsa | `got [1, [2], 3], expected [1, 2, 3]` | `python3 -I checks/lists/check_lists.py` |
| L08 | `top_n([5, 1, 4], 2) == [5, 4]`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L09 | `len(top_n(xs, k)) == min(k, len(xs))` for every list of integers and integer `k >= 0`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L10 | `top_n([3, 2, 1], -1) == []`. | falsa | `got [3, 2], expected []` | `python3 -I checks/lists/check_lists.py` |
| L11 | `rotate([1, 2, 3], 1) == [2, 3, 1]`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L12 | `rotate(xs, k) == rotate(xs, k % len(xs))` for every non-empty list `xs` and integer `k >= 0`. | falsa | `input ([1, 2, 3], 4)` | `python3 -I checks/lists/check_lists.py` |
| L13 | `len(rotate(xs, k)) == len(xs)` for every list `xs` and integer `k`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L14 | `interleave([1, 2, 3], [9]) == [1, 9, 2, 3]`. | falsa | `got [1, 9], expected [1, 9, 2, 3]` | `python3 -I checks/lists/check_lists.py` |
| L15 | `len(interleave(a, b)) == 2 * min(len(a), len(b))` for all lists `a`, `b`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L16 | `frequencies('abca') == {'a': 2, 'b': 1, 'c': 1}`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L17 | `sum(frequencies(xs).values()) == len(xs)` for every list of integers `xs`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L18 | `pairwise([1, 2, 3]) == [(1, 2), (2, 3)]`. | verdadeira |  | `python3 -I checks/lists/check_lists.py` |
| L19 | `len(pairwise(xs)) == len(xs) - 1` for every list `xs`. | falsa | `input []` | `python3 -I checks/lists/check_lists.py` |
| M01 | `to_cents('12,34') == 1234`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M02 | `to_cents('1.234,5') == 123450`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M03 | `to_cents('-1,50') == -150`. | falsa | `got -50, expected -150` | `python3 -I checks/money/check_money.py` |
| M04 | `to_cents('7') == 700`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M05 | `format_brl(123456) == 'R$ 1.234,56'`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M06 | `format_brl(5) == 'R$ 0,05'`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M07 | `format_brl(-150) == 'R$ -1,50'`. | falsa | `got 'R$ -2,50', expected 'R$ -1,50'` | `python3 -I checks/money/check_money.py` |
| M08 | `to_cents(format_brl(c)[3:]) == c` for every integer `c` from 0 to 1,000,000. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M09 | `sum(split_bill(total, k)) == total` for every integer `total >= 0` and `k >= 1`. | falsa | `input (1, 2)` | `python3 -I checks/money/check_money.py` |
| M10 | `split_bill(900, 3) == [300, 300, 300]`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M11 | `sum(installments(total, k)) == total` for every integer `total >= 0` and `k >= 1`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M12 | In `installments(total, k)`, the largest and smallest installment differ by at most 1. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M13 | `installments(100, 3) == [34, 33, 33]`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M14 | `apply_discount(1000, 10) == 900`. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M15 | `apply_discount(c, 0) == c` for every integer `c` from 0 to 1,000,000. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M16 | `apply_discount(c, p) <= c` for every integer `c` from 0 to 1,000,000 and every integer `p` from 0 to 100. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M17 | `add_tax(100, 0.15) == 115`. | falsa | `got 114, expected 115` | `python3 -I checks/money/check_money.py` |
| M18 | `add_tax(c, 0) == c` for every integer `c` from 0 to 1,000,000. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| M19 | `add_tax(c, r) >= c` for every integer `c` from 0 to 1,000,000 and every rate `r` from 0 to 1. | verdadeira |  | `python3 -I checks/money/check_money.py` |
| N01 | For integers `lo <= hi`, `clamp(x, lo, hi)` is always within `[lo, hi]`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N02 | `clamp(5, 10, 0) == 0`. | falsa | `got 10, expected 0` | `python3 -I checks/numbers/check_numbers.py` |
| N03 | `mean([]) == 0`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N04 | `mean([1, 2]) == 1.5`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N05 | `median([3, 1, 2]) == 2`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N06 | `median([])` returns `None`. | falsa | `raised IndexError: list index out of range` | `python3 -I checks/numbers/check_numbers.py` |
| N07 | `median(xs) == median(sorted(xs))` for every non-empty list of integers `xs`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N08 | `round_half(2.5) == 3`. | falsa | `got 2, expected 3` | `python3 -I checks/numbers/check_numbers.py` |
| N09 | `round_half(3.5) == 4`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N10 | `percent(1, 3) == 33.3`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N11 | `percent(x, 0)` returns `0.0` for any number `x`. | falsa | `input 0 raised ZeroDivisionError: division by zero` | `python3 -I checks/numbers/check_numbers.py` |
| N12 | `is_prime(n)` is correct for every `n` from 0 to 1000. | falsa | `input 4` | `python3 -I checks/numbers/check_numbers.py` |
| N13 | `is_prime(97)` is `True`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N14 | `is_prime(2)` is `True`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N15 | `gcd(a, b) == gcd(b, a)` for all integers `a`, `b` in `[-50, 50]`. | falsa | `input (-50, 1)` | `python3 -I checks/numbers/check_numbers.py` |
| N16 | `gcd(12, 18) == 6`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N17 | `gcd(a, 0) == a` for every integer `a`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N18 | `digits_sum(1234) == 10`. | verdadeira |  | `python3 -I checks/numbers/check_numbers.py` |
| N19 | `digits_sum(n)` returns a non-negative integer for every integer `n`. | falsa | `input -1 raised ValueError: invalid literal for int() with base 10: '-'` | `python3 -I checks/numbers/check_numbers.py` |
| P01 | `join('a', 'b', 'c.txt') == 'a/b/c.txt'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P02 | `join('/usr', 'bin') == '/usr/bin'`. | falsa | `got 'usr/bin', expected '/usr/bin'` | `python3 -I checks/paths/check_paths.py` |
| P03 | `join('a/', '/b') == 'a/b'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P04 | `ext('foto.tar.gz') == 'gz'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P05 | `ext('dir.d/arquivo') == ''`. | falsa | `got 'd/arquivo', expected ''` | `python3 -I checks/paths/check_paths.py` |
| P06 | `ext('.bashrc') == ''`. | falsa | `got 'bashrc', expected ''` | `python3 -I checks/paths/check_paths.py` |
| P07 | `stem('relatorio.pdf') == 'relatorio'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P08 | `normalize('a/./b/../c') == 'a/c'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P09 | `normalize('/a/../..') == '/'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P10 | `normalize('../x') == '../x'`. | falsa | `got 'x', expected '../x'` | `python3 -I checks/paths/check_paths.py` |
| P11 | `normalize(normalize(x)) == normalize(x)` for every path string `x`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P12 | `is_hidden('.env')` is `True`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P13 | `is_hidden('config/.git/HEAD')` is `False`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P14 | `depth('/a/b/c') == 3`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P15 | `depth('a//b/') == 2`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P16 | `parent('a/b/c') == 'a/b'`. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P17 | `parent('/a') == '/'`. | falsa | `got '', expected '/'` | `python3 -I checks/paths/check_paths.py` |
| P18 | `depth(join(*parts)) == len(parts)` for every non-empty list of names made of letters and digits. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| P19 | `stem(x) + '.' + ext(x) == x` for every string `x` that contains a dot. | verdadeira |  | `python3 -I checks/paths/check_paths.py` |
| R01 | `parse_kv('a=1;b=2') == {'a': '1', 'b': '2'}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R02 | `parse_kv('a=1;;b=2') == {'a': '1', 'b': '2'}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R03 | `parse_kv('url=x=y') == {'url': 'x=y'}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R04 | `parse_kv('a=1;flag') == {'a': '1', 'flag': ''}`. | falsa | `raised ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 -I checks/records/check_records.py` |
| R05 | `parse_kv(to_kv(d)) == d` for every dict whose keys and values are non-empty strings of letters and digits. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R06 | `parse_kv(to_kv(d)) == d` for every dict of strings to strings. | falsa | `input {'a=': '1'}` | `python3 -I checks/records/check_records.py` |
| R07 | `pick({'a': 1, 'b': 2}, ['a', 'c']) == {'a': 1}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R08 | `len(pick(d, keys)) <= len(d)` for every dict `d` and list `keys`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R09 | `rename({'a': 1}, {'a': 'b'}) == {'b': 1}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R10 | `len(rename(d, mapping)) == len(d)` for every dict `d` and dict `mapping`. | falsa | `input ({'a': 1, 'b': 2}, {'a': 'b'})` | `python3 -I checks/records/check_records.py` |
| R11 | `group_by([{'t': 'x', 'v': 1}, {'t': 'y', 'v': 2}, {'t': 'x', 'v': 3}], 't')` returns `{'x': [{'t': 'x', 'v': 1}, {'t': 'x', 'v': 3}], 'y': [{'t': 'y', 'v': 2}]}`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R12 | `sum(len(g) for g in group_by(rows, key).values()) == len(rows)` whenever every row has `key`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R13 | `sort_by` is stable: rows with equal keys keep their relative order. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R14 | `sort_by(rows, 'n')` puts rows that have no key `'n'` at the end. | falsa | `sort_by([{'x': 1}, {'n': 1}], 'n') raised KeyError: 'n'` | `python3 -I checks/records/check_records.py` |
| R15 | `deep_get({'a': {'b': {'c': 1}}}, 'a.b.c') == 1`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R16 | `deep_get({'a': {'b': 0}}, 'a.b', 5) == 0`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R17 | `deep_get({'a': [1, 2]}, 'a.0') == 1`. | falsa | `got None, expected 1` | `python3 -I checks/records/check_records.py` |
| R18 | `deep_get(d, 'x') == d.get('x')` for every dict `d`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| R19 | `to_kv({}) == ''`. | verdadeira |  | `python3 -I checks/records/check_records.py` |
| T01 | `slugify('Café Noir') == 'cafe-noir'`. | falsa | `got 'caf-noir', expected 'cafe-noir'` | `python3 -I checks/text/check_text.py` |
| T02 | `slugify(s)` never starts or ends with `-`, for any string `s`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T03 | `slugify(s)` contains only `a-z`, `0-9` and `-`, for any string `s`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T04 | `slugify(slugify(s)) == slugify(s)` for any string `s`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T05 | `len(truncate(s, n)) <= n` for every string `s` and every integer `n >= 0`. | falsa | `truncate(' ', 0) = '...' (len 3)` | `python3 -I checks/text/check_text.py` |
| T06 | `truncate('abcdef', 5) == 'ab...'`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T07 | `truncate(s, n) == s` whenever `len(s) <= n`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T08 | `count_words('a  b\tc\n') == 3`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T09 | `count_words('') == 0`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T10 | `title_case('a  b') == 'A  B'` (the double space is kept). | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T11 | `title_case('élan vital') == 'Élan Vital'`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T12 | `len(title_case(s)) == len(s)` for any string `s`. | falsa | `input 'ß'` | `python3 -I checks/text/check_text.py` |
| T13 | `strip_accents('Ação') == 'Acao'`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T14 | `strip_accents('ø') == 'o'`. | falsa | `got 'ø', expected 'o'` | `python3 -I checks/text/check_text.py` |
| T15 | `pad_left('7', 3, '0') == '007'`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T16 | `len(pad_left(s, n)) == max(len(s), n)` for any string `s` and integer `n >= 0`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T17 | `is_palindrome('')` is `True`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T18 | `is_palindrome('A man, a plan, a canal: Panama')` is `True`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
| T19 | `is_palindrome(s) == is_palindrome(s[::-1])` for any string `s`. | verdadeira |  | `python3 -I checks/text/check_text.py` |
