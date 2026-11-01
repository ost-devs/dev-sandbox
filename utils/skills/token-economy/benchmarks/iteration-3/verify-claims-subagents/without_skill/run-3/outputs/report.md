# Relatório de verificação das afirmações sobre `calc/`

Cada checagem é um script determinístico em `checks/` (entradas fixas, ou sementes registradas: 12345). Todos foram executados duas vezes com saída idêntica. Comandos rodam a partir do diretório raiz do projeto.

| id | veredito | contraexemplo (se falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` vira `-`) | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate(' ', 0)` → `'…'` (comprimento 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | | `python3 checks/check_textutil.py` |
| T5 | verdadeira | | `python3 checks/check_textutil.py` |
| T6 | verdadeira | | `python3 checks/check_textutil.py` |
| M1 | verdadeira | | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5)` → `2` (arredondamento par) | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4)` → `True` (também 6, 8, 9, 15, 25, 35, 49…; 18 erros em 0..1000) | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(4,2,29), 12)` → `date(5,2,28)` | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1))` → `-1` | `python3 checks/check_dates.py` |
| D4 | verdadeira | | `python3 checks/check_dates.py` |
| D5 | verdadeira | | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | | `python3 checks/check_collections_util.py` |
| C2 | verdadeira (para elementos hasheáveis; não-hasheáveis dão `TypeError`, considerado fora do escopo) | | `python3 checks/check_collections_util.py` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` (achata só um nível) | `python3 checks/check_collections_util.py` |
| C4 | falsa | `top_n([1,2,3], -1)` retorna 2 itens, não `min(-1, 3)`; vale para n ≥ 0 | `python3 checks/check_collections_util.py` |
| C5 | falsa | `merge_dicts({'k':1},{'k':2})` → `{'k': 2}` (vence `b`) | `python3 checks/check_collections_util.py` |
| C6 | verdadeira | | `python3 checks/check_collections_util.py` |

**Resumo:** 13 verdadeiras, 11 falsas (T2, T3, M2, M3, M5, D2, D3, D6, C3, C4, C5).

Notas: D2 também falha no fim do intervalo (datas do ano 9999 levantam erro); a varredura parou no primeiro contraexemplo. Em D3, C4 e T3 a falsidade depende de ler "qualquer" literalmente (a > b, n negativo, n = 0), como as afirmações estão escritas.
