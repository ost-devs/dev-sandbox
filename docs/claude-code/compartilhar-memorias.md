# Compartilhar memórias entre projetos

A memória automática do Claude é separada por projeto
([por quê](./memoria-e-instrucoes.md#2-memória-automática)). Isso é bom para "os testes deste
repo precisam do Redis", mas ruim para "eu reviso em português" ou "commite sem perguntar": você
ensina a mesma coisa em cada projeto.

A skill [`/share-memories`](../../utils/skills/share-memories/SKILL.md) leva uma memória para um
**grupo** de projetos (todos, uma lista, ou uma categoria como `dev`) e a mantém igual em todos
eles. Ela não muda como nem quando o Claude cria memórias: age depois, a cada memória nova, e
quem decide o destino é você.
O nome e os comandos são em inglês ([glossário](../ingles-para-devs/glossario.md#share-memories)).

## Como funciona

```text
~/.claude/shared-memories/
├── groups.json                ← quais projetos estão em cada grupo e a linha de cada memória
├── nota.md                    ← para você: as compartilhadas e as candidatas, traduzidas
├── nota-ferrum.md             ← opcional: as memórias só do ferrum, traduzidas
└── dev/
    └── review-in-pt.md        ← a única cópia da memória

~/.claude/projects/-ferrum/memory/
├── MEMORY.md                  ← ganha um bloco gerado com uma linha por memória do grupo
└── review-in-pt.md  →  ../../../shared-memories/dev/review-in-pt.md   (link)
```

- **Uma cópia, vários links.** Cada projeto do grupo recebe um link simbólico para a cópia única.
  O Write e o Edit do Claude **se recusam** a escrever através de um link e apontam o arquivo de
  destino ([aprendizado](../aprendizados/2026-10-write-edit-recusam-symlink.md)). Então
  qualquer edição, em qualquer projeto, cai na cópia única: não há cópias para sincronizar.
- **Dois hooks fazem o resto.** Depois de cada Write/Edit, um atualiza a linha da memória no
  `MEMORY.md` de todos os projetos e põe o bloco de volta se o Claude reescreveu o índice.
  No início de cada sessão, o outro liga as memórias do grupo num projeto que ainda não as tem
  (projetos novos entram sozinhos).
- **O Claude propõe, você decide.** Quando nasce uma memória num projeto que está num grupo, o
  hook avisa o Claude. Ele deixa a memória no projeto (o normal) ou, se acha que serve a outros
  projetos, a põe como **candidata** no `nota.md`, traduzida e com o grupo sugerido, e só te
  avisa numa linha, sem pergunta. Ele nunca compartilha sozinho: você revisa as candidatas quando
  quiser, de uma vez, e diz o que fazer.

### O que fica no projeto

Uma memória compartilhada custa uma linha no índice de **toda** sessão de **todo** projeto do
grupo, e uma memória lida onde não se aplica atrapalha. Por isso a skill só compartilha o que
seria usado na maioria dos projetos do grupo. Mesmo assim ele erra: onde uma memória vale é
critério seu (uma liberdade que você deu num projeto de estudo pode não servir nos outros). Por
isso a decisão é sua. O critério que ele usa para propor:

| Memória | Destino |
|---|---|
| "Os testes de API precisam do Redis", "o deploy é sexta" | Fica no projeto |
| "Reviso em português; escreva os arquivos para IA em inglês" | Candidata a grupo |
| Lição geral escrita com nomes deste projeto | Candidata, com uma versão reescrita (mantém um exemplo concreto) |
| Regra curta que vale sempre, em todo lugar | Candidata, com a sugestão de ir para o `~/.claude/CLAUDE.md`, que carrega inteiro; memória só carrega quando lembrada |

> Por que não usar a opção nativa `autoMemoryDirectory`, apontando vários projetos para a mesma
> pasta? Porque ela mistura **todas** as memórias, inclusive as específicas: é o problema da
> v0.1 ([aprendizado](../aprendizados/2026-10-memoria-misturada-entre-projetos.md)) de volta.

## Instalar

1. Copie a skill (no host; vale dentro e fora do container, porque o `~/.claude` é o mesmo):

   ```bash
   cp -r ~/dev-sandbox/utils/skills/share-memories ~/.claude/skills/
   ```

2. Numa sessão nova do Claude, em qualquer projeto, peça: **"instale a share-memories e crie o
   grupo dev com o dev-sandbox e o ferrum"**. Ele mostra o que vai acrescentar ao
   `~/.claude/settings.json` (os dois hooks), grava com uma cópia de segurança
   (`settings.json.bak`) e cria o grupo.

3. Abra uma sessão nova (os hooks valem a partir dela) e peça `/share-memories status`.

## Usar

Na maior parte do tempo, nada além de revisar o `nota.md` de vez em quando (próxima seção).
Para agir você mesmo:

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
| Revisar em português | abra `~/.claude/shared-memories/nota.md` | — |
| Revisar as memórias só de um projeto | "crie a nota de revisão do ferrum" | — |
| Consertar depois de mexer à mão | `/share-memories sync` | `... sync` |

### Revisar em português

As memórias são escritas para o Claude, quase sempre em inglês. Para você revisar sem depender do
inglês, o Claude mantém notas traduzidas ao lado do `groups.json`:

- **`nota.md`:** uma seção `#` por grupo, com cada memória compartilhada traduzida, de onde veio e
  a opinião dele (manter, mudar de grupo, apagar). No fim, `# Candidatas`: o que ele propõe
  compartilhar. Você lê e pede, por exemplo, "compartilhe a candidata Delegar com o grupo dev" ou
  "deixe todos/x.md só no borrow-checked".
- **`nota-<projeto>.md`:** as memórias que só existem naquele projeto (`nota-ferrum.md`). Só
  existe para os projetos que você pedir.

Elas não se atualizam sozinhas (a tradução é do Claude), mas não ficam para trás sem aviso: os
hooks lembram o Claude de atualizar a nota quando uma memória listada nela muda ou nasce, e o
`/share-memories status` lista o que falta ou sobra em cada nota.

As notas não custam contexto: ficam fora da pasta `memory/` e do `MEMORY.md`, então nenhuma sessão
as carrega. O custo aparece só quando nasce ou muda uma memória listada numa nota: o Claude lê a
nota e escreve a tradução, uns 3 mil tokens numa nota de 10 memórias, uma vez.

Fora das notas, quando o Claude te mostra uma memória (para resolver um conflito, por exemplo),
mostra a tradução junto, a não ser que você diga que não quer.

Não edite o bloco `share-memories` do `MEMORY.md`: ele é refeito. Edite a memória.

A linha de cada memória no bloco é a que o Claude escreveu no `MEMORY.md` do projeto onde ela
nasceu (título e resumo). O `share` guarda essa linha no `groups.json`, e o `unshare --keep` a
devolve ao projeto. Para mudar, use `line`. Se a memória não tinha linha própria, o bloco usa o
nome e a descrição dela, e o `status` avisa.

Cada linha termina em `_(shared, group dev)_`. O Claude Code apaga os comentários HTML do
`MEMORY.md` antes de carregá-lo
([aprendizado](../aprendizados/2026-10-comentarios-do-memory-md-nao-chegam-ao-claude.md)), então
essa marca é o único sinal, para o Claude, de que uma edição vale em outros projetos.

## Limites

- **Conflito de nome:** se um projeto do grupo já tem uma memória própria com o mesmo nome e
  conteúdo diferente, nada é sobrescrito; `status` e os hooks avisam, e o Claude junta com você.
- **Edição por `sed -i` ou editor externo** troca o link por um arquivo comum. Se o conteúdo for
  igual, o próximo hook refaz o link; se for diferente, vira conflito.
- **O projeto é a pasta**, não o repositório: o mesmo repo aberto com `dev-docker --nome` ou em
  outro caminho é outro membro (use os dois nomes no grupo).
- **Testado em parte numa sessão real.** Em 28/10/2026 o hook `PostToolUse` disparou e o aviso
  de memória nova chegou ao Claude; o `SessionStart` ainda não foi observado. O script e os
  hooks também são testados com a entrada que a documentação descreve (37 testes em
  [`tests/`](../../utils/skills/share-memories/tests/test_share_memories.py)).

Fontes: <https://code.claude.com/docs/en/memory> (pasta da memória, `autoMemoryDirectory`) e
<https://code.claude.com/docs/en/hooks> (`PostToolUse`, `SessionStart`, `additionalContext`).
Conferido em outubro/2026 (Claude Code 2.1.310).
