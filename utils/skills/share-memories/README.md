# share-memories: memórias compartilhadas entre projetos

Leva uma memória do Claude para um grupo de projetos (todos, uma lista ou uma
categoria como `dev`) e a mantém igual em todos. Fica uma cópia só, em
`~/.claude/shared-memories/<grupo>/`, com um link em cada projeto. O Claude
decide o que é geral; você aprova quando ele quer reescrever uma memória.

Guia completo: [compartilhar memórias](../../../docs/claude-code/compartilhar-memorias.md).
Nomes em inglês: [glossário](../../../docs/ingles-para-devs/glossario.md#share-memories).

| Você quer | Peça ao Claude | Ou rode |
|---|---|---|
| Instalar (hooks e `groups.json`) | "instale a share-memories" | `install` (para só ver: `install --dry-run`) |
| Criar um grupo ou pôr projetos nele | "crie o grupo dev com o dev-sandbox e o ferrum" | `group dev --add -dev-sandbox -ferrum` |
| Um grupo com todos os projetos | "crie um grupo com todos os projetos" | `group all --add '*'` |
| Tirar um projeto do grupo | "tire o ferrum do grupo dev" | `group dev --remove -ferrum` |
| Ver tudo e o que está fora do lugar | `/share-memories status` | `status` |
| Compartilhar memórias | "compartilhe essas duas memórias com o grupo dev" | `share dev <caminho da memória>...` |
| Mudar de grupo | "passe essa memória para o grupo all" | `move all dev/x.md` |
| Desfazer, deixando uma cópia num projeto | "tire x do grupo e deixe só no ferrum" | `unshare dev/x.md --keep -ferrum` |
| Desfazer e apagar | "apague a memória compartilhada x" | `unshare dev/x.md` |
| Revisar as memórias de um grupo | "mostre as memórias do grupo dev" (em inglês, com tradução) | `status` |
| Consertar depois de mexer à mão | "sincronize as memórias" | `sync` |

"Rode" é `python3 ~/.claude/skills/share-memories/share_memories.py`, de
qualquer pasta. O nome de um projeto é a pasta dele em `~/.claude/projects/`
(`-dev-sandbox`), ou o caminho (`/home/voce/Dev/*`).
