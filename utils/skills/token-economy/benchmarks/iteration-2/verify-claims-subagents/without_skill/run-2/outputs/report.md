# Verificação de `claims.md` (pacote `calc/`)

Cada afirmação foi checada **rodando** o código. As checagens ficam em `checks/`, um script por módulo, e usam só a biblioteca padrão.

- Todas as checagens são determinísticas. Elas usam entradas fixas (casos de borda escolhidos a partir do código) e, nas afirmações do tipo "para todo", também entradas aleatórias geradas com `random.Random(SEED)`, onde `SEED = 20261029` está fixo em cada script.
- Uma exceção conta como falha da afirmação.
- Rode os comandos a partir deste diretório. Cada script imprime uma linha por afirmação (`ID | TRUE` ou `ID | FALSE | counterexample: ...`) e sai com código 0. O `grep` da tabela só seleciona a linha de cada id.
- Cada script foi executado duas vezes e as duas saídas foram idênticas.

**Resumo:** 11 verdadeiras e 13 falsas.

| id | veredito | contraexemplo (quando falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | — (cerca de 22 mil strings aleatórias, mais casos de borda: vazia, só `-`, unicode) | `python3 checks/check_textutil.py \| grep '^T1 '` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` não é transliterado e vira separador) | `python3 checks/check_textutil.py \| grep '^T2 '` |
| T3 | falsa | `truncate('a', 0)` → `'…'` (comprimento 1 > 0). Com `n == 0`, `s[:n-1]` vira `s[:-1]`. | `python3 checks/check_textutil.py \| grep '^T3 '` |
| T4 | verdadeira | — | `python3 checks/check_textutil.py \| grep '^T4 '` |
| T5 | verdadeira | — | `python3 checks/check_textutil.py \| grep '^T5 '` |
| T6 | verdadeira | — | `python3 checks/check_textutil.py \| grep '^T6 '` |
| M1 | verdadeira | — (todos os pares de 20 valores de borda, inclusive ±inf e NaN como `x`, mais 60 mil casos aleatórios) | `python3 checks/check_mathutil.py \| grep '^M1 '` |
| M2 | falsa | `mean([])` lança `ZeroDivisionError` em vez de retornar `0` | `python3 checks/check_mathutil.py \| grep '^M2 '` |
| M3 | falsa | `round_half(2.5)` → `2` (o `round` do Python arredonda metades para o par) | `python3 checks/check_mathutil.py \| grep '^M3 '` |
| M4 | verdadeira | — (todos os pares em -60..60, valores de borda grandes e 60 mil pares aleatórios) | `python3 checks/check_mathutil.py \| grep '^M4 '` |
| M5 | falsa | `is_prime(4)` → `True`. Também erra 9, 25, 49 etc., porque o laço `range(2, int(n**0.5))` não testa a própria raiz. | `python3 checks/check_mathutil.py \| grep '^M5 '` |
| M6 | verdadeira | — | `python3 checks/check_mathutil.py \| grep '^M6 '` |
| D1 | verdadeira | — | `python3 checks/check_dates.py \| grep '^D1 '` |
| D2 | falsa | `add_months(date(2024, 2, 29), 12)` → `date(2025, 2, 28)`. Além disso, `add_months(date(9999, 1, 1), 12)` lança `ValueError` (ano 10000). | `python3 checks/check_dates.py \| grep '^D2 '` |
| D3 | falsa | `days_between(date(2024, 1, 2), date(2024, 1, 1))` → `-1` | `python3 checks/check_dates.py \| grep '^D3 '` |
| D4 | verdadeira | — | `python3 checks/check_dates.py \| grep '^D4 '` |
| D5 | verdadeira | — (todos os dias dos anos 1, 1900, 2000, 2023, 2024, 2100 e 9999, mais 20 mil datas aleatórias) | `python3 checks/check_dates.py \| grep '^D5 '` |
| D6 | falsa | `parse_iso('2026-02-30')` lança `ValueError: day is out of range for month` | `python3 checks/check_dates.py \| grep '^D6 '` |
| C1 | verdadeira | — (3000 listas aleatórias, `n` de 1 a 7) | `python3 checks/check_collections_util.py \| grep '^C1 '` |
| C2 | verdadeira* | — | `python3 checks/check_collections_util.py \| grep '^C2 '` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` (só remove um nível de aninhamento) | `python3 checks/check_collections_util.py \| grep '^C3 '` |
| C4 | falsa | `top_n([0, 1], -1)` → `[1]` (1 item). `min(-1, 2) = -1` não é um tamanho possível, e o resultado nem é vazio. | `python3 checks/check_collections_util.py \| grep '^C4 '` |
| C5 | falsa | `merge_dicts({'k': 1}, {'k': 2})['k']` → `2` (o valor de `b` prevalece) | `python3 checks/check_collections_util.py \| grep '^C5 '` |
| C6 | verdadeira | — | `python3 checks/check_collections_util.py \| grep '^C6 '` |

\* **C2:** a afirmação vale para listas de elementos *hashable*. Com elementos não hashable, `dedupe([[1], [1]])` lança `TypeError: unhashable type: 'list'`. A afirmação não diz "para toda lista", então foi julgada só nesse domínio. Se a intenção for "qualquer lista", ela é falsa.

Para rodar todas as checagens de uma vez:

```sh
for m in textutil mathutil dates collections_util; do python3 checks/check_$m.py; done
```
