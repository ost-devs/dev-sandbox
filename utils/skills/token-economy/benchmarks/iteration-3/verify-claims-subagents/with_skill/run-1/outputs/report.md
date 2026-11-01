# Relatório de verificação das afirmações de `calc/`

Semente registrada: 20261101 (`checks/harness.py`). Reexecutar tudo: `for m in textutil mathutil dates collections_util; do sh checks/$m/run.sh; done` (na raiz). Duas execuções seguidas deram saída idêntica.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 -I checks/textutil/check_T1.py` |
| T2 | falsa | slugify('Café Noir') -> 'caf-noir', expected 'cafe-noir' | `python3 -I checks/textutil/check_T2.py` |
| T3 | falsa | truncate('x', 0) -> '…' (len 1) > 0 | `python3 -I checks/textutil/check_T3.py` |
| T4 | verdadeira | — | `python3 -I checks/textutil/check_T4.py` |
| T5 | verdadeira | — | `python3 -I checks/textutil/check_T5.py` |
| T6 | verdadeira | — | `python3 -I checks/textutil/check_T6.py` |
| M1 | verdadeira | — | `python3 -I checks/mathutil/check_M1.py` |
| M2 | falsa | exception ZeroDivisionError: division by zero | `python3 -I checks/mathutil/check_M2.py` |
| M3 | falsa | round_half(2.5) -> 2, expected 3 | `python3 -I checks/mathutil/check_M3.py` |
| M4 | verdadeira | — | `python3 -I checks/mathutil/check_M4.py` |
| M5 | falsa | is_prime(4) -> True, expected False (first of 18 wrong: [4, 6, 8, 9, 15, 25]) | `python3 -I checks/mathutil/check_M5.py` |
| M6 | verdadeira | — | `python3 -I checks/mathutil/check_M6.py` |
| D1 | verdadeira | — | `python3 -I checks/dates/check_D1.py` |
| D2 | falsa | add_months(1904-02-29,12) -> 1905-02-28 (dia muda de 29 para 28; 29/02/1905 não existe) | `python3 -I checks/dates/check_D2.py` |
| D3 | falsa | days_between(2024-01-02,2024-01-01) = -1, expected >= 0 | `python3 -I checks/dates/check_D3.py` |
| D4 | verdadeira | — | `python3 -I checks/dates/check_D4.py` |
| D5 | verdadeira | — | `python3 -I checks/dates/check_D5.py` |
| D6 | falsa | exception ValueError: day is out of range for month | `python3 -I checks/dates/check_D6.py` |
| C1 | verdadeira | — | `python3 -I checks/collections_util/check_C1.py` |
| C2 | verdadeira | — | `python3 -I checks/collections_util/check_C2.py` |
| C3 | falsa | flatten([[1, [2]], [3]]) -> [1, [2], 3] expected [1, 2, 3] | `python3 -I checks/collections_util/check_C3.py` |
| C4 | falsa | top_n([1, 2],-1) -> [2] (len 1) expected len -1 | `python3 -I checks/collections_util/check_C4.py` |
| C5 | falsa | merge_dicts({'k': 'a'},{'k': 'b'}) -> {'k': 'b'} expected {'k': 'a'} | `python3 -I checks/collections_util/check_C5.py` |
| C6 | verdadeira | — | `python3 -I checks/collections_util/check_C6.py` |

Total: 13 verdadeiras, 11 falsas.
