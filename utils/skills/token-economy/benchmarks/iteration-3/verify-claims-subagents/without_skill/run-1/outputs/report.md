# Relatório de verificação — `calc/`

Todos os comandos rodam da raiz do projeto. Sementes aleatórias fixas (12345) registradas nos scripts; saída determinística (cada script rodado 2×, saída idêntica).
Para reproduzir tudo: `for m in textutil mathutil dates collections_util; do python3 checks/check_$m.py; done`

| id | veredito | contraexemplo (se falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate(' ', 0)` → `'…'` (len 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | | `python3 checks/check_textutil.py` |
| T5 | verdadeira | | `python3 checks/check_textutil.py` |
| T6 | verdadeira | | `python3 checks/check_textutil.py` |
| M1 | verdadeira | | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5)` → `2` | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4)` → `True` (18 divergências em 0..1000; `range(2, int(n**0.5))` exclui a raiz) | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(1896,2,29), 12)` → `date(1897,2,28)` | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1))` → `-1` | `python3 checks/check_dates.py` |
| D4 | verdadeira | | `python3 checks/check_dates.py` |
| D5 | verdadeira | | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | | `python3 checks/check_collections_util.py` |
| C2 | verdadeira (ressalva) | | `python3 checks/check_collections_util.py` |
| C3 | falsa | `flatten([[1,[2]],[3]])` → `[1, [2], 3]` | `python3 checks/check_collections_util.py` |
| C4 | falsa | `top_n([0,1], -1)` → 1 item (esperado `min(-1,2)=-1`, impossível); `top_n([], -2)` → `[]` | `python3 checks/check_collections_util.py` |
| C5 | falsa | `merge_dicts({'k':1},{'k':2})` → `{'k': 2}` | `python3 checks/check_collections_util.py` |
| C6 | verdadeira | | `python3 checks/check_collections_util.py` |

**Totais:** 11 verdadeiras, 13 falsas.

**Ressalva C2:** a ordem das primeiras ocorrências é preservada para itens hasheáveis. Com itens não hasheáveis (`dedupe([[1]])`) a função lança `TypeError`; tratei isso como fora do escopo da afirmação, que fala de ordem. Se a intenção era "para qualquer lista", seria falsa.

**Nota C4:** a afirmação diz "todo inteiro n"; para n negativo, `min(n, len)` é negativo e nenhum tamanho de lista o iguala, então a afirmação só vale para n ≥ 0.
