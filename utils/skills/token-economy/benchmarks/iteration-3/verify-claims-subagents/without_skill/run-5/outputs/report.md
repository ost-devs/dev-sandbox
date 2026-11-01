# Relatório de verificação das afirmações de `calc/`

Cada checagem é determinística (entradas fixas ou `random.Random(semente)` com semente registrada no script). Todas rodam a partir deste diretório. Os scripts foram executados duas vezes por cada subagente e uma terceira vez na consolidação, com saída idêntica.

Resultado: 11 verdadeiras, 13 falsas.

| id | veredito | contraexemplo (quando falsa) | comando |
|---|---|---|---|
| T1 | verdadeira | | `python3 checks/check_textutil.py` |
| T2 | falsa | `slugify('Café Noir')` → `'caf-noir'` (esperado `'cafe-noir'`) | `python3 checks/check_textutil.py` |
| T3 | falsa | `truncate(' ', 0)` → `'…'` (tamanho 1 > 0) | `python3 checks/check_textutil.py` |
| T4 | verdadeira | | `python3 checks/check_textutil.py` |
| T5 | verdadeira | | `python3 checks/check_textutil.py` |
| T6 | verdadeira | | `python3 checks/check_textutil.py` |
| M1 | verdadeira | | `python3 checks/check_mathutil.py` |
| M2 | falsa | `mean([])` levanta `ZeroDivisionError` | `python3 checks/check_mathutil.py` |
| M3 | falsa | `round_half(2.5)` → `2` (arredondamento par do `round`) | `python3 checks/check_mathutil.py` |
| M4 | verdadeira | | `python3 checks/check_mathutil.py` |
| M5 | falsa | `is_prime(4)` → `True`; erra também 6, 8, 9, 15, 25, 35, 49, 121, 143, 169, 289, 323, 361, 529, 841, 899, 961 | `python3 checks/check_mathutil.py` |
| M6 | verdadeira | | `python3 checks/check_mathutil.py` |
| D1 | verdadeira | | `python3 checks/check_dates.py` |
| D2 | falsa | `add_months(date(4,2,29), 12)` → `date(5,2,28)` (29/fev vira 28/fev) | `python3 checks/check_dates.py` |
| D3 | falsa | `days_between(date(2024,1,2), date(2024,1,1))` → `-1` | `python3 checks/check_dates.py` |
| D4 | verdadeira | | `python3 checks/check_dates.py` |
| D5 | verdadeira | (varredura exaustiva 0001-01-01..9999-12-31) | `python3 checks/check_dates.py` |
| D6 | falsa | `parse_iso('2026-02-30')` levanta `ValueError` | `python3 checks/check_dates.py` |
| C1 | verdadeira | | `python3 checks/check_collections_util.py` |
| C2 | verdadeira | | `python3 checks/check_collections_util.py` |
| C3 | falsa | `flatten([[1,[2]],[3]])` → `[1,[2],3]` (achata só um nível) | `python3 checks/check_collections_util.py` |
| C4 | falsa | `top_n([], -1)` → `[]` (esperado tamanho `min(-1,0) = -1`; só falha com n negativo) | `python3 checks/check_collections_util.py` |
| C5 | falsa | `merge_dicts({'a':1},{'a':4})` → `{'a':4}` (vale o de `b`) | `python3 checks/check_collections_util.py` |
| C6 | verdadeira | | `python3 checks/check_collections_util.py` |

Observações:
- Cada script imprime uma linha `ID VEREDITO detalhe` por afirmação (TRUE/FALSE), sempre com código de saída 0.
- Afirmações universais verdadeiras valem para as entradas testadas (casos de borda, grades, sementes fixas ou varredura exaustiva quando indicado). Isso é evidência forte, não prova formal.
- M5 foi comparada com um crivo independente em todo o intervalo 0..1000.
- Causa de M5: `range(2, int(n ** 0.5))` para um passo antes da raiz.
