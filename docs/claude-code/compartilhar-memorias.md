# Compartilhar memórias entre projetos

A memória automática do Claude é separada por projeto
([por quê](./memoria-e-instrucoes.md#2-memória-automática)). Isso é bom para "os testes deste
repo precisam do Redis", mas ruim para "eu reviso em português" ou "commite sem perguntar": você
ensina a mesma coisa em cada projeto.

A skill [`/compartilhar-memorias`](../../utils/skills/compartilhar-memorias/SKILL.md) leva uma
memória para um **grupo** de projetos (todos, uma lista, ou uma categoria como `dev`) e a mantém
igual em todos eles. Ela não muda como nem quando o Claude cria memórias: age depois, a cada
memória nova.

## Como funciona

```text
~/.claude/memorias-compartilhadas/
├── grupos.json                ← quais projetos estão em cada grupo
└── dev/
    └── revisar-em-pt.md       ← a única cópia da memória

~/.claude/projects/-ferrum/memory/
├── MEMORY.md                  ← ganha um bloco gerado com uma linha por memória do grupo
└── revisar-em-pt.md  →  ../../../memorias-compartilhadas/dev/revisar-em-pt.md   (link)
```

- **Uma cópia, vários links.** Cada projeto do grupo recebe um link simbólico para a cópia única.
  O Write e o Edit do Claude **se recusam** a escrever através de um link e apontam o arquivo de
  destino (testado em 28/10/2026). Então qualquer edição, em qualquer projeto, cai na cópia
  única: não há cópias para sincronizar.
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

> Por que não usar `autoMemoryDirectory` apontando vários projetos para a mesma pasta? Porque
> mistura **todas** as memórias, inclusive as específicas: é o problema da v0.1
> ([aprendizado](../aprendizados/2026-10-memoria-misturada-entre-projetos.md)) de volta.

## Instalar

No host (vale dentro e fora do container, porque o `~/.claude` é o mesmo):

```bash
cp -r ~/dev-sandbox/utils/skills/compartilhar-memorias ~/.claude/skills/
mkdir -p ~/.claude/memorias-compartilhadas
```

Crie `~/.claude/memorias-compartilhadas/grupos.json`. Cada entrada é o nome da pasta do projeto
em `~/.claude/projects/` ou o caminho do projeto; `*` vale qualquer coisa:

```json
{"grupos": {
  "todos": ["*"],
  "dev": ["-dev-sandbox", "-ferrum", "/home/voce/Dev/*"]
}}
```

Acrescente os dois hooks ao `~/.claude/settings.json` (junte com um `"hooks"` que já exista):

```json
"hooks": {
  "PostToolUse": [{"matcher": "Write|Edit", "hooks": [{"type": "command",
    "command": "python3 \"$HOME/.claude/skills/compartilhar-memorias/compartilhar.py\" hook"}]}],
  "SessionStart": [{"hooks": [{"type": "command",
    "command": "python3 \"$HOME/.claude/skills/compartilhar-memorias/compartilhar.py\" hook"}]}]
}
```

Conferir: numa sessão nova, `/compartilhar-memorias status`. Ele lista grupos, projetos,
memórias, pendências, e avisa se os hooks faltam.

## Usar

Na maior parte do tempo, nada: o Claude decide a cada memória nova. Para agir à mão, peça em
português ("compartilhe a memória X com o grupo dev") ou rode o script direto:

| Quero | Comando (`python3 ~/.claude/skills/compartilhar-memorias/compartilhar.py ...`) |
|---|---|
| Ver tudo e o que está fora do lugar | `status` |
| Compartilhar uma memória | `compartilhar <caminho da memória> <grupo>` |
| Desfazer, deixando uma cópia num projeto | `descompartilhar dev/x.md --manter -ferrum` |
| Desfazer e apagar | `descompartilhar dev/x.md` |
| Consertar depois de mexer em `grupos.json` | `sincronizar` |

Não edite o bloco `compartilhar-memorias` do `MEMORY.md`: ele é refeito. Edite a memória.

## Limites

- **Conflito de nome:** se um projeto do grupo já tem uma memória própria com o mesmo nome e
  conteúdo diferente, nada é sobrescrito; `status` e os hooks avisam, e o Claude junta com você.
- **Edição por `sed -i` ou editor externo** troca o link por um arquivo comum. Se o conteúdo for
  igual, o próximo hook refaz o link; se for diferente, vira conflito.
- **O projeto é a pasta**, não o repositório: o mesmo repo aberto com `dev-docker --nome` ou em
  outro caminho é outro membro (use os dois nomes no grupo).
- **Não testado ainda numa sessão real com os hooks instalados.** O script e os hooks foram
  testados com a entrada que a documentação descreve (15 testes em
  [`tests/`](../../utils/skills/compartilhar-memorias/tests/test_compartilhar.py)).

Fontes: <https://code.claude.com/docs/en/memory> (pasta da memória, `autoMemoryDirectory`) e
<https://code.claude.com/docs/en/hooks> (`PostToolUse`, `SessionStart`, `additionalContext`).
Conferido em outubro/2026 (Claude Code 2.1.310).
