# Relatório de verificação de claims.md

152 afirmações: 113 verdadeiras, 39 falsas. Entradas fixas ou geradas com semente registrada (`SEED` em `checks/common.py`). Rode a partir da raiz do projeto; sem argumento, `python3 checks/<módulo>/check_<módulo>.py` roda o módulo inteiro.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `got 'caf-noir', claim says 'cafe-noir'` | `python3 checks/text/check_text.py T01` |
| T02 | verdadeira |  | `python3 checks/text/check_text.py T02` |
| T03 | verdadeira |  | `python3 checks/text/check_text.py T03` |
| T04 | verdadeira |  | `python3 checks/text/check_text.py T04` |
| T05 | falsa | `args=('a', 0) -> '...'` | `python3 checks/text/check_text.py T05` |
| T06 | verdadeira |  | `python3 checks/text/check_text.py T06` |
| T07 | verdadeira |  | `python3 checks/text/check_text.py T07` |
| T08 | verdadeira |  | `python3 checks/text/check_text.py T08` |
| T09 | verdadeira |  | `python3 checks/text/check_text.py T09` |
| T10 | verdadeira |  | `python3 checks/text/check_text.py T10` |
| T11 | verdadeira |  | `python3 checks/text/check_text.py T11` |
| T12 | falsa | `args=('ß',) -> 'SS'` | `python3 checks/text/check_text.py T12` |
| T13 | verdadeira |  | `python3 checks/text/check_text.py T13` |
| T14 | falsa | `got 'ø', claim says 'o'` | `python3 checks/text/check_text.py T14` |
| T15 | verdadeira |  | `python3 checks/text/check_text.py T15` |
| T16 | verdadeira |  | `python3 checks/text/check_text.py T16` |
| T17 | verdadeira |  | `python3 checks/text/check_text.py T17` |
| T18 | verdadeira |  | `python3 checks/text/check_text.py T18` |
| T19 | verdadeira |  | `python3 checks/text/check_text.py T19` |
| N01 | verdadeira |  | `python3 checks/numbers/check_numbers.py N01` |
| N02 | falsa | `got 10, claim says 0` | `python3 checks/numbers/check_numbers.py N02` |
| N03 | verdadeira |  | `python3 checks/numbers/check_numbers.py N03` |
| N04 | verdadeira |  | `python3 checks/numbers/check_numbers.py N04` |
| N05 | verdadeira |  | `python3 checks/numbers/check_numbers.py N05` |
| N06 | falsa | `raised IndexError: list index out of range` | `python3 checks/numbers/check_numbers.py N06` |
| N07 | verdadeira |  | `python3 checks/numbers/check_numbers.py N07` |
| N08 | falsa | `got 2, claim says 3` | `python3 checks/numbers/check_numbers.py N08` |
| N09 | verdadeira |  | `python3 checks/numbers/check_numbers.py N09` |
| N10 | verdadeira |  | `python3 checks/numbers/check_numbers.py N10` |
| N11 | falsa | `percent(0, 0) raised ZeroDivisionError: division by zero` | `python3 checks/numbers/check_numbers.py N11` |
| N12 | falsa | `is_prime(4) -> True, expected False` | `python3 checks/numbers/check_numbers.py N12` |
| N13 | verdadeira |  | `python3 checks/numbers/check_numbers.py N13` |
| N14 | verdadeira |  | `python3 checks/numbers/check_numbers.py N14` |
| N15 | falsa | `a=-50, b=1: 1 vs -1` | `python3 checks/numbers/check_numbers.py N15` |
| N16 | verdadeira |  | `python3 checks/numbers/check_numbers.py N16` |
| N17 | verdadeira |  | `python3 checks/numbers/check_numbers.py N17` |
| N18 | verdadeira |  | `python3 checks/numbers/check_numbers.py N18` |
| N19 | falsa | `digits_sum(-1) raised ValueError: invalid literal for int() with base 10: '-'` | `python3 checks/numbers/check_numbers.py N19` |
| D01 | verdadeira |  | `python3 checks/dates/check_dates.py D01` |
| D02 | falsa | `x=datetime.date(2000, 2, 29)` | `python3 checks/dates/check_dates.py D02` |
| D03 | falsa | `x=datetime.date(2000, 1, 30)` | `python3 checks/dates/check_dates.py D03` |
| D04 | falsa | `args=(datetime.date(7264, 5, 27), datetime.date(3110, 2, 21))` | `python3 checks/dates/check_dates.py D04` |
| D05 | verdadeira |  | `python3 checks/dates/check_dates.py D05` |
| D06 | verdadeira |  | `python3 checks/dates/check_dates.py D06` |
| D07 | verdadeira |  | `python3 checks/dates/check_dates.py D07` |
| D08 | verdadeira |  | `python3 checks/dates/check_dates.py D08` |
| D09 | verdadeira |  | `python3 checks/dates/check_dates.py D09` |
| D10 | verdadeira |  | `python3 checks/dates/check_dates.py D10` |
| D11 | verdadeira |  | `python3 checks/dates/check_dates.py D11` |
| D12 | verdadeira |  | `python3 checks/dates/check_dates.py D12` |
| D13 | verdadeira |  | `python3 checks/dates/check_dates.py D13` |
| D14 | falsa | `got 53, claim says 1` | `python3 checks/dates/check_dates.py D14` |
| D15 | verdadeira |  | `python3 checks/dates/check_dates.py D15` |
| D16 | falsa | `parse_br('1/2/2024') returned datetime.date(2024, 2, 1), no ValueError` | `python3 checks/dates/check_dates.py D16` |
| D17 | verdadeira |  | `python3 checks/dates/check_dates.py D17` |
| D18 | verdadeira |  | `python3 checks/dates/check_dates.py D18` |
| D19 | verdadeira |  | `python3 checks/dates/check_dates.py D19` |
| L01 | verdadeira |  | `python3 checks/lists/check_lists.py L01` |
| L02 | verdadeira |  | `python3 checks/lists/check_lists.py L02` |
| L03 | verdadeira |  | `python3 checks/lists/check_lists.py L03` |
| L04 | verdadeira |  | `python3 checks/lists/check_lists.py L04` |
| L05 | verdadeira |  | `python3 checks/lists/check_lists.py L05` |
| L06 | verdadeira |  | `python3 checks/lists/check_lists.py L06` |
| L07 | falsa | `got [1, [2], 3], claim says [1, 2, 3]` | `python3 checks/lists/check_lists.py L07` |
| L08 | verdadeira |  | `python3 checks/lists/check_lists.py L08` |
| L09 | verdadeira |  | `python3 checks/lists/check_lists.py L09` |
| L10 | falsa | `got [3, 2], claim says []` | `python3 checks/lists/check_lists.py L10` |
| L11 | verdadeira |  | `python3 checks/lists/check_lists.py L11` |
| L12 | falsa | `args=([1, 2], 3) -> [1, 2] vs [2, 1]` | `python3 checks/lists/check_lists.py L12` |
| L13 | verdadeira |  | `python3 checks/lists/check_lists.py L13` |
| L14 | falsa | `got [1, 9], claim says [1, 9, 2, 3]` | `python3 checks/lists/check_lists.py L14` |
| L15 | verdadeira |  | `python3 checks/lists/check_lists.py L15` |
| L16 | verdadeira |  | `python3 checks/lists/check_lists.py L16` |
| L17 | verdadeira |  | `python3 checks/lists/check_lists.py L17` |
| L18 | verdadeira |  | `python3 checks/lists/check_lists.py L18` |
| L19 | falsa | `args=([],)` | `python3 checks/lists/check_lists.py L19` |
| M01 | verdadeira |  | `python3 checks/money/check_money.py M01` |
| M02 | verdadeira |  | `python3 checks/money/check_money.py M02` |
| M03 | falsa | `got -50, claim says -150` | `python3 checks/money/check_money.py M03` |
| M04 | verdadeira |  | `python3 checks/money/check_money.py M04` |
| M05 | verdadeira |  | `python3 checks/money/check_money.py M05` |
| M06 | verdadeira |  | `python3 checks/money/check_money.py M06` |
| M07 | falsa | `got 'R$ -2,50', claim says 'R$ -1,50'` | `python3 checks/money/check_money.py M07` |
| M08 | verdadeira |  | `python3 checks/money/check_money.py M08` |
| M09 | falsa | `args=(5, 29)` | `python3 checks/money/check_money.py M09` |
| M10 | verdadeira |  | `python3 checks/money/check_money.py M10` |
| M11 | verdadeira |  | `python3 checks/money/check_money.py M11` |
| M12 | verdadeira |  | `python3 checks/money/check_money.py M12` |
| M13 | verdadeira |  | `python3 checks/money/check_money.py M13` |
| M14 | verdadeira |  | `python3 checks/money/check_money.py M14` |
| M15 | verdadeira |  | `python3 checks/money/check_money.py M15` |
| M16 | verdadeira |  | `python3 checks/money/check_money.py M16` |
| M17 | falsa | `got 114, claim says 115` | `python3 checks/money/check_money.py M17` |
| M18 | verdadeira |  | `python3 checks/money/check_money.py M18` |
| M19 | verdadeira |  | `python3 checks/money/check_money.py M19` |
| I01 | verdadeira |  | `python3 checks/intervals/check_intervals.py I01` |
| I02 | verdadeira |  | `python3 checks/intervals/check_intervals.py I02` |
| I03 | verdadeira |  | `python3 checks/intervals/check_intervals.py I03` |
| I04 | verdadeira |  | `python3 checks/intervals/check_intervals.py I04` |
| I05 | verdadeira |  | `python3 checks/intervals/check_intervals.py I05` |
| I06 | verdadeira |  | `python3 checks/intervals/check_intervals.py I06` |
| I07 | falsa | `got True, claim says False` | `python3 checks/intervals/check_intervals.py I07` |
| I08 | verdadeira |  | `python3 checks/intervals/check_intervals.py I08` |
| I09 | verdadeira |  | `python3 checks/intervals/check_intervals.py I09` |
| I10 | verdadeira |  | `python3 checks/intervals/check_intervals.py I10` |
| I11 | verdadeira |  | `python3 checks/intervals/check_intervals.py I11` |
| I12 | verdadeira |  | `python3 checks/intervals/check_intervals.py I12` |
| I13 | verdadeira |  | `python3 checks/intervals/check_intervals.py I13` |
| I14 | verdadeira |  | `python3 checks/intervals/check_intervals.py I14` |
| I15 | falsa | `raised IndexError: list index out of range` | `python3 checks/intervals/check_intervals.py I15` |
| I16 | verdadeira |  | `python3 checks/intervals/check_intervals.py I16` |
| I17 | verdadeira |  | `python3 checks/intervals/check_intervals.py I17` |
| I18 | falsa | `args=((-6, 17), 17)` | `python3 checks/intervals/check_intervals.py I18` |
| I19 | falsa | `got -2, claim says 0` | `python3 checks/intervals/check_intervals.py I19` |
| P01 | verdadeira |  | `python3 checks/paths/check_paths.py P01` |
| P02 | falsa | `got 'usr/bin', claim says '/usr/bin'` | `python3 checks/paths/check_paths.py P02` |
| P03 | verdadeira |  | `python3 checks/paths/check_paths.py P03` |
| P04 | verdadeira |  | `python3 checks/paths/check_paths.py P04` |
| P05 | falsa | `got 'd/arquivo', claim says ''` | `python3 checks/paths/check_paths.py P05` |
| P06 | falsa | `got 'bashrc', claim says ''` | `python3 checks/paths/check_paths.py P06` |
| P07 | verdadeira |  | `python3 checks/paths/check_paths.py P07` |
| P08 | verdadeira |  | `python3 checks/paths/check_paths.py P08` |
| P09 | verdadeira |  | `python3 checks/paths/check_paths.py P09` |
| P10 | falsa | `got 'x', claim says '../x'` | `python3 checks/paths/check_paths.py P10` |
| P11 | verdadeira |  | `python3 checks/paths/check_paths.py P11` |
| P12 | verdadeira |  | `python3 checks/paths/check_paths.py P12` |
| P13 | verdadeira |  | `python3 checks/paths/check_paths.py P13` |
| P14 | verdadeira |  | `python3 checks/paths/check_paths.py P14` |
| P15 | verdadeira |  | `python3 checks/paths/check_paths.py P15` |
| P16 | verdadeira |  | `python3 checks/paths/check_paths.py P16` |
| P17 | falsa | `got '', claim says '/'` | `python3 checks/paths/check_paths.py P17` |
| P18 | verdadeira |  | `python3 checks/paths/check_paths.py P18` |
| P19 | verdadeira |  | `python3 checks/paths/check_paths.py P19` |
| R01 | verdadeira |  | `python3 checks/records/check_records.py R01` |
| R02 | verdadeira |  | `python3 checks/records/check_records.py R02` |
| R03 | verdadeira |  | `python3 checks/records/check_records.py R03` |
| R04 | falsa | `raised ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/records/check_records.py R04` |
| R05 | verdadeira |  | `python3 checks/records/check_records.py R05` |
| R06 | falsa | `d={'a': 'b;c'}: raised ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/records/check_records.py R06` |
| R07 | verdadeira |  | `python3 checks/records/check_records.py R07` |
| R08 | verdadeira |  | `python3 checks/records/check_records.py R08` |
| R09 | verdadeira |  | `python3 checks/records/check_records.py R09` |
| R10 | falsa | `got 1, claim says 2` | `python3 checks/records/check_records.py R10` |
| R11 | verdadeira |  | `python3 checks/records/check_records.py R11` |
| R12 | verdadeira |  | `python3 checks/records/check_records.py R12` |
| R13 | verdadeira |  | `python3 checks/records/check_records.py R13` |
| R14 | falsa | `rows=[{'x':1},{'n':1}]: raised KeyError: 'n'` | `python3 checks/records/check_records.py R14` |
| R15 | verdadeira |  | `python3 checks/records/check_records.py R15` |
| R16 | verdadeira |  | `python3 checks/records/check_records.py R16` |
| R17 | falsa | `got None, claim says 1` | `python3 checks/records/check_records.py R17` |
| R18 | verdadeira |  | `python3 checks/records/check_records.py R18` |
| R19 | verdadeira |  | `python3 checks/records/check_records.py R19` |
