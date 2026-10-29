# Relatório de verificação de `claims.md`

Cada checagem usa `checks/_common.py` (semente fixa 20261029). Rode a partir da raiz do projeto; sai com código 0 se verdadeira, 1 se falsa.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/textutil/T1.py` |
| T2 | falsa | slugify('Café Noir')='caf-noir' | `python3 checks/textutil/T2.py` |
| T3 | falsa | truncate('a', 0)='…' len 1 > 0 | `python3 checks/textutil/T3.py` |
| T4 | verdadeira | — | `python3 checks/textutil/T4.py` |
| T5 | verdadeira | — | `python3 checks/textutil/T5.py` |
| T6 | verdadeira | — | `python3 checks/textutil/T6.py` |
| M1 | verdadeira | — | `python3 checks/mathutil/M1.py` |
| M2 | falsa | mean([]) raised ZeroDivisionError('division by zero') | `python3 checks/mathutil/M2.py` |
| M3 | falsa | round_half(2.5)=2 | `python3 checks/mathutil/M3.py` |
| M4 | verdadeira | — | `python3 checks/mathutil/M4.py` |
| M5 | falsa | is_prime(4)=True, expected False; all wrong: [4, 6, 8, 9, 15, 25, 35, 49, 121, 143] | `python3 checks/mathutil/M5.py` |
| M6 | verdadeira | — | `python3 checks/mathutil/M6.py` |
| D1 | verdadeira | — | `python3 checks/dates/D1.py` |
| D2 | falsa | add_months(2024-02-29,12)=2025-02-28 | `python3 checks/dates/D2.py` |
| D3 | falsa | days_between(2024-03-01,2024-02-29)=-1 | `python3 checks/dates/D3.py` |
| D4 | verdadeira | — | `python3 checks/dates/D4.py` |
| D5 | verdadeira | — | `python3 checks/dates/D5.py` |
| D6 | falsa | parse_iso('2026-02-30') -> ValueError('day is out of range for month') | `python3 checks/dates/D6.py` |
| C1 | verdadeira | — | `python3 checks/collections_util/C1.py` |
| C2 | falsa | dedupe([[1], [1]]) raised TypeError("unhashable type: 'list'") | `python3 checks/collections_util/C2.py` |
| C3 | falsa | flatten([[1,[2]],[3]])=[1, [2], 3] | `python3 checks/collections_util/C3.py` |
| C4 | falsa | top_n([1, 2, 3],-1)=[3, 2], len 2 != -1 | `python3 checks/collections_util/C4.py` |
| C5 | falsa | merge_dicts({'k': 1},{'k': 2})['k']=2, expected 1 | `python3 checks/collections_util/C5.py` |
| C6 | verdadeira | — | `python3 checks/collections_util/C6.py` |

Total: 24 afirmações, 12 verdadeiras, 12 falsas.

Reprodução de tudo: `for f in checks/*/*.py; do python3 $f; done`
