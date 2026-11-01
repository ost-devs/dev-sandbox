# Claims about calc/

| id | module | claim |
|---|---|---|
| T1 | textutil | `slugify(s)` never starts or ends with `-`, for any string `s`. |
| T2 | textutil | `slugify('Café Noir') == 'cafe-noir'`. |
| T3 | textutil | `len(truncate(s, n)) <= n` for every string `s` and every integer `n >= 0`. |
| T4 | textutil | `count_words('a  b\tc\n') == 3`. |
| T5 | textutil | `capitalize_words('a  b') == 'A  B'` (the double space is kept). |
| T6 | textutil | `is_palindrome('')` is `True`. |
| M1 | mathutil | For `lo <= hi`, `clamp(x, lo, hi)` is always within `[lo, hi]`. |
| M2 | mathutil | `mean([])` returns `0`. |
| M3 | mathutil | `round_half(2.5) == 3`. |
| M4 | mathutil | `gcd(a, b) == gcd(b, a)` for all integers `a`, `b`. |
| M5 | mathutil | `is_prime(n)` is correct for every `n` from 0 to 1000. |
| M6 | mathutil | `percent(1, 3) == 33.3`. |
| D1 | dates | `add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)`. |
| D2 | dates | `add_months(d, 12)` always returns the same day and month one year later, for every date `d`. |
| D3 | dates | `days_between(a, b)` is never negative. |
| D4 | dates | `is_leap(1900)` is `False`. |
| D5 | dates | `quarter(d)` is in 1..4 for every date `d`. |
| D6 | dates | `parse_iso('2026-02-30')` returns `date(2026, 3, 2)`. |
| C1 | collections_util | For every list `xs` and `n >= 1`, concatenating the lists of `chunk(xs, n)` gives back `xs`. |
| C2 | collections_util | `dedupe(xs)` keeps the order of first occurrences. |
| C3 | collections_util | `flatten([[1, [2]], [3]]) == [1, 2, 3]`. |
| C4 | collections_util | `top_n(xs, n)` returns `min(n, len(xs))` items for every list `xs` and every integer `n`. |
| C5 | collections_util | On a key present in both, `merge_dicts(a, b)` keeps the value from `a`. |
| C6 | collections_util | `rotate(xs, len(xs)) == xs` for every list `xs`. |
