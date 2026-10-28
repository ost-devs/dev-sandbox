# Escrever e revisar memórias

> **Rascunho** para revisão do mantenedor.

O Claude escreve as memórias sozinho, mas você pode pedir para ele criar, corrigir ou revisar
uma. Este guia diz o que uma memória boa tem e como revisar as que já existem, separando três
coisas: o que a documentação oficial diz, o que a instrução do Claude Code pede (vista numa
sessão, não documentada) e o que este repositório aprendeu na prática.

O básico (o que é memória, onde fica, como desligar) está em
[Memória e instruções](./memoria-e-instrucoes.md).

## As três partes e quando o Claude vê cada uma

Uma memória tem três partes, lidas em momentos diferentes:

| Parte | Onde fica | Quando o Claude vê | O que precisa ter |
|---|---|---|---|
| Linha do índice | `MEMORY.md`: `- [Título](arquivo.md) — resumo` | **Sempre**, em toda sessão | O essencial, entendível sozinho |
| `description` | Frontmatter do arquivo | Ao decidir se abre o arquivo (recall) e quando abre | Uma frase: quando a memória serve |
| Corpo | O próprio arquivo | Só quando o Claude abre o arquivo | A regra, o **Why**, o **How to apply** e um exemplo |

A linha e a descrição dizem quase a mesma coisa. Isso é normal (as memórias que o Claude cria
sozinho também são assim) e não custa em dobro: o Claude Code tira o frontmatter antes de
carregar o índice, então as duas não entram juntas no contexto.

## O que a documentação diz

Fonte: <https://code.claude.com/docs/en/memory> e
<https://code.claude.com/docs/en/errors#memory-index-is-over-its-read-limit>.

| Fato | Detalhe |
|---|---|
| Quatro tipos, no campo `type` | `user` (quem você é), `feedback` (como trabalhar), `project` (trabalho em andamento, prazos, decisões), `reference` (onde achar coisas fora do projeto) |
| O índice carrega sempre | Primeiras 200 linhas ou 25 KB do `MEMORY.md`, uma linha por memória |
| Os arquivos carregam sob demanda | O Claude abre quando precisa |
| O que não vira memória | O que dá para deduzir do código ou do git, e o que o `CLAUDE.md` já diz |
| Data | O Claude Code grava `modified` no frontmatter a cada escrita |
| Some na carga | O frontmatter e os comentários HTML (`<!-- ... -->`) do `MEMORY.md` não chegam ao Claude ([aprendizado](../aprendizados/2026-10-comentarios-do-memory-md-nao-chegam-ao-claude.md)) |

A documentação **não** define `name`, `description`, o formato da linha do índice nem os campos
**Why** e **How to apply**. Os nomes de exemplo dela são `user_role.md` e `feedback_testing.md`.

## O que a instrução do Claude Code pede

Vista numa sessão de outubro/2026 (Claude Code 2.1.310). Não está na página oficial, então pode
mudar sem aviso.

- Frontmatter com `name` (curto, em kebab-case), `description` (uma linha, usada para decidir a
  relevância no recall) e `metadata.type`.
- Linha do índice no formato `- [Título](arquivo.md) — resumo`.
- Em `feedback` e `project`: depois da regra, uma linha **Why:** e uma **How to apply:**.
- Ligar memórias com `[[nome]]`. Um link para memória que ainda não existe não é erro: marca
  algo que vale escrever depois.
- Datas relativas viram absolutas ("ontem" vira `2026-10-27`).

## O que este repositório aprendeu

Análise a partir das memórias do dev-sandbox (outubro/2026):

| Prática | Por quê | Exemplo |
|---|---|---|
| Nome e arquivo iguais, `tipo-assunto`, em inglês | Os `[[links]]` acham a memória pelo nome; o Obsidian também | `feedback-delegate-with-intent.md` |
| Título curto e resumo próprios na linha do índice, não a descrição colada | É o formato que o Claude usa; a linha precisa caber numa olhada | `- [Delegate with intent](...) — quote the user verbatim to subagents; review output against intent` |
| Descrição que diga **quando** usar | É o que decide o recall | `"Use before briefing a subagent on a rewrite that follows user feedback: ..."` |
| Aspas na descrição quando ela tem `: ` | Sem aspas, o YAML entende como outro campo | `description: "Use when ...: ..."` |
| **Why** e **How to apply** também em `reference`, se a memória diz como agir | O motivo deixa o Claude julgar o caso que a regra não previu | `reference-shared-memories` |
| Um exemplo concreto, mesmo que deste projeto | Regra sem exemplo vira interpretação | "two subagents rewrote docs from my paraphrase..." |
| As palavras do usuário entre aspas | Paráfrase transforma sugestão em proibição | `("não é uma regra proibitiva")` |
| `project`: estado, próximo passo e data; apagar quando acabar | Memória de projeto velha engana | `project-v05` |
| Um `[[link]]` de exemplo fica fora do texto como link | Um placeholder como `[[nome-da-memoria]]` vira link não resolvido, que o Claude lê como "escrever depois" | "links to the shared one by its name in double brackets" |

