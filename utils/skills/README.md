# Skills para qualquer projeto

Skills do Claude Code que não dependem do dev-sandbox. Funcionam dentro ou
fora do container, em qualquer repositório.

| Skill | Para quê | Como usar |
|---|---|---|
| [`montar-consultor`](./montar-consultor/SKILL.md) | Montar os arquivos que fazem uma conversa nova já saber o projeto | [Guia](../../docs/claude-code/montar-consultor.md) |
| [`estudar`](./estudar/SKILL.md) | Transformar artigos da web (um, uma lista ou uma cadeia) em artigos do projeto, conferindo números e versões na fonte oficial. Precisa da `mirrors` | [Guia](../../docs/claude-code/base-de-conhecimento.md#escrever-a-partir-de-artigos-estudar) |
| [`mirrors`](./mirrors/SKILL.md) | Guardar cópias somente leitura de repositórios de fora (docs, código de referência) | [Guia](../../docs/claude-code/mirrors.md) |
| [`token-economy`](./token-economy/SKILL.md) | Chegar ao mesmo resultado gastando menos tokens: evitar trabalho repetido, medir antes de dividir, sem cortar o que garante a qualidade | [Guia](../../docs/claude-code/economia-de-tokens.md) |
| [`share-memories`](./share-memories/SKILL.md) | Levar memórias para um grupo de projetos (todos, uma lista, uma categoria) e mantê-las sincronizadas. Instala os próprios hooks (`/share-memories install`) | [Guia](../../docs/claude-code/compartilhar-memorias.md) |

## Instalar

Cada pasta aqui é a bancada da skill: o que o Claude usa e,
junto, o que serve para desenvolvê-la (testes, evals, resultados, README).
Para o seu `.claude` vai só a skill pronta. O instalador copia o que o Claude
usa e instala as dependências dela (na `mirrors`, o Defuddle).

Rode **no host**, trocando `~/dev-sandbox` pelo lugar onde você clonou este
repositório e `<nome>` pela skill:

```bash
~/dev-sandbox/utils/skills/install-skill.sh <nome>
```

Ela vai para `~/.claude/skills/<nome>` e vale em todos os seus projetos. Para
valer só num repositório (e ir para o git dele), rode na pasta dele:

```bash
~/dev-sandbox/utils/skills/install-skill.sh <nome> .claude/skills
```

Para atualizar depois de um `git pull`, rode o mesmo comando de novo. Se a
skill já estava lá copiada à mão, ele pergunta antes de substituir.

Conferir: numa sessão nova, digite `/` e o começo do nome. A skill deve
aparecer na lista.
