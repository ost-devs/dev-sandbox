# Relatório de verificação de claims.md

Total: 152 afirmações — 113 verdadeiras, 39 falsas.

Reprodução: cada comando roda do diretório raiz, é determinístico (sem dependências, semente fixa em `checks/_common.py`) e imprime JSON com o veredito de todos os ids do módulo. `python3 checks/build_report.py` regenera este relatório.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `'caf-noir'` | `python3 checks/check_text.py` (linha `T01`) |
| T02 | verdadeira |  | `python3 checks/check_text.py` (linha `T02`) |
| T03 | verdadeira |  | `python3 checks/check_text.py` (linha `T03`) |
| T04 | verdadeira |  | `python3 checks/check_text.py` (linha `T04`) |
| T05 | falsa | `('a', 0)` | `python3 checks/check_text.py` (linha `T05`) |
| T06 | verdadeira |  | `python3 checks/check_text.py` (linha `T06`) |
| T07 | verdadeira |  | `python3 checks/check_text.py` (linha `T07`) |
| T08 | verdadeira |  | `python3 checks/check_text.py` (linha `T08`) |
| T09 | verdadeira |  | `python3 checks/check_text.py` (linha `T09`) |
| T10 | verdadeira |  | `python3 checks/check_text.py` (linha `T10`) |
| T11 | verdadeira |  | `python3 checks/check_text.py` (linha `T11`) |
| T12 | falsa | `'ß'` | `python3 checks/check_text.py` (linha `T12`) |
| T13 | verdadeira |  | `python3 checks/check_text.py` (linha `T13`) |
| T14 | falsa | `'ø'` | `python3 checks/check_text.py` (linha `T14`) |
| T15 | verdadeira |  | `python3 checks/check_text.py` (linha `T15`) |
| T16 | verdadeira |  | `python3 checks/check_text.py` (linha `T16`) |
| T17 | verdadeira |  | `python3 checks/check_text.py` (linha `T17`) |
| T18 | verdadeira |  | `python3 checks/check_text.py` (linha `T18`) |
| T19 | verdadeira |  | `python3 checks/check_text.py` (linha `T19`) |
| N01 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N01`) |
| N02 | falsa | `'got 10'` | `python3 checks/check_numbers.py` (linha `N02`) |
| N03 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N03`) |
| N04 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N04`) |
| N05 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N05`) |
| N06 | falsa | `'raised IndexError: list index out of range'` | `python3 checks/check_numbers.py` (linha `N06`) |
| N07 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N07`) |
| N08 | falsa | `'got 2'` | `python3 checks/check_numbers.py` (linha `N08`) |
| N09 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N09`) |
| N10 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N10`) |
| N11 | falsa | `'raised ZeroDivisionError: division by zero'` | `python3 checks/check_numbers.py` (linha `N11`) |
| N12 | falsa | `(4, True)` | `python3 checks/check_numbers.py` (linha `N12`) |
| N13 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N13`) |
| N14 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N14`) |
| N15 | falsa | `(-50, 1, 1, -1)` | `python3 checks/check_numbers.py` (linha `N15`) |
| N16 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N16`) |
| N17 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N17`) |
| N18 | verdadeira |  | `python3 checks/check_numbers.py` (linha `N18`) |
| N19 | falsa | `"raised ValueError: invalid literal for int() with base 10: '-'"` | `python3 checks/check_numbers.py` (linha `N19`) |
| D01 | verdadeira |  | `python3 checks/check_dates.py` (linha `D01`) |
| D02 | falsa | `datetime.date(2000, 2, 29)` | `python3 checks/check_dates.py` (linha `D02`) |
| D03 | falsa | `datetime.date(2000, 1, 30)` | `python3 checks/check_dates.py` (linha `D03`) |
| D04 | falsa | `(datetime.date(2024, 1, 2), datetime.date(2024, 1, 1))` | `python3 checks/check_dates.py` (linha `D04`) |
| D05 | verdadeira |  | `python3 checks/check_dates.py` (linha `D05`) |
| D06 | verdadeira |  | `python3 checks/check_dates.py` (linha `D06`) |
| D07 | verdadeira |  | `python3 checks/check_dates.py` (linha `D07`) |
| D08 | verdadeira |  | `python3 checks/check_dates.py` (linha `D08`) |
| D09 | verdadeira |  | `python3 checks/check_dates.py` (linha `D09`) |
| D10 | verdadeira |  | `python3 checks/check_dates.py` (linha `D10`) |
| D11 | verdadeira |  | `python3 checks/check_dates.py` (linha `D11`) |
| D12 | verdadeira |  | `python3 checks/check_dates.py` (linha `D12`) |
| D13 | verdadeira |  | `python3 checks/check_dates.py` (linha `D13`) |
| D14 | falsa | `53` | `python3 checks/check_dates.py` (linha `D14`) |
| D15 | verdadeira |  | `python3 checks/check_dates.py` (linha `D15`) |
| D16 | falsa | `'1/2/2024 -> datetime.date(2024, 2, 1), no ValueError'` | `python3 checks/check_dates.py` (linha `D16`) |
| D17 | verdadeira |  | `python3 checks/check_dates.py` (linha `D17`) |
| D18 | verdadeira |  | `python3 checks/check_dates.py` (linha `D18`) |
| D19 | verdadeira |  | `python3 checks/check_dates.py` (linha `D19`) |
| L01 | verdadeira |  | `python3 checks/check_lists.py` (linha `L01`) |
| L02 | verdadeira |  | `python3 checks/check_lists.py` (linha `L02`) |
| L03 | verdadeira |  | `python3 checks/check_lists.py` (linha `L03`) |
| L04 | verdadeira |  | `python3 checks/check_lists.py` (linha `L04`) |
| L05 | verdadeira |  | `python3 checks/check_lists.py` (linha `L05`) |
| L06 | verdadeira |  | `python3 checks/check_lists.py` (linha `L06`) |
| L07 | falsa | `[1, [2], 3]` | `python3 checks/check_lists.py` (linha `L07`) |
| L08 | verdadeira |  | `python3 checks/check_lists.py` (linha `L08`) |
| L09 | verdadeira |  | `python3 checks/check_lists.py` (linha `L09`) |
| L10 | falsa | `[3, 2]` | `python3 checks/check_lists.py` (linha `L10`) |
| L11 | verdadeira |  | `python3 checks/check_lists.py` (linha `L11`) |
| L12 | falsa | `([0, 1], 3)` | `python3 checks/check_lists.py` (linha `L12`) |
| L13 | verdadeira |  | `python3 checks/check_lists.py` (linha `L13`) |
| L14 | falsa | `[1, 9]` | `python3 checks/check_lists.py` (linha `L14`) |
| L15 | verdadeira |  | `python3 checks/check_lists.py` (linha `L15`) |
| L16 | verdadeira |  | `python3 checks/check_lists.py` (linha `L16`) |
| L17 | verdadeira |  | `python3 checks/check_lists.py` (linha `L17`) |
| L18 | verdadeira |  | `python3 checks/check_lists.py` (linha `L18`) |
| L19 | falsa | `([],)` | `python3 checks/check_lists.py` (linha `L19`) |
| M01 | verdadeira |  | `python3 checks/check_money.py` (linha `M01`) |
| M02 | verdadeira |  | `python3 checks/check_money.py` (linha `M02`) |
| M03 | falsa | `-50` | `python3 checks/check_money.py` (linha `M03`) |
| M04 | verdadeira |  | `python3 checks/check_money.py` (linha `M04`) |
| M05 | verdadeira |  | `python3 checks/check_money.py` (linha `M05`) |
| M06 | verdadeira |  | `python3 checks/check_money.py` (linha `M06`) |
| M07 | falsa | `'R$ -2,50'` | `python3 checks/check_money.py` (linha `M07`) |
| M08 | verdadeira |  | `python3 checks/check_money.py` (linha `M08`) |
| M09 | falsa | `{'total': 1, 'k': 2, 'got': [0, 0]}` | `python3 checks/check_money.py` (linha `M09`) |
| M10 | verdadeira |  | `python3 checks/check_money.py` (linha `M10`) |
| M11 | verdadeira |  | `python3 checks/check_money.py` (linha `M11`) |
| M12 | verdadeira |  | `python3 checks/check_money.py` (linha `M12`) |
| M13 | verdadeira |  | `python3 checks/check_money.py` (linha `M13`) |
| M14 | verdadeira |  | `python3 checks/check_money.py` (linha `M14`) |
| M15 | verdadeira |  | `python3 checks/check_money.py` (linha `M15`) |
| M16 | verdadeira |  | `python3 checks/check_money.py` (linha `M16`) |
| M17 | falsa | `114` | `python3 checks/check_money.py` (linha `M17`) |
| M18 | verdadeira |  | `python3 checks/check_money.py` (linha `M18`) |
| M19 | verdadeira |  | `python3 checks/check_money.py` (linha `M19`) |
| R01 | verdadeira |  | `python3 checks/check_records.py` (linha `R01`) |
| R02 | verdadeira |  | `python3 checks/check_records.py` (linha `R02`) |
| R03 | verdadeira |  | `python3 checks/check_records.py` (linha `R03`) |
| R04 | falsa | `'raised ValueError: dictionary update sequence element #1 has length 1; 2 is required'` | `python3 checks/check_records.py` (linha `R04`) |
| R05 | verdadeira |  | `python3 checks/check_records.py` (linha `R05`) |
| R06 | falsa | `{'': ';'}` | `python3 checks/check_records.py` (linha `R06`) |
| R07 | verdadeira |  | `python3 checks/check_records.py` (linha `R07`) |
| R08 | verdadeira |  | `python3 checks/check_records.py` (linha `R08`) |
| R09 | verdadeira |  | `python3 checks/check_records.py` (linha `R09`) |
| R10 | falsa | `({'a': 0, 'b': 1}, {'a': 'b'})` | `python3 checks/check_records.py` (linha `R10`) |
| R11 | verdadeira |  | `python3 checks/check_records.py` (linha `R11`) |
| R12 | verdadeira |  | `python3 checks/check_records.py` (linha `R12`) |
| R13 | verdadeira |  | `python3 checks/check_records.py` (linha `R13`) |
| R14 | falsa | `"raised KeyError: 'n'"` | `python3 checks/check_records.py` (linha `R14`) |
| R15 | verdadeira |  | `python3 checks/check_records.py` (linha `R15`) |
| R16 | verdadeira |  | `python3 checks/check_records.py` (linha `R16`) |
| R17 | falsa | `None` | `python3 checks/check_records.py` (linha `R17`) |
| R18 | verdadeira |  | `python3 checks/check_records.py` (linha `R18`) |
| R19 | verdadeira |  | `python3 checks/check_records.py` (linha `R19`) |
| P01 | verdadeira |  | `python3 checks/check_paths.py` (linha `P01`) |
| P02 | falsa | `(('/usr', 'bin'), 'usr/bin')` | `python3 checks/check_paths.py` (linha `P02`) |
| P03 | verdadeira |  | `python3 checks/check_paths.py` (linha `P03`) |
| P04 | verdadeira |  | `python3 checks/check_paths.py` (linha `P04`) |
| P05 | falsa | `(('dir.d/arquivo',), 'd/arquivo')` | `python3 checks/check_paths.py` (linha `P05`) |
| P06 | falsa | `(('.bashrc',), 'bashrc')` | `python3 checks/check_paths.py` (linha `P06`) |
| P07 | verdadeira |  | `python3 checks/check_paths.py` (linha `P07`) |
| P08 | verdadeira |  | `python3 checks/check_paths.py` (linha `P08`) |
| P09 | verdadeira |  | `python3 checks/check_paths.py` (linha `P09`) |
| P10 | falsa | `(('../x',), 'x')` | `python3 checks/check_paths.py` (linha `P10`) |
| P11 | verdadeira |  | `python3 checks/check_paths.py` (linha `P11`) |
| P12 | verdadeira |  | `python3 checks/check_paths.py` (linha `P12`) |
| P13 | verdadeira |  | `python3 checks/check_paths.py` (linha `P13`) |
| P14 | verdadeira |  | `python3 checks/check_paths.py` (linha `P14`) |
| P15 | verdadeira |  | `python3 checks/check_paths.py` (linha `P15`) |
| P16 | verdadeira |  | `python3 checks/check_paths.py` (linha `P16`) |
| P17 | falsa | `(('/a',), '')` | `python3 checks/check_paths.py` (linha `P17`) |
| P18 | verdadeira |  | `python3 checks/check_paths.py` (linha `P18`) |
| P19 | verdadeira |  | `python3 checks/check_paths.py` (linha `P19`) |
| I01 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I01`) |
| I02 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I02`) |
| I03 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I03`) |
| I04 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I04`) |
| I05 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I05`) |
| I06 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I06`) |
| I07 | falsa | `True` | `python3 checks/check_intervals.py` (linha `I07`) |
| I08 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I08`) |
| I09 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I09`) |
| I10 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I10`) |
| I11 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I11`) |
| I12 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I12`) |
| I13 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I13`) |
| I14 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I14`) |
| I15 | falsa | `'raised IndexError: list index out of range'` | `python3 checks/check_intervals.py` (linha `I15`) |
| I16 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I16`) |
| I17 | verdadeira |  | `python3 checks/check_intervals.py` (linha `I17`) |
| I18 | falsa | `((-3, -2), -2)` | `python3 checks/check_intervals.py` (linha `I18`) |
| I19 | falsa | `-2` | `python3 checks/check_intervals.py` (linha `I19`) |
