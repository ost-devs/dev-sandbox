# Um consultor do projeto que não depende da conversa

Toda conversa nova com o Claude começa sem saber nada. Depois de horas, ela
parece "conhecer o projeto", e dá vontade de nunca sair dela. Este guia mostra
como guardar esse conhecimento em arquivos que o Claude lê sozinho, para que
**qualquer conversa nova** já comece precisa, sem carregar o peso da antiga.

Foi montado neste repositório e serve de modelo para o seu projeto.
Base: documentação oficial de [memória](https://code.claude.com/docs/en/memory),
[skills](https://code.claude.com/docs/en/skills) e
[subagentes](https://code.claude.com/docs/en/sub-agents). Conferido em
outubro/2026 (Claude Code 2.1.310).

## O problema

Uma conversa longa guarda o conhecimento **no contexto**, e o contexto:

- vai inteiro a cada pedido, então cada mensagem fica mais cara ([por quê](./por-baixo-dos-panos/a-cada-mensagem-o-contexto-vai-junto.md));
- é resumido quando enche, e "instruções detalhadas do começo podem se perder" ([compactação](./por-baixo-dos-panos/compactacao.md));
- morre com `/clear` ou numa conversa nova.

A conversa não é memória. O que vale guardar precisa sair dela.

## As peças

Cada tipo de conhecimento vai para o lugar que carrega na hora certa e custa
o mínimo:

| Peça | Neste repositório | Carrega | Custo fixo | Vai pro git? |
|---|---|---|---|---|
| Instruções do projeto | [`AGENTS.md`](../../AGENTS.md) | Toda sessão | O arquivo inteiro | Sim |
| Rules por pasta | `.claude/rules/scripts-e-imagem.md` (script, imagem, `sandbox/`) e `.claude/rules/documentacao.md` (docs) | Só quando o Claude mexe nesses arquivos | Zero até lá | Sim |
| Skill com o mapa do projeto | `.claude/skills/dev-sandbox/` | Descrição sempre; texto quando o assunto aparece (ou com `/dev-sandbox`) | ~100 tokens | Sim |
| Agente pesquisador | `.claude/agents/claude-code-pesquisador.md` | Roda num contexto separado; só a conclusão volta | Só a descrição | Sim |
| Memória do agente | `.claude/agent-memory/claude-code-pesquisador/` | Quando o agente roda | Nenhum na conversa principal | Sim |
| Skill de fechamento | `.claude/skills/consolidar/` | Só quando você digita `/consolidar` | Zero | Sim |
| Memória automática | `~/.claude/projects/<projeto>/memory/` | Índice em toda sessão | O índice | Não: é sua |

### Por que cada uma

- **`AGENTS.md`:** só o que vale em **toda** tarefa (idioma, fluxo de commits). Cada linha custa contexto em toda sessão.
- **Rules com `paths`:** o checklist "mudou o script? atualize também tal e tal doc" só importa quando alguém mexe no script. Fora disso, não ocupa nada.
- **Skill `dev-sandbox`:** o mapa que custa horas para reconstruir: como as peças se encaixam, as decisões que parecem erradas mas têm motivo, onde cada assunto está escrito. Ela **aponta** para os documentos em vez de copiá-los, para não divergir deles. Tem menos de 5 mil tokens de propósito: depois de uma compactação, a skill usada volta inteira até esse limite.
- **Agente pesquisador:** as páginas oficiais do Claude Code passam de 100 mil caracteres. Ler isso na conversa principal enche o contexto. O agente lê no contexto dele, devolve a conclusão com fonte e versão, e anota o fato na memória própria, que fica no git. Assim, o próximo que perguntar não paga a pesquisa de novo.
- **`/consolidar`:** o hábito que fecha o ciclo (abaixo).
- **Memória automática:** preferências **suas** (idioma, "só commite quando eu pedir"). Não vai pro git, então não vale para colaboradores.

### Separar Claude Code do dev-sandbox?

Separamos **a pesquisa**, não o conhecimento. O que já foi verificado sobre o
Claude Code está nos guias de [`docs/claude-code/`](./README.md), e a skill
manda lê-los primeiro. O que muda rápido (versões, campos novos, flags) fica
com o agente pesquisador, que confere na fonte e data cada fato. Um consultor
único que soubesse tudo de cor ficaria desatualizado sem avisar.

## Como usar no dia a dia

1. **Abra uma conversa nova para cada assunto.** Pergunte direto. Se a resposta
   parecer genérica, peça `/dev-sandbox` para carregar o mapa.
2. **Dúvida de Claude Code que não está nos guias:** *"pergunte ao
   claude-code-pesquisador"*. Ou deixe o Claude delegar sozinho: a descrição
   do agente pede isso.
3. **Antes de encerrar uma conversa longa:** `/consolidar`. O Claude lista o
   que a conversa descobriu, descarta o que dá para deduzir dos arquivos e põe
   cada item no lugar certo. Ele mostra uma tabela e pergunta antes de commitar.
4. **Depois:** `/clear` sem medo.

Para conferir o que carregou numa sessão: `/context` mostra *Memory files*
(instruções e rules) e *Skills*.

## Como manter

- **Um fato, um lugar.** Se aparece em dois arquivos, um deles vai envelhecer.
- **Apague mais do que acrescenta.** Mapa velho engana mais que mapa nenhum.
- **Reveja a memória do agente** de vez em quando: `.claude/agent-memory/claude-code-pesquisador/MEMORY.md`. Os fatos têm data e versão.
- **Mudou algo grande no projeto?** Atualize a skill `dev-sandbox` no mesmo commit.

## No seu projeto

O molde vale para qualquer repositório, inclusive fora do dev-sandbox:

```text
seu-projeto/
├── AGENTS.md                         # só o que vale em toda tarefa
└── .claude/
    ├── rules/<parte>.md              # com paths: — checklist de quem mexe ali
    ├── skills/<projeto>/SKILL.md     # mapa: como funciona, decisões, onde está cada coisa
    ├── skills/consolidar/SKILL.md    # copie a deste repositório
    └── agents/<pesquisador>.md       # opcional: pesquisa externa que muda rápido, com memory: project
```

Comece pequeno: escreva o mapa na primeira vez que uma conversa longa ficar
"esperta", rodando `/consolidar` nela.

## Limites

- Instruções e skills são lidas e seguidas na maior parte das vezes, sem garantia. O que **precisa** acontecer vai num mecanismo (hook, permissão, script).
- O Claude decide sozinho quando carregar uma skill pela descrição. Se não carregar, chame pelo nome.
- Os agentes embutidos Explore e Plan não recebem `AGENTS.md`/`CLAUDE.md` ([subagentes](./por-baixo-dos-panos/subagentes-o-que-herdam.md)).
- A memória de agente não funciona com a memória automática desligada.
