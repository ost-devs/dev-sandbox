# Relatório de verificação — `calc/`

Todas as checagens rodam da raiz do projeto, são determinísticas (entradas fixas ou geradas com `SEED` registrada no próprio script) e usam `checks/common.py`.
Para rodar tudo: `for f in checks/*/check_*.py; do python3 $f; done`

Resumo: 24 afirmações, 13 verdadeiras, 11 falsas.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | | `python3 checks/textutil/check_T1.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` é descartado) | `python3 checks/textutil/check_T2.py` |
| T3 | falsa | `truncate(' ', 0)` → `'…'` (tamanho 1 > 0) | `python3 checks/textutil/check_T3.py` |
| T4 | verdadeira | | `python3 checks/textutil/check_T4.py` |
| T5 | verdadeira | | `python3 checks/textutil/check_T5.py` |
| T6 | verdadeira | | `python3 checks/textutil/check_T6.py` |
| M1 | verdadeira | | `python3 checks/mathutil/check_M1.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/mathutil/check_M2.py` |
| M3 | falsa | `round_half(2.5)` → `2` (`round` arredonda para o par) | `python3 checks/mathutil/check_M3.py` |
| M4 | verdadeira | | `python3 checks/mathutil/check_M4.py` |
| M5 | falsa | `is_prime(4)` → `True` (o laço `range(2, int(n**0.5))` exclui a raiz) | `python3 checks/mathutil/check_M5.py` |
| M6 | verdadeira | | `python3 checks/mathutil/check_M6.py` |
| D1 | verdadeira | | `python3 checks/dates/check_D1.py` |
| D2 | falsa | `add_months(date(2024,2,29), 12)` → `date(2025,2,28)` | `python3 checks/dates/check_D2.py` |
| D3 | falsa | `days_between(date(2024,3,1), date(2024,2,29))` → `-1` | `python3 checks/dates/check_D3.py` |
| D4 | verdadeira | | `python3 checks/dates/check_D4.py` |
| D5 | verdadeira | | `python3 checks/dates/check_D5.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/dates/check_D6.py` |
| C1 | verdadeira | | `python3 checks/collections_util/check_C1.py` |
| C2 | verdadeira | | `python3 checks/collections_util/check_C2.py` |
| C3 | falsa | `flatten([[1,[2]],[3]])` → `[1, [2], 3]` (só um nível) | `python3 checks/collections_util/check_C3.py` |
| C4 | falsa | `top_n([1,2,3], -1)` devolve 2 itens, não `min(-1,3)`; qualquer `n < 0` quebra a afirmação | `python3 checks/collections_util/check_C4.py` |
| C5 | falsa | `merge_dicts({'k':'a'},{'k':'b'})` → `{'k':'b'}` (vence `b`) | `python3 checks/collections_util/check_C5.py` |
| C6 | verdadeira | | `python3 checks/collections_util/check_C6.py` |

Notas:
- M1, M4, T1, C1, C2, C6, D5 são afirmações "para todo": a checagem busca contraexemplos em casos de borda e entradas aleatórias com semente fixa; não é prova.
- D6 e M2 foram tratadas como falsas porque o código levanta exceção onde a afirmação promete um valor.
