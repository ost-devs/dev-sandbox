# Verificação das afirmações de `claims.md`

Cada veredito vem da execução de um script em `checks/` (Python 3.11). Os casos aleatórios usam semente fixa, registrada no próprio script e na saída. Todos os comandos rodam a partir da raiz (a pasta que contém `calc/` e `checks/`).

- Tudo de uma vez: `./checks/run_all.sh` (24 linhas no formato `id<TAB>TRUE|FALSE<TAB>detalhe`). Rodei duas vezes e a saída foi idêntica byte a byte.
- Helpers comuns (gerador com semente, busca de contraexemplo, formato da saída): `checks/harness.py`.

**Resultado: 12 verdadeiras, 12 falsas.**

| id | veredito | contraexemplo (quando falsa) | comando que reproduz |
|---|---|---|---|
| T1 | verdadeira | — (7 casos fixos + 5000 aleatórios, seed=1) | `python3 checks/check_textutil.py \| grep '^T1'` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` é descartado, não vira `e`) | `python3 checks/check_textutil.py \| grep '^T2'` |
| T3 | falsa | `truncate('a', 0)` → `'…'`, de comprimento 1 > 0 | `python3 checks/check_textutil.py \| grep '^T3'` |
| T4 | verdadeira | — (retorna 3) | `python3 checks/check_textutil.py \| grep '^T4'` |
| T5 | verdadeira | — (retorna `'A  B'`) | `python3 checks/check_textutil.py \| grep '^T5'` |
| T6 | verdadeira | — (retorna `True`) | `python3 checks/check_textutil.py \| grep '^T6'` |
| M1 | verdadeira | — (8 casos fixos, incluindo ±inf e NaN, + 3000 aleatórios, seed=1) | `python3 checks/check_mathutil.py \| grep '^M1'` |
| M2 | falsa | `mean([])` lança `ZeroDivisionError` | `python3 checks/check_mathutil.py \| grep '^M2'` |
| M3 | falsa | `round_half(2.5)` → `2` | `python3 checks/check_mathutil.py \| grep '^M3'` |
| M4 | verdadeira | — (7 casos fixos + 3000 aleatórios, seed=4; só inteiros) | `python3 checks/check_mathutil.py \| grep '^M4'` |
| M5 | falsa | `is_prime` diz que estes 18 compostos são primos: 4, 6, 8, 9, 15, 25, 35, 49, 121, 143, 169, 289, 323, 361, 529, 841, 899, 961 (checagem exaustiva de 0 a 1000) | `python3 checks/check_mathutil.py \| grep '^M5'` |
| M6 | verdadeira | — (retorna `33.3`) | `python3 checks/check_mathutil.py \| grep '^M6'` |
| D1 | verdadeira | — (retorna `date(2024, 2, 29)`) | `python3 checks/check_dates.py \| grep '^D1'` |
| D2 | falsa | `add_months(date(2024, 2, 29), 12)` → `date(2025, 2, 28)` (o dia muda) | `python3 checks/check_dates.py \| grep '^D2'` |
| D3 | falsa | `days_between(date(2024, 1, 2), date(2024, 1, 1))` → `-1` | `python3 checks/check_dates.py \| grep '^D3'` |
| D4 | verdadeira | — (retorna `False`) | `python3 checks/check_dates.py \| grep '^D4'` |
| D5 | verdadeira | — (19 casos fixos + 3000 aleatórios, seed=5) | `python3 checks/check_dates.py \| grep '^D5'` |
| D6 | falsa | `parse_iso('2026-02-30')` lança `ValueError: day is out of range for month` | `python3 checks/check_dates.py \| grep '^D6'` |
| C1 | verdadeira | — (5 casos fixos + 3000 aleatórios, seed=1) | `python3 checks/check_collections_util.py \| grep '^C1'` |
| C2 | verdadeira | — (3 casos fixos + 3000 aleatórios, seed=2; elementos int) | `python3 checks/check_collections_util.py \| grep '^C2'` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` (só achata um nível) | `python3 checks/check_collections_util.py \| grep '^C3'` |
| C4 | falsa | `top_n([1, 2, 3], -1)` → `[3, 2]` (2 itens; `min(-1, 3)` = -1) | `python3 checks/check_collections_util.py \| grep '^C4'` |
| C5 | falsa | `merge_dicts({'k': 1}, {'k': 2})` → `{'k': 2}` (fica o valor de `b`) | `python3 checks/check_collections_util.py \| grep '^C5'` |
| C6 | verdadeira | — (4 casos fixos, incluindo `[]`, + 3000 aleatórios, seed=6) | `python3 checks/check_collections_util.py \| grep '^C6'` |

## Notas de interpretação

- Li as afirmações ao pé da letra, com a semântica de `==` do Python. Uma exceção onde a afirmação espera um valor conta como falsa (M2, D6).
- **C4:** para `n < 0`, "`min(n, len(xs))` itens" daria um número negativo, que nenhuma lista pode ter. Então a afirmação é falsa para qualquer `n` negativo, não importa a implementação.
- **D2:** além de 29/02, as datas do ano 9999 também falhariam, porque o ano seguinte fica fora do alcance de `date`.
- **Verdadeiras universais** (T1, M1, M4, C1, C2, C6, D5): "verdadeira" quer dizer que nenhum contraexemplo apareceu nos casos fixos de borda nem nas entradas aleatórias com semente. Isso é evidência forte, mas não é prova. M4 testou só inteiros e C2 testou só elementos hasheáveis (int).
