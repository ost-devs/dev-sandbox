# Verificação das afirmações de `claims.md`

Resultado: **10 verdadeiras, 14 falsas**.

Cada veredito saiu da execução de `checks/check_<módulo>.py`. Os scripts usam só a biblioteca padrão do Python 3.11 e rodam de qualquer diretório. Afirmações com valor fixo são checadas com as entradas exatas. Afirmações universais ("para todo…") são checadas com casos de borda escolhidos à mão mais 10 000 entradas aleatórias de `random.Random(20261029)`. As exceções são M5 (varredura exaustiva de 0 a 1000) e D5 (todos os dias de 2023 e 2024, mais `date.min`/`date.max`). Rodei os quatro scripts duas vezes, de diretórios diferentes e com `PYTHONHASHSEED` diferente, e a saída foi idêntica.

Para rodar tudo, a partir deste diretório:

```
for m in textutil mathutil dates collections_util; do python3 checks/check_$m.py; done
```

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira | — (22 casos de borda + 10 000 strings aleatórias) | `python3 checks/check_textutil.py T1` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (esperado `'cafe-noir'`) | `python3 checks/check_textutil.py T2` |
| T3 | falsa | `truncate('a', 0)` → `'…'` (len 1 > 0) | `python3 checks/check_textutil.py T3` |
| T4 | verdadeira | — | `python3 checks/check_textutil.py T4` |
| T5 | verdadeira | — | `python3 checks/check_textutil.py T5` |
| T6 | verdadeira | — | `python3 checks/check_textutil.py T6` |
| M1 | verdadeira | — (1014 casos de borda, incl. `lo == hi`, inf, nan + 10 000 trios aleatórios) | `python3 checks/check_mathutil.py M1` |
| M2 | falsa | `mean([])` lança `ZeroDivisionError` (esperado `0`) | `python3 checks/check_mathutil.py M2` |
| M3 | falsa | `round_half(2.5)` → `2` (esperado `3`) | `python3 checks/check_mathutil.py M3` |
| M4 | verdadeira | — (256 pares de borda + 10 000 pares aleatórios) | `python3 checks/check_mathutil.py M4` |
| M5 | falsa | `is_prime(4)` → `True` (também 9, 25, 49, …) | `python3 checks/check_mathutil.py M5` |
| M6 | verdadeira | — | `python3 checks/check_mathutil.py M6` |
| D1 | verdadeira | — | `python3 checks/check_dates.py D1` |
| D2 | falsa | `add_months(date(2024, 2, 29), 12)` → `date(2025, 2, 28)` | `python3 checks/check_dates.py D2` |
| D3 | falsa | `days_between(date(2024, 1, 2), date(2024, 1, 1))` → `-1` | `python3 checks/check_dates.py D3` |
| D4 | verdadeira | — | `python3 checks/check_dates.py D4` |
| D5 | verdadeira | — (todos os dias de 2023–2024 + `date.min`/`date.max`) | `python3 checks/check_dates.py D5` |
| D6 | falsa | `parse_iso('2026-02-30')` lança `ValueError: day is out of range for month` | `python3 checks/check_dates.py D6` |
| C1 | verdadeira | — (57 casos de borda + 10 000 pares `(xs, n)` aleatórios) | `python3 checks/check_collections_util.py C1` |
| C2 | falsa¹ | `dedupe([[1], [1], [2]])` lança `TypeError` (esperado `[[1], [2]]`) | `python3 checks/check_collections_util.py C2` |
| C3 | falsa | `flatten([[1, [2]], [3]])` → `[1, [2], 3]` | `python3 checks/check_collections_util.py C3` |
| C4 | falsa | `top_n([], -1)` → `[]` (len 0, esperado `min(-1, 0) = -1`); `top_n([3, 1], -1)` → `[3]` | `python3 checks/check_collections_util.py C4` |
| C5 | falsa | `merge_dicts({'k': 1}, {'k': 2})` → `{'k': 2}` (fica o valor de `b`) | `python3 checks/check_collections_util.py C5` |
| C6 | verdadeira | — (12 casos de borda, incl. `[]` + 10 000 listas aleatórias) | `python3 checks/check_collections_util.py C6` |

¹ C2: com elementos hasheáveis, `dedupe` preserva a ordem das primeiras ocorrências (por exemplo, `dedupe([3, 1, 3, 2, 1])` → `[3, 1, 2]`). A afirmação é falsa só porque vale para "todo `xs`", e `dict.fromkeys` falha com elementos não hasheáveis. Se a afirmação se restringir a elementos hasheáveis, ela é verdadeira.

## Causa no código das afirmações falsas

- T2: `calc/textutil.py:5` troca todo caractere fora de `[a-z0-9]` por `-` e não remove acentos.
- T3: `calc/textutil.py:9` faz `s[:n - 1] + '…'`, que com `n == 0` vira `s[:-1] + '…'`.
- M2: `calc/mathutil.py:6` divide por `len(xs)` sem tratar a lista vazia.
- M3: `calc/mathutil.py:10` usa `round`, que arredonda o .5 para o par mais próximo (*banker's rounding*).
- M5: `calc/mathutil.py:23` usa `range(2, int(n ** 0.5))`, que exclui a raiz, e por isso os quadrados de primos passam como primos.
- D2: `calc/dates.py:10` limita o dia ao último dia do mês, e 29/02 vira 28/02.
- D3: `calc/dates.py:18` devolve `(b - a).days` com sinal.
- D6: `calc/dates.py:30` usa `date.fromisoformat`, que rejeita datas impossíveis.
- C2: `calc/collections_util.py:6` usa `dict.fromkeys`, que exige elementos hasheáveis.
- C3: `calc/collections_util.py:10` achata só um nível.
- C4: `calc/collections_util.py:14` usa `[:n]`, e com `n` negativo o fatiamento corta itens do fim.
- C5: `calc/collections_util.py:18` usa `{**a, **b}`, e o valor de `b` prevalece.
