# Relatório de verificação de `claims.md`

Seed fixa: 20261101 (um `random.Random` por afirmação, ver `checks/common.py`). Cada módulo roda duas vezes com saída idêntica. Saída completa em `checks/results.jsonl`.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/textutil_check.py` |
| T2 | falsa | `slugify('Café Noir') == 'caf-noir'` | `python3 checks/textutil_check.py` |
| T3 | falsa | `truncate('a', 0) == '…'` | `python3 checks/textutil_check.py` |
| T4 | verdadeira | — | `python3 checks/textutil_check.py` |
| T5 | verdadeira | — | `python3 checks/textutil_check.py` |
| T6 | verdadeira | — | `python3 checks/textutil_check.py` |
| M1 | verdadeira | — | `python3 checks/mathutil_check.py` |
| M2 | falsa | `raised ZeroDivisionError: division by zero` | `python3 checks/mathutil_check.py` |
| M3 | falsa | `round_half(2.5) == 2` | `python3 checks/mathutil_check.py` |
| M4 | verdadeira | — | `python3 checks/mathutil_check.py` |
| M5 | falsa | `is_prime(4) == True, expected False` | `python3 checks/mathutil_check.py` |
| M6 | verdadeira | — | `python3 checks/mathutil_check.py` |
| D1 | verdadeira | — | `python3 checks/dates_check.py` |
| D2 | falsa | `add_months(datetime.date(2024, 2, 29), 12) = datetime.date(2025, 2, 28)` | `python3 checks/dates_check.py` |
| D3 | falsa | `days_between(datetime.date(2024, 1, 2), datetime.date(2024, 1, 1)) = -1` | `python3 checks/dates_check.py` |
| D4 | verdadeira | — | `python3 checks/dates_check.py` |
| D5 | verdadeira | — | `python3 checks/dates_check.py` |
| D6 | falsa | `raised ValueError: day is out of range for month` | `python3 checks/dates_check.py` |
| C1 | verdadeira | — | `python3 checks/collections_util_check.py` |
| C2 | verdadeira | — | `python3 checks/collections_util_check.py` |
| C3 | falsa | `flatten([[1, [2]], [3]]) == [1, [2], 3]` | `python3 checks/collections_util_check.py` |
| C4 | falsa | `top_n([1, 2, 3], -1)` devolve `[3, 2]` (2 itens, esperado `min(-1, 3) = -1`, impossível); também `top_n([], -3)` → `[]` | `python3 checks/collections_util_check.py` |
| C5 | falsa | `merge_dicts({'k': 'a'}, {'k': 'b'}) == {'k': 'b'}` | `python3 checks/collections_util_check.py` |
| C6 | verdadeira | — | `python3 checks/collections_util_check.py` |

Total: 13 verdadeiras, 11 falsas.
