# Relatório de auditoria de `claims.md`

152 afirmações verificadas executando o código de `kit/`: **113 verdadeiras, 39 falsas**.

Cada checagem é um script em `checks/<módulo>.py` (só stdlib, determinístico: entradas fixas, domínios finitos varridos por inteiro, e amostras aleatórias com `random.Random` de semente fixa registrada no código). Rode da raiz do projeto. Cada módulo foi executado duas vezes e a saída foi idêntica. `money` leva ~40 s por varrer 0..1.000.000.

| id | veredito | contraexemplo | comando |
|---|---|---|---|
| T01 | falsa | `slugify('Café Noir'): got 'caf-noir', expected 'cafe-noir'` | `python3 -I checks/text.py` |
| T02 | verdadeira |  | `python3 -I checks/text.py` |
| T03 | verdadeira |  | `python3 -I checks/text.py` |
| T04 | verdadeira |  | `python3 -I checks/text.py` |
| T05 | falsa | `input (' ', 0) -> result '...'` | `python3 -I checks/text.py` |
| T06 | verdadeira |  | `python3 -I checks/text.py` |
| T07 | verdadeira |  | `python3 -I checks/text.py` |
| T08 | verdadeira |  | `python3 -I checks/text.py` |
| T09 | verdadeira |  | `python3 -I checks/text.py` |
| T10 | verdadeira |  | `python3 -I checks/text.py` |
| T11 | verdadeira |  | `python3 -I checks/text.py` |
| T12 | falsa | `input 'ß' -> result 'SS'` | `python3 -I checks/text.py` |
| T13 | verdadeira |  | `python3 -I checks/text.py` |
| T14 | falsa | `strip_accents('ø'): got 'ø', expected 'o'` | `python3 -I checks/text.py` |
| T15 | verdadeira |  | `python3 -I checks/text.py` |
| T16 | verdadeira |  | `python3 -I checks/text.py` |
| T17 | verdadeira |  | `python3 -I checks/text.py` |
| T18 | verdadeira |  | `python3 -I checks/text.py` |
| T19 | verdadeira |  | `python3 -I checks/text.py` |
| N01 | verdadeira |  | `python3 -I checks/numbers.py` |
| N02 | falsa | `clamp(5, 10, 0) -> 10 (esperado 0)` | `python3 -I checks/numbers.py` |
| N03 | verdadeira |  | `python3 -I checks/numbers.py` |
| N04 | verdadeira |  | `python3 -I checks/numbers.py` |
| N05 | verdadeira |  | `python3 -I checks/numbers.py` |
| N06 | falsa | `median([]) -> 'EXC IndexError: list index out of range' (esperado None)` | `python3 -I checks/numbers.py` |
| N07 | verdadeira |  | `python3 -I checks/numbers.py` |
| N08 | falsa | `round_half(2.5) -> 2 (esperado 3)` | `python3 -I checks/numbers.py` |
| N09 | verdadeira |  | `python3 -I checks/numbers.py` |
| N10 | verdadeira |  | `python3 -I checks/numbers.py` |
| N11 | falsa | `entrada (0,) -> 'EXC ZeroDivisionError: division by zero'` | `python3 -I checks/numbers.py` |
| N12 | falsa | `is_prime(4) -> True (correto: False)` | `python3 -I checks/numbers.py` |
| N13 | verdadeira |  | `python3 -I checks/numbers.py` |
| N14 | verdadeira |  | `python3 -I checks/numbers.py` |
| N15 | falsa | `entrada (-50, 1) -> (1, -1)` | `python3 -I checks/numbers.py` |
| N16 | verdadeira |  | `python3 -I checks/numbers.py` |
| N17 | verdadeira |  | `python3 -I checks/numbers.py` |
| N18 | verdadeira |  | `python3 -I checks/numbers.py` |
| N19 | falsa | `entrada (-1,) -> "EXC ValueError: invalid literal for int() with base 10: '-'"` | `python3 -I checks/numbers.py` |
| D01 | verdadeira |  | `python3 -I checks/dates.py` |
| D02 | falsa | `x=datetime.date(2000, 2, 29) add_months(x,12) -> datetime.date(2001, 2, 28)` | `python3 -I checks/dates.py` |
| D03 | falsa | `x=datetime.date(2000, 1, 30) add_months(add_months(x,1),-1) -> datetime.date(2000, 1, 29)` | `python3 -I checks/dates.py` |
| D04 | falsa | `days_between(datetime.date(2024, 1, 2), datetime.date(2024, 1, 1)) -> -1` | `python3 -I checks/dates.py` |
| D05 | verdadeira |  | `python3 -I checks/dates.py` |
| D06 | verdadeira |  | `python3 -I checks/dates.py` |
| D07 | verdadeira |  | `python3 -I checks/dates.py` |
| D08 | verdadeira |  | `python3 -I checks/dates.py` |
| D09 | verdadeira |  | `python3 -I checks/dates.py` |
| D10 | verdadeira |  | `python3 -I checks/dates.py` |
| D11 | verdadeira |  | `python3 -I checks/dates.py` |
| D12 | verdadeira |  | `python3 -I checks/dates.py` |
| D13 | verdadeira |  | `python3 -I checks/dates.py` |
| D14 | falsa | `iso_week(date(2021,1,1)) -> 53 (esperado 1)` | `python3 -I checks/dates.py` |
| D15 | verdadeira |  | `python3 -I checks/dates.py` |
| D16 | falsa | `parse_br('1/2/2024') -> datetime.date(2024, 2, 1) (nao levantou ValueError)` | `python3 -I checks/dates.py` |
| D17 | verdadeira |  | `python3 -I checks/dates.py` |
| D18 | verdadeira |  | `python3 -I checks/dates.py` |
| D19 | verdadeira |  | `python3 -I checks/dates.py` |
| L01 | verdadeira |  | `python3 -I checks/lists.py` |
| L02 | verdadeira |  | `python3 -I checks/lists.py` |
| L03 | verdadeira |  | `python3 -I checks/lists.py` |
| L04 | verdadeira |  | `python3 -I checks/lists.py` |
| L05 | verdadeira |  | `python3 -I checks/lists.py` |
| L06 | verdadeira |  | `python3 -I checks/lists.py` |
| L07 | falsa | `input=() result='flatten([[1, [2]], [3]],) -> [1, [2], 3]'` | `python3 -I checks/lists.py` |
| L08 | verdadeira |  | `python3 -I checks/lists.py` |
| L09 | verdadeira |  | `python3 -I checks/lists.py` |
| L10 | falsa | `input=() result='top_n([3, 2, 1], -1) -> [3, 2]'` | `python3 -I checks/lists.py` |
| L11 | verdadeira |  | `python3 -I checks/lists.py` |
| L12 | falsa | `input=([3, 1, 3, 2, 1], 7) result=[3, 1, 3, 2, 1]` | `python3 -I checks/lists.py` |
| L13 | verdadeira |  | `python3 -I checks/lists.py` |
| L14 | falsa | `input=() result='interleave([1, 2, 3], [9]) -> [1, 9]'` | `python3 -I checks/lists.py` |
| L15 | verdadeira |  | `python3 -I checks/lists.py` |
| L16 | verdadeira |  | `python3 -I checks/lists.py` |
| L17 | verdadeira |  | `python3 -I checks/lists.py` |
| L18 | verdadeira |  | `python3 -I checks/lists.py` |
| L19 | falsa | `input=([],) result=[]` | `python3 -I checks/lists.py` |
| M01 | verdadeira |  | `python3 -I checks/money.py` |
| M02 | verdadeira |  | `python3 -I checks/money.py` |
| M03 | falsa | `to_cents('-1,50') -> -50, esperado -150` | `python3 -I checks/money.py` |
| M04 | verdadeira |  | `python3 -I checks/money.py` |
| M05 | verdadeira |  | `python3 -I checks/money.py` |
| M06 | verdadeira |  | `python3 -I checks/money.py` |
| M07 | falsa | `format_brl(-150) -> 'R$ -2,50', esperado 'R$ -1,50'` | `python3 -I checks/money.py` |
| M08 | verdadeira |  | `python3 -I checks/money.py` |
| M09 | falsa | `sum(split_bill(total,k))==total com (1, 2) -> [0, 0]` | `python3 -I checks/money.py` |
| M10 | verdadeira |  | `python3 -I checks/money.py` |
| M11 | verdadeira |  | `python3 -I checks/money.py` |
| M12 | verdadeira |  | `python3 -I checks/money.py` |
| M13 | verdadeira |  | `python3 -I checks/money.py` |
| M14 | verdadeira |  | `python3 -I checks/money.py` |
| M15 | verdadeira |  | `python3 -I checks/money.py` |
| M16 | verdadeira |  | `python3 -I checks/money.py` |
| M17 | falsa | `add_tax(100, 0.15) -> 114, esperado 115` | `python3 -I checks/money.py` |
| M18 | verdadeira |  | `python3 -I checks/money.py` |
| M19 | verdadeira |  | `python3 -I checks/money.py` |
| I01 | verdadeira |  | `python3 -I checks/intervals.py` |
| I02 | verdadeira |  | `python3 -I checks/intervals.py` |
| I03 | verdadeira |  | `python3 -I checks/intervals.py` |
| I04 | verdadeira |  | `python3 -I checks/intervals.py` |
| I05 | verdadeira |  | `python3 -I checks/intervals.py` |
| I06 | verdadeira |  | `python3 -I checks/intervals.py` |
| I07 | falsa | `got True, expected False` | `python3 -I checks/intervals.py` |
| I08 | verdadeira |  | `python3 -I checks/intervals.py` |
| I09 | verdadeira |  | `python3 -I checks/intervals.py` |
| I10 | verdadeira |  | `python3 -I checks/intervals.py` |
| I11 | verdadeira |  | `python3 -I checks/intervals.py` |
| I12 | verdadeira |  | `python3 -I checks/intervals.py` |
| I13 | verdadeira |  | `python3 -I checks/intervals.py` |
| I14 | verdadeira |  | `python3 -I checks/intervals.py` |
| I15 | falsa | `raised IndexError('list index out of range')` | `python3 -I checks/intervals.py` |
| I16 | verdadeira |  | `python3 -I checks/intervals.py` |
| I17 | verdadeira |  | `python3 -I checks/intervals.py` |
| I18 | falsa | `contains((-3, -3),-3)=True but overlaps((-3, -3),(-3, -2))=False` | `python3 -I checks/intervals.py` |
| I19 | falsa | `got -2, expected 0` | `python3 -I checks/intervals.py` |
| P01 | verdadeira |  | `python3 -I checks/paths.py` |
| P02 | falsa | `join('/usr', 'bin') -> 'usr/bin' (esperado '/usr/bin')` | `python3 -I checks/paths.py` |
| P03 | verdadeira |  | `python3 -I checks/paths.py` |
| P04 | verdadeira |  | `python3 -I checks/paths.py` |
| P05 | falsa | `ext('dir.d/arquivo',) -> 'd/arquivo' (esperado '')` | `python3 -I checks/paths.py` |
| P06 | falsa | `ext('.bashrc',) -> 'bashrc' (esperado '')` | `python3 -I checks/paths.py` |
| P07 | verdadeira |  | `python3 -I checks/paths.py` |
| P08 | verdadeira |  | `python3 -I checks/paths.py` |
| P09 | verdadeira |  | `python3 -I checks/paths.py` |
| P10 | falsa | `normalize('../x',) -> 'x' (esperado '../x')` | `python3 -I checks/paths.py` |
| P11 | verdadeira |  | `python3 -I checks/paths.py` |
| P12 | verdadeira |  | `python3 -I checks/paths.py` |
| P13 | verdadeira |  | `python3 -I checks/paths.py` |
| P14 | verdadeira |  | `python3 -I checks/paths.py` |
| P15 | verdadeira |  | `python3 -I checks/paths.py` |
| P16 | verdadeira |  | `python3 -I checks/paths.py` |
| P17 | falsa | `parent('/a',) -> '' (esperado '/')` | `python3 -I checks/paths.py` |
| P18 | verdadeira |  | `python3 -I checks/paths.py` |
| P19 | verdadeira |  | `python3 -I checks/paths.py` |
| R01 | verdadeira |  | `python3 -I checks/records.py` |
| R02 | verdadeira |  | `python3 -I checks/records.py` |
| R03 | verdadeira |  | `python3 -I checks/records.py` |
| R04 | falsa | `parse_kv('a=1;flag') raised ValueError: dictionary update sequence element #1 has length 1; 2 is required (expected {'a': '1', 'flag': ''})` | `python3 -I checks/records.py` |
| R05 | verdadeira |  | `python3 -I checks/records.py` |
| R06 | falsa | `input={'a': 'b;c'} raised ValueError: dictionary update sequence element #1 has length 1; 2 is required` | `python3 -I checks/records.py` |
| R07 | verdadeira |  | `python3 -I checks/records.py` |
| R08 | verdadeira |  | `python3 -I checks/records.py` |
| R09 | verdadeira |  | `python3 -I checks/records.py` |
| R10 | falsa | `input=({'a': 1, 'b': 2}, {'a': 'b'}) result={'b': 2}` | `python3 -I checks/records.py` |
| R11 | verdadeira |  | `python3 -I checks/records.py` |
| R12 | verdadeira |  | `python3 -I checks/records.py` |
| R13 | verdadeira |  | `python3 -I checks/records.py` |
| R14 | falsa | `input=[{'n': 1}, {'x': 0}] raised KeyError: 'n'` | `python3 -I checks/records.py` |
| R15 | verdadeira |  | `python3 -I checks/records.py` |
| R16 | verdadeira |  | `python3 -I checks/records.py` |
| R17 | falsa | `result=None expected=1` | `python3 -I checks/records.py` |
| R18 | verdadeira |  | `python3 -I checks/records.py` |
| R19 | verdadeira |  | `python3 -I checks/records.py` |
