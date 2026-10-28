# Os comentários HTML do `MEMORY.md` não chegam ao Claude

- **Data:** 2026-10
- **Ambiente:** Claude Code 2.1.310, dentro do dev-sandbox
- **Base:** documentação: <https://code.claude.com/docs/en/errors#memory-index-is-over-its-read-limit>,
  lida em 28/10/2026 no mirror local (vale da v2.1.211 em diante)

## Sintoma
A skill `share-memories` marca o bloco gerado no `MEMORY.md` com dois comentários:

```text
<!-- share-memories:start (generated; edit the memories, not these lines) -->
...
<!-- share-memories:end -->
```

A ideia era que o Claude lesse o aviso "edit the memories, not these lines" e soubesse que
aquelas linhas são de memórias compartilhadas. Ele não lê.

## Causa
A documentação diz: *"YAML frontmatter and block-level HTML comments are stripped before the
index is loaded"*. O Claude Code tira os comentários antes de pôr o índice no contexto. O mesmo
vale para o `CLAUDE.md` ([memory](https://code.claude.com/docs/en/memory)). O comentário só
aparece quando o Claude abre o arquivo com Read, por exemplo antes de reescrevê-lo.

## Solução
Pôr na própria linha o que o Claude precisa saber. Cada linha do bloco termina em
`_(shared, group dev)_`: no índice carregado, é o único sinal de que a memória vale em outros
projetos, e de qual grupo. Assim ele mantém a edição geral antes de escrever, e não só quando o
Write recusa o link simbólico ([aprendizado](./2026-10-write-edit-recusam-symlink.md)).

Os comentários continuam úteis para o script (acham o bloco) e para quem abre o arquivo.

## O que mudou no dev-sandbox
A marca passou de `_(group dev)_` para `_(shared, group dev)_` em
[`share_memories.py`](../../utils/skills/share-memories/share_memories.py)
([guia](../claude-code/compartilhar-memorias.md)).
