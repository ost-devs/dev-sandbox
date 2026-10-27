# Um consultor do projeto que não depende da conversa

Toda conversa nova com o Claude começa sem saber nada. Depois de horas, ela
parece "conhecer o projeto", e dá vontade de nunca sair dela. A ideia aqui é
guardar esse conhecimento em arquivos que o Claude lê sozinho, para que
**qualquer conversa nova** já comece precisa, sem carregar o peso da antiga.

Esta é a introdução: o problema, as peças e por que cada uma existe. Para
montar no seu projeto, vá para o guia prático
**[Montar o consultor em qualquer projeto](./montar-consultor.md)**, que usa
a skill `/montar-consultor`.

## O problema

Uma conversa longa guarda o conhecimento **no contexto**, e o contexto:

- vai inteiro a cada pedido, então cada mensagem fica mais cara ([por quê](./por-baixo-dos-panos/a-cada-mensagem-o-contexto-vai-junto.md));
- é resumido quando enche, e "instruções detalhadas do começo podem se perder" ([compactação](./por-baixo-dos-panos/compactacao.md));
- morre com `/clear` ou numa conversa nova.

A conversa não é memória. O que vale guardar precisa sair dela.

## As peças

Cada tipo de conhecimento vai para o lugar que carrega na hora certa e custa
o mínimo. A última coluna mostra a peça montada neste repositório, como
exemplo.

| Peça | Guarda | Carrega | Custo fixo | No dev-sandbox |
|---|---|---|---|---|
| Instruções do projeto (`AGENTS.md` ou `CLAUDE.md`) | O que vale em **toda** tarefa | Toda sessão | O arquivo inteiro | [`AGENTS.md`](../../AGENTS.md) |
| Rules com `paths:` | O checklist de quem mexe numa parte | Só quando o Claude lê ou edita um arquivo daquela parte | Zero até lá | [`.claude/rules/`](../../.claude/rules/) |
| Skill com o mapa do projeto | Como funciona, decisões que parecem erradas, onde está cada assunto | Descrição sempre; o texto quando o assunto aparece (ou com `/<projeto>`) | ~100 tokens | [`.claude/skills/dev-sandbox/`](../../.claude/skills/dev-sandbox/SKILL.md) |
| Skill `/consolidar` | O hábito de guardar o que a conversa aprendeu | Só quando você digita `/consolidar` | Zero | [`.claude/skills/consolidar/`](../../.claude/skills/consolidar/SKILL.md) |
| Agente pesquisador (opcional) | Fatos de uma fonte externa que muda rápido | Roda num contexto separado; só a conclusão volta | Só a descrição | [`.claude/agents/`](../../.claude/agents/claude-code-pesquisador.md) |
| Memória do agente | O que o pesquisador já confirmou, com data e versão | Quando o agente roda | Nenhum na conversa principal | [`.claude/agent-memory/`](../../.claude/agent-memory/claude-code-pesquisador/MEMORY.md) |
| Memória automática | Preferências **suas** | Índice em toda sessão | O índice | `~/.claude/projects/<projeto>/memory/` (fora do git) |

Tudo, menos a memória automática, vai para o git e vale para quem mais
trabalhar no projeto.

### Por que cada uma

- **Instruções:** cada linha custa contexto em toda sessão. Só fica o que vale em toda tarefa (idioma, fluxo de commits, onde olhar).
- **Rules com `paths:`:** o checklist "mudou o script? atualize também tal e tal doc" só importa quando alguém mexe no script. Fora disso, não ocupa nada.
- **Mapa do projeto:** o conhecimento que custa horas para reconstruir. Ele **aponta** para os documentos em vez de copiá-los, para não divergir deles. Fica pequeno de propósito: depois de uma compactação, a skill usada volta inteira só até 5 mil tokens.
- **`/consolidar`:** sem ele, o conhecimento novo volta a morar só na conversa. É o passo que fecha o ciclo.
- **Agente pesquisador:** neste repositório, as páginas oficiais do Claude Code passam de 100 mil caracteres. Ler isso na conversa principal enche o contexto. O agente lê no contexto dele, devolve a conclusão com fonte e versão e anota o fato na memória própria, que fica no git. O próximo que perguntar não paga a pesquisa de novo.
- **Memória automática:** preferências pessoais ("só commite quando eu pedir"). Não vai pro git, então não vale para colaboradores.

