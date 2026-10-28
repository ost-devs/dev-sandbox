# Glossário

Nomes e comandos em inglês das skills do dev-sandbox. A pronúncia é aproximada, escrita como se
lê em português.

## share-memories

Skill que [compartilha memórias entre projetos](../claude-code/compartilhar-memorias.md).

| Inglês | Pronúncia | Significa | Na skill |
|---|---|---|---|
| **share** | *xér* | compartilhar | `share dev <memória>`: leva a memória para o grupo `dev` |
| **memories** | *mé-mo-ris* | memórias | as anotações que o Claude guarda sozinho sobre você e o projeto |
| **share-memories** | *xér mé-mo-ris* | compartilhar memórias | o nome da skill: `/share-memories` |
| **shared** | *xérd* | compartilhada(s) | `~/.claude/shared-memories/`: a pasta com a cópia única de cada memória; `_(shared, group dev)_` no fim da linha do índice |
| **group** | *grup* | grupo | `group dev --add ...`: cria o grupo ou põe projetos nele |
| **groups** | *grups* | grupos | `groups.json`: o arquivo que diz quais projetos estão em cada grupo |
| **all** | *ól* | todos | nome sugerido para o grupo com todos os projetos (`group all --add '*'`) |
| **status** | *stei-tus* | situação | `status`: mostra grupos, projetos, memórias e o que está fora do lugar |
| **unshare** | *ân-xér* | deixar de compartilhar | `unshare dev/x.md`: tira a memória do grupo |
| **keep** | *kip* | manter, ficar com | `--keep -ferrum`: ao tirar do grupo, uma cópia fica no projeto ferrum |
| **move** | *múv* | mover | `move all dev/x.md`: passa a memória do grupo `dev` para o `all` |
| **line** | *láin* | linha | `line dev/x.md`: mostra ou muda a linha da memória no `MEMORY.md` |
| **title** | *tái-tou* | título | `--title "..."`: o texto entre colchetes na linha do índice |
| **summary** | *sâ-ma-ri* | resumo | `--summary "..."`: o texto depois do travessão na linha do índice |
| **add** | *éd* | acrescentar | `--add -ferrum`: põe o projeto no grupo |
| **remove** | *ri-múv* | tirar | `--remove -ferrum`: tira o projeto do grupo |
| **delete** | *di-lít* | apagar | `group dev --delete`: apaga um grupo vazio |
| **sync** | *sínc* | sincronizar | `sync`: refaz links e índices depois de uma mudança à mão |
| **project** | *pró-djekt* | projeto | `--project -ferrum`: só neste projeto |
| **install** | *ins-tól* | instalar | `install`: acrescenta os hooks ao `settings.json` |
| **dry run** | *drai rân* | ensaio, "a seco" | `--dry-run`: mostra o que faria, sem mudar nada |
| **hook** | *húk* | gancho | comando que o Claude Code roda sozinho em certos momentos (depois de editar um arquivo, no início da sessão) |
| **start / end** | *start / énd* | início / fim | marcam o bloco gerado no `MEMORY.md` (`share-memories:start`) |
| **conflict** | *cón-flikt* | conflito | um projeto tem um arquivo próprio com o mesmo nome de uma memória do grupo |
| **pending** | *pén-din* | pendente | o que `status` acha fora do lugar |
| **missing** | *mí-sin* | faltando | `-ferrum: missing x.md`: o link ainda não está lá |
| **stale link** | *steil link* | link velho | link para uma memória que saiu do grupo |
