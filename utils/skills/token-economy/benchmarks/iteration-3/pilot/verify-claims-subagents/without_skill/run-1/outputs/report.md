# Relatório de verificação das afirmações sobre `calc/`

Cada checagem fica em `checks/<módulo>.py`, roda da raiz do projeto e é determinística. As sementes são constantes nos arquivos: textutil 12345, mathutil 20240607, dates 20240229, collections_util 12345. Rodei cada script duas vezes e as saídas foram idênticas.

Resumo: 12 verdadeiras e 12 falsas.

| id | veredito | contraexemplo (quando falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | | `python3 checks/textutil.py` |
| T2 | falsa | `slugify('Café Noir')` devolve `'caf-noir'`, não `'cafe-noir'` | `python3 checks/textutil.py` |
| T3 | falsa | `truncate(' ', 0)` devolve `'…'` (tamanho 1 > 0) | `python3 checks/textutil.py` |
| T4 | verdadeira | | `python3 checks/textutil.py` |
| T5 | verdadeira | | `python3 checks/textutil.py` |
| T6 | verdadeira | | `python3 checks/textutil.py` |
| M1 | verdadeira | | `python3 checks/mathutil.py` |
| M2 | falsa | `mean([])` lança `ZeroDivisionError` | `python3 checks/mathutil.py` |
| M3 | falsa | `round_half(2.5)` devolve `2` (arredondamento para par) | `python3 checks/mathutil.py` |
| M4 | verdadeira | | `python3 checks/mathutil.py` |
| M5 | falsa | `is_prime(4)` devolve `True`; o laço `range(2, int(n**0.5))` não inclui a raiz | `python3 checks/mathutil.py` |
| M6 | verdadeira | | `python3 checks/mathutil.py` |
| D1 | verdadeira | | `python3 checks/dates.py` |
| D2 | falsa | `add_months(date(2024,2,29), 12)` devolve `date(2025,2,28)` | `python3 checks/dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1))` devolve `-1` | `python3 checks/dates.py` |
| D4 | verdadeira | | `python3 checks/dates.py` |
| D5 | verdadeira | | `python3 checks/dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` lança `ValueError: day is out of range for month` | `python3 checks/dates.py` |
| C1 | verdadeira | | `python3 checks/collections_util.py` |
| C2 | verdadeira | | `python3 checks/collections_util.py` |
| C3 | falsa | `flatten([[1,[2]],[3]])` devolve `[1,[2],3]`; só desce um nível | `python3 checks/collections_util.py` |
| C4 | falsa | `top_n([1,2,3], -1)` devolve 2 itens (`[3,2]`), não `min(-1,3)` | `python3 checks/collections_util.py` |
| C5 | falsa | `merge_dicts({0:2},{0:6})` devolve `{0:6}`; vale o valor de `b` | `python3 checks/collections_util.py` |
| C6 | verdadeira | | `python3 checks/collections_util.py` |

## Alcance das checagens "verdadeira"

Uma afirmação universal marcada como verdadeira só significa que nenhum contraexemplo apareceu no que foi testado:

- **Testes aleatórios com semente:** T1, M1, M4, C1, C2, C6.
- **Varreduras exaustivas:** D5 (todas as datas dos anos 1 a 9999).
- **C2:** foi testada só com elementos hasháveis.
- **M1:** os casos com limites `nan` ficaram de fora, porque a condição `lo <= hi` é falsa neles.
- **M5:** o contraexemplo `is_prime(4)` foi achado contra um teste independente por divisão sucessiva para 0..1000. Em `dates` e `mathutil`, os contraexemplos citados vêm da saída dos scripts, exceto o de C4 em `[1,2,3]` e `-1`, que veio do relato do subagente.
