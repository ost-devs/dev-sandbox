# share-memories: memórias compartilhadas entre projetos

Leva uma memória do Claude para um grupo de projetos (todos, uma lista ou uma
categoria como `dev`) e a mantém igual em todos. Fica uma cópia só, em
`~/.claude/shared-memories/<grupo>/`, com um link em cada projeto. O Claude
decide o que é geral; você aprova quando ele quer reescrever uma memória.

Guia completo: [compartilhar memórias](../../../docs/claude-code/compartilhar-memorias.md).
Nomes em inglês: [glossário](../../../docs/ingles-para-devs/glossario.md#share-memories).

## Como ler a tabela

Cada linha mostra o mesmo pedido de dois jeitos: em palavras, numa sessão
do Claude, ou como comando. No comando, `...` é o começo:

| Onde | Troque `...` por |
|---|---|
| Numa sessão do Claude | `/share-memories` |
| No terminal, sem o Claude (host ou container, de qualquer pasta) | `python3 ~/.claude/skills/share-memories/share_memories.py` |

O que está entre `< >` é seu: `<dev>` é um exemplo de grupo, `<ferrum>` de
projeto (o nome da pasta dele em `~/.claude/projects/`, como `-ferrum`, ou o
caminho, como `/home/voce/Dev/*`).

| Você quer | Peça ao Claude | Ou use o comando |
|---|---|---|
| Instalar (hooks e `groups.json`) | "instale a share-memories" | `... install` (só ver: `... install --dry-run`) |
| Criar um grupo ou pôr projetos nele | "crie o grupo <dev> com o <dev-sandbox> e o <ferrum>" | `... group <dev> --add <-dev-sandbox> <-ferrum>` |
| Um grupo com todos os projetos | "crie um grupo com todos os projetos" | `... group <all> --add '*'` |
| Tirar um projeto do grupo | "tire o <ferrum> do grupo <dev>" | `... group <dev> --remove <-ferrum>` |
| Ver tudo e o que está fora do lugar | "como estão as memórias compartilhadas?" | `... status` |
| Compartilhar memórias | "compartilhe essa memória com o grupo <dev>" | `... share <dev> <caminho da memória>` |
| Mudar de grupo | "passe essa memória para o grupo <all>" | `... move <all> <dev/x.md>` |
| Desfazer, deixando uma cópia num projeto | "tire essa memória do grupo e deixe só no <ferrum>" | `... unshare <dev/x.md> --keep <-ferrum>` |
| Desfazer e apagar | "apague a memória compartilhada <x>" | `... unshare <dev/x.md>` |
| Revisar as memórias de um grupo | "mostre as memórias do grupo <dev>" | `... status` |
| Consertar depois de mexer à mão | "sincronize as memórias" | `... sync` |
