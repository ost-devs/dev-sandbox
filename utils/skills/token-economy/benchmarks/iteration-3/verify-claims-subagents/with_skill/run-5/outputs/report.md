# Relatório de verificação de `calc/`

24 afirmações: 13 verdadeiras, 11 falsas. Semente das checagens aleatórias: 20261101 (`checks/common.py`).
Reproduzir tudo: `python3 checks/build_report.py` (reescreve este arquivo).

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/textutil/T1.py` |
| T2 | falsa | slugify('Café Noir') == 'caf-noir', expected 'cafe-noir' | `python3 checks/textutil/T2.py` |
| T3 | falsa | truncate('a', 0) == '…' has len 1 > 0 | `python3 checks/textutil/T3.py` |
| T4 | verdadeira | — | `python3 checks/textutil/T4.py` |
| T5 | verdadeira | — | `python3 checks/textutil/T5.py` |
| T6 | verdadeira | — | `python3 checks/textutil/T6.py` |
| M1 | verdadeira | — | `python3 checks/mathutil/M1.py` |
| M2 | falsa | raised ZeroDivisionError: division by zero | `python3 checks/mathutil/M2.py` |
| M3 | falsa | round_half(2.5) = 2 | `python3 checks/mathutil/M3.py` |
| M4 | verdadeira | — | `python3 checks/mathutil/M4.py` |
| M5 | falsa | is_prime(4) = True, expected False | `python3 checks/mathutil/M5.py` |
| M6 | verdadeira | — | `python3 checks/mathutil/M6.py` |
| D1 | verdadeira | — | `python3 checks/dates/D1.py` |
| D2 | falsa | add_months(0004-02-29, 12) = 0005-02-28 | `python3 checks/dates/D2.py` |
| D3 | falsa | days_between(2024-01-02, 2024-01-01) = -1 | `python3 checks/dates/D3.py` |
| D4 | verdadeira | — | `python3 checks/dates/D4.py` |
| D5 | verdadeira | — | `python3 checks/dates/D5.py` |
| D6 | falsa | raised ValueError: day is out of range for month | `python3 checks/dates/D6.py` |
| C1 | verdadeira | — | `python3 checks/collections_util/C1.py` |
| C2 | verdadeira | — | `python3 checks/collections_util/C2.py` |
| C3 | falsa | flatten([[1, [2]], [3]]) -> [1, [2], 3], expected [1, 2, 3] | `python3 checks/collections_util/C3.py` |
| C4 | falsa | xs=[] n=-3 -> len 0, expected min(n, len(xs)) = -3 | `python3 checks/collections_util/C4.py` |
| C5 | falsa | a={'k': 1} b={'k': 2} -> {'k': 2}, expected value from a (1) | `python3 checks/collections_util/C5.py` |
| C6 | verdadeira | — | `python3 checks/collections_util/C6.py` |
