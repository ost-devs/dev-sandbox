# Diferenças entre `csvline.old.parse` e `csvline.new.parse`

- Casos gerados: 200 (seed `20261029`; 45 escritos à mão + aleatórios)
- Casos com diferença: 166 (detalhe em `diffs.jsonl`)

Regerar tudo (determinístico):

```
python3 difftool.py
```

## aspa sem fechar: new mantém a aspa literal e quebra nas vírgulas internas — 72 caso(s)

Exemplo mínimo: input `'"'`

- old: `['']`
- new: `['"']`

## aspas no meio do campo / texto após aspa de fechamento: new mantém as aspas, old as remove — 38 caso(s)

Exemplo mínimo: input `'""c'`

- old: `['c']`
- new: `['""c']`

## espaços/tabs ao redor do campo são removidos (new faz strip) — 32 caso(s)

Exemplo mínimo: input `'\t'`

- old: `['\t']`
- new: `['']`

## escape `""` dentro de aspas não é desescapado (new devolve o texto cru) — 14 caso(s)

Exemplo mínimo: input `'""""'`

- old: `['"']`
- new: `['""""']`

## campo vazio final descartado (`a,b,` -> 2 campos em vez de 3) — 7 caso(s)

Exemplo mínimo: input `','`

- old: `['', '']`
- new: `['']`

## campo vazio final descartado + espaços removidos — 3 caso(s)

Exemplo mínimo: input `'\t,'`

- old: `['\t', '']`
- new: `['']`
