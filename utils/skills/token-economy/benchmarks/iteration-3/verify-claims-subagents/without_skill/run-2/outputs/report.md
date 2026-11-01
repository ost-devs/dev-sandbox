# Relatório de verificação — `calc/`

Cada módulo foi verificado por um subagente, em paralelo. Cada script de `checks/` é determinista: entradas fixas, ou aleatórias com `random.Random(12345)`. Cada um foi rodado duas vezes com saída idêntica, e a saída está gravada em `checks/*.out`. Rode tudo a partir da raiz do projeto.

Resultado: 13 verdadeiras, 11 falsas.

| id | veredito | contraexemplo (quando falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | – | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` vira `-`) | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate(' ', 0)` → `'…'` (tamanho 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | – | `python3 checks/check_textutil.py` |
| T5 | verdadeira | – | `python3 checks/check_textutil.py` |
| T6 | verdadeira | – | `python3 checks/check_textutil.py` |
| M1 | verdadeira (NaN não testado) | – | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5)` → `2` (arredondamento bancário) | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | – | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4)` → `True`; 18 erros em 0..1000 (4, 6, 8, 9, 15, 25, 35, 49, …), pois o laço usa `range(2, int(n**0.5))` e para um antes da raiz | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | – | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | – | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(2024,2,29), 12)` → `date(2025,2,28)` | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,3,1), date(2024,1,1))` → `-60` | `python3 checks/check_dates.py` |
| D4 | verdadeira | – | `python3 checks/check_dates.py` |
| D5 | verdadeira | – | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | – | `python3 checks/check_collections_util.py` |
| C2 | verdadeira (só elementos hasheáveis; com listas aninhadas levanta `TypeError`) | – | `python3 checks/check_collections_util.py` |
| C3 | falsa | `flatten([[1,[2]],[3]])` → `[1,[2],3]` (achata só um nível) | `python3 checks/check_collections_util.py` |
| C4 | falsa | `n` negativo: `top_n([1,2,3], -1)` → `[3,2]` (2 itens; o esperado seria `min(-1,3)`, impossível). O script grava o caso `top_n([], -6)` → `[]` | `python3 checks/check_collections_util.py` |
| C5 | falsa | `merge_dicts({'k':1},{'k':2})` → `{'k':2}` (vence `b`) | `python3 checks/check_collections_util.py` |
| C6 | verdadeira | – | `python3 checks/check_collections_util.py` |

## Observações
- C4: o contraexemplo do script (`top_n([], -6)`) é pouco ilustrativo. O de `top_n([1,2,3], -1)` acima foi conferido à mão e não está no script. Para `n >= 0` a afirmação vale.
- C2: se "toda lista" incluir elementos não hasheáveis, a afirmação seria falsa.
- M1: NaN não foi testado.
- As verdadeiras valem para as entradas buscadas (exaustivas ou com semente), não são provas formais.
