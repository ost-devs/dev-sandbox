# Verificação das afirmações de `claims.md`

Cada veredito vem de um script em `checks/<módulo>/check_<id>.py`, executado a partir da raiz do workspace (Python 3.11). As entradas geradas usam a semente fixa `harness.SEED = 20261029`. Rodar `python3 checks/run_all.py` executa as 24 checagens e imprime uma linha JSON por afirmação, com o método e o número de casos testados. Duas execuções completas deram saídas idênticas byte a byte.

**Resultado: 11 verdadeiras, 13 falsas.**

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — | `python3 checks/textutil/check_T1.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (o `é` é removido em vez de virar `e`) | `python3 checks/textutil/check_T2.py` |
| T3 | falsa | `truncate('a', 0)` → `'…'`, comprimento 1 > 0 | `python3 checks/textutil/check_T3.py` |
| T4 | verdadeira | — | `python3 checks/textutil/check_T4.py` |
| T5 | verdadeira | — | `python3 checks/textutil/check_T5.py` |
| T6 | verdadeira | — | `python3 checks/textutil/check_T6.py` |
| M1 | verdadeira | — | `python3 checks/mathutil/check_M1.py` |
| M2 | falsa | `mean([])` lança `ZeroDivisionError` | `python3 checks/mathutil/check_M2.py` |
| M3 | falsa | `round_half(2.5)` → `2` (arredondamento bancário do Python) | `python3 checks/mathutil/check_M3.py` |
| M4 | verdadeira | — | `python3 checks/mathutil/check_M4.py` |
| M5 | falsa | `is_prime(4)` → `True` (`range(2, int(n**0.5))` não testa a raiz) | `python3 checks/mathutil/check_M5.py` |
| M6 | verdadeira | — | `python3 checks/mathutil/check_M6.py` |
| D1 | verdadeira | — | `python3 checks/dates/check_D1.py` |
| D2 | falsa | `add_months(date(2024, 2, 29), 12)` → `date(2025, 2, 28)` | `python3 checks/dates/check_D2.py` |
| D3 | falsa | `days_between(date(2024, 1, 2), date(2024, 1, 1))` → `-1` | `python3 checks/dates/check_D3.py` |
| D4 | verdadeira | — | `python3 checks/dates/check_D4.py` |
| D5 | verdadeira | — | `python3 checks/dates/check_D5.py` |
| D6 | falsa | `parse_iso('2026-02-30')` lança `ValueError: day is out of range for month` | `python3 checks/dates/check_D6.py` |
| C1 | verdadeira | — | `python3 checks/collections_util/check_C1.py` |
| C2 | verdadeira | — | `python3 checks/collections_util/check_C2.py` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` (achata só um nível) | `python3 checks/collections_util/check_C3.py` |
| C4 | falsa | `top_n([1, 2, 3], -1)` → 2 itens (`[3, 2]`); `n` negativo corta pelo fim | `python3 checks/collections_util/check_C4.py` |
| C5 | falsa | `merge_dicts({'k': 'a'}, {'k': 'b'})['k']` → `'b'` (prevalece `b`) | `python3 checks/collections_util/check_C5.py` |
| C6 | verdadeira | — | `python3 checks/collections_util/check_C6.py` |

## Notas

- Verdadeira aqui quer dizer que não apareceu contraexemplo nos casos testados, não que a afirmação foi provada. A cobertura é exaustiva onde o domínio é finito: M5 (0..1000, comparado a um crivo) e D2/D5 (todas as datas de 0001-01-01 a 2100-12-31). Nos outros casos, os testes cobrem casos de borda escolhidos à mão, entradas pequenas enumeradas por completo e entradas aleatórias com semente fixa. O método e o número de casos de cada checagem aparecem no campo `method` da saída.
- C4: com `n` negativo, `min(n, len(xs))` é negativo, e nenhuma lista tem esse número de itens. A afirmação já falha por esse motivo. O script mostra `top_n([], -1)`, e o exemplo da tabela mostra o efeito prático. Para `n >= 0` ela vale.
- Exceções contam como violação (M2, D6).
