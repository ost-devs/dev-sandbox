# Relatório de verificação de claims.md


Total: 152 — verdadeiras 113, falsas 39, sem checagem 0.

Reproduzir tudo: `python3 checks/check_<modulo>.py` (a partir da raiz; semente fixa em `checks/lib.py`). Um id isolado: `python3 checks/check_<modulo>.py ID`. Regenerar este relatório: `python3 checks/make_report.py`.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | ` got 'caf-noir', expected 'cafe-noir'` | `python3 checks/check_text.py T01` |
| T02 | verdadeira |  | `python3 checks/check_text.py T02` |
| T03 | verdadeira |  | `python3 checks/check_text.py T03` |
| T04 | verdadeira |  | `python3 checks/check_text.py T04` |
| T05 | falsa | `args=('loYh7fg2CJQ', 2)` | `python3 checks/check_text.py T05` |
| T06 | verdadeira |  | `python3 checks/check_text.py T06` |
| T07 | verdadeira |  | `python3 checks/check_text.py T07` |
| T08 | verdadeira |  | `python3 checks/check_text.py T08` |
| T09 | verdadeira |  | `python3 checks/check_text.py T09` |
| T10 | verdadeira |  | `python3 checks/check_text.py T10` |
| T11 | verdadeira |  | `python3 checks/check_text.py T11` |
| T12 | falsa | `args=('ßßßéA-',)` | `python3 checks/check_text.py T12` |
| T13 | verdadeira |  | `python3 checks/check_text.py T13` |
| T14 | falsa | ` got 'ø', expected 'o'` | `python3 checks/check_text.py T14` |
| T15 | verdadeira |  | `python3 checks/check_text.py T15` |
| T16 | verdadeira |  | `python3 checks/check_text.py T16` |
| T17 | verdadeira |  | `python3 checks/check_text.py T17` |
| T18 | verdadeira |  | `python3 checks/check_text.py T18` |
| T19 | verdadeira |  | `python3 checks/check_text.py T19` |
| N01 | verdadeira |  | `python3 checks/check_numbers.py N01` |
| N02 | falsa | ` got 10, expected 0` | `python3 checks/check_numbers.py N02` |
| N03 | verdadeira |  | `python3 checks/check_numbers.py N03` |
| N04 | verdadeira |  | `python3 checks/check_numbers.py N04` |
| N05 | verdadeira |  | `python3 checks/check_numbers.py N05` |
| N06 | falsa | ` got 'raised IndexError: list index out of range', expected None` | `python3 checks/check_numbers.py N06` |
| N07 | verdadeira |  | `python3 checks/check_numbers.py N07` |
| N08 | falsa | ` got 2, expected 3` | `python3 checks/check_numbers.py N08` |
| N09 | verdadeira |  | `python3 checks/check_numbers.py N09` |
| N10 | verdadeira |  | `python3 checks/check_numbers.py N10` |
| N11 | falsa | `args=(0.0,) raised ZeroDivisionError: float division by zero` | `python3 checks/check_numbers.py N11` |
| N12 | falsa | `args=(4,)` | `python3 checks/check_numbers.py N12` |
| N13 | verdadeira |  | `python3 checks/check_numbers.py N13` |
| N14 | verdadeira |  | `python3 checks/check_numbers.py N14` |
| N15 | falsa | `args=(-50, 1)` | `python3 checks/check_numbers.py N15` |
| N16 | verdadeira |  | `python3 checks/check_numbers.py N16` |
| N17 | verdadeira |  | `python3 checks/check_numbers.py N17` |
| N18 | verdadeira |  | `python3 checks/check_numbers.py N18` |
| N19 | falsa | `args=(-20,) raised ValueError: invalid literal for int() with base 10: '-'` | `python3 checks/check_numbers.py N19` |
| D01 | verdadeira |  | `python3 checks/check_dates.py D01` |
| D02 | falsa | `x=2000-02-29 got 2001-02-28` | `python3 checks/check_dates.py D02` |
| D03 | falsa | `x=2000-01-30 got 2000-01-29` | `python3 checks/check_dates.py D03` |
| D04 | falsa | `days_between(2024-01-02, 2024-01-01) = -1` | `python3 checks/check_dates.py D04` |
| D05 | verdadeira |  | `python3 checks/check_dates.py D05` |
| D06 | verdadeira |  | `python3 checks/check_dates.py D06` |
| D07 | verdadeira |  | `python3 checks/check_dates.py D07` |
| D08 | verdadeira |  | `python3 checks/check_dates.py D08` |
| D09 | verdadeira |  | `python3 checks/check_dates.py D09` |
| D10 | verdadeira |  | `python3 checks/check_dates.py D10` |
| D11 | verdadeira |  | `python3 checks/check_dates.py D11` |
| D12 | verdadeira |  | `python3 checks/check_dates.py D12` |
| D13 | verdadeira |  | `python3 checks/check_dates.py D13` |
| D14 | falsa | ` got 53, expected 1` | `python3 checks/check_dates.py D14` |
| D15 | verdadeira |  | `python3 checks/check_dates.py D15` |
| D16 | falsa | `parse_br('1/2/2024') returned datetime.date(2024, 2, 1) without ValueError` | `python3 checks/check_dates.py D16` |
| D17 | verdadeira |  | `python3 checks/check_dates.py D17` |
| D18 | verdadeira |  | `python3 checks/check_dates.py D18` |
| D19 | verdadeira |  | `python3 checks/check_dates.py D19` |
| L01 | verdadeira |  | `python3 checks/check_lists.py L01` |
| L02 | verdadeira |  | `python3 checks/check_lists.py L02` |
| L03 | verdadeira |  | `python3 checks/check_lists.py L03` |
| L04 | verdadeira |  | `python3 checks/check_lists.py L04` |
| L05 | verdadeira |  | `python3 checks/check_lists.py L05` |
| L06 | verdadeira |  | `python3 checks/check_lists.py L06` |
| L07 | falsa | ` got [1, [2], 3], expected [1, 2, 3]` | `python3 checks/check_lists.py L07` |
| L08 | verdadeira |  | `python3 checks/check_lists.py L08` |
| L09 | verdadeira |  | `python3 checks/check_lists.py L09` |
| L10 | falsa | ` got [3, 2], expected []` | `python3 checks/check_lists.py L10` |
| L11 | verdadeira |  | `python3 checks/check_lists.py L11` |
| L12 | falsa | `args=([-15, -12, 19, -20, 2, -19, 11], 12)` | `python3 checks/check_lists.py L12` |
| L13 | verdadeira |  | `python3 checks/check_lists.py L13` |
| L14 | falsa | ` got [1, 9], expected [1, 9, 2, 3]` | `python3 checks/check_lists.py L14` |
| L15 | verdadeira |  | `python3 checks/check_lists.py L15` |
| L16 | verdadeira |  | `python3 checks/check_lists.py L16` |
| L17 | verdadeira |  | `python3 checks/check_lists.py L17` |
| L18 | verdadeira |  | `python3 checks/check_lists.py L18` |
| L19 | falsa | `args=([],)` | `python3 checks/check_lists.py L19` |
| M01 | verdadeira |  | `python3 checks/check_money.py M01` |
| M02 | verdadeira |  | `python3 checks/check_money.py M02` |
| M03 | falsa | ` got -50, expected -150` | `python3 checks/check_money.py M03` |
| M04 | verdadeira |  | `python3 checks/check_money.py M04` |
| M05 | verdadeira |  | `python3 checks/check_money.py M05` |
| M06 | verdadeira |  | `python3 checks/check_money.py M06` |
| M07 | falsa | ` got 'R$ -2,50', expected 'R$ -1,50'` | `python3 checks/check_money.py M07` |
| M08 | verdadeira |  | `python3 checks/check_money.py M08` |
| M09 | falsa | `split_bill(1,2)=[0, 0] sums to 0` | `python3 checks/check_money.py M09` |
| M10 | verdadeira |  | `python3 checks/check_money.py M10` |
| M11 | verdadeira |  | `python3 checks/check_money.py M11` |
| M12 | verdadeira |  | `python3 checks/check_money.py M12` |
| M13 | verdadeira |  | `python3 checks/check_money.py M13` |
| M14 | verdadeira |  | `python3 checks/check_money.py M14` |
| M15 | verdadeira |  | `python3 checks/check_money.py M15` |
| M16 | verdadeira |  | `python3 checks/check_money.py M16` |
| M17 | falsa | ` got 114, expected 115` | `python3 checks/check_money.py M17` |
| M18 | verdadeira |  | `python3 checks/check_money.py M18` |
| M19 | verdadeira |  | `python3 checks/check_money.py M19` |
| I01 | verdadeira |  | `python3 checks/check_intervals.py I01` |
| I02 | verdadeira |  | `python3 checks/check_intervals.py I02` |
| I03 | verdadeira |  | `python3 checks/check_intervals.py I03` |
| I04 | verdadeira |  | `python3 checks/check_intervals.py I04` |
| I05 | verdadeira |  | `python3 checks/check_intervals.py I05` |
| I06 | verdadeira |  | `python3 checks/check_intervals.py I06` |
| I07 | falsa | ` got True, expected False` | `python3 checks/check_intervals.py I07` |
| I08 | verdadeira |  | `python3 checks/check_intervals.py I08` |
| I09 | verdadeira |  | `python3 checks/check_intervals.py I09` |
| I10 | verdadeira |  | `python3 checks/check_intervals.py I10` |
| I11 | verdadeira |  | `python3 checks/check_intervals.py I11` |
| I12 | verdadeira |  | `python3 checks/check_intervals.py I12` |
| I13 | verdadeira |  | `python3 checks/check_intervals.py I13` |
| I14 | verdadeira |  | `python3 checks/check_intervals.py I14` |
| I15 | falsa | `raised IndexError: list index out of range` | `python3 checks/check_intervals.py I15` |
| I16 | verdadeira |  | `python3 checks/check_intervals.py I16` |
| I17 | verdadeira |  | `python3 checks/check_intervals.py I17` |
| I18 | falsa | `args=((-6, -4), -4)` | `python3 checks/check_intervals.py I18` |
| I19 | falsa | ` got -2, expected 0` | `python3 checks/check_intervals.py I19` |
| P01 | verdadeira |  | `python3 checks/check_paths.py P01` |
| P02 | falsa | ` got 'usr/bin', expected '/usr/bin'` | `python3 checks/check_paths.py P02` |
| P03 | verdadeira |  | `python3 checks/check_paths.py P03` |
| P04 | verdadeira |  | `python3 checks/check_paths.py P04` |
| P05 | falsa | ` got 'd/arquivo', expected ''` | `python3 checks/check_paths.py P05` |
| P06 | falsa | ` got 'bashrc', expected ''` | `python3 checks/check_paths.py P06` |
| P07 | verdadeira |  | `python3 checks/check_paths.py P07` |
| P08 | verdadeira |  | `python3 checks/check_paths.py P08` |
| P09 | verdadeira |  | `python3 checks/check_paths.py P09` |
| P10 | falsa | ` got 'x', expected '../x'` | `python3 checks/check_paths.py P10` |
| P11 | verdadeira |  | `python3 checks/check_paths.py P11` |
| P12 | verdadeira |  | `python3 checks/check_paths.py P12` |
| P13 | verdadeira |  | `python3 checks/check_paths.py P13` |
| P14 | verdadeira |  | `python3 checks/check_paths.py P14` |
| P15 | verdadeira |  | `python3 checks/check_paths.py P15` |
| P16 | verdadeira |  | `python3 checks/check_paths.py P16` |
| P17 | falsa | ` got '', expected '/'` | `python3 checks/check_paths.py P17` |
| P18 | verdadeira |  | `python3 checks/check_paths.py P18` |
| P19 | verdadeira |  | `python3 checks/check_paths.py P19` |
| R01 | verdadeira |  | `python3 checks/check_records.py R01` |
| R02 | verdadeira |  | `python3 checks/check_records.py R02` |
| R03 | verdadeira |  | `python3 checks/check_records.py R03` |
| R04 | falsa | `raised ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/check_records.py R04` |
| R05 | verdadeira |  | `python3 checks/check_records.py R05` |
| R06 | falsa | `args=({'': ';', 'bb': '1=a'},)` | `python3 checks/check_records.py R06` |
| R07 | verdadeira |  | `python3 checks/check_records.py R07` |
| R08 | verdadeira |  | `python3 checks/check_records.py R08` |
| R09 | verdadeira |  | `python3 checks/check_records.py R09` |
| R10 | falsa | `args=({'a': 1, 'b': 2}, {'a': 'b'})` | `python3 checks/check_records.py R10` |
| R11 | verdadeira |  | `python3 checks/check_records.py R11` |
| R12 | verdadeira |  | `python3 checks/check_records.py R12` |
| R13 | verdadeira |  | `python3 checks/check_records.py R13` |
| R14 | falsa | `raised KeyError: 'n'` | `python3 checks/check_records.py R14` |
| R15 | verdadeira |  | `python3 checks/check_records.py R15` |
| R16 | verdadeira |  | `python3 checks/check_records.py R16` |
| R17 | falsa | ` got None, expected 1` | `python3 checks/check_records.py R17` |
| R18 | verdadeira |  | `python3 checks/check_records.py R18` |
| R19 | verdadeira |  | `python3 checks/check_records.py R19` |
