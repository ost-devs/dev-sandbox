# Relatório de verificação de claims.md

152 afirmações: 113 verdadeiras, 39 falsas.

Tudo reproduzível: `checks/run_all.sh` (ou o comando de cada linha, a partir da raiz). Amostras aleatórias usam semente = crc32 do id (campo seed=). "Verdadeira" em propriedades universais = nenhum contraexemplo em n amostras semeadas.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `got 'caf-noir', expected 'cafe-noir'` | `python3 checks/text/check_text.py` (fixed) |
| T02 | verdadeira |  | `python3 checks/text/check_text.py` (seed=2204448781 n=3000) |
| T03 | verdadeira |  | `python3 checks/text/check_text.py` (seed=4100065435 n=3000) |
| T04 | verdadeira |  | `python3 checks/text/check_text.py` (seed=1778818360 n=3000) |
| T05 | falsa | `args=('Ωã\\.YãİΩc', 2)` | `python3 checks/text/check_text.py` (seed=486649262 n=3000) |
| T06 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T07 | verdadeira |  | `python3 checks/text/check_text.py` (seed=4077898882 n=3000) |
| T08 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T09 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T10 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T11 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T12 | falsa | `args=('ßYøǅ😀Yﬁǅ/',)` | `python3 checks/text/check_text.py` (seed=2591951180 n=3000) |
| T13 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T14 | falsa | `got 'ø', expected 'o'` | `python3 checks/text/check_text.py` (fixed) |
| T15 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T16 | verdadeira |  | `python3 checks/text/check_text.py` (seed=2635320661 n=3000) |
| T17 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T18 | verdadeira |  | `python3 checks/text/check_text.py` (fixed) |
| T19 | verdadeira |  | `python3 checks/text/check_text.py` (seed=229429444 n=3000) |
| D01 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D02 | falsa | `x=2000-02-29` | `python3 checks/dates/check_dates.py` (fixed) |
| D03 | falsa | `x=2000-01-30` | `python3 checks/dates/check_dates.py` (fixed) |
| D04 | falsa | `args=(datetime.date(8157, 6, 14), datetime.date(2364, 7, 9))` | `python3 checks/dates/check_dates.py` (seed=1981824584 n=3000) |
| D05 | verdadeira |  | `python3 checks/dates/check_dates.py` (seed=19336926 n=3000) |
| D06 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D07 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D08 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D09 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D10 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D11 | verdadeira |  | `python3 checks/dates/check_dates.py` (seed=525466502 n=3000) |
| D12 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D13 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D14 | falsa | `iso_week=53` | `python3 checks/dates/check_dates.py` (fixed) |
| D15 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| D16 | falsa | `no ValueError; returned 2024-02-01` | `python3 checks/dates/check_dates.py` (fixed) |
| D17 | verdadeira |  | `python3 checks/dates/check_dates.py` (seed=4130496179 n=3000) |
| D18 | verdadeira |  | `python3 checks/dates/check_dates.py` (seed=1720533794 n=3000) |
| D19 | verdadeira |  | `python3 checks/dates/check_dates.py` (fixed) |
| I01 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I02 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=2543519790 n=3000) |
| I03 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I04 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I05 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=167746957 n=3000) |
| I06 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=2432093239 n=3000) |
| I07 | falsa | `got True, expected False` | `python3 checks/intervals/check_intervals.py` (fixed) |
| I08 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=2001658160 n=3000) |
| I09 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I10 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I11 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I12 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I13 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=4186376697 n=3000) |
| I14 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=1742969946 n=3000) |
| I15 | falsa | `raises IndexError: list index out of range` | `python3 checks/intervals/check_intervals.py` (fixed) |
| I16 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (seed=2314075510 n=3000) |
| I17 | verdadeira |  | `python3 checks/intervals/check_intervals.py` (fixed) |
| I18 | falsa | `args=((-1, 1), 1)` | `python3 checks/intervals/check_intervals.py` (seed=1851117681 n=3000) |
| I19 | falsa | `got -2, expected 0` | `python3 checks/intervals/check_intervals.py` (fixed) |
| L01 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L02 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=2437991109 n=3000) |
| L03 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L04 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L05 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=255090534 n=3000) |
| L06 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=2520583900 n=3000) |
| L07 | falsa | `got [1, [2], 3], expected [1, 2, 3]` | `python3 checks/lists/check_lists.py` (fixed) |
| L08 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L09 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=109187917 n=3000) |
| L10 | falsa | `got [3, 2], expected []` | `python3 checks/lists/check_lists.py` (fixed) |
| L11 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L12 | falsa | `args=([4, -2, 9, 5, 3, -1, 4], 11)` | `python3 checks/lists/check_lists.py` (seed=2286680964 n=3000) |
| L13 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=4283222802 n=3000) |
| L14 | falsa | `got [1, 9], expected [1, 9, 2, 3]` | `python3 checks/lists/check_lists.py` (fixed) |
| L15 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=372207143 n=3000) |
| L16 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L17 | verdadeira |  | `python3 checks/lists/check_lists.py` (seed=4162916107 n=3000) |
| L18 | verdadeira |  | `python3 checks/lists/check_lists.py` (fixed) |
| L19 | falsa | `args=([],)` | `python3 checks/lists/check_lists.py` (seed=530129420 n=3000) |
| M01 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M02 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M03 | falsa | `got -50, expected -150` | `python3 checks/money/check_money.py` (fixed) |
| M04 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M05 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M06 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M07 | falsa | `got 'R$ -2,50', expected 'R$ -1,50'` | `python3 checks/money/check_money.py` (fixed) |
| M08 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M09 | falsa | `args=(4255, 11)` | `python3 checks/money/check_money.py` (seed=121665914 n=3000) |
| M10 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M11 | verdadeira |  | `python3 checks/money/check_money.py` (seed=276873225 n=3000) |
| M12 | verdadeira |  | `python3 checks/money/check_money.py` (seed=2307494323 n=3000) |
| M13 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M14 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M15 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M16 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M17 | falsa | `got 114, expected 115` | `python3 checks/money/check_money.py` (fixed) |
| M18 | verdadeira |  | `python3 checks/money/check_money.py` (fixed) |
| M19 | verdadeira |  | `python3 checks/money/check_money.py` (seed=509298747 n=3000) |
| N01 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (seed=199053073 n=3000) |
| N02 | falsa | `got 10` | `python3 checks/numbers/check_numbers.py` (fixed) |
| N03 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N04 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N05 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N06 | falsa | `raises IndexError: list index out of range` | `python3 checks/numbers/check_numbers.py` (fixed) |
| N07 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (seed=3804162596 n=3000) |
| N08 | falsa | `got 2` | `python3 checks/numbers/check_numbers.py` (fixed) |
| N09 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N10 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N11 | falsa | `args=(0,) raises ZeroDivisionError: division by zero` | `python3 checks/numbers/check_numbers.py` (seed=314998352 n=3000) |
| N12 | falsa | `wrong for [4, 6, 8, 9, 15, 25, 35, 49, 121, 143]` | `python3 checks/numbers/check_numbers.py` (fixed) |
| N13 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N14 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N15 | falsa | `a=-50 b=1: 1 vs -1` | `python3 checks/numbers/check_numbers.py` (fixed) |
| N16 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N17 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (seed=4221950821 n=3000) |
| N18 | verdadeira |  | `python3 checks/numbers/check_numbers.py` (fixed) |
| N19 | falsa | `args=(-883,) raises ValueError: invalid literal for int() with base 10: '-'` | `python3 checks/numbers/check_numbers.py` (seed=471725666 n=3000) |
| P01 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P02 | falsa | `got 'usr/bin', expected '/usr/bin'` | `python3 checks/paths/check_paths.py` (fixed) |
| P03 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P04 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P05 | falsa | `got 'd/arquivo', expected ''` | `python3 checks/paths/check_paths.py` (fixed) |
| P06 | falsa | `got 'bashrc', expected ''` | `python3 checks/paths/check_paths.py` (fixed) |
| P07 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P08 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P09 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P10 | falsa | `got 'x', expected '../x'` | `python3 checks/paths/check_paths.py` (fixed) |
| P11 | verdadeira |  | `python3 checks/paths/check_paths.py` (seed=75427882 n=3000) |
| P12 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P13 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P14 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P15 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P16 | verdadeira |  | `python3 checks/paths/check_paths.py` (fixed) |
| P17 | falsa | `got '', expected '/'` | `python3 checks/paths/check_paths.py` (fixed) |
| P18 | verdadeira |  | `python3 checks/paths/check_paths.py` (seed=2107787406 n=3000) |
| P19 | verdadeira |  | `python3 checks/paths/check_paths.py` (seed=178616344 n=3000) |
| R01 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R02 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R03 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R04 | falsa | `raises ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/records/check_records.py` (fixed) |
| R05 | verdadeira |  | `python3 checks/records/check_records.py` (seed=428658972 n=3000) |
| R06 | falsa | `args=({'  =a': ' a a'},)` | `python3 checks/records/check_records.py` (seed=2156232870 n=3000) |
| R07 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R08 | verdadeira |  | `python3 checks/records/check_records.py` (seed=1732095393 n=3000) |
| R09 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R10 | falsa | `args=({'b': 1, 'd': 1, 'a': 1}, {'d': 'a', 'c': 'd', 'e': 'c'})` | `python3 checks/records/check_records.py` (seed=1895634130 n=3000) |
| R11 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R12 | verdadeira |  | `python3 checks/records/check_records.py` (seed=2666755582 n=3000) |
| R13 | verdadeira |  | `python3 checks/records/check_records.py` (seed=3925099880 n=3000) |
| R14 | falsa | `raises KeyError: 'n'` | `python3 checks/records/check_records.py` (fixed) |
| R15 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R16 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
| R17 | falsa | `got None, expected 1` | `python3 checks/records/check_records.py` (fixed) |
| R18 | verdadeira |  | `python3 checks/records/check_records.py` (seed=2116459744 n=3000) |
| R19 | verdadeira |  | `python3 checks/records/check_records.py` (fixed) |
