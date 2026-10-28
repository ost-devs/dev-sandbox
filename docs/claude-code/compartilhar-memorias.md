# Compartilhar memórias entre projetos

A memória automática do Claude é separada por projeto
([por quê](./memoria-e-instrucoes.md#2-memória-automática)). Isso é bom para "os testes deste
repo precisam do Redis", mas ruim para "eu reviso em português" ou "commite sem perguntar": você
ensina a mesma coisa em cada projeto.

A skill [`/share-memories`](../../utils/skills/share-memories/SKILL.md) leva uma memória para um
**grupo** de projetos (todos, uma lista, ou uma categoria como `dev`) e a mantém igual em todos
eles. Ela não muda como nem quando o Claude cria memórias: age depois, a cada memória nova.
O nome e os comandos são em inglês ([glossário](../ingles-para-devs/glossario.md#share-memories)).

## Como funciona

```text
~/.claude/shared-memories/
├── groups.json                ← quais projetos estão em cada grupo
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
- **O Claude decide, você aprova as edições.** Quando nasce uma memória num projeto que está num
  grupo, o hook avisa o Claude. Ele deixa a memória no projeto (o normal), compartilha como está
  e te avisa numa linha, ou, se a lição é geral mas o texto fala só deste projeto, **te mostra**
  uma versão reescrita e só a grava com o seu "sim".

### O que fica no projeto

Uma memória compartilhada custa uma linha no índice de **toda** sessão de **todo** projeto do
grupo, e uma memória lida onde não se aplica atrapalha. Por isso a skill só compartilha o que
seria usado na maioria dos projetos do grupo:

| Memória | Destino |
|---|---|
| "Os testes de API precisam do Redis", "o deploy é sexta" | Fica no projeto |
| "Reviso em português; escreva os arquivos para IA em inglês" | Grupo |
| Lição geral escrita com nomes deste projeto | Grupo, reescrita com a sua permissão (mantém um exemplo concreto) |
| Regra curta que vale sempre, em todo lugar | `~/.claude/CLAUDE.md`, que carrega inteiro; memória só carrega quando lembrada |

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

Na maior parte do tempo, nada: o Claude decide a cada memória nova. Para agir você mesmo:

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
| Revisar as memórias de um grupo | "mostre as memórias do grupo dev" | `status` |
| Consertar depois de mexer à mão | "sincronize as memórias" | `sync` |

"Rode" é `python3 ~/.claude/skills/share-memories/share_memories.py`, de qualquer pasta. Um
projeto é o nome da pasta dele em `~/.claude/projects/` (`-dev-sandbox`) ou o caminho
(`/home/voce/Dev/*`); `*` vale qualquer coisa.

As memórias são escritas para o Claude, quase sempre em inglês. Quando ele te mostra uma (para
revisar, reescrever ou resolver um conflito), mostra a tradução junto, a não ser que você diga
que não quer.

Não edite o bloco `share-memories` do `MEMORY.md`: ele é refeito. Edite a memória.

## Limites

- **Conflito de nome:** se um projeto do grupo já tem uma memória própria com o mesmo nome e
  conteúdo diferente, nada é sobrescrito; `status` e os hooks avisam, e o Claude junta com você.
- **Edição por `sed -i` ou editor externo** troca o link por um arquivo comum. Se o conteúdo for
  igual, o próximo hook refaz o link; se for diferente, vira conflito.
- **O projeto é a pasta**, não o repositório: o mesmo repo aberto com `dev-docker --nome` ou em
  outro caminho é outro membro (use os dois nomes no grupo).
- **Não testado ainda numa sessão real com os hooks instalados.** O script e os hooks foram
  testados com a entrada que a documentação descreve (25 testes em
  [`tests/`](../../utils/skills/share-memories/tests/test_share_memories.py)).

Fontes: <https://code.claude.com/docs/en/memory> (pasta da memória, `autoMemoryDirectory`) e
<https://code.claude.com/docs/en/hooks> (`PostToolUse`, `SessionStart`, `additionalContext`).
Conferido em outubro/2026 (Claude Code 2.1.310).
