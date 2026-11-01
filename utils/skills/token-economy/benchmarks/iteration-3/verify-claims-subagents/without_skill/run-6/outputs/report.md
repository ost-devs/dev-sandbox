# Relatório de verificação das afirmações sobre `calc/`

Todas as checagens rodam a partir deste diretório, sem dependências além do Python 3 (testado com 3.11.2). A semente aleatória é fixa (12345) e é impressa pelos scripts. Cada script foi executado duas vezes e a saída foi idêntica.

Em "verdadeira" para afirmações universais (T1, M1, M4, C1, C2, C6), o resultado significa que nenhum contraexemplo apareceu na busca, e não que há prova. D5 foi checada exaustivamente em todas as datas de `date.min` a `date.max`.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate('\t', 0)` → `'…'` (comprimento 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | — | `python3 checks/check_textutil.py` |
| T5 | verdadeira | — | `python3 checks/check_textutil.py` |
| T6 | verdadeira | — | `python3 checks/check_textutil.py` |
| M1 | verdadeira | — | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5)` → `2` (arredonda para par) | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | — | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4)` → `True`; 18 erros em 0..1000 (4, 6, 8, 9, 15, …) | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | — | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | — | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(4, 2, 29), 12)` → `date(5, 2, 28)` (vale para qualquer 29/fev, p. ex. 2024) | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1))` → `-1` | `python3 checks/check_dates.py` |
| D4 | verdadeira | — | `python3 checks/check_dates.py` |
| D5 | verdadeira | — | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | — | `python3 checks/check_collections_util.py` |
| C2 | verdadeira | — | `python3 checks/check_collections_util.py` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` (achata só um nível) | `python3 checks/check_collections_util.py` |
| C4 | falsa | `top_n([], -1)` → `[]` (esperado `min(-1, 0)` itens); `n` negativo quebra a fatia | `python3 checks/check_collections_util.py` |
| C5 | falsa | `merge_dicts({'k':1}, {'k':2})` → `{'k': 2}` (b prevalece) | `python3 checks/check_collections_util.py` |
| C6 | verdadeira | — | `python3 checks/check_collections_util.py` |

Resumo: 11 verdadeiras, 13 falsas.
