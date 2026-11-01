# Relatório de auditoria de claims.md

Total: 152 afirmações — 113 verdadeiras, 39 falsas.

Semente registrada: 20261101 (checks/_lib.py); propriedades "para qualquer" testadas com 5000 casos gerados. Cada script é determinístico (rodado duas vezes, saída idêntica).
Regerar este relatório: `python3 checks/make_report.py`. Verdadeira em propriedade aleatória = nenhum contraexemplo em 5000 casos (evidência, não prova).

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `got 'caf-noir', expected 'cafe-noir'` | `python3 checks/text.py T01` |
| T02 | verdadeira |  | `python3 checks/text.py T02` |
| T03 | verdadeira |  | `python3 checks/text.py T03` |
| T04 | verdadeira |  | `python3 checks/text.py T04` |
| T05 | falsa | `s='é\n01uw mı3ßymΣ\naQf' n=1 -> 'é\n01uw mı3ßymΣ\na...' (len 19)` | `python3 checks/text.py T05` |
| T06 | verdadeira |  | `python3 checks/text.py T06` |
| T07 | verdadeira |  | `python3 checks/text.py T07` |
| T08 | verdadeira |  | `python3 checks/text.py T08` |
| T09 | verdadeira |  | `python3 checks/text.py T09` |
| T10 | verdadeira |  | `python3 checks/text.py T10` |
| T11 | verdadeira |  | `python3 checks/text.py T11` |
| T12 | falsa | `s='ßbXDΣbF-lV:n' -> 'SSbXDΣbF-lV:n' (len 13 vs 12)` | `python3 checks/text.py T12` |
| T13 | verdadeira |  | `python3 checks/text.py T13` |
| T14 | falsa | `got 'ø', expected 'o'` | `python3 checks/text.py T14` |
| T15 | verdadeira |  | `python3 checks/text.py T15` |
| T16 | verdadeira |  | `python3 checks/text.py T16` |
| T17 | verdadeira |  | `python3 checks/text.py T17` |
| T18 | verdadeira |  | `python3 checks/text.py T18` |
| T19 | verdadeira |  | `python3 checks/text.py T19` |
| N01 | verdadeira |  | `python3 checks/numbers.py N01` |
| N02 | falsa | `got 10, expected 0` | `python3 checks/numbers.py N02` |
| N03 | verdadeira |  | `python3 checks/numbers.py N03` |
| N04 | verdadeira |  | `python3 checks/numbers.py N04` |
| N05 | verdadeira |  | `python3 checks/numbers.py N05` |
| N06 | falsa | `exception IndexError: list index out of range` | `python3 checks/numbers.py N06` |
| N07 | verdadeira |  | `python3 checks/numbers.py N07` |
| N08 | falsa | `got 2, expected 3` | `python3 checks/numbers.py N08` |
| N09 | verdadeira |  | `python3 checks/numbers.py N09` |
| N10 | verdadeira |  | `python3 checks/numbers.py N10` |
| N11 | falsa | `exception ZeroDivisionError: float division by zero` | `python3 checks/numbers.py N11` |
| N12 | falsa | `wrong (n, is_prime(n)) e.g. [(4, True), (6, True), (8, True), (9, True), (15, True)]; 18 total` | `python3 checks/numbers.py N12` |
| N13 | verdadeira |  | `python3 checks/numbers.py N13` |
| N14 | verdadeira |  | `python3 checks/numbers.py N14` |
| N15 | falsa | `gcd(-50,1)=1 but gcd(1,-50)=-1` | `python3 checks/numbers.py N15` |
| N16 | verdadeira |  | `python3 checks/numbers.py N16` |
| N17 | verdadeira |  | `python3 checks/numbers.py N17` |
| N18 | verdadeira |  | `python3 checks/numbers.py N18` |
| N19 | falsa | `exception ValueError: invalid literal for int() with base 10: '-'` | `python3 checks/numbers.py N19` |
| D01 | verdadeira |  | `python3 checks/dates.py D01` |
| D02 | falsa | `x=datetime.date(2000, 2, 29) add_months(x,12)=datetime.date(2001, 2, 28)` | `python3 checks/dates.py D02` |
| D03 | falsa | `x=datetime.date(2023, 3, 31) result=datetime.date(2023, 3, 30)` | `python3 checks/dates.py D03` |
| D04 | falsa | `a=datetime.date(9873, 9, 24) b=datetime.date(5092, 5, 13) days_between=-1746358` | `python3 checks/dates.py D04` |
| D05 | verdadeira |  | `python3 checks/dates.py D05` |
| D06 | verdadeira |  | `python3 checks/dates.py D06` |
| D07 | verdadeira |  | `python3 checks/dates.py D07` |
| D08 | verdadeira |  | `python3 checks/dates.py D08` |
| D09 | verdadeira |  | `python3 checks/dates.py D09` |
| D10 | verdadeira |  | `python3 checks/dates.py D10` |
| D11 | verdadeira |  | `python3 checks/dates.py D11` |
| D12 | verdadeira |  | `python3 checks/dates.py D12` |
| D13 | verdadeira |  | `python3 checks/dates.py D13` |
| D14 | falsa | `iso_week=53` | `python3 checks/dates.py D14` |
| D15 | verdadeira |  | `python3 checks/dates.py D15` |
| D16 | falsa | `no ValueError; returned datetime.date(2024, 2, 1)` | `python3 checks/dates.py D16` |
| D17 | verdadeira |  | `python3 checks/dates.py D17` |
| D18 | verdadeira |  | `python3 checks/dates.py D18` |
| D19 | verdadeira |  | `python3 checks/dates.py D19` |
| M01 | verdadeira |  | `python3 checks/money.py M01` |
| M02 | verdadeira |  | `python3 checks/money.py M02` |
| M03 | falsa | `got -50, expected -150` | `python3 checks/money.py M03` |
| M04 | verdadeira |  | `python3 checks/money.py M04` |
| M05 | verdadeira |  | `python3 checks/money.py M05` |
| M06 | verdadeira |  | `python3 checks/money.py M06` |
| M07 | falsa | `got 'R$ -2,50', expected 'R$ -1,50'` | `python3 checks/money.py M07` |
| M08 | verdadeira |  | `python3 checks/money.py M08` |
| M09 | falsa | `total=1 k=9 -> [0, 0, 0, 0, 0, 0, 0, 0, 0] sum=0` | `python3 checks/money.py M09` |
| M10 | verdadeira |  | `python3 checks/money.py M10` |
| M11 | verdadeira |  | `python3 checks/money.py M11` |
| M12 | verdadeira |  | `python3 checks/money.py M12` |
| M13 | verdadeira |  | `python3 checks/money.py M13` |
| M14 | verdadeira |  | `python3 checks/money.py M14` |
| M15 | verdadeira |  | `python3 checks/money.py M15` |
| M16 | verdadeira |  | `python3 checks/money.py M16` |
| M17 | falsa | `got 114, expected 115` | `python3 checks/money.py M17` |
| M18 | verdadeira |  | `python3 checks/money.py M18` |
| M19 | verdadeira |  | `python3 checks/money.py M19` |
| L01 | verdadeira |  | `python3 checks/lists.py L01` |
| L02 | verdadeira |  | `python3 checks/lists.py L02` |
| L03 | verdadeira |  | `python3 checks/lists.py L03` |
| L04 | verdadeira |  | `python3 checks/lists.py L04` |
| L05 | verdadeira |  | `python3 checks/lists.py L05` |
| L06 | verdadeira |  | `python3 checks/lists.py L06` |
| L07 | falsa | `got [1, [2], 3]` | `python3 checks/lists.py L07` |
| L08 | verdadeira |  | `python3 checks/lists.py L08` |
| L09 | verdadeira |  | `python3 checks/lists.py L09` |
| L10 | falsa | `got [3, 2]` | `python3 checks/lists.py L10` |
| L11 | verdadeira |  | `python3 checks/lists.py L11` |
| L12 | falsa | `xs=[14, 18, 13, -11, -9, 2] k=17: rotate(xs,k)=[14, 18, 13, -11, -9, 2] rotate(xs,k%len)=[2, 14, 18, 13, -11, -9]` | `python3 checks/lists.py L12` |
| L13 | verdadeira |  | `python3 checks/lists.py L13` |
| L14 | falsa | `got [1, 9]` | `python3 checks/lists.py L14` |
| L15 | verdadeira |  | `python3 checks/lists.py L15` |
| L16 | verdadeira |  | `python3 checks/lists.py L16` |
| L17 | verdadeira |  | `python3 checks/lists.py L17` |
| L18 | verdadeira |  | `python3 checks/lists.py L18` |
| L19 | falsa | `xs=[] len(pairwise)=0 expected -1` | `python3 checks/lists.py L19` |
| R01 | verdadeira |  | `python3 checks/records.py R01` |
| R02 | verdadeira |  | `python3 checks/records.py R02` |
| R03 | verdadeira |  | `python3 checks/records.py R03` |
| R04 | falsa | `exception ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 checks/records.py R04` |
| R05 | verdadeira |  | `python3 checks/records.py R05` |
| R06 | falsa | `d={'_²Od́½': 'uih', '=': 'hx\t'} to_kv='_²Od́½=uih;==hx\t' -> {'_²Od́½': 'uih', '': '=hx\t'}` | `python3 checks/records.py R06` |
| R07 | verdadeira |  | `python3 checks/records.py R07` |
| R08 | verdadeira |  | `python3 checks/records.py R08` |
| R09 | verdadeira |  | `python3 checks/records.py R09` |
| R10 | falsa | `d={'aaabcb': '', 'b': '', 'bacc': 'ba', 'bacbca': 'bbaa', 'c': 'abc'} mapping={'b': 'c', 'c': 'c', 'd': 'd'} -> {'aaabcb': '', 'c': 'abc', 'bacc': 'ba', 'bacbca': 'bbaa'}` | `python3 checks/records.py R10` |
| R11 | verdadeira |  | `python3 checks/records.py R11` |
| R12 | verdadeira |  | `python3 checks/records.py R12` |
| R13 | verdadeira |  | `python3 checks/records.py R13` |
| R14 | falsa | `rows=[{'i': 99}] -> exception KeyError: KeyError('n')` | `python3 checks/records.py R14` |
| R15 | verdadeira |  | `python3 checks/records.py R15` |
| R16 | verdadeira |  | `python3 checks/records.py R16` |
| R17 | falsa | `got None, expected 1` | `python3 checks/records.py R17` |
| R18 | verdadeira |  | `python3 checks/records.py R18` |
| R19 | verdadeira |  | `python3 checks/records.py R19` |
| P01 | verdadeira |  | `python3 checks/paths.py P01` |
| P02 | falsa | `got 'usr/bin', expected '/usr/bin'` | `python3 checks/paths.py P02` |
| P03 | verdadeira |  | `python3 checks/paths.py P03` |
| P04 | verdadeira |  | `python3 checks/paths.py P04` |
| P05 | falsa | `got 'd/arquivo', expected ''` | `python3 checks/paths.py P05` |
| P06 | falsa | `got 'bashrc', expected ''` | `python3 checks/paths.py P06` |
| P07 | verdadeira |  | `python3 checks/paths.py P07` |
| P08 | verdadeira |  | `python3 checks/paths.py P08` |
| P09 | verdadeira |  | `python3 checks/paths.py P09` |
| P10 | falsa | `got 'x', expected '../x'` | `python3 checks/paths.py P10` |
| P11 | verdadeira |  | `python3 checks/paths.py P11` |
| P12 | verdadeira |  | `python3 checks/paths.py P12` |
| P13 | verdadeira |  | `python3 checks/paths.py P13` |
| P14 | verdadeira |  | `python3 checks/paths.py P14` |
| P15 | verdadeira |  | `python3 checks/paths.py P15` |
| P16 | verdadeira |  | `python3 checks/paths.py P16` |
| P17 | falsa | `got '', expected '/'` | `python3 checks/paths.py P17` |
| P18 | verdadeira |  | `python3 checks/paths.py P18` |
| P19 | verdadeira |  | `python3 checks/paths.py P19` |
| I01 | verdadeira |  | `python3 checks/intervals.py I01` |
| I02 | verdadeira |  | `python3 checks/intervals.py I02` |
| I03 | verdadeira |  | `python3 checks/intervals.py I03` |
| I04 | verdadeira |  | `python3 checks/intervals.py I04` |
| I05 | verdadeira |  | `python3 checks/intervals.py I05` |
| I06 | verdadeira |  | `python3 checks/intervals.py I06` |
| I07 | falsa | `got True` | `python3 checks/intervals.py I07` |
| I08 | verdadeira |  | `python3 checks/intervals.py I08` |
| I09 | verdadeira |  | `python3 checks/intervals.py I09` |
| I10 | verdadeira |  | `python3 checks/intervals.py I10` |
| I11 | verdadeira |  | `python3 checks/intervals.py I11` |
| I12 | verdadeira |  | `python3 checks/intervals.py I12` |
| I13 | verdadeira |  | `python3 checks/intervals.py I13` |
| I14 | verdadeira |  | `python3 checks/intervals.py I14` |
| I15 | falsa | `exception IndexError: list index out of range` | `python3 checks/intervals.py I15` |
| I16 | verdadeira |  | `python3 checks/intervals.py I16` |
| I17 | verdadeira |  | `python3 checks/intervals.py I17` |
| I18 | falsa | `a=(-3, -2) x=-2 contains=True overlaps(a,(x,x+1))=False` | `python3 checks/intervals.py I18` |
| I19 | falsa | `got -2` | `python3 checks/intervals.py I19` |