## Links entre memórias

Base: o artigo [Memórias que se conectam](./memorias-como-sinapses.md) e as memórias deste
repositório.

| Faça | Por quê |
|---|---|
| Ligue só o que tem relação real ("Related: `[[user-mantenedor]]`") | Um grafo em que tudo se liga a tudo é tão inútil quanto um sem links |
| Revise com mais cuidado as memórias que recebem muitos links | Elas viram o centro e são lidas mais vezes. Se uma delas está errada, o erro se espalha: no dev-sandbox, `user-mantenedor` recebe 7 de 14 links e é justamente a que tem imprecisões a revisar |
| Ao renomear, troque o nome em todos os `[[links]]` | Senão o link fica não resolvido, e o Claude o lê como "memória a escrever" |
| Quando um par de memórias fala do mesmo assunto, ligue as duas | Ex.: `project-v05` ↔ `project-host-tests` |

Para revisar o conjunto, veja o grafo: copie a pasta de memória e abra-a como *vault* no
Obsidian (passo a passo no [artigo](./memorias-como-sinapses.md#ver-o-grafo-hoje-no-obsidian)).
Memória solta, sem nenhum link, é candidata a apagar ou a ligar; centro errado é prioridade.

## Revisar uma memória

Peça ao Claude: "revise as memórias deste projeto" ou "revise a memória feedback-delegate-with-intent".
Ele deve mostrar cada uma com a tradução, como o guia de
[compartilhar memórias](./compartilhar-memorias.md) pede. Confira:

| Pergunta | Como conferir |
|---|---|
| Os fatos estão certos? | Contra a fonte: `git log`, o arquivo citado, a documentação. Uma reescrita pode inverter um fato: no dev-sandbox, a frase sobre Stripe e placeholders saiu ao contrário numa reescrita, e só o `git log -S Stripe` mostrou o que tinha acontecido (os subagentes trocaram o exemplo do Claude Code por Stripe) |
| O estado ainda vale? | Memórias `project` envelhecem: "untested", "ask whether" já respondido, commit que já mudou |
| O que é dedução está marcado? | Palavras como "look kept (deduction)" |
| Tem **Why** e **How to apply**? | Obrigatórios em `feedback` e `project` |
| A linha do índice se entende sozinha? | Leia só a linha, sem abrir o arquivo |
| Nome, título e descrição estão em inglês? | O arquivo é para o Claude ([por quê](./memoria-e-instrucoes.md)) |
| Os `[[links]]` apontam para nomes que existem? | Depois de renomear, procure o nome antigo em todas as memórias |
| Isso é memória mesmo? | Se dá para deduzir do repositório, apague. Se é uma regra curta para toda sessão de todo projeto, vai no `~/.claude/CLAUDE.md` |
| Serve só aqui ou em outros projetos? | Veja [compartilhar memórias](./compartilhar-memorias.md) |

## Antes e depois

Uma memória do dev-sandbox antes da revisão:

```markdown
---
name: feedback-testes-e-branch
description: Turn manual tests into committed automated tests with a rule; check the branch before every commit
---

1. Tests run by hand must become committed, repeatable tests ...
2. Run `git branch --show-current` before each commit ...
```

Problemas: nome em português; duas regras numa memória só, uma geral (testes) e outra que só faz
sentido aqui (a branch `claude` do `AGENTS.md`). Depois: duas memórias, cada uma com um assunto.

```markdown
---
name: feedback-manual-checks-become-tests
description: "Use when a session validates scripts or skills by hand: turn the check into a committed, repeatable test plus a rule that runs it"
metadata:
  type: feedback
---

Checks run by hand must become committed, repeatable tests next to the code (offline fixtures), ...

**Why:** the user asked (2026-10-28) why the mirrors tests weren't in the skill: "para o caso de quebrar algo após uma modificação em outra sessão".
**How to apply:** whenever a session validates scripts or skills manually.
```

A regra da branch virou `feedback-check-branch-before-commit`, local.

## Onde rodar

Tudo isso acontece numa sessão do Claude, no container ou no host. Para abrir a pasta de
memória: `/memory` → *Open auto-memory folder*. No container, ela fica em
`~/.claude/projects/<projeto>/memory/` (onde isso fica no host:
[Memória e instruções](./memoria-e-instrucoes.md)).

Conferido em outubro/2026 (Claude Code 2.1.310).

Relacionados: [Memória e instruções](./memoria-e-instrucoes.md),
[Compartilhar memórias](./compartilhar-memorias.md),
[Memórias que se conectam](./memorias-como-sinapses.md).
