# Relatório de verificação — `calc/`

Todos os comandos rodam a partir deste diretório. Sementes: `random.Random(12345)` (impressa pelos scripts); D é exaustivo/determinístico. Cada script foi executado duas vezes com saída idêntica.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir') == 'caf-noir'` (o `é` vira `-`) | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate(' ', 0) == '…'` (tamanho 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | — | `python3 checks/check_textutil.py` |
| T5 | verdadeira | — | `python3 checks/check_textutil.py` |
| T6 | verdadeira | — | `python3 checks/check_textutil.py` |
| M1 | verdadeira | — | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5) == 2` (arredonda para par) | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | — | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4) == True`; 18 erros em 0..1000: 4, 6, 8, 9, 15, 25, 35, 49, 121, 143… (`range(2, int(n**0.5))` exclui a raiz) | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | — | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | — | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(4,2,29), 12) == date(5,2,28)` | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1)) == -1` | `python3 checks/check_dates.py` |
| D4 | verdadeira | — | `python3 checks/check_dates.py` |
| D5 | verdadeira | — | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | — | `python3 checks/check_collections.py` |
| C2 | verdadeira | — (para itens hashable; com itens não hashable, p.ex. `[[1],[2]]`, levanta `TypeError` — a afirmação não cobre esse caso, mas vale a ressalva) | `python3 checks/check_collections.py` |
| C3 | falsa | `flatten([[1,[2]],[3]]) == [1,[2],3]` (só um nível) | `python3 checks/check_collections.py` |
| C4 | falsa | `top_n([3,1,2], -1) == [3,2]` (2 itens; esperado `min(-1,3)`) — vale para n negativo; para n ≥ 0 está correta | `python3 checks/check_collections.py` |
| C5 | falsa | `merge_dicts({'k':1},{'k':2}) == {'k':2}` (vence `b`) | `python3 checks/check_collections.py` |
| C6 | verdadeira | — | `python3 checks/check_collections.py` |

**Resumo:** 13 verdadeiras (T1, T4, T5, T6, M1, M4, M6, D1, D4, D5, C1, C2, C6) e 11 falsas (T2, T3, M2, M3, M5, D2, D3, D6, C3, C4, C5).
