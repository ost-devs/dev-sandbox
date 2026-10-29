# Diferenças entre `csvline.old.parse` e `csvline.new.parse`

200 entradas geradas (seed `20261029`), 158 com resultado diferente (detalhe em `diffs.jsonl`).
Cada diferença cai em um único tipo (o primeiro que se aplica na ordem abaixo); entradas com várias causas
aparecem só no tipo de maior prioridade. Exemplo = a menor entrada do grupo.

| Tipo | Casos |
|---|---|
| Aspa sem par (campo não fechado ou aspa solta) | 72 |
| Aspa escapada `""` dentro de campo entre aspas | 14 |
| Espaço/tab nas bordas de campo | 25 |
| Campo vazio final removido | 14 |
| Aspa no meio de campo ou texto fora das aspas | 33 |

## Aspa sem par (campo não fechado ou aspa solta) (72)

old: aspa abre campo quoted que vai até o fim da linha (vírgulas viram texto); new: aspa vira caractere literal e a linha continua sendo dividida nas vírgulas.

Exemplo mínimo: `"\""`

- old: `[""]`
- new: `["\""]`

## Aspa escapada `""` dentro de campo entre aspas (14)

old: `""` vira uma aspa literal; new: o regex `[^"]*` não aceita `""`, então o campo inteiro (com as aspas) sai como texto literal.

Exemplo mínimo: `"\"\"\"\""`

- old: `["\""]`
- new: `["\"\"\"\""]`

## Espaço/tab nas bordas de campo (25)

old: preserva espaços; new: remove espaços/tabs antes e depois de cada campo (inclusive depois da aspa de fechamento).

Exemplo mínimo: `"\t"`

- old: `["\t"]`
- new: `[""]`

## Campo vazio final removido (14)

old: `a,` dá `['a', '']`; new: o último campo vazio depois de vírgula final desaparece.

Exemplo mínimo: `","`

- old: `["", ""]`
- new: `[""]`

## Aspa no meio de campo ou texto fora das aspas (33)

old: tira toda aspa não escapada, esteja onde estiver (`a"b"c` vira `abc`); new: só reconhece aspas no início do campo, o resto fica literal.

Exemplo mínimo: `"\"\"bb"`

- old: `["bb"]`
- new: `["\"\"bb"]`

## Como reproduzir

```
python3 -I gen_diffs.py diffs.jsonl diff-report.md
```

Determinístico: lista fixa de casos escritos à mão + casos aleatórios com `random.Random(SEED)`; rodar de novo gera arquivos idênticos.
