# Relatório de verificação das afirmações sobre `calc/`

Rodar a partir da raiz do projeto (`/tmp/dev-home/.cache/token-economy-runs/verify-claims-subagents-with_skill-55b2d4bb`). Cada `check.py` imprime uma linha por afirmação (`id`, veredito, contraexemplo); a saída gravada está em `checks/<módulo>/results.tsv`. Entradas aleatórias usam a semente registrada `20261101` (em `checks/common.py`); duas execuções deram saída idêntica.

Resultado: 13 verdadeiras, 11 falsas.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T1 | verdadeira |  | `python3 checks/textutil/check.py` (linha T1) |
| T2 | falsa | slugify('Café Noir')='caf-noir' | `python3 checks/textutil/check.py` (linha T2) |
| T3 | falsa | s=' ', n=0 -> '…' (len 1) | `python3 checks/textutil/check.py` (linha T3) |
| T4 | verdadeira |  | `python3 checks/textutil/check.py` (linha T4) |
| T5 | verdadeira |  | `python3 checks/textutil/check.py` (linha T5) |
| T6 | verdadeira |  | `python3 checks/textutil/check.py` (linha T6) |
| M1 | verdadeira |  | `python3 checks/mathutil/check.py` (linha M1) |
| M2 | falsa | mean([]) raises ZeroDivisionError: division by zero | `python3 checks/mathutil/check.py` (linha M2) |
| M3 | falsa | round_half(2.5)=2 | `python3 checks/mathutil/check.py` (linha M3) |
| M4 | verdadeira |  | `python3 checks/mathutil/check.py` (linha M4) |
| M5 | falsa | smallest is_prime(4)=True, expected False (18 wrong in 0..1000) | `python3 checks/mathutil/check.py` (linha M5) |
| M6 | verdadeira |  | `python3 checks/mathutil/check.py` (linha M6) |
| D1 | verdadeira |  | `python3 checks/dates/check.py` (linha D1) |
| D2 | falsa | add_months(0004-02-29,12)=0005-02-28 | `python3 checks/dates/check.py` (linha D2) |
| D3 | falsa | days_between(2024-02-29,2024-02-28)=-1 | `python3 checks/dates/check.py` (linha D3) |
| D4 | verdadeira |  | `python3 checks/dates/check.py` (linha D4) |
| D5 | verdadeira |  | `python3 checks/dates/check.py` (linha D5) |
| D6 | falsa | parse_iso('2026-02-30') raises ValueError: day is out of range for month | `python3 checks/dates/check.py` (linha D6) |
| C1 | verdadeira |  | `python3 checks/collections_util/check.py` (linha C1) |
| C2 | verdadeira |  | `python3 checks/collections_util/check.py` (linha C2) |
| C3 | falsa | flatten([[1, [2]], [3]]) = [1, [2], 3] (só achata um nível) | `python3 checks/collections_util/check.py` (linha C3) |
| C4 | falsa | top_n([1, 2, 3], -1) devolve 2 itens, não min(-1, 3) | `python3 checks/collections_util/check.py` (linha C4) |
| C5 | falsa | merge_dicts({'a': 0}, {'a': 1})['a'] = 1 (vale o de b) | `python3 checks/collections_util/check.py` (linha C5) |
| C6 | verdadeira |  | `python3 checks/collections_util/check.py` (linha C6) |