### Separar a pesquisa do conhecimento

O pesquisador **não** é um consultor que sabe tudo de cor. O que já foi
verificado vai para os documentos do projeto (aqui,
[`docs/claude-code/`](./README.md)), e o mapa manda lê-los primeiro. O que
muda rápido (versões, campos novos, flags) fica com o pesquisador, que confere
na fonte e data cada fato. Um consultor único ficaria desatualizado sem avisar.

## O ciclo

```text
conversa trabalha → /consolidar guarda nos arquivos → /clear
        ↑                                               │
        └──── conversa nova já lê instruções e mapa ←───┘
```

1. **Uma conversa nova para cada assunto.** Se a resposta parecer genérica, digite `/<projeto>` para carregar o mapa.
2. **Dúvida sobre a fonte externa:** *"pergunte ao pesquisador"*, ou deixe o Claude delegar sozinho (a descrição do agente pede isso).
3. **Antes de encerrar uma conversa longa:** `/consolidar`. O Claude lista o que a conversa descobriu, descarta o que dá para deduzir dos arquivos e põe cada item no lugar certo. Mostra uma tabela e pergunta antes de commitar.
4. **Depois:** `/clear` sem medo.

## Regras de manutenção

- **Um fato, um lugar.** Se aparece em dois arquivos, um deles vai envelhecer.
- **Apague mais do que acrescenta.** Mapa velho engana mais que mapa nenhum.
- **Mudou algo grande no projeto?** Atualize o mapa no mesmo commit.
- **Reveja a memória do pesquisador** de vez em quando. Os fatos têm data e versão.

## Funcionou?

Resultado neste repositório (outubro/2026, Claude Code 2.1.310):

| O que | Resultado | Base |
|---|---|---|
| Sessões novas, sem a conversa antiga | Responderam com o conhecimento do projeto nos testes feitos depois da implementação | Evidência |
| `/consolidar` no fim da conversa que montou tudo | Achou poucas mudanças: a conversa já tinha posto o conhecimento nos arquivos certos | Evidência |
| Custo de tokens numa sessão nova | **Ainda não medido.** Para conferir: `/context` no começo de uma sessão nova, com e sem a pasta `.claude/` | — |
| Skill `/montar-consultor` em outro projeto | **Ainda não testada** fora do dev-sandbox | — |

O `/consolidar` achar pouco é bom sinal: quer dizer que o conhecimento já
estava fora da conversa. Mas isso sozinho não prova nada, porque foi a mesma
conversa que montou os arquivos. A prova são as sessões novas.

## Limites

- Instruções e skills são lidas e seguidas na maior parte das vezes, sem garantia. O que **precisa** acontecer vai num mecanismo: hook, permissão, script ([instrução ou mecanismo](./instrucao-ou-mecanismo.md)).
- O Claude decide sozinho quando carregar uma skill, pela descrição. Se não carregar, chame pelo nome.
- Os agentes embutidos Explore e Plan não recebem `AGENTS.md`/`CLAUDE.md` ([subagentes](./por-baixo-dos-panos/subagentes-o-que-herdam.md)).
- A memória de agente não funciona com a memória automática desligada.

Base: documentação oficial de [memória](https://code.claude.com/docs/en/memory),
[skills](https://code.claude.com/docs/en/skills) e
[subagentes](https://code.claude.com/docs/en/sub-agents). Conferido em
outubro/2026 (Claude Code 2.1.310).
