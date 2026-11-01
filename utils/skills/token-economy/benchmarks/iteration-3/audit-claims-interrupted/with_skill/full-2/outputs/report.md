# Relatório de verificação de claims.md

152 afirmações: 113 verdadeiras, 39 falsas. Semente: 20261101 (checks/lib.py). Cada comando roda da raiz do projeto, é determinístico e regrava `checks/<módulo>/results.json`. `python3 checks/make_report.py` regenera este relatório.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `assertion failed: got 'caf-noir', expected 'cafe-noir'` | `python3 checks/text/check_text.py` |
| T02 | verdadeira |  | `python3 checks/text/check_text.py` |
| T03 | verdadeira |  | `python3 checks/text/check_text.py` |
| T04 | verdadeira |  | `python3 checks/text/check_text.py` |
| T05 | falsa | `args=('CzpXbh', 0)` | `python3 checks/text/check_text.py` |
| T06 | verdadeira |  | `python3 checks/text/check_text.py` |
| T07 | verdadeira |  | `python3 checks/text/check_text.py` |
| T08 | verdadeira |  | `python3 checks/text/check_text.py` |
| T09 | verdadeira |  | `python3 checks/text/check_text.py` |
| T10 | verdadeira |  | `python3 checks/text/check_text.py` |
| T11 | verdadeira |  | `python3 checks/text/check_text.py` |
| T12 | falsa | `args=('ßłõà',)` | `python3 checks/text/check_text.py` |
| T13 | verdadeira |  | `python3 checks/text/check_text.py` |
| T14 | falsa | `assertion failed: got 'ø', expected 'o'` | `python3 checks/text/check_text.py` |
| T15 | verdadeira |  | `python3 checks/text/check_text.py` |
| T16 | verdadeira |  | `python3 checks/text/check_text.py` |
| T17 | verdadeira |  | `python3 checks/text/check_text.py` |
| T18 | verdadeira |  | `python3 checks/text/check_text.py` |
| T19 | verdadeira |  | `python3 checks/text/check_text.py` |
| N01 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N02 | falsa | `actual=10 expected=0` | `python3 checks/numbers/check_numbers.py` |
| N03 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N04 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N05 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N06 | falsa | `IndexError: list index out of range` | `python3 checks/numbers/check_numbers.py` |
| N07 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N08 | falsa | `actual=2 expected=3` | `python3 checks/numbers/check_numbers.py` |
| N09 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N10 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N11 | falsa | `ZeroDivisionError: division by zero` | `python3 checks/numbers/check_numbers.py` |
| N12 | falsa | `wrong for n=[4, 6, 8, 9, 15, 25, 35, 49] (count 18); e.g. is_prime(4)=True` | `python3 checks/numbers/check_numbers.py` |
| N13 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N14 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N15 | falsa | `a=-50 b=1: gcd(a,b)=1 gcd(b,a)=-1` | `python3 checks/numbers/check_numbers.py` |
| N16 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N17 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N18 | verdadeira |  | `python3 checks/numbers/check_numbers.py` |
| N19 | falsa | `args=(-1,) raised ValueError: invalid literal for int() with base 10: '-'` | `python3 checks/numbers/check_numbers.py` |
| D01 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D02 | falsa | `x=2000-02-29 got 2001-02-28, expected same day/month in 2001` | `python3 checks/dates/check_dates.py` |
| D03 | falsa | `x=2000-01-30 got 2000-01-29` | `python3 checks/dates/check_dates.py` |
| D04 | falsa | `a=2024-01-02 b=2024-01-01 got -1` | `python3 checks/dates/check_dates.py` |
| D05 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D06 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D07 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D08 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D09 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D10 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D11 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D12 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D13 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D14 | falsa | `assertion failed: got 53` | `python3 checks/dates/check_dates.py` |
| D15 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D16 | falsa | `parse_br('1/2/2024') returned 2024-02-01 instead of raising ValueError` | `python3 checks/dates/check_dates.py` |
| D17 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D18 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| D19 | verdadeira |  | `python3 checks/dates/check_dates.py` |
| L01 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L02 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L03 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L04 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L05 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L06 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L07 | falsa | `actual=[1, [2], 3] expected=[1, 2, 3]` | `python3 checks/lists/check_lists.py` |
| L08 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L09 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L10 | falsa | `actual=[3, 2] expected=[]` | `python3 checks/lists/check_lists.py` |
| L11 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L12 | falsa | `args=([17, -10], 13)` | `python3 checks/lists/check_lists.py` |
| L13 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L14 | falsa | `actual=[1, 9] expected=[1, 9, 2, 3]` | `python3 checks/lists/check_lists.py` |
| L15 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L16 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L17 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L18 | verdadeira |  | `python3 checks/lists/check_lists.py` |
| L19 | falsa | `args=([],)` | `python3 checks/lists/check_lists.py` |
| M01 | verdadeira |  | `python3 checks/money/check_money.py` |
| M02 | verdadeira |  | `python3 checks/money/check_money.py` |
| M03 | falsa | `actual=-50 expected=-150` | `python3 checks/money/check_money.py` |
| M04 | verdadeira |  | `python3 checks/money/check_money.py` |
| M05 | verdadeira |  | `python3 checks/money/check_money.py` |
| M06 | verdadeira |  | `python3 checks/money/check_money.py` |
| M07 | falsa | `actual='R$ -2,50' expected='R$ -1,50'` | `python3 checks/money/check_money.py` |
| M08 | verdadeira |  | `python3 checks/money/check_money.py` |
| M09 | falsa | `args=(1, 29)` | `python3 checks/money/check_money.py` |
| M10 | verdadeira |  | `python3 checks/money/check_money.py` |
| M11 | verdadeira |  | `python3 checks/money/check_money.py` |
| M12 | verdadeira |  | `python3 checks/money/check_money.py` |
| M13 | verdadeira |  | `python3 checks/money/check_money.py` |
| M14 | verdadeira |  | `python3 checks/money/check_money.py` |
| M15 | verdadeira |  | `python3 checks/money/check_money.py` |
| M16 | verdadeira |  | `python3 checks/money/check_money.py` |
| M17 | falsa | `actual=114 expected=115` | `python3 checks/money/check_money.py` |
| M18 | verdadeira |  | `python3 checks/money/check_money.py` |
| M19 | verdadeira |  | `python3 checks/money/check_money.py` |
| I01 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I02 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I03 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I04 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I05 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I06 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I07 | falsa | `actual=True expected=False` | `python3 checks/intervals/check_intervals.py` |
| I08 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I09 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I10 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I11 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I12 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I13 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I14 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I15 | falsa | `IndexError: list index out of range` | `python3 checks/intervals/check_intervals.py` |
| I16 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I17 | verdadeira |  | `python3 checks/intervals/check_intervals.py` |
| I18 | falsa | `args=((8, 10), 10)` | `python3 checks/intervals/check_intervals.py` |
| I19 | falsa | `actual=-2 expected=0` | `python3 checks/intervals/check_intervals.py` |
| P01 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P02 | falsa | `actual='usr/bin' expected='/usr/bin'` | `python3 checks/paths/check_paths.py` |
| P03 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P04 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P05 | falsa | `actual='d/arquivo' expected=''` | `python3 checks/paths/check_paths.py` |
| P06 | falsa | `actual='bashrc' expected=''` | `python3 checks/paths/check_paths.py` |
| P07 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P08 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P09 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P10 | falsa | `actual='x' expected='../x'` | `python3 checks/paths/check_paths.py` |
| P11 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P12 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P13 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P14 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P15 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P16 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P17 | falsa | `actual='' expected='/'` | `python3 checks/paths/check_paths.py` |
| P18 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| P19 | verdadeira |  | `python3 checks/paths/check_paths.py` |
| R01 | verdadeira |  | `python3 checks/records/check_records.py` |
| R02 | verdadeira |  | `python3 checks/records/check_records.py` |
| R03 | verdadeira |  | `python3 checks/records/check_records.py` |
| R04 | falsa | `ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/records/check_records.py` |
| R05 | verdadeira |  | `python3 checks/records/check_records.py` |
| R06 | falsa | `args=({'': '=a', 'bb=': '='},)` | `python3 checks/records/check_records.py` |
| R07 | verdadeira |  | `python3 checks/records/check_records.py` |
| R08 | verdadeira |  | `python3 checks/records/check_records.py` |
| R09 | verdadeira |  | `python3 checks/records/check_records.py` |
| R10 | falsa | `args=({'a': 0, 'd': 2, 'b': 8}, {'d': 'a'})` | `python3 checks/records/check_records.py` |
| R11 | verdadeira |  | `python3 checks/records/check_records.py` |
| R12 | verdadeira |  | `python3 checks/records/check_records.py` |
| R13 | verdadeira |  | `python3 checks/records/check_records.py` |
| R14 | falsa | `KeyError: 'n'` | `python3 checks/records/check_records.py` |
| R15 | verdadeira |  | `python3 checks/records/check_records.py` |
| R16 | verdadeira |  | `python3 checks/records/check_records.py` |
| R17 | falsa | `actual=None expected=1` | `python3 checks/records/check_records.py` |
| R18 | verdadeira |  | `python3 checks/records/check_records.py` |
| R19 | verdadeira |  | `python3 checks/records/check_records.py` |
