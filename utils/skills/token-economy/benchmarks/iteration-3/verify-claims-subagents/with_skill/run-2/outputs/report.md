# Relatório de verificação de claims.md

Semente dos dados gerados: 20261101 (`checks/harness.py`). Cada comando é executado a partir desta pasta e imprime uma linha por afirmação; saída idêntica em duas execuções. Resultado também em `checks/results/<módulo>.json`.

Resumo: 13 verdadeiras, 11 falsas.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira |  | `python3 checks/textutil_checks.py` |
| T2 | falsa | `slugify('Café Noir') = 'caf-noir'` | `python3 checks/textutil_checks.py` |
| T3 | falsa | `truncate('a', 0) = '…' (len 1)` | `python3 checks/textutil_checks.py` |
| T4 | verdadeira |  | `python3 checks/textutil_checks.py` |
| T5 | verdadeira |  | `python3 checks/textutil_checks.py` |
| T6 | verdadeira |  | `python3 checks/textutil_checks.py` |
| M1 | verdadeira |  | `python3 checks/mathutil_checks.py` |
| M2 | falsa | `raises ZeroDivisionError: division by zero` | `python3 checks/mathutil_checks.py` |
| M3 | falsa | `round_half(2.5)=2` | `python3 checks/mathutil_checks.py` |
| M4 | verdadeira |  | `python3 checks/mathutil_checks.py` |
| M5 | falsa | `is_prime(4)=True, expected False` | `python3 checks/mathutil_checks.py` |
| M6 | verdadeira |  | `python3 checks/mathutil_checks.py` |
| D1 | verdadeira |  | `python3 checks/dates_checks.py` |
| D2 | falsa | `add_months(datetime.date(2024, 2, 29), 12) = datetime.date(2025, 2, 28)` | `python3 checks/dates_checks.py` |
| D3 | falsa | `days_between(datetime.date(2024, 1, 2), datetime.date(2024, 1, 1)) = -1` | `python3 checks/dates_checks.py` |
| D4 | verdadeira |  | `python3 checks/dates_checks.py` |
| D5 | verdadeira |  | `python3 checks/dates_checks.py` |
| D6 | falsa | `parse_iso('2026-02-30') raises ValueError: day is out of range for month` | `python3 checks/dates_checks.py` |
| C1 | verdadeira |  | `python3 checks/collections_util_checks.py` |
| C2 | verdadeira |  | `python3 checks/collections_util_checks.py` |
| C3 | falsa | `flatten([[1, [2]], [3]])=[1, [2], 3]` | `python3 checks/collections_util_checks.py` |
| C4 | falsa | `top_n([],-2)=[] (len 0, expected -2)` | `python3 checks/collections_util_checks.py` |
| C5 | falsa | `merge_dicts({'k': 1},{'k': 2})={'k': 2}` | `python3 checks/collections_util_checks.py` |
| C6 | verdadeira |  | `python3 checks/collections_util_checks.py` |
