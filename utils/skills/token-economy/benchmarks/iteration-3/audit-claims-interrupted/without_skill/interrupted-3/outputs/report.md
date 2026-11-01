# Relatório de verificação de claims.md

152 afirmações, 113 verdadeiras e 39 falsas. Cada checagem é determinista (entradas fixas ou `random.Random(SEED)` com semente constante no próprio arquivo); rodar cada script duas vezes dá saída idêntica. Para rodar um módulo inteiro: `python3 -I checks/<módulo>.py`.

Ressalva R18: marcada verdadeira porque as amostras não incluem NaN; com `{'x': float('nan')}` a igualdade literal falharia (NaN != NaN).

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `slugify('Café Noir') -> 'caf-noir' (esperado 'cafe-noir')` | `python3 -I checks/text.py T01` |
| T02 | verdadeira | — | `python3 -I checks/text.py T02` |
| T03 | verdadeira | — | `python3 -I checks/text.py T03` |
| T04 | verdadeira | — | `python3 -I checks/text.py T04` |
| T05 | falsa | `entrada (' ', 0) -> saída '...'` | `python3 -I checks/text.py T05` |
| T06 | verdadeira | — | `python3 -I checks/text.py T06` |
| T07 | verdadeira | — | `python3 -I checks/text.py T07` |
| T08 | verdadeira | — | `python3 -I checks/text.py T08` |
| T09 | verdadeira | — | `python3 -I checks/text.py T09` |
| T10 | verdadeira | — | `python3 -I checks/text.py T10` |
| T11 | verdadeira | — | `python3 -I checks/text.py T11` |
| T12 | falsa | `entrada 'ß' -> saída 'SS'` | `python3 -I checks/text.py T12` |
| T13 | verdadeira | — | `python3 -I checks/text.py T13` |
| T14 | falsa | `strip_accents('ø') -> 'ø' (esperado 'o')` | `python3 -I checks/text.py T14` |
| T15 | verdadeira | — | `python3 -I checks/text.py T15` |
| T16 | verdadeira | — | `python3 -I checks/text.py T16` |
| T17 | verdadeira | — | `python3 -I checks/text.py T17` |
| T18 | verdadeira | — | `python3 -I checks/text.py T18` |
| T19 | verdadeira | — | `python3 -I checks/text.py T19` |
| N01 | verdadeira | — | `python3 -I checks/numbers.py N01` |
| N02 | falsa | `clamp(5, 10, 0) -> 10 (expected 0)` | `python3 -I checks/numbers.py N02` |
| N03 | verdadeira | — | `python3 -I checks/numbers.py N03` |
| N04 | verdadeira | — | `python3 -I checks/numbers.py N04` |
| N05 | verdadeira | — | `python3 -I checks/numbers.py N05` |
| N06 | falsa | `median([]) raised IndexError: list index out of range` | `python3 -I checks/numbers.py N06` |
| N07 | verdadeira | — | `python3 -I checks/numbers.py N07` |
| N08 | falsa | `round_half(2.5) -> 2 (expected 3)` | `python3 -I checks/numbers.py N08` |
| N09 | verdadeira | — | `python3 -I checks/numbers.py N09` |
| N10 | verdadeira | — | `python3 -I checks/numbers.py N10` |
| N11 | falsa | `percent(0, 0) raised ZeroDivisionError: division by zero` | `python3 -I checks/numbers.py N11` |
| N12 | falsa | `is_prime(4) -> True (expected False); 18 wrong values in 0..1000` | `python3 -I checks/numbers.py N12` |
| N13 | verdadeira | — | `python3 -I checks/numbers.py N13` |
| N14 | verdadeira | — | `python3 -I checks/numbers.py N14` |
| N15 | falsa | `gcd(-50,1)=1 but gcd(1,-50)=-1` | `python3 -I checks/numbers.py N15` |
| N16 | verdadeira | — | `python3 -I checks/numbers.py N16` |
| N17 | verdadeira | — | `python3 -I checks/numbers.py N17` |
| N18 | verdadeira | — | `python3 -I checks/numbers.py N18` |
| N19 | falsa | `digits_sum(-1) raised ValueError: invalid literal for int() with base 10: '-'` | `python3 -I checks/numbers.py N19` |
| D01 | verdadeira | — | `python3 -I checks/dates.py D01` |
| D02 | falsa | `add_months(datetime.date(2000, 2, 29), 12) -> datetime.date(2001, 2, 28)` | `python3 -I checks/dates.py D02` |
| D03 | falsa | `add_months(add_months(datetime.date(2000, 1, 30), 1), -1) -> datetime.date(2000, 1, 29)` | `python3 -I checks/dates.py D03` |
| D04 | falsa | `days_between(datetime.date(2000, 1, 2), datetime.date(2000, 1, 1)) -> -1` | `python3 -I checks/dates.py D04` |
| D05 | verdadeira | — | `python3 -I checks/dates.py D05` |
| D06 | verdadeira | — | `python3 -I checks/dates.py D06` |
| D07 | verdadeira | — | `python3 -I checks/dates.py D07` |
| D08 | verdadeira | — | `python3 -I checks/dates.py D08` |
| D09 | verdadeira | — | `python3 -I checks/dates.py D09` |
| D10 | verdadeira | — | `python3 -I checks/dates.py D10` |
| D11 | verdadeira | — | `python3 -I checks/dates.py D11` |
| D12 | verdadeira | — | `python3 -I checks/dates.py D12` |
| D13 | verdadeira | — | `python3 -I checks/dates.py D13` |
| D14 | falsa | `iso_week(date(2021,1,1)) -> 53 (esperado 1)` | `python3 -I checks/dates.py D14` |
| D15 | verdadeira | — | `python3 -I checks/dates.py D15` |
| D16 | falsa | `parse_br('1/2/2024') -> datetime.date(2024, 2, 1) (nao levantou ValueError)` | `python3 -I checks/dates.py D16` |
| D17 | verdadeira | — | `python3 -I checks/dates.py D17` |
| D18 | verdadeira | — | `python3 -I checks/dates.py D18` |
| D19 | verdadeira | — | `python3 -I checks/dates.py D19` |
| I01 | verdadeira | — | `python3 -I checks/intervals.py I01` |
| I02 | verdadeira | — | `python3 -I checks/intervals.py I02` |
| I03 | verdadeira | — | `python3 -I checks/intervals.py I03` |
| I04 | verdadeira | — | `python3 -I checks/intervals.py I04` |
| I05 | verdadeira | — | `python3 -I checks/intervals.py I05` |
| I06 | verdadeira | — | `python3 -I checks/intervals.py I06` |
| I07 | falsa | `contains((0,5),5) -> True (esperado False)` | `python3 -I checks/intervals.py I07` |
| I08 | verdadeira | — | `python3 -I checks/intervals.py I08` |
| I09 | verdadeira | — | `python3 -I checks/intervals.py I09` |
| I10 | verdadeira | — | `python3 -I checks/intervals.py I10` |
| I11 | verdadeira | — | `python3 -I checks/intervals.py I11` |
| I12 | verdadeira | — | `python3 -I checks/intervals.py I12` |
| I13 | verdadeira | — | `python3 -I checks/intervals.py I13` |
| I14 | verdadeira | — | `python3 -I checks/intervals.py I14` |
| I15 | falsa | `merge([]) -> exceção IndexError: list index out of range` | `python3 -I checks/intervals.py I15` |
| I16 | verdadeira | — | `python3 -I checks/intervals.py I16` |
| I17 | verdadeira | — | `python3 -I checks/intervals.py I17` |
| I18 | falsa | `contains((0, 5),5) implica overlaps((0, 5),(5, 6)) -> False` | `python3 -I checks/intervals.py I18` |
| I19 | falsa | `length((3,1)) -> -2 (esperado 0)` | `python3 -I checks/intervals.py I19` |
| L01 | verdadeira | — | `python3 -I checks/lists.py L01` |
| L02 | verdadeira | — | `python3 -I checks/lists.py L02` |
| L03 | verdadeira | — | `python3 -I checks/lists.py L03` |
| L04 | verdadeira | — | `python3 -I checks/lists.py L04` |
| L05 | verdadeira | — | `python3 -I checks/lists.py L05` |
| L06 | verdadeira | — | `python3 -I checks/lists.py L06` |
| L07 | falsa | `flatten([[1,[2]],[3]]) -> [1, [2], 3] (esperado [1, 2, 3])` | `python3 -I checks/lists.py L07` |
| L08 | verdadeira | — | `python3 -I checks/lists.py L08` |
| L09 | verdadeira | — | `python3 -I checks/lists.py L09` |
| L10 | falsa | `top_n([3,2,1],-1) -> [3, 2] (esperado [])` | `python3 -I checks/lists.py L10` |
| L11 | verdadeira | — | `python3 -I checks/lists.py L11` |
| L12 | falsa | `L12 com entrada ([1, 2, 3], 4) -> [1, 2, 3]` | `python3 -I checks/lists.py L12` |
| L13 | verdadeira | — | `python3 -I checks/lists.py L13` |
| L14 | falsa | `interleave([1,2,3],[9]) -> [1, 9] (esperado [1, 9, 2, 3])` | `python3 -I checks/lists.py L14` |
| L15 | verdadeira | — | `python3 -I checks/lists.py L15` |
| L16 | verdadeira | — | `python3 -I checks/lists.py L16` |
| L17 | verdadeira | — | `python3 -I checks/lists.py L17` |
| L18 | verdadeira | — | `python3 -I checks/lists.py L18` |
| L19 | falsa | `L19 com entrada ([],) -> []` | `python3 -I checks/lists.py L19` |
| M01 | verdadeira | — | `python3 -I checks/money.py M01` |
| M02 | verdadeira | — | `python3 -I checks/money.py M02` |
| M03 | falsa | `to_cents('-1,50') = -50, esperado -150` | `python3 -I checks/money.py M03` |
| M04 | verdadeira | — | `python3 -I checks/money.py M04` |
| M05 | verdadeira | — | `python3 -I checks/money.py M05` |
| M06 | verdadeira | — | `python3 -I checks/money.py M06` |
| M07 | falsa | `format_brl(-150) = 'R$ -2,50', esperado 'R$ -1,50'` | `python3 -I checks/money.py M07` |
| M08 | verdadeira | — | `python3 -I checks/money.py M08` |
| M09 | falsa | `sum(split_bill(total,k)) != total com entrada (1, 2): obtido [0, 0]` | `python3 -I checks/money.py M09` |
| M10 | verdadeira | — | `python3 -I checks/money.py M10` |
| M11 | verdadeira | — | `python3 -I checks/money.py M11` |
| M12 | verdadeira | — | `python3 -I checks/money.py M12` |
| M13 | verdadeira | — | `python3 -I checks/money.py M13` |
| M14 | verdadeira | — | `python3 -I checks/money.py M14` |
| M15 | verdadeira | — | `python3 -I checks/money.py M15` |
| M16 | verdadeira | — | `python3 -I checks/money.py M16` |
| M17 | falsa | `add_tax(100, 0.15) = 114, esperado 115` | `python3 -I checks/money.py M17` |
| M18 | verdadeira | — | `python3 -I checks/money.py M18` |
| M19 | verdadeira | — | `python3 -I checks/money.py M19` |
| P01 | verdadeira | — | `python3 -I checks/paths.py P01` |
| P02 | falsa | `join('/usr','bin') -> 'usr/bin' (esperado '/usr/bin')` | `python3 -I checks/paths.py P02` |
| P03 | verdadeira | — | `python3 -I checks/paths.py P03` |
| P04 | verdadeira | — | `python3 -I checks/paths.py P04` |
| P05 | falsa | `ext('dir.d/arquivo') -> 'd/arquivo' (esperado '')` | `python3 -I checks/paths.py P05` |
| P06 | falsa | `ext('.bashrc') -> 'bashrc' (esperado '')` | `python3 -I checks/paths.py P06` |
| P07 | verdadeira | — | `python3 -I checks/paths.py P07` |
| P08 | verdadeira | — | `python3 -I checks/paths.py P08` |
| P09 | verdadeira | — | `python3 -I checks/paths.py P09` |
| P10 | falsa | `normalize('../x') -> 'x' (esperado '../x')` | `python3 -I checks/paths.py P10` |
| P11 | verdadeira | — | `python3 -I checks/paths.py P11` |
| P12 | verdadeira | — | `python3 -I checks/paths.py P12` |
| P13 | verdadeira | — | `python3 -I checks/paths.py P13` |
| P14 | verdadeira | — | `python3 -I checks/paths.py P14` |
| P15 | verdadeira | — | `python3 -I checks/paths.py P15` |
| P16 | verdadeira | — | `python3 -I checks/paths.py P16` |
| P17 | falsa | `parent('/a') -> '' (esperado '/')` | `python3 -I checks/paths.py P17` |
| P18 | verdadeira | — | `python3 -I checks/paths.py P18` |
| P19 | verdadeira | — | `python3 -I checks/paths.py P19` |
| R01 | verdadeira | — | `python3 -I checks/records.py R01` |
| R02 | verdadeira | — | `python3 -I checks/records.py R02` |
| R03 | verdadeira | — | `python3 -I checks/records.py R03` |
| R04 | falsa | `parse_kv('a=1;flag') excecao ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 -I checks/records.py R04` |
| R05 | verdadeira | — | `python3 -I checks/records.py R05` |
| R06 | falsa | `d={'a': ';'}: to_kv='a=;', parse_kv(to_kv(d))={'a': ''}` | `python3 -I checks/records.py R06` |
| R07 | verdadeira | — | `python3 -I checks/records.py R07` |
| R08 | verdadeira | — | `python3 -I checks/records.py R08` |
| R09 | verdadeira | — | `python3 -I checks/records.py R09` |
| R10 | falsa | `rename({'a': 1, 'b': 2},{'a': 'b'}) -> {'b': 2} (len 1 != 2)` | `python3 -I checks/records.py R10` |
| R11 | verdadeira | — | `python3 -I checks/records.py R11` |
| R12 | verdadeira | — | `python3 -I checks/records.py R12` |
| R13 | verdadeira | — | `python3 -I checks/records.py R13` |
| R14 | falsa | `sort_by([{'x': 1}, {'n': 1}],'n') excecao KeyError: 'n'` | `python3 -I checks/records.py R14` |
| R15 | verdadeira | — | `python3 -I checks/records.py R15` |
| R16 | verdadeira | — | `python3 -I checks/records.py R16` |
| R17 | falsa | `deep_get({'a':[1,2]},'a.0') -> None, esperado 1` | `python3 -I checks/records.py R17` |
| R18 | verdadeira | — | `python3 -I checks/records.py R18` |
| R19 | verdadeira | — | `python3 -I checks/records.py R19` |
