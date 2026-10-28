# share-memories: memórias compartilhadas entre projetos

Leva uma memória do Claude para um grupo de projetos (todos, uma lista ou uma
categoria como `dev`) e a mantém igual em todos. Fica uma cópia só, em
`~/.claude/shared-memories/<grupo>/`, com um link em cada projeto. O Claude
decide o que é geral; você aprova quando ele quer reescrever uma memória.

Guia completo: [compartilhar memórias](../../../docs/claude-code/compartilhar-memorias.md).
Nomes em inglês: [glossário](../../../docs/ingles-para-devs/glossario.md#share-memories).

Um projeto é a pasta dele em `~/.claude/projects/` (`-ferrum`) ou o caminho
(`/home/voce/Dev/*`).

| Você quer | Peça ao Claude | Ou rode `python3 ~/.claude/skills/share-memories/share_memories.py ...` |
|---|---|---|
| Instalar (hooks e `groups.json`) | `/share-memories install` | `... install` (só mostrar: `--dry-run`) |
| Criar um grupo ou pôr projetos nele | "crie o grupo dev com o dev-sandbox e o ferrum" | `... group dev --add -dev-sandbox -ferrum` |
| Um grupo com todos os projetos | "crie o grupo all com todos os projetos" | `... group all --add '*'` |
| Tirar um projeto do grupo | "tire o ferrum do grupo dev" | `... group dev --remove -ferrum` |
| Ver tudo e o que está fora do lugar | `/share-memories status` | `... status` |
| Compartilhar memórias | "compartilhe essa memória com o grupo dev" | `... share dev <caminho da memória>` |
| Mudar de grupo | "passe dev/x.md para o grupo all" | `... move all dev/x.md` |
| Mudar a linha da memória no `MEMORY.md` | "mude o título de dev/x.md no índice para Delegate with intent" | `... line dev/x.md --title "Delegate with intent"` (resumo: `--summary "..."`) |
| Desfazer, deixando uma cópia num projeto | "tire dev/x.md do grupo e deixe só no ferrum" | `... unshare dev/x.md --keep -ferrum` |
| Desfazer e apagar | `/share-memories unshare dev/x.md` | `... unshare dev/x.md` |
| Revisar as memórias de um grupo | "mostre as memórias do grupo dev" | `... status` |
| Consertar depois de mexer à mão | `/share-memories sync` | `... sync` |
